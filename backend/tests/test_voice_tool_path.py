"""
Voice tool path verifier (001-maf-rehost, T10). Owned by Barton (Loop Protocol rule 3).

Asserts the realtime voice tool ``analyze_and_route_query`` is repointed at the All Clear
pipeline adapter: it returns incident-domain fields (intent_category, queue, severity,
outcome, incident_id) rather than the retired FERPA ticket/department stub.
"""

from __future__ import annotations

import json

import pytest

from app.services.mock.realtime import MockRealtimeService


async def test_voice_analyze_routes_through_pipeline() -> None:
    service = MockRealtimeService()
    resp = await service.execute_tool(
        call_id="c1",
        tool_name="analyze_and_route_query",
        arguments={"query": "There's a downed power line sparking at 5th and Main"},
        session_id="voice-1",
    )
    assert resp.error is None
    payload = json.loads(resp.result)
    # Incident-domain contract, not the retired ticket/department stub.
    assert payload["intent_category"] == "FIELD_HAZARD"
    assert payload["queue"] == "field-operations"
    assert payload["severity"] == "SEV2"
    assert payload["outcome"] == "OPEN_INCIDENT"
    assert payload["incident_id"].startswith("AC-")
    assert "ticket_id" not in payload


async def test_voice_public_safety_escalates() -> None:
    service = MockRealtimeService()
    resp = await service.execute_tool(
        call_id="c2",
        tool_name="analyze_and_route_query",
        arguments={"query": "Building on fire, people trapped inside"},
        session_id="voice-2",
    )
    payload = json.loads(resp.result)
    assert payload["severity"] == "SEV1"
    assert payload["escalated"] is True


async def test_voice_dedup_attaches_within_session() -> None:
    service = MockRealtimeService()
    text = "downed power line sparking at 5th and Main blocking the sidewalk"
    first = json.loads(
        (await service.execute_tool("c3", "analyze_and_route_query", {"query": text}, "voice-3")).result
    )
    second = json.loads(
        (
            await service.execute_tool(
                "c4", "analyze_and_route_query", {"query": text + " now"}, "voice-3"
            )
        ).result
    )
    assert first["outcome"] == "OPEN_INCIDENT"
    assert second["outcome"] == "ATTACH_TO_INCIDENT"
