#!/usr/bin/env python
"""
Classification eval checkpoint for QueryAgent (001-maf-rehost, T4d / verifier for T5).

Runs the mock-mode QueryAgent over mock_data/eval_signals_60.jsonl and reports
intent_category accuracy. Owned by Barton (Loop Protocol rule 3): builders may not
edit this script, the eval set, or the threshold to make a task pass.

Usage:
    python scripts/check_eval.py --min-accuracy 0.90     # T5: exit 0 iff acc >= min
    python scripts/check_eval.py --expect-fail-on-stub   # T4: exit 0 iff acc <  0.90
                                                          #     (proves the verifier
                                                          #      correctly fails on a
                                                          #      stub/absent QueryAgent)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

_BACKEND = Path(__file__).resolve().parent.parent
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))
_EVAL = _BACKEND / "mock_data" / "eval_signals_60.jsonl"
_STUB_CEILING = 0.90  # an implementation scoring below this is treated as a stub


def _load_eval() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in _EVAL.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


async def _run_accuracy() -> tuple[float, int, int]:
    """Return (accuracy, correct, total). Accuracy 0.0 if QueryAgent is absent/stub."""
    try:
        from agent_framework import ChatOptions

        from app.agents.query_agent import build_query_agent
        from app.agents.schemas import SignalClassification
        from app.services.mock.maf_chat_client import MockChatClient
    except Exception as exc:  # noqa: BLE001 - absent agent == stub
        print(f"[check_eval] QueryAgent not importable yet (stub): {exc}")
        return (0.0, 0, len(_load_eval()))

    rows = _load_eval()
    agent = build_query_agent(MockChatClient())
    correct = 0
    failures: list[str] = []
    for row in rows:
        resp = await agent.run(
            row["text"], options=ChatOptions(response_format=SignalClassification)
        )
        value = resp.value
        predicted = getattr(getattr(value, "intent_category", None), "value", None)
        if predicted == row["expected_category"]:
            correct += 1
        else:
            failures.append(f"  expected {row['expected_category']:<22} got {predicted!s:<22} :: {row['text'][:60]}")

    total = len(rows)
    if failures:
        print("[check_eval] misclassifications:")
        print("\n".join(failures))
    return (correct / total if total else 0.0, correct, total)


def main() -> int:
    parser = argparse.ArgumentParser(description="QueryAgent classification eval checkpoint")
    parser.add_argument("--min-accuracy", type=float, default=None)
    parser.add_argument("--expect-fail-on-stub", action="store_true")
    args = parser.parse_args()

    accuracy, correct, total = asyncio.run(_run_accuracy())
    print(f"[check_eval] accuracy={accuracy:.3f} ({correct}/{total})")

    if args.expect_fail_on_stub:
        if accuracy < _STUB_CEILING:
            print(f"[check_eval] OK: accuracy below {_STUB_CEILING} as expected for a stub")
            return 0
        print(f"[check_eval] FAIL: expected a failing stub but accuracy >= {_STUB_CEILING}")
        return 1

    min_acc = args.min_accuracy if args.min_accuracy is not None else _STUB_CEILING
    if accuracy >= min_acc:
        print(f"[check_eval] PASS: accuracy >= {min_acc}")
        return 0
    print(f"[check_eval] FAIL: accuracy {accuracy:.3f} < {min_acc}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
