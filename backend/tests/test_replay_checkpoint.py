"""
Surge replay checkpoint (001-maf-rehost, T4 verifier for T7/T9).

Streams mock_data/surge_replay_25.json through the AllClearPipeline in mock mode and
asserts the dedup outcome: <=6 open incidents and >=19 attachments (Exercise 5).
Owned by Barton (Loop Protocol rule 3): builders may not edit this test or fixture.

Until the RouterExecutor (T7) and AllClearPipeline (T9) exist, the import below fails
and this test errors out -- the intended "fails on stub" state.
"""

import json
from collections import Counter
from pathlib import Path

import pytest

from app.agents.schemas import RoutingOutcome

_FIXTURE = Path(__file__).parent.parent / "mock_data" / "surge_replay_25.json"


@pytest.fixture
def replay_signals() -> list[dict[str, str]]:
    data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    return data["signals"]


async def test_surge_replay_dedup_checkpoint(replay_signals: list[dict[str, str]]) -> None:
    # Imported lazily so collection still happens before T9 exists; the import
    # error here is the intended fail-on-stub signal.
    from app.agents.pipeline import build_mock_pipeline

    pipeline = build_mock_pipeline()
    outcomes: Counter[str] = Counter()
    for sig in replay_signals:
        result = await pipeline.process_signal(
            text=sig["text"], session_id=sig["id"], channel=sig["channel"]
        )
        outcomes[result.routing.outcome.value] += 1

    opened = outcomes[RoutingOutcome.OPEN_INCIDENT.value]
    attached = outcomes[RoutingOutcome.ATTACH_TO_INCIDENT.value]
    assert opened + attached == 25
    assert opened <= 6, f"expected <=6 open incidents, got {opened}"
    assert attached >= 19, f"expected >=19 attachments, got {attached}"
