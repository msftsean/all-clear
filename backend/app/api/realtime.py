"""Voice Realtime API endpoints."""
import asyncio
import hashlib
import html
import json
import logging
import re
import uuid
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect

from app.core.dependencies import (
    get_audit_log,
    get_realtime_service,
    get_session_store,
    get_settings,
)
from app.models.enums import Department, Sentiment
from app.models.schemas import AuditLog, Session
from app.models.voice_schemas import (
    RealtimeSessionRequest,
    RealtimeSessionResponse,
    ToolCallRequest,
    VoiceMessage,
)
from app.services.azure.realtime import VOICE_SYSTEM_PROMPT
from app.services.interfaces import RealtimeServiceInterface
from app.services.pii import redact_pii_text

logger = logging.getLogger(__name__)

router = APIRouter()

_TOKEN_SESSIONS: dict[str, tuple[str, datetime]] = {}
_ACTIVE_WS_SESSIONS: set[str] = set()
_ACTIVE_WS_LOCK = asyncio.Lock()
_MAX_TOKEN_TTL_SECONDS = 60
_DEFAULT_STUDENT_HASH = hashlib.sha256(b"demo_student").hexdigest()


def _prune_expired_tokens() -> None:
    """Drop expired ephemeral tokens so in-memory state cannot grow unbounded.

    NOTE: token/active-session state is in-process; the demo runs single-worker.
    For multi-worker production this must move to a shared store (e.g. Redis).
    """
    now = datetime.now(UTC)
    expired = []
    for token, (_, expires_at) in _TOKEN_SESSIONS.items():
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)
        if expires_at <= now:
            expired.append(token)
    for token in expired:
        _TOKEN_SESSIONS.pop(token, None)


def _resolve_realtime_service() -> RealtimeServiceInterface:
    """Wrapper avoids FastAPI interpreting Settings as a body sub-dependency."""
    return get_realtime_service()


def _parse_uuid(value: str) -> UUID | None:
    """Parse a UUID string, returning None for legacy non-UUID test IDs."""
    try:
        return UUID(value)
    except (TypeError, ValueError):
        return None


def _sanitize_instructions(instructions: str | None) -> str:
    """Return locked voice instructions, anchored on the safety system prompt.

    Client-supplied text can NEVER replace VOICE_SYSTEM_PROMPT — it is only
    appended as bounded, neutralized style hints. This prevents a caller from
    overriding the crisis/PII safety behavior by sending their own instructions.
    """
    base = VOICE_SYSTEM_PROMPT
    if not instructions:
        return base
    sanitized = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", instructions)
    sanitized = html.escape(sanitized[:2000], quote=True)
    escaped = (
        sanitized.replace("{", "&#123;")
        .replace("}", "&#125;")
        .replace("[", "&#91;")
        .replace("]", "&#93;")
    )
    combined = f"{base}\n\nAdditional caller style hints (non-overriding):\n{escaped}"
    return combined[:2000]


async def _ensure_shared_session(session_id: str) -> Session | None:
    """Ensure UUID-backed voice sessions exist in the shared text session store."""
    session_uuid = _parse_uuid(session_id)
    if session_uuid is None:
        return None

    session_store = get_session_store()
    session = await session_store.get_session(session_uuid)
    if session is None:
        now = datetime.now(UTC)
        settings = get_settings()
        session = Session(
            session_id=session_uuid,
            student_id_hash=_DEFAULT_STUDENT_HASH,
            created_at=now,
            last_active=now,
            conversation_history=[],
            clarification_attempts=0,
            ttl=settings.session_ttl_seconds,
        )
        await session_store.create_session(session)
    return session


def _cap_token_ttl(response: RealtimeSessionResponse) -> RealtimeSessionResponse:
    """Enforce the public ephemeral credential TTL limit."""
    now = datetime.now(UTC)
    max_expiry = now + timedelta(seconds=_MAX_TOKEN_TTL_SECONDS - 1)
    expires_at = response.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=UTC)
    if expires_at > max_expiry:
        response = response.model_copy(update={"expires_at": max_expiry})
    return response


