"""Tests for the coach load-test coordinator (single-flight + idempotent).

Verifies the concurrency guard that prevents a second click — or another coach —
from starting a duplicate load run, against both the in-memory (mock-mode) and
Cosmos (etag CAS) lock backends.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from app.services.demo_loadtest import LoadTestCoordinator, clamp_count
from tests.test_azure_incident_store import FakeCosmosContainer


class _GatedPipeline:
    """Fake pipeline whose process_signal blocks until released, so a run stays
    'running' deterministically while the test asserts the concurrency guard."""

    def __init__(self) -> None:
        self.gate = asyncio.Event()
        self.calls = 0

    async def process_signal(self, *, text: str, session_id: str, channel: str):
        self.calls += 1
        await self.gate.wait()
        return SimpleNamespace(
            action=SimpleNamespace(incident_id="AC-0001"),
            routing=SimpleNamespace(magnitude=self.calls),
        )


@pytest.fixture
def gated_pipeline(monkeypatch) -> _GatedPipeline:
    pipe = _GatedPipeline()
    monkeypatch.setattr("app.core.dependencies.get_pipeline", lambda: pipe)
    return pipe


def test_clamp_count_bounds() -> None:
    assert clamp_count(0) == 1
    assert clamp_count(9999) == 150
    assert clamp_count(40) == 40


@pytest.mark.asyncio
async def test_starts_idle_then_reports_running(gated_pipeline) -> None:
    coord = LoadTestCoordinator(container=None)
    assert (await coord.status())["running"] is False

    started = await coord.start(count=3, mode="same", started_by="sean")
    assert started["running"] is True
    assert started["total"] == 3
    assert started["started_by"] == "sean"
    run_id = started["run_id"]

    # Second start while running must NOT launch a new run (idempotent guard).
    again = await coord.start(count=99, mode="varied", started_by="another-coach")
    assert again["running"] is True
    assert again["run_id"] == run_id
    assert again["total"] == 3  # unchanged — the in-flight job wins

    gated_pipeline.gate.set()
    await coord._task  # let the background run finish

    done = await coord.status()
    assert done["running"] is False
    assert done["status"] == "idle"
    assert done["sent"] == 3
    assert done["ok"] == 3
    assert done["failed"] == 0
    assert done["incidents"] == 1
    assert done["max_magnitude"] == 3
    # process_signal was called exactly 3 times — the duplicate start added none.
    assert gated_pipeline.calls == 3


@pytest.mark.asyncio
async def test_can_run_again_after_completion(gated_pipeline) -> None:
    coord = LoadTestCoordinator(container=None)
    gated_pipeline.gate.set()  # don't block; runs complete immediately

    first = await coord.start(count=2, mode="same")
    await coord._task
    assert (await coord.status())["running"] is False

    second = await coord.start(count=2, mode="same")
    assert second["running"] is True
    assert second["run_id"] != first["run_id"]
    await coord._task


@pytest.mark.asyncio
async def test_cosmos_lock_backend_is_single_flight(gated_pipeline) -> None:
    container = FakeCosmosContainer()
    coord = LoadTestCoordinator(container=container)

    started = await coord.start(count=2, mode="same")
    assert started["running"] is True

    blocked = await coord.start(count=2, mode="same")
    assert blocked["running"] is True
    assert blocked["run_id"] == started["run_id"]

    gated_pipeline.gate.set()
    await coord._task

    final = await coord.status()
    assert final["running"] is False
    assert final["sent"] == 2
