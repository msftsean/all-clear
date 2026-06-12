"""
RouterExecutor verifier (001-maf-rehost, T7). Owned by Barton (Loop Protocol rule 3).

Asserts the two T7 invariants:
1. The router module imports NO language-model client (Constitution Art. II): the source
   contains no "chat" substring and importing it pulls in no agent_framework chat client.
2. Routing is deterministic and rule-correct: severity/SLA mapping, escalation, and
   dedup ATTACH vs OPEN behave as specified, with zero model calls.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from pathlib import Path

import pytest

from app.agents.envelopes import ClassifiedSignal
from app.agents.router_agent import RouterExecutor
from app.agents.schemas import (
    EscalationReason,
    IncidentRecord,
    Queue,
    RoutingOutcome,
    Severity,
    SignalCategory,
    SignalClassification,
    SignalEntities,
)
from app.core.config import Settings
from app.services.mock.embeddings import mock_embed
from app.services.mock.incident_store import MockIncidentStore

_ROUTER_SRC = Path(__file__).parent.parent / "app" / "agents" / "router_agent.py"


def _settings() -> Settings:
    return Settings()


def _router(store: MockIncidentStore) -> RouterExecutor:
    return RouterExecutor(mock_embed, store, _settings())


def _classify(
    category: SignalCategory,
    *,
    queue: Queue,
    confidence: float = 0.9,
    severity_indicators: list[str] | None = None,
    requires_escalation: bool = False,
    escalation_reason: EscalationReason | None = None,
    pii_types: list[str] | None = None,
) -> SignalClassification:
    return SignalClassification(
        intent="test",
        intent_category=category,
        target_queue=queue,
        confidence=confidence,
        entities=SignalEntities(severity_indicators=severity_indicators or []),
        requires_escalation=requires_escalation,
        escalation_reason=escalation_reason,
        pii_detected=bool(pii_types),
        pii_types=pii_types or [],
    )


# --- Invariant 1: no language-model client in the router ----------------------


def test_router_source_has_no_chat_substring() -> None:
    src = _ROUTER_SRC.read_text(encoding="utf-8")
    assert "chat" not in src.lower(), "RouterExecutor must not reference any chat/LLM client"


def test_router_imports_no_chat_client() -> None:
    # Importing the router must not bind any *ChatClient symbol into its namespace.
    import app.agents.router_agent as router_mod

    leaked = [n for n in dir(router_mod) if "chatclient" in n.lower()]
    assert leaked == [], f"router leaked chat-client symbols: {leaked}"


# --- Invariant 2: deterministic rule-correct routing --------------------------


async def test_public_safety_is_sev1_life_safety() -> None:
    store = MockIncidentStore()
    cls = _classify(
        SignalCategory.PUBLIC_SAFETY,
        queue=Queue.FIELD_OPERATIONS,
        severity_indicators=["fire", "trapped"],
    )
    decision, _ = await _router(store).decide("building on fire people trapped", cls)
    assert decision.severity is Severity.SEV1
    assert decision.sla_minutes == 15
    assert decision.escalate is True
    assert decision.escalation_reason is EscalationReason.LIFE_SAFETY
    assert decision.outcome is RoutingOutcome.OPEN_INCIDENT


async def test_compliance_forces_sev1_statutory() -> None:
    store = MockIncidentStore()
    cls = _classify(
        SignalCategory.COMPLIANCE_REPORT,
        queue=Queue.COMPLIANCE_DESK,
        escalation_reason=EscalationReason.STATUTORY_CLOCK,
        requires_escalation=True,
    )
    decision, _ = await _router(store).decide("recall must be filed in statutory window", cls)
    assert decision.severity is Severity.SEV1
    assert decision.escalation_reason is EscalationReason.STATUTORY_CLOCK


async def test_outage_is_sev2_engineering() -> None:
    store = MockIncidentStore()
    cls = _classify(SignalCategory.INFRASTRUCTURE_OUTAGE, queue=Queue.ENGINEERING)
    decision, _ = await _router(store).decide("neighborhood lost power", cls)
    assert decision.severity is Severity.SEV2
    assert decision.sla_minutes == 60
    assert decision.target_queue is Queue.ENGINEERING
    assert decision.escalate is False


async def test_human_request_escalates_sev3() -> None:
    store = MockIncidentStore()
    cls = _classify(
        SignalCategory.HUMAN_REQUEST,
        queue=Queue.ESCALATIONS,
        requires_escalation=True,
        escalation_reason=EscalationReason.USER_REQUESTED_HUMAN,
    )
    decision, _ = await _router(store).decide("let me speak to a person", cls)
    assert decision.severity is Severity.SEV3
    assert decision.target_queue is Queue.ESCALATIONS
    assert decision.escalation_reason is EscalationReason.USER_REQUESTED_HUMAN


async def test_general_inquiry_is_sev4() -> None:
    store = MockIncidentStore()
    cls = _classify(SignalCategory.GENERAL_INQUIRY, queue=Queue.CUSTOMER_COMMS)
    decision, _ = await _router(store).decide("hi there", cls)
    assert decision.severity is Severity.SEV4


async def test_low_confidence_escalates() -> None:
    store = MockIncidentStore()
    cls = _classify(SignalCategory.CUSTOMER_INQUIRY, queue=Queue.CUSTOMER_COMMS, confidence=0.4)
    decision, _ = await _router(store).decide("uh, something about my account maybe", cls)
    assert decision.escalate is True
    assert decision.escalation_reason is EscalationReason.CONFIDENCE_TOO_LOW


async def test_dedup_attaches_to_similar_open_incident() -> None:
    store = MockIncidentStore()
    text = "downed power line sparking at 5th and Main blocking the sidewalk"
    cls = _classify(SignalCategory.FIELD_HAZARD, queue=Queue.FIELD_OPERATIONS)

    # Seed one open incident with the embedding of the first signal.
    embedding = await mock_embed(text)
    incident_id = await store.next_incident_id()
    await store.create_incident(
        IncidentRecord(
            incident_id=incident_id,
            queue=Queue.FIELD_OPERATIONS,
            severity=Severity.SEV2,
            summary="downed line",
            intent_category=SignalCategory.FIELD_HAZARD,
            sla_minutes=60,
            created_at=datetime.now(timezone.utc),
        ),
        embedding,
    )

    # A near-identical re-report attaches.
    dup, _ = await _router(store).decide(
        "downed power line sparking at 5th and Main blocking the sidewalk now", cls
    )
    assert dup.outcome is RoutingOutcome.ATTACH_TO_INCIDENT
    assert dup.matched_incident_id == incident_id
    assert dup.magnitude == 2

    # An unrelated field hazard opens a new incident.
    fresh, _ = await _router(store).decide(
        "large fallen oak tree blocking the northbound highway ramp", cls
    )
    assert fresh.outcome is RoutingOutcome.OPEN_INCIDENT