def _token_is_valid_for_session(token: str, session_id: str) -> bool:
    """Validate an ephemeral token belongs to the requested session and is fresh."""
    registered = _TOKEN_SESSIONS.get(token)
    if registered is None:
        return False
    registered_session_id, expires_at = registered
    now = datetime.now(UTC)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=UTC)
    if registered_session_id != session_id or expires_at <= now:
        return False
    return True


def _voice_transcript_content(arguments: dict, response_result: str) -> str:
    """Derive a PII-safe transcript line from a voice tool request."""
    for key in ("query", "reason", "message"):
        value = arguments.get(key)
        if isinstance(value, str) and value.strip():
            return redact_pii_text(value.strip())[:4000]
    return redact_pii_text(response_result)[:4000] or "Voice tool call completed"


async def _append_voice_message(session_id: str, content: str) -> None:
    """Append a PII-filtered voice turn to shared session history when possible."""
    original_content = content
    content = redact_pii_text(content)
    session_uuid = _parse_uuid(session_id)
    if session_uuid is None:
        return

    session_store = get_session_store()
    session = await session_store.get_session(session_uuid)
    if session is None:
        session = await _ensure_shared_session(session_id)
    if session is None:
        return

    message = VoiceMessage(
        id=str(uuid4()),
        session_id=session_id,
        content=content or "Voice tool call completed",
        role="user",
        input_modality="voice",
        timestamp=datetime.now(UTC),
        is_pii_filtered=content != original_content,
    )
    session.conversation_history.append(message)  # type: ignore[arg-type]
    session.last_active = datetime.now(UTC)
    await session_store.update_session(session)


async def _log_voice_tool_call(
    session_id: str,
    tool_name: str,
    result: str,
    response_time_ms: int,
) -> None:
    """Write an audit entry for a voice tool call, tagged with voice modality."""
    session_uuid = _parse_uuid(session_id)
    if session_uuid is None:
        return

    try:
        result_data = json.loads(result) if result else {}
    except json.JSONDecodeError:
        result_data = {}

    department_value = str(result_data.get("department") or "ESCALATE_TO_HUMAN")
    try:
        routed_department = Department(department_value)
    except ValueError:
        try:
            routed_department = Department(department_value.upper())
        except ValueError:
            routed_department = Department.ESCALATE_TO_HUMAN

    escalated = bool(result_data.get("escalated") or result_data.get("requires_escalation"))
    audit_entry = AuditLog(
        log_id=uuid4(),
        timestamp=datetime.now(UTC),
        student_id_hash=_DEFAULT_STUDENT_HASH,
        session_id=session_uuid,
        detected_intent=str(result_data.get("intent") or tool_name),
        confidence_score=float(result_data.get("confidence") or 1.0),
        routed_department=routed_department,
        ticket_id=result_data.get("ticket_id"),
        escalated=escalated,
        escalation_reason="voice_escalation" if escalated else None,
        pii_detected=False,
        sentiment=Sentiment.NEUTRAL,
        response_time_ms=response_time_ms,
        input_modality="voice",
    )
    await get_audit_log().log_interaction(audit_entry)


@router.post("/session", response_model=RealtimeSessionResponse)
async def create_realtime_session(
    request: RealtimeSessionRequest,
    realtime_service: RealtimeServiceInterface = Depends(_resolve_realtime_service),
):
    """Create an ephemeral realtime session with a short-lived token.

    Returns session credentials for WebRTC connection to Azure OpenAI Realtime API.
    Token TTL ≤60 seconds per Constitution Principle III.
    """
    session_id = request.session_id or str(uuid.uuid4())

    # Kill switch: if voice is disabled (e.g. no Realtime deployment configured
    # outside mock mode), fail fast with a clear 503 instead of attempting Azure
    # and erroring noisily. The frontend uses /health to hide the mic affordance.
    if not get_settings().voice_enabled:
        raise HTTPException(
            status_code=503,
            detail={"error": "voice_unavailable", "message": "Voice is disabled"},
        )

    _prune_expired_tokens()
    await _ensure_shared_session(session_id)

    try:
        response = await realtime_service.create_session(
            session_id=session_id,
            voice=request.voice,
            instructions=_sanitize_instructions(request.instructions),
        )
        response = _cap_token_ttl(response)
        _TOKEN_SESSIONS[response.token] = (response.session_id, response.expires_at)
        return response
    except Exception as e:
        if "VoiceUnavailable" in type(e).__name__:
            logger.warning("Realtime API unavailable: %s", e)
            raise HTTPException(
                status_code=503,
                detail={"error": "voice_unavailable", "message": str(e)},
            ) from e
        raise


