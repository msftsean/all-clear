"""
Mock Realtime service for testing and demo mode.
Returns deterministic responses without requiring Azure credentials.
"""

import json
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.agents.safety import voice_crisis_result
from app.models.voice_schemas import RealtimeSessionResponse, ToolCallResponse, ToolDefinition
from app.services.azure.realtime import VOICE_SYSTEM_PROMPT
from app.services.interfaces import RealtimeServiceInterface
from app.services.pii import redact_pii


class MockRealtimeService(RealtimeServiceInterface):
    """Mock implementation of the Azure OpenAI Realtime API service."""

    _pipeline = None

    def _get_pipeline(self, factory):
        """Lazily build and cache the incident pipeline (persists dedup state)."""
        if self._pipeline is None:
            self._pipeline = factory()
        return self._pipeline

    async def create_session(
        self,
        session_id: str,
        voice: str,
        instructions: str | None = None,
    ) -> RealtimeSessionResponse:
        """Return a mock ephemeral session token."""
        self._last_session_config = {
            "session": {
                "type": "realtime",
                "model": "gpt-realtime",
                "audio": {"output": {"voice": voice}},
                "input_audio_transcription": {"model": "whisper-1"},
                "instructions": instructions or VOICE_SYSTEM_PROMPT,
            },
        }
        return RealtimeSessionResponse(
            session_id=session_id,
            token=f"eph_mock_{uuid4()}",
            expires_at=datetime.now(UTC) + timedelta(seconds=60),
            endpoint="http://localhost:8000/mock",
            deployment="gpt-realtime",
        )

    async def get_tool_definitions(self) -> list[ToolDefinition]:
        """Return the incident-triage tool definitions."""
        return [
            ToolDefinition(
                name="analyze_and_route_query",
                description="Classify an inbound signal, deduplicate it, and open or attach an incident.",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The caller's incident signal",
                        }
                    },
                    "required": ["query"],
                },
            ),
            ToolDefinition(
                name="check_ticket_status",
                description="Check the current status of an All Clear incident by its ID.",
                parameters={
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "All Clear incident ID to check",
                        }
                    },
                    "required": ["ticket_id"],
                },
            ),
            ToolDefinition(
                name="search_knowledge_base",
                description="Search operational guidance for a signal or incident.",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for knowledge base",
                        }
                    },
                    "required": ["query"],
                },
            ),
            ToolDefinition(
                name="escalate_to_human",
                description=(
                    "Escalate an incident to a human queue. Use this for life-safety, "
                    "statutory-clock, public-risk, or explicit human-handoff requests."
                ),
                parameters={
                    "type": "object",
                    "properties": {
                        "reason": {
                            "type": "string",
                            "description": "Reason for escalation",
                        },
                        "queue": {
                            "type": "string",
                            "description": "Target All Clear queue",
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
        """Execute a mock pipeline tool call."""
        arguments = redact_pii(arguments)
        crisis = voice_crisis_result(arguments)
        if crisis is not None:
            return ToolCallResponse(call_id=call_id, result=json.dumps(crisis), error=None)
        if tool_name in {"analyze_and_route_query", "analyze_and_route_signal"}:
            query = arguments.get("query", "")
            # Repointed at the All Clear pipeline adapter (001-maf-rehost, T10):
            # the voice tool now runs the real three-agent incident pipeline instead
            # of a bespoke keyword stub, so voice and text stay in lockstep.
            import hashlib
            from app.agents.pipeline import build_mock_pipeline

            _voice_student_hash = hashlib.sha256(b"demo_student").hexdigest()
            pipeline = self._get_pipeline(build_mock_pipeline)
            outcome = await pipeline.process_signal(
                text=query, session_id=session_id, channel="voice",
                student_id_hash=_voice_student_hash,
            )
            result = json.dumps({
                "intent": outcome.classification.intent,
                "intent_category": outcome.classification.intent_category.value,
                "queue": outcome.routing.target_queue.value,
                "severity": outcome.routing.severity.value,
                "outcome": outcome.routing.outcome.value,
                "incident_id": outcome.action.incident_id,
                "escalated": outcome.action.escalated,
                "estimated_response_time": outcome.action.estimated_response_time,
                "message": outcome.action.user_message,
            })
        elif tool_name in {"check_ticket_status", "check_incident_status"}:
            incident_id = arguments.get("incident_id", arguments.get("ticket_id", "AC-0001"))
            result = json.dumps({
                "incident_id": incident_id,
                "status": "open",
                "queue": "field-operations",
                "created_at": "2026-01-01T10:00:00Z",
                "severity": "SEV3",
                "estimated_response": "2026-01-01T14:00:00Z",
            })
        elif tool_name == "search_knowledge_base":
            result = json.dumps({
                "articles": [
                    {
                        "article_id": "KB-001",
                        "title": "Field response for a downed power line",
                        "snippet": "Keep people clear of the area and dispatch field operations.",
                        "relevance_score": 0.92,
                    },
                    {
                        "article_id": "KB-002",
                        "title": "Public communications during an outage",
                        "snippet": "Publish only human-approved updates with an incident reference.",
                        "relevance_score": 0.74,
                    },
                ]
            })
        elif tool_name == "escalate_to_human":
            result = json.dumps({
                "escalated": True,
                "reason": arguments.get("reason", "User requested escalation"),
                "queue": arguments.get("queue", "escalations"),
                "severity": arguments.get("severity", "SEV1"),
                "incident_id": f"AC-{uuid4().hex[:4].upper()}",
                "message": "The incident is queued for human response.",
            })
        else:
            return ToolCallResponse(
                call_id=call_id,
                result="",
                error=f"Unknown tool: {tool_name}",
            )

        return ToolCallResponse(call_id=call_id, result=redact_pii(result), error=None)
