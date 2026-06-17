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
        """Return the 4 pipeline tool definitions."""
        return [
            ToolDefinition(
                name="analyze_and_route_query",
                description="Analyze a student support query, classify intent, and route to the appropriate department.",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user's support query",
                        }
                    },
                    "required": ["query"],
                },
            ),
            ToolDefinition(
                name="check_ticket_status",
                description="Check the current status of a support ticket by its ID.",
                parameters={
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "Ticket ID to check status for",
                        }
                    },
                    "required": ["ticket_id"],
                },
            ),
            ToolDefinition(
                name="search_knowledge_base",
                description="Search the university knowledge base for articles related to a query.",
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
                    "Transfer the student to a human support agent. Use this when the student "
                    "explicitly asks for a human, mentions policy-related topics (appeals, "
                    "waivers, refunds, financial aid), or discusses sensitive topics (Title IX, "
                    "mental health, discrimination, threats, safety). Provide the reason and set "
                    "priority to 'urgent' for Title IX and mental health topics."
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
                            "description": "Target department",
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
        if tool_name == "analyze_and_route_query":
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
        elif tool_name == "check_ticket_status":
            ticket_id = arguments.get("ticket_id", "TKT-MOCK-0001")
            result = json.dumps({
                "ticket_id": ticket_id,
                "status": "in_progress",
                "department": "IT",
                "created_at": "2026-01-01T10:00:00Z",
                "estimated_resolution": "2026-01-01T14:00:00Z",
                "assigned_to": "Support Team",
            })
        elif tool_name == "search_knowledge_base":
            result = json.dumps({
                "articles": [
                    {
                        "article_id": "KB-001",
                        "title": "How to Reset Your Password",
                        "snippet": "Visit the IT portal at https://it.university.edu and click 'Forgot Password'.",
                        "relevance_score": 0.92,
                    },
                    {
                        "article_id": "KB-002",
                        "title": "VPN Setup Guide",
                        "snippet": "Download the VPN client from the software portal and use your university credentials.",
                        "relevance_score": 0.74,
                    },
                ]
            })
        elif tool_name == "escalate_to_human":
            result = json.dumps({
                "escalated": True,
                "reason": arguments.get("reason", "User requested escalation"),
                "department": arguments.get("department", "IT"),
                "priority": arguments.get("priority", "urgent"),
                "ticket_id": f"ESC-MOCK-{uuid4().hex[:8].upper()}",
                "message": "A human agent will be with you shortly.",
            })
        else:
            return ToolCallResponse(
                call_id=call_id,
                result="",
                error=f"Unknown tool: {tool_name}",
            )

        return ToolCallResponse(call_id=call_id, result=redact_pii(result), error=None)
