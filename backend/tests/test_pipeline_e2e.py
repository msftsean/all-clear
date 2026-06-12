"""
Pipeline end-to-end verifier (001-maf-rehost, T9). Owned by Barton (Loop Protocol rule 3).

Asserts: text in -> typed PipelineResult out, with SSE lifecycle events published onto
the existing transcript_bus, and that the canonical WorkflowBuilder chain runs.
"""

from __future__ import annotations

import pytest

from app.agents.envelopes import RoutedSignal  # noqa: F401  (import smoke)
from app.agents.pipeline import AllClearPipeline, InboundSignal, build_mock_pipeline
from app.agents.schemas import (
    ActionStatus,
    PipelineResult,
    RoutingOutcome,
    SignalCategory,
)
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
    assert result.action.status is ActionStatus.OPENED
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
