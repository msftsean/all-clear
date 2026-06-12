"""
Lab 05 - Agent Orchestration Test Script.
Tests the All Clear pipeline: QueryAgent -> RouterExecutor -> ActionAgent.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
from pathlib import Path

import pytest

LAB_DIR = Path(__file__).parent
START_DIR = LAB_DIR / "start"
if str(START_DIR) not in sys.path:
    sys.path.insert(0, str(START_DIR))

OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
OPENAI_KEY = os.environ.get("AZURE_OPENAI_API_KEY") or os.environ.get("AZURE_OPENAI_KEY")
SEARCH_ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.environ.get("AZURE_SEARCH_KEY")
INDEX_NAME = os.environ.get("AZURE_SEARCH_INDEX_NAME", "all-clear-kb")

requires_azure = pytest.mark.skipif(
    not OPENAI_ENDPOINT or not OPENAI_KEY,
    reason="Azure OpenAI credentials not configured",
)


@pytest.mark.asyncio
async def test_query_agent_offline_classification():
    """QueryAgent classifies incident-triage signals without routing."""
    from query_agent import QueryAgent, SignalCategory

    agent = QueryAgent(model="gpt-5.1")
    cases = [
        ("Power line down across Main St, sparking on the road", SignalCategory.PUBLIC_SAFETY),
        ("Smell of gas near the community center", SignalCategory.PUBLIC_SAFETY),
        ("Need to file the NFIRS report for last night's fire", SignalCategory.COMPLIANCE_REPORT),
        ("I want to speak to a human", SignalCategory.HUMAN_REQUEST),
    ]

    for signal, expected in cases:
        result = await agent.classify(signal)
        assert result.category == expected
        assert result.confidence >= 0.5


@pytest.mark.asyncio
async def test_router_executor_sev1_open_incident():
    """RouterExecutor maps life-safety/field hazard signals to SEV1 and escalation."""
    from query_agent import QueryAgent
    from router_agent import RouterExecutor, RoutingOutcome, Severity

    classification = await QueryAgent().classify("Power line down across Main St, sparking near a school")
    decision = await RouterExecutor().route(classification)

    assert decision.outcome == RoutingOutcome.OPEN_INCIDENT
    assert decision.severity == Severity.SEV1
    assert decision.sla_minutes == 15
    assert decision.target_queue == "field-operations"
    assert decision.escalate


@pytest.mark.asyncio
async def test_router_executor_dedup_attach_report():
    """A duplicate signal attaches as a report and increments magnitude."""
    from query_agent import QueryAgent, SignalCategory
    from router_agent import OpenIncident, RouterExecutor, RoutingOutcome

    open_incident = OpenIncident(
        incident_id="AC-0042",
        category=SignalCategory.PUBLIC_SAFETY,
        summary="Power line down across Main St sparking on road",
        magnitude=37,
    )
    classification = await QueryAgent().classify("Power line down across Main St sparking on road")
    decision = await RouterExecutor(open_incidents=[open_incident]).route(classification)

    assert decision.outcome == RoutingOutcome.ATTACH_TO_INCIDENT
    assert decision.matched_incident_id == "AC-0042"
    assert decision.magnitude == 38


@pytest.mark.asyncio
async def test_action_agent_opens_ac_incident_with_citations():
    """ActionAgent opens AC-#### incidents and returns citation-grounded sitrep data."""
    from action_agent import ActionAgent
    from query_agent import QueryAgent
    from router_agent import RouterExecutor

    classification = await QueryAgent().classify("Smell of gas near the community center")
    decision = await RouterExecutor().route(classification)
    action = await ActionAgent().execute(decision)

    assert action.status == "opened"
    assert action.incident_id is not None and re.match(r"^AC-\d{4,}$", action.incident_id)
    assert action.escalated
    assert action.sitrep is not None
    assert action.citations, "No citation, no claim"


@pytest.mark.asyncio
async def test_full_pipeline_multi_turn_session():
    """Pipeline preserves session state across multiple signals."""
    from pipeline import AgentPipeline

    pipeline = AgentPipeline(model_deployment="gpt-5.1")
    first, session_id = await pipeline.process("Water main break flooding the 200 block")
    second, same_session = await pipeline.process("Any update on the Elm Street outage?", session_id)

    assert first.incident_id and first.incident_id.startswith("AC-")
    assert same_session == session_id
    session = pipeline.session_manager.get(session_id)
    assert session is not None
    assert len(session.turns) == 2
    assert second.content


@requires_azure
@pytest.mark.asyncio
async def test_query_agent_live_azure_shape():
    """Optional live-Azure smoke test for QueryAgent structured output."""
    from openai import AzureOpenAI
    from query_agent import QueryAgent, SignalCategory

    client = AzureOpenAI(
        azure_endpoint=OPENAI_ENDPOINT,
        api_key=OPENAI_KEY,
        api_version="2025-01-01-preview",
    )
    result = await QueryAgent(client=client, model="gpt-5.1").classify(
        "Power line down across Main St, sparking on the road"
    )
    assert result.category in set(SignalCategory)


async def main() -> int:
    """Run a readable teaching smoke test without requiring Azure credentials."""
    from pipeline import AgentPipeline

    print("=" * 60)
    print("Lab 05 - All Clear Agent Orchestration Smoke Test")
    print("=" * 60)

    pipeline = AgentPipeline(model_deployment="gpt-5.1")
    signals = [
        "Power line down across Main St, sparking on the road",
        "Any update on the Elm Street outage?",
        "I want to speak to a human",
    ]
    session_id = None
    for signal in signals:
        action, session_id = await pipeline.process(signal, session_id)
        print(f"Signal: {signal}")
        print(f"Action: {action.status} {action.incident_id} {action.severity.value} {action.queue}")
        print(f"Response: {action.user_message}")
        print("-" * 60)

    print(f"Session maintained: {session_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))



