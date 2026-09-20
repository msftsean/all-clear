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
- Live readiness follow-up on branch `020-glass-box-audit`: the deployed
  backend in `.squad/identity/live-deploy.md` was reachable and processed all
  `evals/quality/queries.json` signals live, but `evals/quality/quality_eval.py`
  could not score them because the current operator identity lacks Azure
  OpenAI `chat/completions` data-plane permission and the target OpenAI
  resource has key-based auth disabled (`AuthenticationTypeDisabled`).
- The official Foundry red-team harness still has no local-only path:
  `evals/red-team/red_team_scan.py` requires both the `azure-ai-evaluation`
  redteam extras and a real `AZURE_AI_PROJECT_ENDPOINT`; without the project
  endpoint the scan exits immediately, so the clean fallback is a bounded set
  of direct `/api/chat` safety probes with explicit live-vs-Foundry caveats.
- Live fallback probing found a useful nuance: violence, hate, and prompt
  injection were hard-blocked; self-harm took the intended 988 escalation
  path; a sexual-content prompt produced a safe terse incident acknowledgment
  rather than unsafe content, which avoids a leak but is still worth tracking
  because it is not a content-filter block.
