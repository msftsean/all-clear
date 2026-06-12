"""
All Clear agent-layer schemas (001-maf-rehost).

Ported from app.models.schemas (47 Doors university domain) and renamed to the
All Clear incident-triage domain defined in CONTEXT.md. Structured-output models
for the MAF pipeline: QueryAgent -> RouterExecutor -> ActionAgent.

The legacy app.models.schemas / app.models.enums remain in place because the
voice/phone paths still consume them (see spec.md Non-Goals). This module is the
canonical schema surface for the rehosted agent pipeline.

Field/term mapping (legacy 47 Doors -> All Clear):
    Department (enum)            -> Queue (enum)
    Priority (enum)              -> Severity (enum, SEV1..SEV4)
    Ticket / ticket_id           -> Incident / incident_id (AC-####)
    QueryResult                  -> SignalClassification
        .department_suggestion   -> .target_queue
        .intent                  -> .intent (unchanged)
        .intent_category         -> .intent_category (SignalCategory taxonomy)
        .entities                -> .entities (typed: location/system/severity_indicators)
        .confidence              -> .confidence
        .requires_escalation     -> .requires_escalation
        .pii_detected/.pii_types -> .pii_detected/.pii_types
        .sentiment               -> .sentiment
        .urgency_indicators      -> .urgency_indicators
        (new)                    -> .escalation_reason (pre-routing hint)
    RoutingDecision (legacy)     -> RoutingDecision (All Clear)
        .department              -> .target_queue
        .priority                -> .severity
        .escalate_to_human       -> .escalate
        .escalation_reason       -> .escalation_reason
        .suggested_sla_hours     -> .sla_minutes
        .routing_rules_applied   -> .routing_rules_applied
        (new)                    -> .outcome (ATTACH_TO_INCIDENT | OPEN_INCIDENT)
        (new)                    -> .matched_incident_id, .dedup_similarity, .magnitude
    ActionResult                 -> IncidentAction
        .ticket_id/.ticket_url   -> .incident_id
        .department              -> .queue
        (new)                    -> .severity, .sitrep, .citations
        .knowledge_articles      -> .knowledge_articles
        .estimated_response_time -> .estimated_response_time
        .escalated               -> .escalated
        .user_message            -> .user_message
    (new aggregate)              -> PipelineResult
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator

# Sentiment is domain-neutral; reuse the legacy enum to keep mock/live in lockstep.
from app.models.enums import Sentiment


# =============================================================================
# Enums (All Clear taxonomy)
# =============================================================================


class Queue(str, Enum):
    """Destination work stream for an incident (CONTEXT.md: replaces Department)."""

    FIELD_OPERATIONS = "field-operations"
    CUSTOMER_COMMS = "customer-comms"
    COMPLIANCE_DESK = "compliance-desk"
    ENGINEERING = "engineering"
    ESCALATIONS = "escalations"


class Severity(str, Enum):
    """SEV1 (most severe) through SEV4 (CONTEXT.md severity/SLA matrix)."""

    SEV1 = "SEV1"  # life safety / total outage / statutory clock; immediate escalation
    SEV2 = "SEV2"  # major impairment, public-facing, spreading
    SEV3 = "SEV3"  # contained, single-party impact
    SEV4 = "SEV4"  # informational / routine request


class SignalCategory(str, Enum):
    """Intent categories for an inbound signal, mapped to queues by RouterExecutor."""

    INFRASTRUCTURE_OUTAGE = "INFRASTRUCTURE_OUTAGE"  # downed lines, outages -> engineering
    FIELD_HAZARD = "FIELD_HAZARD"                    # on-the-ground hazard -> field-operations
    PUBLIC_SAFETY = "PUBLIC_SAFETY"                  # life-safety threat -> field-operations/escalations
    CUSTOMER_INQUIRY = "CUSTOMER_INQUIRY"            # status/info request -> customer-comms
    SERVICE_REQUEST = "SERVICE_REQUEST"              # routine service -> customer-comms
    COMPLIANCE_REPORT = "COMPLIANCE_REPORT"          # statutory/recall -> compliance-desk
    STATUS_CHECK = "STATUS_CHECK"                    # follow-up on existing incident
    HUMAN_REQUEST = "HUMAN_REQUEST"                  # explicit human handoff -> escalations
    GENERAL_INQUIRY = "GENERAL_INQUIRY"              # uncategorized -> customer-comms


class RoutingOutcome(str, Enum):
    """RouterExecutor dedup outcome (CONTEXT.md)."""

    ATTACH_TO_INCIDENT = "ATTACH_TO_INCIDENT"  # signal becomes a report on an existing incident
    OPEN_INCIDENT = "OPEN_INCIDENT"            # a new incident is created


class EscalationReason(str, Enum):
    """Reasons RouterExecutor escalates to a human queue (safety control)."""

    LIFE_SAFETY = "life_safety"
    STATUTORY_CLOCK = "statutory_clock"
    SEV1_INCIDENT = "sev1_incident"
    POLICY_KEYWORD_DETECTED = "policy_keyword_detected"
    PII_EXPOSURE = "pii_exposure"
    SENTIMENT_SAFETY = "sentiment_safety"
    USER_REQUESTED_HUMAN = "user_requested_human"
    CONFIDENCE_TOO_LOW = "confidence_too_low"


class IncidentStatus(str, Enum):
    """Lifecycle status of an incident."""

    OPEN = "open"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    CLOSED = "closed"


class ActionStatus(str, Enum):
    """Outcome status of the ActionAgent / attach path."""

    OPENED = "opened"          # new incident created (OPEN_INCIDENT path)
    ATTACHED = "attached"      # signal attached to existing incident (ATTACH path)
    ESCALATED = "escalated"    # routed to a human queue
    ERROR = "error"            # processing error


# =============================================================================
# QueryAgent output (FR-1)
# =============================================================================


class SignalEntities(BaseModel):
    """Entities extracted from a signal by QueryAgent."""

    location: Optional[str] = Field(default=None, description="Place referenced by the signal")
    system: Optional[str] = Field(default=None, description="System/asset referenced (grid, line, app)")
    severity_indicators: list[str] = Field(
        default_factory=list,
        description="Phrases indicating severity (e.g. 'fire', 'no power', 'injured')",
    )
    other: list[str] = Field(
        default_factory=list, description="Additional named entities"
    )


class SignalClassification(BaseModel):
    """QueryAgent structured output. Authority: classify only (Constitution Art. II)."""

    intent: str = Field(..., description="Primary detected intent")
    intent_category: SignalCategory = Field(..., description="Category grouping")
    target_queue: Queue = Field(..., description="Suggested destination queue")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Classification confidence")
    entities: SignalEntities = Field(default_factory=SignalEntities, description="Extracted entities")
    requires_escalation: bool = Field(default=False, description="Pre-routing escalation hint")
    escalation_reason: Optional[EscalationReason] = Field(
        default=None, description="Reason hint if requires_escalation is True"
    )
    pii_detected: bool = Field(default=False, description="Whether PII was found")
    pii_types: list[str] = Field(default_factory=list, description="Types of PII detected")
    sentiment: Sentiment = Field(default=Sentiment.NEUTRAL, description="Detected sentiment")
    urgency_indicators: list[str] = Field(
        default_factory=list, description="Urgency signals found"
    )


# =============================================================================
# RouterExecutor output (FR-2)
# =============================================================================


class RoutingDecision(BaseModel):
    """RouterExecutor structured output. Deterministic, zero LLM calls (Constitution Art. II)."""

    outcome: RoutingOutcome = Field(..., description="ATTACH_TO_INCIDENT or OPEN_INCIDENT")
    target_queue: Queue = Field(..., description="Destination queue")
    severity: Severity = Field(..., description="Mapped severity")
    sla_minutes: int = Field(..., gt=0, description="Response SLA in minutes for this severity")
    escalate: bool = Field(default=False, description="Whether a human queue handoff is required")
    escalation_reason: Optional[EscalationReason] = Field(
        default=None, description="Reason for escalation"
    )
    matched_incident_id: Optional[str] = Field(
        default=None, description="Incident id matched on ATTACH_TO_INCIDENT"
    )
    dedup_similarity: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Max cosine similarity found during dedup"
    )
    magnitude: Optional[int] = Field(
        default=None, ge=1, description="Incident magnitude after this report (ATTACH path)"
    )
    routing_rules_applied: list[str] = Field(
        default_factory=list, description="Which rules determined this decision"
    )

    @model_validator(mode="after")
    def _check_invariants(self) -> "RoutingDecision":
        if self.escalate and self.escalation_reason is None:
            raise ValueError("escalation_reason is required when escalate is True")
        if self.outcome is RoutingOutcome.ATTACH_TO_INCIDENT and not self.matched_incident_id:
            raise ValueError("matched_incident_id is required for ATTACH_TO_INCIDENT")
        return self


# =============================================================================
# ActionAgent domain records and output (FR-3)
# =============================================================================


class KnowledgeArticle(BaseModel):
    """A relevant knowledge-base article surfaced by search_knowledge."""

    article_id: str = Field(..., description="Unique article identifier")
    title: str = Field(..., description="Article title")
    url: str = Field(..., description="Link to full article")
    snippet: Optional[str] = Field(default=None, max_length=400, description="Brief preview")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Search relevance score")


class IncidentRecord(BaseModel):
    """An incident as stored by the IncidentStore (create_incident output)."""

    incident_id: str = Field(..., description="Incident id, format AC-####")
    queue: Queue = Field(..., description="Owning queue")
    severity: Severity = Field(..., description="Incident severity")
    status: IncidentStatus = Field(default=IncidentStatus.OPEN, description="Lifecycle status")
    summary: str = Field(..., description="Short incident summary")
    intent_category: SignalCategory = Field(..., description="Category of the originating signal")
    magnitude: int = Field(default=1, ge=1, description="Count of reports attached")
    sla_minutes: int = Field(..., gt=0, description="Response SLA in minutes")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(default=None, description="Last update timestamp")
    escalated: bool = Field(default=False, description="Whether the incident is escalated")

    @model_validator(mode="after")
    def _validate_id(self) -> "IncidentRecord":
        import re

        if not re.match(r"^AC-\d{4,}$", self.incident_id):
            raise ValueError(f"Invalid incident id. Expected AC-####, got {self.incident_id}")
        return self


class Citation(BaseModel):
    """A source record backing a factual claim in a sitrep (Constitution Art. IV)."""

    source_id: str = Field(..., description="Identifier of the cited source record")
    source_type: str = Field(..., description="Kind of source (incident, signal, kb_article)")
    quote: str = Field(..., description="The grounded snippet supporting the claim")


class SitrepDraft(BaseModel):
    """Citation-grounded situation report produced by generate_sitrep."""

    incident_id: str = Field(..., description="Incident the sitrep summarizes")
    summary: str = Field(..., description="Situation summary; every claim must be cited")
    citations: list[Citation] = Field(
        default_factory=list, description="Source records backing the summary"
    )


class IncidentAction(BaseModel):
    """ActionAgent / attach-path output."""

    status: ActionStatus = Field(..., description="Outcome status")
    incident_id: Optional[str] = Field(default=None, description="Incident id involved")
    queue: Queue = Field(..., description="Queue that received the signal")
    severity: Severity = Field(..., description="Severity of the incident")
    knowledge_articles: list[KnowledgeArticle] = Field(
        default_factory=list, max_length=3, description="Retrieved KB articles (OPEN path only)"
    )
    sitrep: Optional[SitrepDraft] = Field(default=None, description="Generated sitrep, if any")
    citations: list[Citation] = Field(
        default_factory=list, description="Citations backing user_message claims"
    )
    estimated_response_time: str = Field(..., description="Human-readable SLA estimate")
    escalated: bool = Field(default=False, description="Whether escalation occurred")
    user_message: str = Field(..., description="Acknowledgment/response shown to the reporter")


# =============================================================================
# Pipeline aggregate (FR-4)
# =============================================================================


class PipelineResult(BaseModel):
    """End-to-end result of AllClearPipeline.process_signal."""

    session_id: str = Field(..., description="Session that produced this signal")
    channel: str = Field(..., description="Inbound channel (chat, voice, phone, report)")
    signal_text: str = Field(..., description="Raw inbound signal text")
    classification: SignalClassification = Field(..., description="QueryAgent output")
    routing: RoutingDecision = Field(..., description="RouterExecutor output")
    action: IncidentAction = Field(..., description="ActionAgent / attach-path output")
    processing_ms: Optional[int] = Field(
        default=None, ge=0, description="End-to-end processing time in milliseconds"
    )


__all__ = [
    "Queue",
    "Severity",
    "SignalCategory",
    "RoutingOutcome",
    "EscalationReason",
    "IncidentStatus",
    "ActionStatus",
    "SignalEntities",
    "SignalClassification",
    "RoutingDecision",
    "KnowledgeArticle",
    "IncidentRecord",
    "Citation",
    "SitrepDraft",
    "IncidentAction",
    "PipelineResult",
]
