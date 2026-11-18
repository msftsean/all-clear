"""
Pipeline end-to-end verifier (001-maf-rehost, T9). Owned by Barton (Loop Protocol rule 3).

Asserts: text in -> typed PipelineResult out, with SSE lifecycle events published onto
the existing transcript_bus, and that the canonical WorkflowBuilder chain runs.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from app.agents.action_agent import ActionExecutor, ActionToolbox
from app.agents.envelopes import RoutedSignal  # noqa: F401  (import smoke)
from app.agents.pipeline import AllClearPipeline, InboundSignal, build_mock_pipeline
from app.agents.router_agent import RouterExecutor
from app.agents.schemas import (
    ActionStatus,
    PipelineResult,
    Queue,
    RoutingOutcome,
    Severity,
    SignalCategory,
    SignalClassification,
    SignalEntities,
)
from app.core.config import Settings
from app.models.enums import Sentiment
from app.services.mock.embeddings import mock_embed
from app.services.mock.incident_store import MockIncidentStore
from app.services.mock.knowledge_service import MockKnowledgeService
from app.services.transcript_bus import transcript_bus


async def test_process_signal_returns_pipeline_result() -> None:
    pipeline = build_mock_pipeline()
    result = await pipeline.process_signal(
        "There's a downed power line sparking at 5th and Main",
        session_id="s-e2e",
        channel="chat",
    )
    assert isinstance(result, PipelineResult)
    assert result.classification.intent_category is SignalCategory.FIELD_HAZARD
    assert result.routing.outcome is RoutingOutcome.OPEN_INCIDENT
    assert result.routing.severity is Severity.SEV1
    assert result.routing.sla_minutes == 15
    assert result.routing.escalate is True
    assert result.action.status is ActionStatus.ESCALATED
    assert result.action.incident_id is not None
    assert result.processing_ms is not None and result.processing_ms >= 0


async def test_process_signal_publishes_bus_events() -> None:
    pipeline = build_mock_pipeline()
    collected: list[dict] = []

    async with transcript_bus.subscribe() as q:
        result = await pipeline.process_signal(
            "Whole neighborhood lost power about ten minutes ago",
            session_id="s-bus",
            channel="voice",
        )
        # Drain everything published during processing.
        while not q.empty():
            collected.append(q.get_nowait())

    types = [e.get("type") for e in collected]
    assert "signal.classified" in types
    assert "signal.routed" in types
    assert any(t in ("incident.opened", "incident.attached") for t in types)
    assert "pipeline.complete" in types
    assert all(e.get("session_id") == "s-bus" for e in collected)
    assert result.channel == "voice"


async def test_workflow_chain_runs_end_to_end() -> None:
    pipeline = build_mock_pipeline()
    run_result = await pipeline.workflow.run(
        InboundSignal(text="building on fire, people trapped", session_id="wf", channel="chat")
    )
    outputs = run_result.get_outputs()
    actions = [o for o in outputs if getattr(o, "incident_id", None) is not None]
    assert actions, f"workflow produced no IncidentAction output: {outputs!r}"


async def test_dedup_attaches_second_similar_signal() -> None:
    pipeline = build_mock_pipeline()
    text = "downed power line sparking at 5th and Main blocking the sidewalk"
    first = await pipeline.process_signal(text, session_id="s1")
    second = await pipeline.process_signal(text + " right now", session_id="s2")
    assert first.routing.outcome is RoutingOutcome.OPEN_INCIDENT
    assert second.routing.outcome is RoutingOutcome.ATTACH_TO_INCIDENT
    assert second.action.status is ActionStatus.ATTACHED


async def test_sparking_field_hazard_and_duplicate_preserve_sev1_escalation() -> None:
    classification = SignalClassification(
        intent="report_field_hazard",
        intent_category=SignalCategory.FIELD_HAZARD,
        target_queue=Queue.FIELD_OPERATIONS,
        confidence=0.95,
        entities=SignalEntities(
            system="power line",
            severity_indicators=["downed", "sparking"],
        ),
        requires_escalation=False,
        sentiment=Sentiment.URGENT,
    )

    class FixedClassifier:
        async def run(self, _text: str, **_kwargs: object) -> SimpleNamespace:
            return SimpleNamespace(value=classification)

    settings = Settings()
    store = MockIncidentStore()
    pipeline = AllClearPipeline(
        FixedClassifier(),  # type: ignore[arg-type]
        RouterExecutor(mock_embed, store, settings),
        ActionExecutor(
            ActionToolbox(store, MockKnowledgeService(), mock_embed, settings),
            store,
        ),
        store=store,
        bus=None,
    )
    text = "There's a downed power line sparking on Oak Street near the school."
    first = await pipeline.process_signal(text, session_id="electrical-first")
    duplicate = await pipeline.process_signal(text, session_id="electrical-duplicate")

    assert first.routing.outcome is RoutingOutcome.OPEN_INCIDENT
    assert duplicate.routing.outcome is RoutingOutcome.ATTACH_TO_INCIDENT
    assert duplicate.action.incident_id == first.action.incident_id
    assert duplicate.routing.magnitude == 2
    assert duplicate.routing.dedup_similarity == 1.0
    for result in (first, duplicate):
        assert result.routing.severity is Severity.SEV1
        assert result.routing.sla_minutes == 15
        assert result.routing.escalate is True
    record = await store.get_incident(first.action.incident_id)
    assert record is not None
    assert record.severity is Severity.SEV1
    assert record.sla_minutes == 15
    assert record.escalated is True
    assert record.magnitude == 2
    assert store.report_count(record.incident_id) == 1
    assert len(store.audit) == 2


async def test_text_pipeline_redacts_pii_before_return_and_attach_persistence() -> None:
    pipeline = build_mock_pipeline()
    seed = "Downed power line sparking outside Oak substation"
    raw_ssn = "123-45-6789"
    raw_card = "4111 1111 1111 1111"
    pii_signal = f"{seed}. My SSN is {raw_ssn} and card is {raw_card}."

    first = await pipeline.process_signal(pii_signal, session_id="pii-open")
    second = await pipeline.process_signal(pii_signal, session_id="pii-attach")

    assert first.routing.outcome is RoutingOutcome.OPEN_INCIDENT
    assert second.routing.outcome is RoutingOutcome.ATTACH_TO_INCIDENT
    assert second.classification.pii_detected is True
    assert "[REDACTED]" in second.signal_text
    assert raw_ssn not in second.signal_text
    assert raw_card not in second.signal_text
    assert "4111111111111111" not in second.signal_text.replace(" ", "")

    store = pipeline.store
    assert store is not None
    incident_id = second.routing.matched_incident_id
    assert incident_id is not None
    reports = store._reports[incident_id]
    assert reports
    assert all(raw_ssn not in report for report in reports)
    assert all(raw_card not in report for report in reports)
    assert all("4111111111111111" not in report.replace(" ", "") for report in reports)
    assert any("[REDACTED]" in report for report in reports)
    assert store.audit[-1].actor == "ActionAgent.attach_report"


async def test_concurrent_duplicate_routes_commit_before_slow_knowledge_search(
    capsys: pytest.CaptureFixture[str],
) -> None:
    classification = SignalClassification(
        intent="report_field_hazard",
        intent_category=SignalCategory.FIELD_HAZARD,
        target_queue=Queue.FIELD_OPERATIONS,
        confidence=0.95,
        entities=SignalEntities(),
    )

    class FixedClassifier:
        async def run(self, _text: str, **_kwargs: object) -> SimpleNamespace:
            return SimpleNamespace(value=classification)

    class SlowKnowledgeService(MockKnowledgeService):
        def __init__(self) -> None:
            super().__init__()
            self.search_started = asyncio.Event()
            self.finish_search = asyncio.Event()

        async def search(self, query: str, department: str | None = None, limit: int = 3):
            self.search_started.set()
            await self.finish_search.wait()
            return []

    async def real_vector_provider(_text: str) -> list[float]:
        return [0.125, -0.5, 0.75, 0.25]

    settings = Settings()
    store = MockIncidentStore()
    knowledge = SlowKnowledgeService()
    action = ActionExecutor(
        ActionToolbox(store, knowledge, real_vector_provider, settings),
        store,
    )
    pipeline = AllClearPipeline(
        FixedClassifier(),  # type: ignore[arg-type]
        RouterExecutor(real_vector_provider, store, settings),
        action,
        store=store,
        bus=None,
    )

    first_task = asyncio.create_task(
        pipeline.process_signal("Flooding near the station on Wilson Boulevard", channel="report")
    )
    await asyncio.wait_for(knowledge.search_started.wait(), timeout=2)
    second_task = asyncio.create_task(
        pipeline.process_signal(
            "Water is covering the sidewalk on Wilson Boulevard", channel="report"
        )
    )
    second_result = None
    try:
        second_result = await asyncio.wait_for(second_task, timeout=1)
    except TimeoutError:
        pass
    finally:
        knowledge.finish_search.set()

    first_result = await first_task
    assert second_result is not None, "A slow open-path knowledge search held the dedup lock"
    assert first_result.routing.outcome is RoutingOutcome.OPEN_INCIDENT
    assert second_result.routing.outcome is RoutingOutcome.ATTACH_TO_INCIDENT
    assert second_result.action.incident_id == first_result.action.incident_id
    assert first_result.action.sitrep is not None
    assert store.report_count(first_result.action.incident_id) == 1
    record = await store.get_incident(first_result.action.incident_id)
    assert record is not None and record.magnitude == 2
    assert len(store.audit) == 2
    output = capsys.readouterr().out
    assert output.count("surge_pipeline_phases") == 2
    assert "best_similarity=1.0000" in output
    assert "incident_id=" in output
    assert "Flooding near the station on Wilson Boulevard" not in output
    assert "Water is covering the sidewalk on Wilson Boulevard" not in output


async def test_embedding_runs_outside_atomic_dedup_window() -> None:
    classification = SignalClassification(
        intent="report_field_hazard",
        intent_category=SignalCategory.FIELD_HAZARD,
        target_queue=Queue.FIELD_OPERATIONS,
        confidence=0.95,
        entities=SignalEntities(),
    )

    class FixedClassifier:
        async def run(self, _text: str, **_kwargs: object) -> SimpleNamespace:
            return SimpleNamespace(value=classification)

    first_embedding_started = asyncio.Event()
    release_first_embedding = asyncio.Event()

    async def delayed_embedding(text: str) -> list[float]:
        if text.startswith("first:"):
            first_embedding_started.set()
            await release_first_embedding.wait()
        return [0.125, -0.5, 0.75, 0.25]

    settings = Settings()
    store = MockIncidentStore()
    knowledge = MockKnowledgeService()
    action = ActionExecutor(
        ActionToolbox(store, knowledge, delayed_embedding, settings),
        store,
    )
    pipeline = AllClearPipeline(
        FixedClassifier(),  # type: ignore[arg-type]
        RouterExecutor(delayed_embedding, store, settings),
        action,
        store=store,
        bus=None,
    )

    first_task = asyncio.create_task(
        pipeline.process_signal("first: flooding near Wilson Boulevard", channel="report")
    )
    await asyncio.wait_for(first_embedding_started.wait(), timeout=2)
    second_result = await asyncio.wait_for(
        pipeline.process_signal("second: water covering Wilson Boulevard", channel="report"),
        timeout=1,
    )
    release_first_embedding.set()
    first_result = await first_task

    assert second_result.routing.outcome is RoutingOutcome.OPEN_INCIDENT
    assert first_result.routing.outcome is RoutingOutcome.ATTACH_TO_INCIDENT
    assert first_result.action.incident_id == second_result.action.incident_id
    assert store.report_count(second_result.action.incident_id) == 1
    record = await store.get_incident(second_result.action.incident_id)
    assert record is not None and record.magnitude == 2
    assert len(store.audit) == 2
