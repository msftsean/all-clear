"""
ActionAgent verifier (001-maf-rehost, T8). Owned by Barton (Loop Protocol rule 3).

Asserts: on the OPEN path the ActionExecutor opens an incident in the store with an
audit entry, runs a knowledge search, and drafts a cited sitrep; on the ATTACH path it
attaches a report (magnitude increments, audit entry) and runs NO knowledge search.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from app.agents.action_agent import ActionExecutor, ActionToolbox, build_action_agent
from app.agents.envelopes import RoutedSignal
from app.agents.schemas import (
    ActionStatus,
    EscalationReason,
    IncidentRecord,
    Queue,
    RoutingDecision,
    RoutingOutcome,
    Severity,
    SignalCategory,
    SignalClassification,
    SignalEntities,
)
from app.core.config import Settings
from app.services.mock.embeddings import mock_embed
from app.services.mock.incident_store import MockIncidentStore
from app.services.mock.knowledge_service import MockKnowledgeService
from app.services.mock.maf_chat_client import MockChatClient


def _toolbox(store: MockIncidentStore) -> ActionToolbox:
    return ActionToolbox(store, MockKnowledgeService(), mock_embed, Settings())


def _classification(category: SignalCategory, *, location: str | None = None) -> SignalClassification:
    return SignalClassification(
        intent="report_field_hazard",
        intent_category=category,
        target_queue=Queue.FIELD_OPERATIONS,
        confidence=0.92,
        entities=SignalEntities(location=location),
    )


def _open_decision() -> RoutingDecision:
    return RoutingDecision(
        outcome=RoutingOutcome.OPEN_INCIDENT,
        target_queue=Queue.FIELD_OPERATIONS,
        severity=Severity.SEV2,
        sla_minutes=60,
        magnitude=1,
    )


def test_build_action_agent_constructs() -> None:
    store = MockIncidentStore()
    agent = build_action_agent(MockChatClient(), _toolbox(store))
    assert agent.name == "ActionAgent"


async def test_open_path_creates_incident_with_audit_and_sitrep() -> None:
    store = MockIncidentStore()
    executor = ActionExecutor(_toolbox(store), store)
    text = "downed power line sparking at 5th and Main"
    routed = RoutedSignal(
        signal_text=text,
        classification=_classification(SignalCategory.FIELD_HAZARD, location="5th and Main"),
        routing=_open_decision(),
        embedding=await mock_embed(text),
        session_id="s1",
        channel="chat",
    )
    action = await executor.run_action(routed)

    assert action.status is ActionStatus.OPENED
    assert action.incident_id is not None
    # Incident landed in the store with an audit entry.
    stored = await store.get_incident(action.incident_id)
    assert stored is not None
    assert any(a.action == "create" and a.target == action.incident_id for a in store.audit)
    # Sitrep is grounded: it has at least the incident citation.
    assert action.sitrep is not None
    assert any(c.source_type == "incident" for c in action.sitrep.citations)


async def test_attach_path_increments_magnitude_no_knowledge_search() -> None:
    store = MockIncidentStore()
    executor = ActionExecutor(_toolbox(store), store)

    # Seed an existing open incident.
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
        await mock_embed("downed power line at 5th and Main"),
    )

    routed = RoutedSignal(
        signal_text="another caller about the downed line at 5th and Main",
        classification=_classification(SignalCategory.FIELD_HAZARD),
        routing=RoutingDecision(
            outcome=RoutingOutcome.ATTACH_TO_INCIDENT,
            target_queue=Queue.FIELD_OPERATIONS,
            severity=Severity.SEV2,
            sla_minutes=60,
            matched_incident_id=incident_id,
            dedup_similarity=0.97,
            magnitude=2,
        ),
        embedding=[],
    )
    action = await executor.run_action(routed)

    assert action.status is ActionStatus.ATTACHED
    assert action.incident_id == incident_id
    assert action.knowledge_articles == []  # no knowledge search on attach path
    assert store.report_count(incident_id) == 1
    updated = await store.get_incident(incident_id)
    assert updated is not None and updated.magnitude == 2
    assert any(a.action == "attach" and a.target == incident_id for a in store.audit)


async def test_escalated_open_incident_stays_open_for_dedup() -> None:
    store = MockIncidentStore()
    executor = ActionExecutor(_toolbox(store), store)
    decision = RoutingDecision(
        outcome=RoutingOutcome.OPEN_INCIDENT,
        target_queue=Queue.FIELD_OPERATIONS,
        severity=Severity.SEV1,
        sla_minutes=15,
        escalate=True,
        escalation_reason=EscalationReason.LIFE_SAFETY,
        magnitude=1,
    )
    text = "building on fire people trapped"
    routed = RoutedSignal(
        signal_text=text,
        classification=_classification(SignalCategory.PUBLIC_SAFETY),
        routing=decision,
        embedding=await mock_embed(text),
    )
    action = await executor.run_action(routed)
    assert action.status is ActionStatus.ESCALATED
    # Even escalated incidents remain dedup-visible (same category).
    open_ids = await store.get_open_incident_vectors(SignalCategory.PUBLIC_SAFETY)
    assert len(open_ids) == 1
