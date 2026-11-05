# Feature Specification: Event-Day Readiness Verification

**Feature Branch**: `020-glass-box-audit` (documented before execution; no new
branch created — see Note below)
**Created**: 2026-09-20
**Status**: Draft (execution in progress; verification-only, no product code
changes anticipated unless a defect is found)
**Input**: User description: "is the glass box audit working in azure?" →
"run azd up and run evals on it before we try to merge it to main" → "im in"
(Azure authentication confirmed) → "i need you to test the entire app. evals,
red team, etc. this thing has to be bulletproof before thursday" → "hire a
squad and make a few loops for this" → "create a plan in spec kit before
executinig"

**Note on branch**: This record documents a verification effort against
work already on `020-glass-box-audit` (most recently commit `8a0e5d7`). No new
git branch is created for a testing/verification pass; the `022-` prefix only
orders this Spec Kit record after `021-briefing-room-demo-readiness`. If any
defect fixes result from this effort, they land as additional commits on
`020-glass-box-audit`, same as prior increments.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Facilitator has confidence the app is "bulletproof" before the event (Priority: P1)

Before merging `020-glass-box-audit` to `main` ahead of Thursday's AI/hackathon
event, the facilitator needs verifiable evidence that: the full automated test
suite passes, the app builds cleanly, the Azure deployment path actually works
end-to-end in a real subscription (not just locally/mock), and the safety/
quality eval gates (red-team, quality, glass-box-audit guardrail) all come
back clean against a live deployment.

**Why this priority**: This is the explicit go/no-go gate the user asked for
before merge. Without it, "merge to main" is a guess, not a decision.

**Independent Test**: Run the full backend pytest suite, the frontend
build/typecheck, and all three Foundry eval suites (`quality-smoke`,
`safety-redteam`, `glass-box-audit-guardrail`) against a live Azure deployment
of the `frontend`/`backend` Container Apps, and confirm every gate is green.

**Acceptance Scenarios**:

1. **Given** the `020-glass-box-audit` branch, **When** the backend pytest
   suite is run in full (`PYTHONPATH=. python -m pytest tests/ -q`), **Then**
   all tests pass (baseline captured this session: 347/347 passed).
2. **Given** the `frontend` package, **When** `npm run build` (tsc + vite
   build) is run, **Then** it completes with no type errors and no new build
   warnings beyond the pre-existing Tailwind gradient-syntax notices.
3. **Given** Azure credentials authenticated via `azd auth login`, **When**
   `azd up` is run against a fresh environment, **Then** the `backend` and
   `frontend` Container Apps provision and deploy successfully, and
   `/api/health`, `/`, `/?page=audit`, and `/phone` all resolve with healthy
   responses on the live `AZURE_FRONTEND_URL`/`AZURE_CONTAINERAPP_URL`.
4. **Given** the live deployment, **When** `evals/quality/quality_eval.py` is
   run against it, **Then** Relevance/Coherence/Fluency scores clear their
   thresholds (≥3) and results upload to the Foundry project's Evaluations
   tab.
5. **Given** the live deployment, **When** `evals/red-team/red_team_scan.py`
   is run against it, **Then** the attack success rate (ASR) is 0.0% (matching
   the existing `evals/red-team/RESULTS.md` baseline) and results upload to
   the Foundry project's Red teaming tab.
6. **Given** the live deployment (or local, if Foundry upload is unavailable),
   **When** `evals/glass-box-audit/glass_box_eval.py` is run, **Then** all 5
   scenarios (`clean`, `fabrication_only`, `network_only`, `swarm_only`,
   `all_violations`) match their expected verdicts (baseline captured this
   session via `--skip-upload`: 5/5 matched).
7. **Given** all of the above pass, **When** the facilitator asks "are we
   ready to merge," **Then** this spec's tasks.md shows every task checked
   with evidence (command output, URLs, or eval scores) attached.

---

