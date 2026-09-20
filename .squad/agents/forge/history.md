# History

## Project Context

All Clear is a Python/FastAPI and TypeScript accelerator requested by
MARYLAND ADMIN 01.

## Learnings
- Built the additive Glass-Box Audit Foundry guardrail eval surface in
  `evals/glass-box-audit/` with `glass_box_eval.py`, `scenarios.json`,
  `README.md`, and `requirements.txt`, plus the exported dataset
  `.foundry/datasets/glass-box-audit-guardrail-seed-v1.jsonl` and the new
  `.foundry/agent-metadata.yaml` evaluation suite entry.
- The `--skip-upload` path in `evals/glass-box-audit/glass_box_eval.py`
  deliberately defers all Azure SDK imports until the upload branch so the
  deterministic local gate works with stdlib only, matching the request's
  stricter behavior relative to `evals/quality/quality_eval.py`.
- Deviation from the earlier data-model wording: the scenario builders use
  minimal synthetic `TraceEvent` instances rather than reusing
  `audit_simulation.py` construction helpers, because the request explicitly
  authorized short in-process traces to exercise `evaluate_trace()` without
  re-running the 100-record simulation.
