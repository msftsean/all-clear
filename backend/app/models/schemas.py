"""Session and audit records shared by All Clear input channels."""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.models.enums import Sentiment


class ConversationTurn(BaseModel):
    """A PII-safe signal and response preserved in a session."""

    turn_number: int = Field(..., ge=1)
    timestamp: datetime
    intent: str
    escalated: bool = False
    signal_text: Optional[str] = Field(default=None, max_length=4000)
    agent_response: Optional[str] = Field(default=None, max_length=4000)
    incident_id: Optional[str] = None
    input_modality: Literal["text", "voice", "phone"] = "text"


class Session(BaseModel):
    """An anonymous conversation session for signal history."""

    session_id: UUID
    student_id_hash: str = Field(
        ..., min_length=64, max_length=64, description="Hashed anonymous reporter identifier"
    )
    created_at: datetime
    last_active: datetime
    conversation_history: list[ConversationTurn] = Field(default_factory=list, max_length=50)
    ttl: int = Field(default=7776000, description="Retention period in seconds")
    topic_summary: Optional[str] = Field(default=None, max_length=200)
    incident_ids: list[str] = Field(default_factory=list)
    status: Literal["active", "closed"] = "active"


class AuditLog(BaseModel):
    """Immutable audit record for a classified signal or voice tool call."""

    log_id: UUID
    timestamp: datetime
    student_id_hash: str = Field(
        ..., min_length=64, max_length=64, description="Hashed anonymous reporter identifier"
    )
    session_id: UUID
    detected_intent: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    routed_queue: str = Field(..., description="All Clear destination queue")
    incident_id: Optional[str] = None
    escalated: bool = False
    escalation_reason: Optional[str] = None
    pii_detected: bool = False
    sentiment: Sentiment = Sentiment.NEUTRAL
    response_time_ms: int = Field(..., ge=0)
    input_modality: Literal["text", "voice", "phone"] = "text"

    @field_validator("escalation_reason")
    @classmethod
    def require_reason_when_escalated(cls, value: Optional[str], info) -> Optional[str]:
        if info.data.get("escalated", False) and value is None:
            raise ValueError("escalation_reason is required when escalated is True")
        return value
