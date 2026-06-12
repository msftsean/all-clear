"""Tests for the All Clear agent schemas (001-maf-rehost, T2)."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.agents.schemas import (
    ActionStatus,
    Citation,
    EscalationReason,
    IncidentAction,
    IncidentRecord,
    IncidentStatus,
    KnowledgeArticle,
    PipelineResult,
    Queue,
    RoutingDecision,
    RoutingOutcome,
    Severity,
    SignalCategory,
    SignalClassification,
    SignalEntities,
    SitrepDraft,
)
from app.models.enums import Sentiment


def _classification() -> SignalClassification:
    return SignalClassification(
        intent="report_downed_line",
        intent_category=SignalCategory.INFRASTRUCTURE_OUTAGE,
        target_queue=Queue.ENGINEERING,
        confidence=0.93,
        entities=SignalEntities(location="5th & Main", system="power grid", severity_indicators=["sparks"]),
    )


def test_queue_and_severity_values() -> None:
    assert Queue.FIELD_OPERATIONS.value == "field-operations"
    assert {s.value for s in Severity} == {"SEV1", "SEV2", "SEV3", "SEV4"}


def test_signal_classification_roundtrip() -> None:
    c = _classification()
    dumped = c.model_dump()
    assert dumped["target_queue"] == "engineering"
    assert dumped["sentiment"] == Sentiment.NEUTRAL.value
    assert SignalClassification.model_validate(dumped) == c


def test_routing_decision_open_incident() -> None:
    d = RoutingDecision(
        outcome=RoutingOutcome.OPEN_INCIDENT,
        target_queue=Queue.ENGINEERING,
        severity=Severity.SEV2,
        sla_minutes=60,
        routing_rules_applied=["category_to_queue", "severity_sev2"],
    )
    assert d.matched_incident_id is None


def test_routing_decision_attach_requires_incident_id() -> None:
    with pytest.raises(ValidationError):
        RoutingDecision(
            outcome=RoutingOutcome.ATTACH_TO_INCIDENT,
            target_queue=Queue.ENGINEERING,
            severity=Severity.SEV2,
            sla_minutes=60,
        )


def test_routing_decision_escalate_requires_reason() -> None:
    with pytest.raises(ValidationError):
        RoutingDecision(
            outcome=RoutingOutcome.OPEN_INCIDENT,
            target_queue=Queue.ESCALATIONS,
            severity=Severity.SEV1,
            sla_minutes=15,
            escalate=True,
        )
    ok = RoutingDecision(
        outcome=RoutingOutcome.OPEN_INCIDENT,
        target_queue=Queue.ESCALATIONS,
        severity=Severity.SEV1,
        sla_minutes=15,
        escalate=True,
        escalation_reason=EscalationReason.SEV1_INCIDENT,
    )
    assert ok.escalate is True


def test_incident_record_id_validation() -> None:
    rec = IncidentRecord(
        incident_id="AC-0042",
        queue=Queue.ENGINEERING,
        severity=Severity.SEV2,
        summary="Downed power line at 5th & Main",
        intent_category=SignalCategory.INFRASTRUCTURE_OUTAGE,
        sla_minutes=60,
        created_at=datetime.now(timezone.utc),
    )
    assert rec.status is IncidentStatus.OPEN
    with pytest.raises(ValidationError):
        IncidentRecord(
            incident_id="TKT-42",
            queue=Queue.ENGINEERING,
            severity=Severity.SEV2,
            summary="bad id",
            intent_category=SignalCategory.INFRASTRUCTURE_OUTAGE,
            sla_minutes=60,
            created_at=datetime.now(timezone.utc),
        )


def test_incident_action_and_sitrep() -> None:
    action = IncidentAction(
        status=ActionStatus.OPENED,
        incident_id="AC-0042",
        queue=Queue.ENGINEERING,
        severity=Severity.SEV2,
        knowledge_articles=[
            KnowledgeArticle(article_id="KB-1", title="Outage SOP", url="http://kb/1", relevance_score=0.8)
        ],
        sitrep=SitrepDraft(
            incident_id="AC-0042",
            summary="One downed line reported.",
            citations=[Citation(source_id="AC-0042", source_type="incident", quote="downed line")],
        ),
        estimated_response_time="1 hour",
        user_message="Thanks, crews are en route.",
    )
    assert action.sitrep is not None
    assert action.sitrep.citations[0].source_type == "incident"


def test_pipeline_result_composition() -> None:
    result = PipelineResult(
        session_id="sess-1",
        channel="chat",
        signal_text="downed line sparking at 5th and main",
        classification=_classification(),
        routing=RoutingDecision(
            outcome=RoutingOutcome.OPEN_INCIDENT,
            target_queue=Queue.ENGINEERING,
            severity=Severity.SEV2,
            sla_minutes=60,
        ),
        action=IncidentAction(
            status=ActionStatus.OPENED,
            incident_id="AC-0042",
            queue=Queue.ENGINEERING,
            severity=Severity.SEV2,
            estimated_response_time="1 hour",
            user_message="Logged.",
        ),
    )
    assert result.routing.outcome is RoutingOutcome.OPEN_INCIDENT
    assert result.action.incident_id == "AC-0042"


def test_legacy_field_mapping_documented() -> None:
    """The module must document the legacy 47 Doors -> All Clear field mapping (T2 done-when)."""
    import app.agents.schemas as schemas_mod

    doc = schemas_mod.__doc__ or ""
    for legacy in ["Department", "Priority", "QueryResult", "department_suggestion", "suggested_sla_hours"]:
        assert legacy in doc, f"mapping comment missing legacy term: {legacy}"
