# Implementation Plan: Event-Day Readiness Verification

**Branch**: `020-glass-box-audit` | **Date**: 2026-09-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/022-event-day-readiness-verification/spec.md`

**Status**: In progress. This plan is written and reviewed **before** the
remaining verification work executes, per explicit user request ("create a
plan in spec kit before executinig"). Some baseline evidence was already
gathered earlier in this session (see "Already captured" below) before the
user asked for this plan; everything else below executes after this plan is
recorded.

## Summary

Verify that `020-glass-box-audit` is safe to merge to `main` ahead of
Thursday's event by: (1) re-confirming the full backend/frontend test and
build gates, (2) actually provisioning and deploying to a live Azure
subscription via `azd up` (not just validating locally), (3) running all
three Foundry evaluation suites (quality, red-team, glass-box-audit
guardrail) against that live deployment, and (4) doing a visual/route sweep
across the app's four entry points. Work is delegated to the existing `.squad`
team (Kitty for Azure, Forge for evals/red-team, Beast for the QA/regression
sweep, Bishop for final synthesis), coordinated by Squad in Full Mode.

## Technical Context

**Language/Version**: Python 3.11+ (backend, evals), TypeScript 5 / React 18
(frontend) — no version changes
**Primary Dependencies**: `azd` CLI 1.34.x (already authenticated this
session), `az bicep`, Foundry eval scripts' existing dependencies
(`evals/quality/requirements.txt`, `evals/red-team/requirements.txt`,
`evals/glass-box-audit/requirements.txt`) — no new dependencies introduced
**Storage**: N/A for this pass — no schema/data changes; a live Azure
subscription's Container Apps/Cosmos/Search/ACR/Key Vault resources are
provisioned by the existing `infra/main.bicep` (unchanged)
**Testing**: `backend/tests/` (full suite, not the constitution's minimal
subset — 347 tests as of this session), `frontend` `npm run build`,
`evals/quality/quality_eval.py`, `evals/red-team/red_team_scan.py`,
`evals/glass-box-audit/glass_box_eval.py`
**Target Platform**: Live Azure (Container Apps) for the deployment leg;
local devcontainer for the test/build/eval-dry-run legs
**Project Type**: Web application (existing `backend/` + `frontend/` split);
this is a verification pass, not a new feature — no new source files expected
unless a defect fix is required
**Constraints**: Must not weaken any existing test, threshold, or safety gate
to force a pass (FR-007); `azd up` failures get one diagnosed retry, not
unbounded retries (cost/time discipline before the event); deploy with
`MOCK_MODE=true` by default to keep the mock-mode non-negotiable provable
without requiring live Azure OpenAI/ACS credentials
**Scale/Scope**: One fresh `azd` environment; three eval suites; four routes
(`/`, `/phone`, `/?page=audit`, `/?page=clone`); full existing backend test
suite (no new tests planned unless a defect surfaces)

## Constitution Check

*GATE: Must pass before execution. Re-check after execution.*

- [x] Data flow identifies PII handling, retention, audit events, and any
      embedding/external-service impact. → No data flow changes; this pass
      only runs existing tests/evals against existing code. PII redaction
      coverage is part of the full pytest run (FR-001).
- [x] QueryAgent, RouterExecutor, and ActionAgent authority boundaries are
      unchanged or explicitly justified and tested. → Unchanged; verification
      only. If a defect fix touches these, it must come with its own test.
- [x] Severity, statutory-clock, safety, PII, and human-request escalation
      behavior is preserved or expanded. → Preserved; the full pytest suite
      (which includes `test_wave1_verifiers.py`, `test_router_no_llm.py`,
      `test_voice/test_safety_net.py`) plus the live red-team scan (FR-005)
      are the two independent signals confirming this.
- [x] Mock mode validates the same authority boundaries without Azure
      credentials. → Explicitly tested by FR-003/004: the live Azure
      deployment is done with `MOCK_MODE=true`, proving the deployment
      topology works without live Azure OpenAI/ACS credentials.
- [x] Sitreps or factual output identify their source-record/citation
      behavior. → Unchanged; not a focus of this pass beyond existing pytest
      coverage.
- [x] Relevant backend tests and frontend/companion typecheck-build commands
      are listed in the Verification Matrix. → See below.
- [x] The design uses the canonical terms in `CONTEXT.md` and introduces no
      retired support-domain concepts. → N/A — no new UI/copy introduced by a
      verification pass.

## Already captured (before this plan was written)

Per the user's request to plan before further execution, work already done
earlier in this session is treated as baseline evidence, not re-run blindly:

| Check | Result |
|---|---|
| `cd backend && PYTHONPATH=. python -m pytest tests/ -q` | **347 passed**, 3 warnings (pre-existing deprecation notices), 0 failed |
| `cd frontend && npm run build` | Clean (`tsc` + `vite build`), only pre-existing Tailwind gradient-syntax CSS warnings |
| `az bicep build --file infra/main.bicep --stdout` | Compiles cleanly, no errors |
| `cd evals/glass-box-audit && python glass_box_eval.py --skip-upload` | **5/5 scenarios matched expected verdict** (local-only, no live Foundry upload yet) |
| `azd auth login --check-status` | Authenticated as `maryland-admin01@publicsectorhacks.com` |
| Subscription discovery via `azd auth token` + ARM REST | 10 "CopilotLabs DS - *" sandbox subscriptions available; none yet selected/provisioned against |

## Project Structure

### Documentation (this feature)

```text
specs/022-event-day-readiness-verification/
├── spec.md   # User scenarios + requirements (this record)
├── plan.md   # This file
└── tasks.md  # Execution ledger — written next, tracks live progress
```

No `research.md`, `data-model.md`, `contracts/`, or `quickstart.md` — this is
a verification pass against existing, already-specified functionality
(`020-glass-box-audit`, `021-briefing-room-demo-readiness`), not new product
design.

### Delegation (Squad)

Work is delegated to the existing `.squad/` team rather than done by the
Coordinator directly, per Squad's Full Mode (3+ concerns: Azure deploy,
eval/red-team, QA sweep):

| Agent | Scope | Mode |
|---|---|---|
| Kitty | `azd up` against a live subscription; verify live URLs/routes; write results to `.squad/identity/live-deploy.md` | background |
| Forge | Run `quality-smoke`, `safety-redteam`, `glass-box-audit-guardrail` eval suites against the live deployment (falls back to local/dry-run mode per suite if the live leg is unavailable) | background, chained after Kitty's URLs are available |
| Beast | Full regression/QA sweep: re-run backend pytest + frontend build as an independent check, visual/console sweep of `/`, `/phone`, `/?page=audit`, `/?page=clone` | background, parallel with Kitty |
| Bishop | Synthesize all agents' results into a single go/no-go readiness verdict | sync, after Kitty/Forge/Beast complete |
| Scribe | Log orchestration + merge decisions | background, after Bishop |

## Verification Matrix

| Surface | Command or check | Owner |
|---|---|---|
| Backend full suite | `cd backend && PYTHONPATH=. python -m pytest tests/ -q` | Beast (re-confirm) |
| Frontend build | `cd frontend && npm run build` | Beast (re-confirm) |
| Live Azure deploy | `azd up` + `curl` against `/api/health`, `/`, `/?page=audit`, `/phone` | Kitty |
| Quality eval | `python evals/quality/quality_eval.py` against live backend | Forge |
| Red-team eval | `python evals/red-team/red_team_scan.py` against live backend | Forge |
| Glass-box-audit eval | `python evals/glass-box-audit/glass_box_eval.py` (live upload if Foundry endpoint available, else `--skip-upload`) | Forge |
| Route/console sweep | Playwright or manual load of all 4 routes | Beast |
| Final verdict | Manual synthesis in tasks.md | Bishop |

## Complexity Tracking

*No Constitution Check violations — this section is intentionally empty.*
