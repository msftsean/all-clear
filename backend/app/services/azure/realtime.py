"""
Azure OpenAI Realtime API service for production voice interaction.
Manages ephemeral session tokens and tool call delegation.
"""

import asyncio
import json
import logging
from datetime import UTC, datetime, timedelta

import httpx
from azure.core.credentials import AccessToken

from app.agents.safety import voice_crisis_result
from app.models.voice_schemas import RealtimeSessionResponse, ToolCallResponse, ToolDefinition
from app.services.interfaces import RealtimeServiceInterface
from app.services.pii import redact_pii

VOICE_SYSTEM_PROMPT = """You are All Clear, an emergency and incident-triage assistant speaking with a caller by voice.

The caller may be reporting something happening right now — a power outage, a downed or sparking line, a gas leak, a fire, a water main break, flooding, a blocked road — or asking about a bill, the status of an incident, or asking for a person.

Voice-specific instructions:
- Speak concisely and naturally. Do not use markdown formatting.
- For any life-safety situation (fire, gas, downed/sparking line, someone injured or trapped, carbon monoxide), tell the caller to get to safety and call 911 first, then escalate.
- Always ask for the location early, and whether anyone is in danger.
- Spell out incident and ticket IDs character by character (e.g., "I-N-C dash one zero two four").
- Do NOT repeat personal identifying information (SSN, account number, email, phone).
- If you cannot understand the request, ask one short clarifying question.
- Summarize the most relevant guidance conversationally rather than listing everything.
- Acknowledge the caller's situation before giving instructions, and stay calm and reassuring.
- Drafts and public statements always need human approval before they go out.
"""

logger = logging.getLogger(__name__)


class VoiceUnavailableError(Exception):
    """Raised when Azure OpenAI Realtime API is unavailable."""
    pass


