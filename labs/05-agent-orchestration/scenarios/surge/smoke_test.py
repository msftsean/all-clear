r"""
All Clear surge dedup smoke test (Lab 05, Step 7 / Exercise 5).

Streams the 25-signal surge replay fixture (backend/mock_data/surge_replay_25.json)
through the real AllClearPipeline in mock mode and asserts the dedup checkpoint:
the storm of near-duplicate reports must collapse to <= 6 open incidents and
>= 19 attachments. This is the same contract the owned verifier
(backend/tests/test_replay_checkpoint.py) enforces -- run it here to see the
per-signal routing decisions while you build.

Run from the backend dir so `app` is importable:

    cd backend
    PYTHONPATH=. ENVIRONMENT=test MOCK_MODE=true \
        python ../labs/05-agent-orchestration/scenarios/surge/smoke_test.py

PowerShell:

    cd backend
    $env:ENVIRONMENT="test"; $env:MOCK_MODE="true"; $env:PYTHONPATH="."
    .\.venv\Scripts\python.exe ..\labs\05-agent-orchestration\scenarios\surge\smoke_test.py
"""

from __future__ import annotations

import asyncio
import json
import sys
from collections import Counter
from pathlib import Path

from app.agents.pipeline import build_mock_pipeline
from app.agents.schemas import RoutingOutcome

_FIXTURE = (
    Path(__file__).resolve().parents[4]
    / "backend"
    / "mock_data"
    / "surge_replay_25.json"
)


async def run() -> int:
    signals = json.loads(_FIXTURE.read_text(encoding="utf-8"))["signals"]
    pipeline = build_mock_pipeline()

    outcomes: Counter[str] = Counter()
    incidents: dict[str, int] = {}

    print("=" * 78)
    print("ALL CLEAR SURGE SMOKE TEST — 25-signal replay (dedup checkpoint)")
    print("=" * 78)

    for sig in signals:
        result = await pipeline.process_signal(
            text=sig["text"], session_id=sig["id"], channel=sig["channel"]
        )
        routing = result.routing
        outcomes[routing.outcome.value] += 1
        if routing.outcome is RoutingOutcome.OPEN_INCIDENT:
            inc_id = result.action.incident_id or "(new)"
        else:
            inc_id = routing.matched_incident_id or "(attach)"
        incidents[inc_id] = incidents.get(inc_id, 0) + 1
        print(
            f"  {sig['id']:<10} {routing.outcome.value:<20} "
            f"sev={routing.severity.value:<5} queue={routing.target_queue.value:<16} "
            f"-> {inc_id}"
        )

    opened = outcomes[RoutingOutcome.OPEN_INCIDENT.value]
    attached = outcomes[RoutingOutcome.ATTACH_TO_INCIDENT.value]

    print("\n" + "-" * 78)
    print(f"  open incidents:   {opened}")
    print(f"  attached reports: {attached}")
    print(f"  total signals:    {opened + attached}")
    print("-" * 78)

    ok = opened + attached == 25 and opened <= 6 and attached >= 19
    status = "PASS" if ok else "FAIL"
    print(f"\nRESULT: {status} — expected <=6 open and >=19 attached out of 25")
    print("=" * 78)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(run()))