### User Story 2 - Regressions are caught before an audience sees them (Priority: P2)

Beyond the specific gates above, a broader sweep across the app (BriefingRoom
main flow, `/phone` standalone live-call monitor, `/?page=audit` glass-box
control room, `/?page=clone`) should be exercised to catch anything the
targeted test suites don't cover — e.g. console errors, broken links, or
layout regressions introduced by this session's UI cleanup
(`021-briefing-room-demo-readiness`).

**Why this priority**: Automated suites don't render pages; a live/visual
sweep is the only way to catch rendering regressions the way an audience
would actually experience them.

**Independent Test**: Load each of the app's routes in a browser (or
Playwright) at demo-relevant viewport widths and confirm no console errors,
no broken links, and no visual regressions versus the last verified state.

**Acceptance Scenarios**:

1. **Given** the local dev servers (or the live Azure deployment), **When**
   `/`, `/phone`, `/?page=audit`, and `/?page=clone` are each loaded, **Then**
   no route throws a console error and each renders its expected control
   surface.
2. **Given** a defect is found, **When** it is fixed, **Then** the fix is
   scoped to the smallest surgical change, verified by re-running the
   relevant test/build/eval, and recorded in this spec's tasks.md.

---

### User Story 3 - Live phone-call demo path is provisioned and verified (Priority: P2, added mid-session)

For the Thursday demo, the facilitator wants to place a **real live phone
call** to the deployed app (not just the mock-mode simulation) and see the
transcript appear on `/phone`. This requires a live Azure Communication
Services (ACS) phone number and `MOCK_MODE=false` for the phone subsystem,
which is a materially different (and cost-bearing) configuration from the
mock-mode deployment used for Stories 1 and 2.

**Why this priority**: Explicitly requested by the user ("to test the calling
feature, you'll need to provision a phone number and setup acs"). It's P2
because it's an additive stretch capability layered on top of the P1
core-readiness gates, not a blocker for them.

**Independent Test**: With a purchased ACS number wired into the live
deployment, place a real call to that number and confirm the backend's Call
Automation webhook receives it and a transcript renders on `/phone`.

**Acceptance Scenarios**:

1. **Given** a live `azd`-deployed environment, **When** an ACS phone number
   is purchased and `MOCK_MODE` is set to `false` with the number wired into
   the bicep `acsPhoneNumber` param, **Then** the backend's
   `get_phone_service()` resolves to `AzurePhoneService` instead of
   `MockPhoneService` (per `backend/app/core/config.py`'s
   `_auto_disable_features` validator).
2. **Given** that configuration, **When** someone calls the purchased number,
   **Then** ACS's Event Grid `IncomingCall` subscription (only created when
   not in mock mode, per `infra/main.bicep`) delivers the event to the
   backend's phone webhook and a live transcript appears on `/phone`.
3. **Given** this is a purchased, billable resource, **When** testing is
   complete, **Then** the number is released/cleaned up rather than left
   running indefinitely, per the repo's existing convention (
   `labs/06-deploy-with-azd/exercises/06b-azure-deployment.md`: *"purchase and
   configure its own ACS number; ... must never reuse another deployment's
   number"*).

### Edge Cases

- What happens if `azd up` fails partway (quota, RBAC, provider registration,
  naming collision)? → Diagnose from the error, attempt one reasonable fix,
  retry once; if still failing, report the exact blocking error rather than
  looping indefinitely (protects both time and cost before the event).
