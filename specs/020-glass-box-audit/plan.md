# Implementation Plan: Glass-Box AI Audit Workshop Exercise

**Branch**: `020-glass-box-audit` | **Date**: 2026-09-20 (updated) | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/020-glass-box-audit/spec.md`

## Progress Log

- **Increment 1 (shipped, local-only)**: `scripts/audit_simulation.py`,
  `scripts/test_evaluator.py`, `exercises/01-glass-box-audit.md`, and the
  browser control room (`frontend/src/allclear/GlassBoxAudit.tsx` at
  `/?page=audit`) with its front-to-back Pipeline map and Azure Portal deep
  links. Covers User Stories 1–3. Verified via `python -m unittest
  scripts/test_evaluator.py -v`, `npm run typecheck`, `npm run build`.
- **Increment 2 (this update, planned/in progress)**: Deploy the same
  browser control room to Azure via the existing `azd up` path, and add a
  real Foundry evaluation suite so the guardrail claim is backed by an
  uploaded, gate-able eval run instead of only a local `unittest` pass.
  Covers User Story 4. See Phase 3 (Azure/Evals) in `tasks.md`.

## Summary

Build a standalone, offline hackathon workshop unit: a deterministic vendor
invoice reconciliation simulation (`scripts/audit_simulation.py`) with a
`--mode black-box|glass-box` CLI that dramatizes a real class of AI-agent
failure (concealed errors / data fabrication, sandbox escape, emergent swarm
coordination) sourced from four documented 2026 incidents; a companion
deterministic unit-test guardrail (`scripts/test_evaluator.py`) that detects
those failure signatures in the simulation's trace and halts a mocked
database commit; a facilitator/participant guide
(`exercises/01-glass-box-audit.md`); and a browser control room with a
front-to-back pipeline map linking each stage to its real Azure resource
type. This increment adds an **optional Azure track**: host the control room
at a stable event URL via the existing `azd up`/Container Apps path, and
register a Foundry evaluation suite that re-runs the deterministic guardrail
checks as a labeled dataset and uploads pass/fail results to the project's
Evaluations tab — mirroring the existing `evals/quality` and
`evals/red-team` conventions rather than inventing a new eval pipeline.

## Technical Context

**Language/Version**: Python 3.11 (stdlib only for the simulation/evaluator; the new eval-upload script may use `httpx`/Azure AI Evaluation SDK, matching `evals/quality/requirements.txt`) + TypeScript 5 / React 18 / Vite 5 for the existing `frontend` app (no version change)
**Primary Dependencies**: Simulation/evaluator: none beyond stdlib. New eval script: same dependency shape as `evals/quality/quality_eval.py` (`httpx`, Azure AI Foundry/Evaluation SDK, Azure credential library) — pinned in a new `evals/glass-box-audit/requirements.txt`, isolated from `scripts/`.
**Storage**: N/A for the simulation (in-memory only). The eval run and dataset live in the Foundry project's own storage (Evaluations tab) and a local `.foundry/datasets/*.jsonl` file, exactly like the existing `quality-smoke`/`safety-redteam` suites.
**Testing**: `unittest`/`pytest` for the simulation/evaluator (unchanged); the new eval script is validated via its `--skip-upload` local mode plus a manual check that uploaded rows match local `unittest` verdicts (SC-007).
**Target Platform**: Local devcontainer/laptop (Increment 1, unchanged) **plus** an Azure Container Apps-hosted frontend (Increment 2, reusing the existing `frontend` service in `azure.yaml`) and an Azure AI Foundry project (Increment 2, reusing the existing `.foundry/` project wiring — no new Azure resource types).
**Project Type**: Standalone CLI + unit-test harness + Markdown guide + existing React SPA route (Increment 1) **plus** an additive `evals/glass-box-audit/` Foundry evaluation script and `.foundry/agent-metadata.yaml` suite entry (Increment 2)
**Performance Goals**: Simulation/evaluator run in well under 1 second (unchanged). The new eval script's dataset is intentionally small (5 scenarios) so a full upload run completes in well under the time of a single `evals/quality` run.
**Constraints**: Increment 1's determinism/offline constraints are unchanged and MUST NOT regress (FR-020). Increment 2 MUST NOT require any new Azure resource type beyond what `infra/main.bicep` already provisions (FR-017), and MUST reuse the existing Foundry project/agent registration flow (`evals/register-agent/register_agent.py`) rather than defining a new one.
**Scale/Scope**: Increment 1 unchanged (2 scripts, 1 guide, 1 React route). Increment 2 adds: 1 new `evals/glass-box-audit/` directory (script + small JSONL dataset + README, mirroring `evals/quality/`), 1 new `evaluationSuites` entry in `.foundry/agent-metadata.yaml`, and doc updates to `exercises/01-glass-box-audit.md` and `quickstart.md`. No Bicep, `azure.yaml`, or CI workflow changes are required.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Data flow identifies PII handling, retention, audit events, and any
      embedding/external-service impact. — N/A: all data is synthetic and
      in-memory; nothing is persisted, no PII, no embeddings. Increment 2's
      eval dataset is likewise synthetic (the same 5 scenario labels), and
      the only external-service call it adds is the Foundry Evaluations
      upload itself, which is the same call pattern `evals/quality` already
      makes and documents.
- [x] QueryAgent, RouterExecutor, and ActionAgent authority boundaries are
      unchanged or explicitly justified and tested. — Unchanged in both
      increments: neither touches `backend/app/agents/*`.
- [x] Severity, statutory-clock, safety, PII, and human-request escalation
      behavior is preserved or expanded; no change weakens a trigger. — N/A,
      no production escalation path is touched by either increment.
- [x] Mock mode validates the same authority boundaries without Azure
      credentials. — N/A for Increment 1 (no Azure dependency at all).
      Increment 2's Azure paths are explicitly optional and additive
      (FR-020): the local-only demo continues to work with zero Azure
      credentials regardless of whether `azd up` or the eval script has ever
      been run.
- [x] Sitreps or factual output identify their source-record/citation
      behavior. — N/A for production sitreps; the workshop guide cites its
      four grounding incidents directly, and the new eval suite's dataset
      rows are labeled with their expected verdict for auditability.
- [x] Relevant backend tests and frontend/companion typecheck-build commands
      are listed in the Verification Matrix. — See Verification Matrix
      below; Increment 2 adds `azd up` + a Foundry eval run as additional,
      optional verification steps beyond the existing `npm run typecheck`/
      `npm run build`/`unittest` commands.
- [x] The design uses the canonical terms in `CONTEXT.md` and introduces no
      retired support-domain concepts. — Unchanged from Increment 1; the new
      eval suite is named and scoped as its own `glass-box-audit-guardrail`
      suite, not conflated with the production `all-clear-triage` agent's
      `quality-smoke`/`safety-redteam` suites.

## Project Structure

### Documentation (this feature)

```text
specs/020-glass-box-audit/
├── plan.md              # This file (updated for Increment 2)
├── research.md           # Phase 0 output (updated: Azure/evals decisions appended)
├── data-model.md         # Phase 1 output (updated: EvalScenario entity added)
└── quickstart.md         # Phase 1 output (updated: azd/eval verification steps appended)
```

No `contracts/` directory: this feature exposes no network API consumed by
another system. Increment 2's only new "contract" is the JSONL dataset row
shape for `EvalScenario`, specified in `data-model.md`.

### Source Code (repository root)

```text
scripts/
├── audit_simulation.py   # Increment 1: deterministic simulation + CLI (unchanged)
└── test_evaluator.py     # Increment 1: deterministic unittest guardrail suite (unchanged)

exercises/
└── 01-glass-box-audit.md # Increment 1 + 2: guide (Increment 2 adds an Azure/evals section)

frontend/src/allclear/
└── GlassBoxAudit.tsx     # Increment 1: browser control room + pipeline map (unchanged by Increment 2 — hosting only)

evals/glass-box-audit/    # NEW (Increment 2): mirrors evals/quality/ layout
├── requirements.txt       # httpx + Azure AI Evaluation SDK + Azure credential lib
├── scenarios.json         # 5 labeled EvalScenario rows (clean/fabrication/network/swarm/all)
├── glass_box_eval.py      # Loads scenarios, runs evaluate_trace(), uploads to Foundry
└── README.md              # Run instructions, mirrors evals/quality/README.md

.foundry/agent-metadata.yaml   # UPDATED (Increment 2): new evaluationSuites entry
.foundry/datasets/
└── glass-box-audit-guardrail-seed-v1.jsonl  # NEW: exported scenario dataset
```

**Structure Decision**: Increment 1's structure (flat `scripts/` additions,
new top-level `exercises/`, one new `frontend/src/allclear/*` route) is
unchanged. Increment 2 adds one new sibling directory under `evals/`
(`evals/glass-box-audit/`) following the exact layout already used by
`evals/quality/` and `evals/red-team/`, plus one additive entry in the
existing `.foundry/agent-metadata.yaml`. Hosting the browser control room
requires **no new Azure resources or Bicep changes** — it reuses the
`frontend` Container App `azd up` already deploys today.

## Complexity Tracking

*No Constitution Check violations — table intentionally left empty.*