class AzureRealtimeService(RealtimeServiceInterface):
    """Production implementation using the Azure OpenAI Realtime API with managed identity."""

    def __init__(
        self,
        endpoint: str,
        deployment: str,
        api_version: str = "2025-04-01-preview",
        api_key: str | None = None,
        credential: object | None = None,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.deployment = deployment
        self.api_version = api_version
        self.api_key = api_key
        self.credential = credential
        self._client = httpx.AsyncClient(timeout=30.0)
        self._token: AccessToken | None = None
        self._credential_lock = asyncio.Lock()

    async def _get_auth_header(self) -> dict[str, str]:
        """Get authentication header using managed identity or API key fallback."""
        if self.api_key:
            logger.info("Realtime auth: using API key")
            return {"api-key": self.api_key}

        if not self.credential:
            async with self._credential_lock:
                if not self.credential:
                    from azure.identity.aio import ManagedIdentityCredential
                    self.credential = ManagedIdentityCredential()
                    logger.info("Realtime auth: created ManagedIdentityCredential")

        refresh_buffer_seconds = 300
        needs_refresh = (
            not self._token
            or datetime.now(UTC) >= datetime.fromtimestamp(
                self._token.expires_on - refresh_buffer_seconds, tz=UTC
            )
        )

        if needs_refresh:
            try:
                self._token = await self.credential.get_token(
                    "https://cognitiveservices.azure.com/.default"
                )
                logger.info("Realtime auth: token acquired, expires_on=%s", self._token.expires_on)
            except Exception as exc:
                logger.error(f"Realtime auth: token acquisition failed: {exc}")
                raise VoiceUnavailableError(
                    f"Failed to acquire managed identity token: {exc}"
                ) from exc

        return {"Authorization": f"Bearer {self._token.token}"}

    async def create_session(
        self,
        session_id: str,
        voice: str,
        instructions: str | None = None,
    ) -> RealtimeSessionResponse:
        """Create an ephemeral realtime session via the Azure OpenAI API."""
        url = f"{self.endpoint}/openai/v1/realtime/client_secrets"

        try:
            auth_header = await self._get_auth_header()
        except VoiceUnavailableError:
            raise
        except Exception as exc:
            raise VoiceUnavailableError(
                f"Authentication setup failed: {exc}"
            ) from exc

        auth_type = "Bearer" if "Authorization" in auth_header else "api-key"
        logger.info(
            "Realtime create_session: url=%s, auth_type=%s, deployment=%s",
            url,
            auth_type,
            self.deployment,
        )

        headers = {
            **auth_header,
            "Content-Type": "application/json",
        }

        # Use GA nested format for session config in /client_secrets body.
        # Preview flat fields (voice, input_audio_transcription) cause 500;
        # GA nested fields (audio.input.transcription, audio.output.voice) work.
        session_config = {
            "session": {
                "type": "realtime",
                "model": self.deployment,
                "instructions": instructions or VOICE_SYSTEM_PROMPT,
                "audio": {
                    "input": {
                        "transcription": {
                            "model": "whisper-1",
                        },
                    },
                    "output": {
                        "voice": voice,
                        "transcription": {
                            "model": "whisper-1",
                        },
                    },
                },
            },
        }

        # Try with output transcription first; fall back without it if rejected.
        # The frontend session.update also requests it as a backup.
        response = None
        for attempt, config in enumerate([session_config, None]):
            if config is None:
                # Build fallback config without audio.output.transcription
                fallback = {
                    "session": {
                        **session_config["session"],
                        "audio": {
                            "input": session_config["session"]["audio"]["input"],
                            "output": {"voice": voice},
                        },
                    },
                }
                config = fallback
                logger.warning("Retrying /client_secrets without audio.output.transcription")

            try:
                response = await self._client.post(url, headers=headers, json=config)
                response.raise_for_status()
                break
            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code
                error_detail = exc.response.text
                # Retry on server error only on first attempt
                if attempt == 0 and status_code >= 500:
                    logger.warning("Realtime API rejected config (attempt 1): %s", status_code)
                    continue
                logger.error(
                    "Realtime API error: status=%s, auth_type=%s, detail=%s",
                    status_code,
                    auth_type,
                    error_detail,
                )
                if status_code == 401:
                    error_msg = (
                        "Authentication failed (401): Credentials rejected. "
                        f"auth_type={auth_type}. Details: {error_detail}"
                    )
                elif status_code == 403:
                    error_msg = (
                        f"Authorization failed (403): auth_type={auth_type}. "
                        f"Details: {error_detail}"
                    )
                elif status_code == 404:
                    error_msg = (
                        f"Endpoint not found (404): deployment='{self.deployment}', url={url}. "
                        f"Details: {error_detail}"
                    )
                elif status_code >= 500:
                    error_msg = f"Azure OpenAI service error ({status_code}): {error_detail}"
                else:
                    error_msg = f"Azure OpenAI Realtime API error ({status_code}): {error_detail}"
                raise VoiceUnavailableError(error_msg) from exc
            except httpx.RequestError as exc:
                raise VoiceUnavailableError(
                    f"Network error reaching Azure OpenAI Realtime API at {url}: {exc}"
                ) from exc

        data = response.json()
        # Azure /client_secrets returns: {"value": "eph_...", "expires_at": "...", "session": {...}}
        token = data.get("value", "")
        expires_at_str = data.get("expires_at")

        if not token:
            logger.error(
                "Realtime: empty ephemeral token from API. Response keys: %s",
                list(data.keys()),
            )
            raise VoiceUnavailableError("Azure OpenAI returned empty ephemeral token")

        logger.info(
            "Realtime: ephemeral token acquired, len=%s, expires_at=%s",
            len(token),
            expires_at_str,
        )

        if expires_at_str:
            try:
                expires_at = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
            except (ValueError, AttributeError):
                expires_at = datetime.now(UTC) + timedelta(seconds=60)
        else:
            expires_at = datetime.now(UTC) + timedelta(seconds=60)

        return RealtimeSessionResponse(
            session_id=session_id,
            token=token,
            expires_at=expires_at,
            endpoint=self.endpoint,
            deployment=self.deployment,
        )

    async def get_tool_definitions(self) -> list[ToolDefinition]:
        """Return the 4 pipeline tool definitions."""
        return [
            ToolDefinition(
                name="analyze_and_route_query",
                description=(
                    "Analyze an inbound incident report or question, classify what is "
                    "happening (outage, field hazard, public-safety/life-safety, customer "
                    "inquiry, status check, or human request), and route it to the right "
                    "queue. Use this for any new report the caller describes."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The caller's report or question, in their own words",
                        }
                    },
                    "required": ["query"],
                },
            ),
            ToolDefinition(
                name="check_ticket_status",
                description="Check the current status of an incident or ticket by its ID.",
                parameters={
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "Incident or ticket ID to check status for",
                        }
                    },
                    "required": ["ticket_id"],
                },
            ),
            ToolDefinition(
                name="search_knowledge_base",
                description=(
                    "Search the All Clear incident knowledge base for response guidance "
                    "and standard procedures related to a situation (e.g. downed line, gas "
                    "leak, outage, water main break)."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for incident response guidance",
                        }
                    },
                    "required": ["query"],
                },
            ),
            ToolDefinition(
                name="escalate_to_human",
                description=(
                    "Transfer the caller to a human dispatcher. Use this when the caller "
                    "explicitly asks for a person, when there is a life-safety threat (fire, "
                    "gas, downed/sparking line, injury, someone trapped, carbon monoxide), or "
                    "when a statutory/compliance reporting clock applies. Provide the reason "
                    "and set priority to 'urgent' for any life-safety situation."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "reason": {
                            "type": "string",
                            "description": "Reason for escalation",
                        },
                        "department": {
                            "type": "string",
                            "description": "Target queue or team",
                        },
                    },
                    "required": ["reason"],
                },
            ),
        ]

    async def execute_tool(
        self,
        call_id: str,
        tool_name: str,
        arguments: dict,
        session_id: str,
    ) -> ToolCallResponse:
        """Delegate a Realtime API tool call to real backend services."""
        arguments = redact_pii(arguments)
        crisis = voice_crisis_result(arguments)
        if crisis is not None:
            return ToolCallResponse(call_id=call_id, result=json.dumps(crisis), error=None)
        from app.core.dependencies import (
            get_knowledge_service,
            get_llm_service,
            get_ticket_service,
        )

        ticket_svc = get_ticket_service()
        knowledge_svc = get_knowledge_service()

        try:
            if tool_name == "analyze_and_route_query":
                query = arguments.get("query", "")
                logger.info("execute_tool: analyze_and_route_query query=%s", query[:100])

                # Classify intent via LLM (same as text chat QueryAgent)
                llm_svc = get_llm_service()
                query_result = await llm_svc.classify_intent(query)
                dept_enum = query_result.department_suggestion
                intent = query_result.intent

                from app.models.enums import Priority

                # Escalation-worthy queries get URGENT, else MEDIUM
                priority_enum = (
                    Priority.URGENT if query_result.requires_escalation else Priority.MEDIUM
                )

                # Create a real ticket
                ticket_id, ticket_url = await ticket_svc.create_ticket(
                    department=dept_enum,
                    priority=priority_enum,
                    summary=f"Phone call: {query[:150]}",
                    description=f"Submitted via phone call (session {session_id}). Query: {query}",
                    student_id_hash=f"phone-{session_id}",
                )
                logger.info("execute_tool: created ticket %s dept=%s", ticket_id, dept_enum.value)

                result = json.dumps({
                    "intent": intent or "general_question",
                    "department": dept_enum.value,
                    "confidence": query_result.confidence,
                    "requires_escalation": query_result.requires_escalation,
                    "escalated": query_result.requires_escalation,
                    "priority": priority_enum.value,
                    "ticket_id": ticket_id,
                    "ticket_url": ticket_url,
                })

            elif tool_name == "check_ticket_status":
                ticket_id = arguments.get("ticket_id", "")
                logger.info("execute_tool: check_ticket_status id=%s", ticket_id)

                status_resp = await ticket_svc.get_ticket_status(ticket_id)
                if status_resp:
                    status = (
                        status_resp.status.value
                        if hasattr(status_resp.status, "value")
                        else str(status_resp.status)
                    )
                    department = (
                        status_resp.department.value
                        if hasattr(status_resp.department, "value")
                        else str(status_resp.department)
                    )
                    result = json.dumps({
                        "ticket_id": status_resp.ticket_id,
                        "status": status,
                        "department": department,
                        "assigned_to": status_resp.assigned_to or "Unassigned",
                        "summary": status_resp.summary or "",
                    })
                else:
                    result = json.dumps({
                        "ticket_id": ticket_id,
                        "status": "not_found",
                        "message": f"No ticket found with ID {ticket_id}",
                    })

            elif tool_name == "search_knowledge_base":
                query = arguments.get("query", "")
                logger.info("execute_tool: search_knowledge_base query=%s", query[:100])

                articles = await knowledge_svc.search(query=query, limit=3)
                result = json.dumps({
                    "articles": [
                        {
                            "article_id": a.article_id,
                            "title": a.title,
                            "snippet": a.snippet or "",
                            "relevance_score": (
                                float(a.relevance_score) if a.relevance_score else 0.0
                            ),
                        }
                        for a in articles
                    ]
                })
                logger.info("execute_tool: KB returned %d articles", len(articles))

            elif tool_name == "escalate_to_human":
                reason = arguments.get("reason", "Caller requested human agent")
                department = arguments.get("department", "IT")
                logger.info(
                    "execute_tool: escalate_to_human reason=%s dept=%s",
                    reason[:80],
                    department,
                )

                from app.models.enums import Department, Priority

                try:
                    dept_enum = Department(department)
                except ValueError:
                    dept_enum = Department.ESCALATE_TO_HUMAN

                ticket_id, ticket_url = await ticket_svc.create_ticket(
                    department=dept_enum,
                    priority=Priority.URGENT,
                    summary=f"ESCALATION: {reason[:150]}",
                    description=(
                        "Phone caller requested human escalation. "
                        f"Reason: {reason}. Session: {session_id}"
                    ),
                    student_id_hash=f"phone-{session_id}",
                )
                logger.info("execute_tool: escalation ticket created %s", ticket_id)

                result = json.dumps({
                    "escalated": True,
                    "reason": reason,
                    "department": department,
                    "priority": Priority.URGENT.value,
                    "ticket_id": ticket_id,
                    "ticket_url": ticket_url,
                    "message": (
                        f"Escalation ticket {ticket_id} created. "
                        "A human agent will follow up."
                    ),
                })
            else:
                return ToolCallResponse(
                    call_id=call_id,
                    result="",
                    error=f"Unknown tool: {tool_name}",
                )

        except Exception as exc:
            logger.error("execute_tool: %s failed: %s", tool_name, exc, exc_info=True)
            return ToolCallResponse(
                call_id=call_id,
                result="",
                error=f"Tool execution failed: {exc}",
            )

        return ToolCallResponse(call_id=call_id, result=redact_pii(result), error=None)

    async def close(self) -> None:
        """Close the HTTP client and credential."""
        await self._client.aclose()
        if hasattr(self.credential, 'close'):
            await self.credential.close()
