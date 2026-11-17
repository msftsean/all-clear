"""Offline regressions for the Lab 07 boundary and real Lab 05 routing."""

import importlib.util
import json
import logging
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

LABS = Path(__file__).resolve().parents[1]


def load_module(name, path, monkeypatch):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, module)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(params=["start", "solution"])
def server(request, monkeypatch):
    monkeypatch.syspath_prepend(str(LABS.parent / "backend"))
    # Lab 05 tests also import these names from start; isolate the MCP contract.
    for name in ("query_agent", "router_agent", "action_agent", "pipeline"):
        load_module(
            name, LABS / "05-agent-orchestration" / "solution" / f"{name}.py",
            monkeypatch,
        )
    return load_module(
        f"lab07_{request.param}",
        LABS / "07-mcp-server" / request.param / "mcp_server.py",
        monkeypatch,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "detail,private_value,model_pii",
    [
        ("email student@example.edu", "student@example.edu", False),
        ("SSN 123-45-6789", "123-45-6789", False),
        ("student id is 12345678", "12345678", False),
        ("DOB: 01/02/2000", "01/02/2000", False),
        ("reference [REDACTED]", None, False),
        ("reference 42", None, True),
    ],
)
async def test_trusted_pii_survives_model_classification(
    server, monkeypatch, caplog, detail, private_value, model_pii,
):
    from pipeline import AgentPipeline
    from query_agent import QueryAgent
    from router_agent import RouterExecutor

    model_requests = []
    decisions = []

    def complete(**kwargs):
        model_requests.append(kwargs)
        return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(
            content=json.dumps({
                "category": "SERVICE_REQUEST", "confidence": 0.95,
                "pii_detected": model_pii,
            }),
        ))])

    client = SimpleNamespace(chat=SimpleNamespace(
        completions=SimpleNamespace(create=complete),
    ))
    router = RouterExecutor()
    route = router.route

    async def record_route(classification, signal_text):
        decision = await route(classification, signal_text)
        decisions.append(decision)
        return decision

    monkeypatch.setattr(router, "route", record_route)
    pipeline = AgentPipeline(
        query_agent=QueryAgent(client=client), router_executor=router,
    )
    monkeypatch.setattr(server, "get_agent_pipeline", lambda: pipeline)
    caplog.set_level(logging.INFO)

    signal = f"Schedule a routine inspection; {detail}"
    response = json.loads(await server.classify_signal(
        signal, session_id="untrusted-session",
    ))

    assert "error" not in response, response.get("error")
    assert response["session_id"] != "untrusted-session"
    session = pipeline.session_manager.get(response["session_id"])
    incident = pipeline.action_agent.incidents[response["incident_id"]]
    decision = decisions[0]
    assert decision.classification.confidence == 0.95
    assert decision.severity.value == "SEV4"
    assert decision.sla_minutes == 1440
    expected_escalation = private_value is not None or model_pii
    assert decision.classification.pii_detected is expected_escalation
    assert decision.escalate is expected_escalation
    assert decision.escalation_reason == (
        "pii_exposure" if expected_escalation else None
    )
    assert incident["escalated"] is expected_escalation
    if private_value:
        assert "[REDACTED]" in incident["summary"]
        for surface in (
            json.dumps(model_requests), caplog.text, repr(session),
            repr(incident), repr(decision), json.dumps(response),
        ):
            assert private_value not in surface


@pytest.mark.asyncio
async def test_fallback_preserves_pii_escalation(server, monkeypatch):
    monkeypatch.setattr(server, "get_agent_pipeline", lambda: None)
    response = json.loads(await server.classify_signal(
        "Schedule a routine inspection; email student@example.edu",
    ))
    assert response["pii_detected"] is True
    assert response["requires_escalation"] is True
    assert "student@example.edu" not in json.dumps(response)
