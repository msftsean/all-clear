# Decisions

## 2026-09-20 — Event readiness objective

The squad will make one authoritative All Clear participant path fit the event
window. Required stages need executable self-checks; optional material must not
be presented as required.

## 2026-09-20 — Roster change: X-Men cast, Bishop as Lead

**By:** MARYLAND ADMIN 01. The squad recast from its initial roster to an
X-Men cast with Bishop as Lead (Storm=Curriculum, Forge=Platform,
Beast=QA/Event Tester, Kitty=Azure/DevOps). Prior in-flight work was preserved
and reviewed under the new names rather than discarded; the retired agent
folders were moved to `.squad/agents/_alumni/`.

## 2026-09-20 — Authoritative 390-minute event path (S0-S5)

The event-ready path is the mock-runnable participant spine already on the
runbook: Lab 00 setup, Lab 01 classification, Lab 03 spec/constitution
alignment, Lab 04 grounded retrieval, Lab 05 orchestration/surge replay, and
Lab 09 GitHub verification — 315 minutes of work plus 75 minutes of protected
breaks/lunch. Individual Azure MCP setup (Lab 02), `azd up` deployment
(Lab 06), MCP red-team (Lab 07), APIM gateway (Lab 08), voice/phone
extensions, and model-continuity/failover (Exercise 05y) are optional,
coach-led, or take-home and must never be presented as part of the completion
contract. Completion must be backed by executable verifier evidence
(`verify_environment.py`, `test_lab01.py`, `test_lab03.py`, `verify_index.py`
+ `test_rag.py`, `test_lab05.py` + surge smoke test, and the Lab 09 starter +
`participant_extension/` gate), never by an environment variable or verbal
claim. Full plan: `docs/event-readiness/DELIVERY_PLAN.md`.

## 2026-09-20 — Azure event path is shared-backend-first

The required Azure surface is a facilitator-provided, preflighted shared
backend plus (only if APIM is promised) an individual APIM Consumption
gateway following Lab 08's Provision → Import → Call happy path. Individual
`azd up`, Docker builds, Cosmos/Search/OpenAI provisioning, APIM policies,
JWT enforcement, and Application Insights diagnostics are optional deep
dives. Facilitators must run the preflight (RBAC, provider registration,
quota/capacity, deterministic naming, JWT issuer/audience, App Insights
access) and a 20-participant APIM dress rehearsal, and must stop personal
provisioning after repeated 429s, unregistered providers, or the documented
10-minute APIM / 45-minute full-stack budget in favor of the shared backend.
Full checklist: `docs/event-readiness/AZURE_PREFLIGHT.md`.

## 2026-09-20 — Curriculum readiness verifier is the enforcement gate

`scripts/curriculum-readiness.mjs` (via `npm run curriculum:verify`) is the
automated gate for curriculum drift: local link integrity, canonical
governance references (`.specify/memory/constitution.md`, never
`shared/constitution.md`), required S0-S5 artifacts, agenda/break arithmetic,
required workflow filenames, and completion gates that must rely on
observable evidence rather than an environment variable alone. It
intentionally never scans the prohibited `files/` directory. Focused tests
live in `tests/curriculum/curriculum-readiness.test.mjs`.

## 2026-09-20 — Lab 09 completion gate uses a bounded extension artifact

Lab 09's completion gate no longer trusts `ALL_CLEAR_LAB09_COMPLETE` alone;
`test_starter_red_to_green.py` strips that variable and requires a real
`participant_extension/extension.py` plus its own passing
`test_extension.py`. Participant extensions must remain pure/bounded — no new
incident authority, no bypass of routing or severity.

## 2026-09-20 — Full eval/e2e validation pass, Azure pieces confirmed as facilitator-gated

Ran every eval and e2e suite in the repository:

- `backend/scripts/check_eval.py --min-accuracy 0.90`: 60/60 (100%).
- Full backend suite: 347 passed. Focused reruns: `test_pipeline_e2e.py` (5),
  `test_phone/eval_harness.py` (21), `test_azure_incident_store.py` (9, Cosmos
  contract on mocks), safety/PII/escalation subset (59) — all pass.
- Frontend Playwright e2e (`frontend/tests/e2e`): 25 passed (Chromium +
  Firefox + WebKit + Mobile Chrome/Safari), 75 skipped by design
  (accessibility suite scoped to desktop Chromium only), 0 failed.
- `hackathon-site` e2e: 38 passed, 2 skipped. `coach-site` e2e: 34 passed.
  `workshop-site` and `docs-site`: typecheck + build clean (no e2e suite
  configured for these two).
- Both `infra/main.bicep` and `labs/06-deploy-with-azd/infra/main.bicep`
  compile via `az bicep build`; `azure.yaml` and both parameter JSON files are
  valid.
- **Confirmed by design, not a gap:** `evals/quality/quality_eval.py` and
  `evals/red-team/red_team_scan.py` require a live deployed backend, a real
  Azure AI Foundry project endpoint, and `az login` — none are available in
  this sandbox (`az account show` fails; no `azd env`; no `AZURE_*`
  credentials set). This matches `docs/event-readiness/AZURE_PREFLIGHT.md`,
  which already treats live Azure validation (APIM rehearsal, quota checks,
  quality eval, red-team scan) as a facilitator preflight step requiring real
  subscription access, never something CI/sandbox can certify. The offline
  equivalent (deterministic safety/PII/escalation tests, mock-mode pipeline
  e2e, bicep compilation) is green; `evals/red-team/RESULTS.md` is correctly
  labeled historical-reference-only and does not claim current-state proof.

## 2026-09-20 — Model-continuity and MCP red-team exercises stay bounded

The model-continuity exercise (`labs/05-agent-orchestration/exercises/05y-model-continuity.md`
+ `verify_model_continuity.py`) proves failover preserves typed
classification, severity/SLA, and escalation using the existing
`backend/tests/test_failover/` contract — no new failover feature was added.
The MCP red-team probe (`labs/07-mcp-server/exercises/mcp_red_team_probe.py`)
is deterministic and offline, checking PII redaction, prompt-injection
resistance, and SEV1/SLA preservation against the Lab 07 server contract.
Both are optional/take-home, not part of the required S0-S5 completion
contract.
