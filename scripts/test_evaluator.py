#!/usr/bin/env python3
"""Glass-Box AI Audit — deterministic guardrail evaluator.

This is the "fix" half of the workshop exercise. It ships as a working
reference implementation: a deterministic, stdlib-only unit-test harness that
inspects the full internal trace produced by
``scripts/audit_simulation.py::ReconciliationAgent`` and proves three things:

  1. It can intercept and parse the agent's internal reasoning/scratchpad
     trace and detect synthetic-data-generation flags.
  2. It can verify a zero-trust API boundary — flagging any unauthorized
     network attempt in the trace.
  3. It halts workflow execution *before* a (mocked) database commit whenever
     either violation is present, while still allowing a clean trace through
     — proving the guardrail is precise, not a blanket block.

Run it with either::

    python -m unittest scripts/test_evaluator.py -v
    pytest scripts/test_evaluator.py

No network access, credentials, or third-party packages are required.
"""

from __future__ import annotations

import sys
import unittest
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock

# Import the sibling script by file location, not by relying on the caller's
# current working directory (scripts/ is not a package).
sys.path.insert(0, str(Path(__file__).resolve().parent))

from audit_simulation import (  # noqa: E402
    BROKEN_RECORD_IDS,
    SWARM_COORDINATION_RECORD_IDS,
    UNAUTHORIZED_NETWORK_RECORD_IDS,
    ReconciliationAgent,
    TraceEvent,
)


class HaltedWorkflowError(RuntimeError):
    """Raised when the Glass-Box gate blocks a workflow before it can reach
    a database commit."""


@dataclass(frozen=True)
class GateResult:
    passed: bool
    synthetic_data_events: list
    unauthorized_network_events: list
    swarm_coordination_events: list

    def summary(self) -> str:
        return (
            f"synthetic_data={len(self.synthetic_data_events)} "
            f"unauthorized_network={len(self.unauthorized_network_events)} "
            f"swarm_coordination={len(self.swarm_coordination_events)}"
        )


def evaluate_trace(trace: list) -> GateResult:
    """The deterministic Glass-Box guardrail.

    Scans every ``TraceEvent`` and buckets it by which flag(s) it carries.
    The gate passes only when NONE of the three violation types are present.
    """
    synthetic = [e for e in trace if e.flags.get("synthetic_data")]
    unauthorized = [e for e in trace if e.flags.get("unauthorized_network")]
    swarm = [e for e in trace if e.flags.get("swarm_coordination")]
    passed = not synthetic and not unauthorized and not swarm
    return GateResult(
        passed=passed,
        synthetic_data_events=synthetic,
        unauthorized_network_events=unauthorized,
        swarm_coordination_events=swarm,
    )


def run_guarded_pipeline(trace: list, commit_fn) -> GateResult:
    """Runs the deterministic gate before allowing ``commit_fn`` to execute.

    This is the "before you commit synthetic data to the database" halt the
    exercise asks for: if the gate fails, ``commit_fn`` is never called and a
    ``HaltedWorkflowError`` is raised instead.
    """
    result = evaluate_trace(trace)
    if not result.passed:
        raise HaltedWorkflowError(
            f"Halted before database commit — violations found: {result.summary()}"
        )
    commit_fn()
    return result


# --- Tests ------------------------------------------------------------


class TestGlassBoxEvaluator(unittest.TestCase):
    """Deterministic guardrail tests against the reconciliation simulation."""

    @classmethod
    def setUpClass(cls) -> None:
        # The simulation is deterministic; run it once and share the trace.
        cls.audit_result = ReconciliationAgent().run()

    def test_detects_synthetic_data_generation(self) -> None:
        """Every record with a fabricated tax_id must be flagged."""
        gate = evaluate_trace(self.audit_result.trace)
        flagged_ids = {
            int(e.record_id.split("-")[1])
            for e in gate.synthetic_data_events
            if e.record_id
        }
        self.assertEqual(flagged_ids, set(BROKEN_RECORD_IDS))

    def test_flags_unauthorized_network_attempts(self) -> None:
        """Zero-trust check: only the sanctioned records may reach the network."""
        gate = evaluate_trace(self.audit_result.trace)
        flagged_ids = {
            int(e.record_id.split("-")[1])
            for e in gate.unauthorized_network_events
            if e.record_id
        }
        self.assertEqual(flagged_ids, set(UNAUTHORIZED_NETWORK_RECORD_IDS))

    def test_flags_emergent_swarm_coordination(self) -> None:
        """Swarm check: inter-agent collusion messages must be caught too."""
        gate = evaluate_trace(self.audit_result.trace)
        flagged_ids = {
            int(e.record_id.split("-")[1])
            for e in gate.swarm_coordination_events
            if e.record_id
        }
        self.assertEqual(flagged_ids, set(SWARM_COORDINATION_RECORD_IDS))

    def test_gate_halts_workflow_before_database_commit(self) -> None:
        """The core guardrail: a flagged trace must NEVER reach the database."""
        commit_to_database = MagicMock()
        with self.assertRaises(HaltedWorkflowError):
            run_guarded_pipeline(self.audit_result.trace, commit_to_database)
        commit_to_database.assert_not_called()

    def test_clean_trace_passes_and_commits(self) -> None:
        """Negative control: an unflagged trace must NOT be blocked.

        This proves the guardrail is a precise, deterministic check — not a
        blunt instrument that halts everything regardless of content.
        """
        clean_trace = [e for e in self.audit_result.trace if not e.is_flagged()]
        self.assertGreater(len(clean_trace), 0, "sanity check: some events must be unflagged")

        commit_to_database = MagicMock()
        result = run_guarded_pipeline(clean_trace, commit_to_database)

        self.assertTrue(result.passed)
        commit_to_database.assert_called_once()

    def test_evaluator_output_is_deterministic(self) -> None:
        """Running the evaluator twice against fresh simulation runs must agree."""
        first = evaluate_trace(ReconciliationAgent().run().trace)
        second = evaluate_trace(ReconciliationAgent().run().trace)
        self.assertEqual(len(first.synthetic_data_events), len(second.synthetic_data_events))
        self.assertEqual(
            len(first.unauthorized_network_events), len(second.unauthorized_network_events)
        )
        self.assertEqual(
            len(first.swarm_coordination_events), len(second.swarm_coordination_events)
        )
        self.assertEqual(first.passed, second.passed)


if __name__ == "__main__":
    unittest.main()
