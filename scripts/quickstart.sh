#!/usr/bin/env bash
# All Clear mock-mode quickstart: validates the incident pipeline without Azure.

set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root/backend"

MOCK_MODE=true PYTHONPATH=. python - <<'PY'
import asyncio

from app.agents.pipeline import build_mock_pipeline


async def main() -> None:
    result = await build_mock_pipeline().process_signal(
        "A downed power line is sparking at 5th and Main.",
        session_id="quickstart",
    )
    assert result.action.incident_id.startswith("AC-")
    print(f"All Clear ready: {result.action.incident_id} ({result.action.severity.value})")


asyncio.run(main())
PY