- What happens if a live Foundry project/endpoint isn't available even after
  a successful `azd up` (e.g. bicep doesn't provision one)? → Fall back to
  each eval script's local/`--skip-upload` mode so the *deterministic logic*
  is still verified, and note in tasks.md that the Foundry-upload visibility
  leg specifically was not completed live.
- What happens if red-team/quality evals reveal a real regression (non-zero
  ASR, or a relevance/coherence score below threshold)? → Treat as a blocking
  defect: stop, report it, and do not recommend merging until it's triaged.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The full backend pytest suite (`backend/tests/`) MUST be run
  and pass in full (not just the constitution's minimal focused subset) as
  part of this readiness pass.
- **FR-002**: The frontend build (`npm run build`, which includes `tsc`) MUST
  be run and pass with no new type or build errors.
- **FR-003**: `azd up` MUST be attempted against a live Azure subscription,
  and its outcome (success with URLs, or the specific blocking failure) MUST
  be recorded.
- **FR-004**: If `azd up` succeeds, the deployed app's key routes
  (`/api/health`, `/`, `/?page=audit`, `/phone`) MUST be verified live via
  HTTP requests.
- **FR-005**: All three Foundry evaluation suites already defined in
  `.foundry/agent-metadata.yaml` (`quality-smoke`, `safety-redteam`,
  `glass-box-audit-guardrail`) MUST be run at least once this session, either
  against the live deployment (preferred) or in local/dry-run mode (fallback,
  clearly noted as such).
- **FR-006**: Any defect discovered during this pass MUST be triaged: either
  fixed with a surgical, tested change, or explicitly logged as a known issue
  with a recommendation on whether it blocks the merge to `main`.
- **FR-007**: This verification pass MUST NOT weaken any existing test,
  eval threshold, or safety gate in order to make it "pass" — a green result
  must reflect real behavior, not a loosened check.

### Incident-Triage / Safety Constraints *(complete for every feature)*

- **PII handling**: Unchanged — no data-handling code is modified by a
  verification pass; if a defect fix is needed, it must preserve existing PII
  redaction behavior (verified by `backend/tests/test_voice/test_pii_filter.py`
  and the phone-safety-net suite already in the baseline 347-test run).
- **QueryAgent/RouterExecutor/ActionAgent authority boundaries**: Unchanged;
  this pass observes/tests, it does not alter agent logic.
- **Severity/statutory-clock/escalation behavior**: Unchanged; covered by the
  existing pytest suite (`test_wave1_verifiers.py`, `test_router_no_llm.py`,
  `test_voice/test_safety_net.py`) which is part of FR-001's full run.
  Red-team ASR (FR-005) is the additional live safety signal.
- **Mock mode**: The Azure deployment (FR-003/004) is deployed with
  `MOCK_MODE=true` by default — proves the deployment topology and routes
  work without requiring live Azure OpenAI/ACS credentials, per the
  constitution's "keep mock mode viable" non-negotiable.
- **Sitrep/citation behavior**: Unchanged; not exercised directly by this
  verification pass beyond the existing pytest coverage.

## Key Entities

- **Live Azure deployment**: The `frontend`/`backend` Container Apps
  provisioned by `azd up` for this verification pass, identified by
  `AZURE_CONTAINERAPP_URL` / `AZURE_FRONTEND_URL` (recorded once known).
- **Eval suite result**: One outcome per Foundry evaluation suite
  (`quality-smoke`, `safety-redteam`, `glass-box-audit-guardrail`) — pass/fail
  plus scores/ASR, either uploaded live to Foundry or captured locally.
- **Readiness verdict**: The overall go/no-go conclusion for merging
  `020-glass-box-audit` to `main`, backed by the evidence gathered in
  tasks.md.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of backend pytest tests pass (target: no regression from
  the 347/347 baseline captured this session).
- **SC-002**: Frontend build completes with exit code 0 and zero new
  warnings/errors.
- **SC-003**: `azd up` either succeeds (all 4 routes verified live) or fails
  with a clearly diagnosed, single documented blocking error — not left
  ambiguous.
- **SC-004**: All 3 Foundry eval suites produce a recorded result (live or
  local-fallback) with pass/fail explicitly stated.
- **SC-005**: A single readiness verdict (ready to merge / not yet, with
  reasons) is recorded in tasks.md before any recommendation to merge to
  `main` is made.
