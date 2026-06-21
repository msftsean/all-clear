"""Wave 1 verifier additions for spec 019 (tests/checkpoints only)."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.agents.pipeline import build_mock_pipeline
from app.agents.schemas import ActionStatus, RoutingOutcome

_REPO_ROOT = Path(__file__).resolve().parents[2]
_README = _REPO_ROOT / "README.md"
_DOC_RESPONSIBLE_AI = _REPO_ROOT / "docs" / "responsible-ai.md"
_DOC_LAB_TO_PROD = _REPO_ROOT / "docs" / "lab-to-production.md"
_FRONTEND_SRC = _REPO_ROOT / "frontend" / "src"


async def test_spec4a_soc_sentinel_pack_dedup_attaches_duplicate_signal() -> None:
    pipeline = build_mock_pipeline()
    base = (
        "soc sentinel alert storm service down outage in city data center "
        "impacting dispatch dashboard"
    )
    first = await pipeline.process_signal(base, session_id="spec4a-1", channel="report")
    second = await pipeline.process_signal(
        f"{base} duplicate telemetry confirms same outage",
        session_id="spec4a-2",
        channel="chat",
    )

    assert first.routing.outcome is RoutingOutcome.OPEN_INCIDENT
    assert second.routing.outcome is RoutingOutcome.ATTACH_TO_INCIDENT
    assert second.action.status is ActionStatus.ATTACHED
    assert second.routing.matched_incident_id == first.action.incident_id


async def test_spec4b_city_ops_311_911_pack_dedup_attaches_duplicate_signal() -> None:
    pipeline = build_mock_pipeline()
    base = (
        "311 911 call surge downed power line sparking on harford road "
        "blocking intersection"
    )
    first = await pipeline.process_signal(base, session_id="spec4b-1", channel="phone")
    second = await pipeline.process_signal(
        "311 911 call surge downed power line sparking on harford road "
        "blocking crosswalk",
        session_id="spec4b-2",
        channel="phone",
    )

    assert first.routing.outcome is RoutingOutcome.OPEN_INCIDENT
    assert second.routing.outcome is RoutingOutcome.ATTACH_TO_INCIDENT
    assert second.action.status is ActionStatus.ATTACHED
    assert second.routing.matched_incident_id == first.action.incident_id


async def test_spec4c_water_utility_pack_dedup_attaches_duplicate_signal() -> None:
    pipeline = build_mock_pipeline()
    base = (
        "water utility leak surge water main break flooding pine avenue "
        "neighborhood street submerged"
    )
    first = await pipeline.process_signal(base, session_id="spec4c-1", channel="report")
    second = await pipeline.process_signal(
        f"{base} duplicate resident confirms flooding reached driveway",
        session_id="spec4c-2",
        channel="chat",
    )

    assert first.routing.outcome is RoutingOutcome.OPEN_INCIDENT
    assert second.routing.outcome is RoutingOutcome.ATTACH_TO_INCIDENT
    assert second.action.status is ActionStatus.ATTACHED
    assert second.routing.matched_incident_id == first.action.incident_id


async def test_spec4d_traffic_transport_pack_dedup_attaches_duplicate_signal() -> None:
    pipeline = build_mock_pipeline()
    base = (
        "traffic operations road blocked by crash debris at i95 interchange "
        "multi lane closure"
    )
    first = await pipeline.process_signal(base, session_id="spec4d-1", channel="phone")
    second = await pipeline.process_signal(
        f"{base} duplicate report confirms closure still active",
        session_id="spec4d-2",
        channel="report",
    )

    assert first.routing.outcome is RoutingOutcome.OPEN_INCIDENT
    assert second.routing.outcome is RoutingOutcome.ATTACH_TO_INCIDENT
    assert second.action.status is ActionStatus.ATTACHED
    assert second.routing.matched_incident_id == first.action.incident_id


def test_spec3_todo_readme_links_responsible_ai_map() -> None:
    readme = _README.read_text(encoding="utf-8")
    link = "./docs/responsible-ai.md"

    if link not in readme or not _DOC_RESPONSIBLE_AI.exists():
        pytest.xfail(
            "TODO(SPEC-3): add docs/responsible-ai.md and README link before enabling strict link gate."
        )

    assert link in readme
    assert _DOC_RESPONSIBLE_AI.exists()


def test_spec6_todo_readme_links_lab_to_production_doc() -> None:
    readme = _README.read_text(encoding="utf-8")
    link = "./docs/lab-to-production.md"

    if link not in readme or not _DOC_LAB_TO_PROD.exists():
        pytest.xfail(
            "TODO(SPEC-6): add docs/lab-to-production.md and README link before enabling strict link gate."
        )

    assert link in readme
    assert _DOC_LAB_TO_PROD.exists()


def test_spec3_todo_frontend_trust_view_links_responsible_ai_map() -> None:
    front_files = list(_FRONTEND_SRC.rglob("*.tsx"))
    linked_files = [
        path
        for path in front_files
        if "responsible-ai.md" in path.read_text(encoding="utf-8")
    ]
    if not linked_files:
        pytest.xfail(
            "TODO(SPEC-3): Trust view link to docs/responsible-ai.md not implemented yet."
        )

    assert linked_files


def test_spec6_todo_frontend_links_lab_to_production_doc() -> None:
    front_files = list(_FRONTEND_SRC.rglob("*.tsx"))
    linked_files = [
        path
        for path in front_files
        if "lab-to-production.md" in path.read_text(encoding="utf-8")
    ]
    if not linked_files:
        pytest.xfail(
            "TODO(SPEC-6): capstone UI link to docs/lab-to-production.md not implemented yet."
        )

    assert linked_files