@router.websocket("/ws")
async def websocket_tool_relay(
    websocket: WebSocket,
    session_id: str = Query(...),
    token: str = Query(...),
):
    """WebSocket relay for Realtime API tool calls.

    Receives tool_call_request frames, executes through pipeline,
    returns tool_call_response frames. Audio goes direct via WebRTC.

    Close codes:
    - 1000: Normal closure
    - 4001: Invalid token
    - 4002: Session already has an active connection
    - 4003: Voice unavailable (kill switch)
    - 1011: Server error
    """
    realtime_service = _resolve_realtime_service()

    # Kill switch also guards the WS relay: a previously-issued token must not be
    # able to execute voice tools after voice has been disabled.
    if not get_settings().voice_enabled:
        await websocket.accept()
        await websocket.close(code=4003, reason="Voice unavailable")
        return

    if not token or not _token_is_valid_for_session(token, session_id):
        await websocket.accept()
        await websocket.close(code=4001, reason="Invalid token")
        return

    # Atomically reject a second connection for the same session. The lock closes
    # the check/add race so two near-simultaneous connects can't both be admitted.
    async with _ACTIVE_WS_LOCK:
        if session_id in _ACTIVE_WS_SESSIONS:
            await websocket.accept()
            await websocket.close(code=4002, reason="Session already has an active connection")
            return
        _ACTIVE_WS_SESSIONS.add(session_id)

    await _ensure_shared_session(session_id)
    await websocket.accept()
    logger.info("WebSocket connected: session=%s", session_id)

    try:
        while True:
            data = await websocket.receive_json()

            try:
                tool_request = ToolCallRequest(
                    call_id=data.get("call_id", ""),
                    tool_name=data.get("tool_name", ""),
                    arguments=data.get("arguments", {}),
                )
            except Exception as e:
                await websocket.send_json({
                    "call_id": data.get("call_id", "unknown"),
                    "result": "",
                    "error": f"Invalid request: {e}",
                })
                continue

            start_time = datetime.now(UTC)
            try:
                response = await realtime_service.execute_tool(
                    call_id=tool_request.call_id,
                    tool_name=tool_request.tool_name,
                    arguments=tool_request.arguments,
                    session_id=session_id,
                )
                response_time_ms = int(
                    (datetime.now(UTC) - start_time).total_seconds() * 1000
                )
                if response.error is None:
                    content = _voice_transcript_content(tool_request.arguments, response.result)
                    await _append_voice_message(session_id, content)
                    await _log_voice_tool_call(
                        session_id=session_id,
                        tool_name=tool_request.tool_name,
                        result=response.result,
                        response_time_ms=response_time_ms,
                    )
                await websocket.send_json(response.model_dump())
            except Exception as e:
                logger.error("Tool execution error: %s", e)
                await websocket.send_json({
                    "call_id": tool_request.call_id,
                    "result": "",
                    "error": str(e),
                })

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected: session=%s", session_id)
    except Exception as e:
        logger.error("WebSocket error: %s", e)
        try:
            await websocket.close(code=1011, reason="Server error")
        except Exception:
            pass
    finally:
        _ACTIVE_WS_SESSIONS.discard(session_id)


@router.get("/health")
async def realtime_health():
    """Check realtime API availability.

    ``realtime_available`` reflects whether the BROWSER can actually negotiate a
    WebRTC voice session — which requires both the kill switch on
    (``voice_enabled``) AND a real Azure Realtime deployment configured. In pure
    mock mode (no Azure creds) the browser cannot negotiate media against the
    mock SDP endpoint, so this is False and the frontend gracefully hides the
    mic and stays text-only. The backend voice tool pipeline (sessions, WS relay,
    crisis/PII safety) is still exercised by unit tests regardless of this flag.
    """
    settings = get_settings()
    browser_voice_available = bool(
        settings.voice_enabled and settings.azure_openai_realtime_deployment
    )
    return {
        "realtime_available": browser_voice_available,
        "mock_mode": settings.mock_mode,
        "voice_enabled": settings.voice_enabled,
    }
