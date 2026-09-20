---

description: "Execution ledger for Event-Day Readiness Verification — updated live as work completes"
---

# Tasks: Event-Day Readiness Verification

**Input**: Design documents from `/specs/022-event-day-readiness-verification/`
**Prerequisites**: plan.md, spec.md (both in this directory)

**Status**: Plan reviewed; execution resuming. Tasks below reflect what's
already done (checked, with evidence) versus what remains before a merge
recommendation is made.

## Phase 0: Baseline (already done, captured this session before this plan)

- [x] T001 Full backend pytest suite: `cd backend && PYTHONPATH=. python -m pytest tests/ -q` → **347 passed**, 0 failed
- [x] T002 [P] Frontend build: `cd frontend && npm run build` → clean, only pre-existing Tailwind CSS warnings
- [x] T003 [P] Bicep validation: `az bicep build --file infra/main.bicep --stdout` → compiles cleanly
- [x] T004 [P] Glass-box-audit eval local dry-run: `python evals/glass-box-audit/glass_box_eval.py --skip-upload` → **5/5 scenarios matched expected verdict**
- [x] T005 Azure auth confirmed: `azd auth login --check-status` → authenticated as `maryland-admin01@publicsectorhacks.com`
- [x] T006 Subscription discovery: 10 "CopilotLabs DS - *" sandbox subscriptions enumerated via `azd auth token` + ARM REST call

**Checkpoint**: Everything that doesn't require a live Azure resource is
green. No defects found yet.

---

## Phase 1: Live Azure deployment (User Story 1) — owner: Kitty

- [ ] T007 [US1] `azd env new` a fresh environment against a chosen "CopilotLabs DS - *" subscription, region `eastus2` (or another red-team-supported region if there's a reason), `MOCK_MODE=true`
      Evidence (2026-09-20): Created azd env `all-clear-demo` in subscription
      `a8a91d76-473f-49e2-ba21-1d394ba9a968` / `eastus2`; `azd env get-values`
      showed `AZURE_ENV_NAME="all-clear-demo"` and `MOCK_MODE="true"`.
- [ ] T008 [US1] Run `azd up --no-prompt`; capture full output; on failure, diagnose + one retry, then stop and report if still failing (per spec Edge Cases)
      Evidence (2026-09-20): First `azd up --no-prompt` hung in ARM on
      `Microsoft.EventGrid/systemTopics/eventSubscriptions/incoming-call`
      because checked-in `infra/main.parameters.json` defaults overrode azd env
      values, leaving `mockMode=false` / phone wiring active. One bounded retry
      after forcing mock-mode params failed with
      `ContainerAppSecretInvalid` on secret `acs-connection-string`. Stopped
      after that single retry and cleaned the sandbox with
      `azd down --purge --force`.
- [ ] T009 [US1] Record `AZURE_CONTAINERAPP_URL`, `AZURE_FRONTEND_URL`, and `AZURE_AI_PROJECT_ENDPOINT` (if provisioned) to `.squad/identity/live-deploy.md`
      Evidence (2026-09-20): Recorded the failed deployment state and captured
      URLs in `.squad/identity/live-deploy.md`.
- [ ] T010 [US1] Verify live: `/api/health` (backend), `/`, `/?page=audit`, `/phone` (frontend) all resolve healthy/200
      Evidence (2026-09-20): Provisioned frontend URL returned 200 on `/`,
      `/?page=audit`, and `/phone`, but served the default Azure Container Apps
      welcome page; backend `/api/health` timed out. No live app verification
      succeeded.

**Root-cause fixes applied (2026-09-20, by Squad coordinator) — committed to
`020-glass-box-audit`:**

1. **`infra/main.bicep`** — the `acs-connection-string` Container App secret
   was set to `mockMode ? '' : ...`. Azure Container Apps rejects
   **empty-string** secret values (`ContainerAppSecretInvalid`), unlike the
   `cosmos-db-key` secret right above it which correctly uses a `'mock'`
   placeholder. Fixed to match that pattern:
   `mockMode ? 'mock' : acs.listKeys().primaryConnectionString`. This was the
   proximate cause of the `ContainerAppSecretInvalid` retry failure.
2. **`infra/main.parameters.json`** — `mockMode`, `deployRealtime`, and
   `acsPhoneNumber` were hardcoded literal JSON values (`false`/`true`/`""`),
   so `azd env set MOCK_MODE ...` had **zero effect** on the actual deployed
   configuration — every `azd up` silently deployed in full non-mock mode
   with real Azure OpenAI (gpt-5.1) + realtime model regardless of azd
   environment settings. This is almost certainly why the *first* `azd up`
   hung (real GPT-5.1/realtime model provisioning + quota checks instead of
   the intended fast, credential-free mock-mode path — matches Kitty's
   observation that `mockMode=false` stayed active despite the env value).
   Fixed using azd's documented environment-variable-substitution
   convention: `"value": "${MOCK_MODE=true}"`,
   `"value": "${DEPLOY_REALTIME=false}"`, `"value": "${ACS_PHONE_NUMBER=}"` —
   defaults now match the constitution's "keep mock mode viable"
   non-negotiable, while remaining fully overridable per-environment via
   `azd env set` (needed for Phase 1b's real-ACS test and for lab 06b's
   full-fidelity deployment exercise, which can now do `azd env set
   MOCK_MODE false` and have it actually take effect).
   Verified via `azd provision --preview` (no resources created): with
   `MOCK_MODE=true` (default) and no `DEPLOY_REALTIME` override, the preview
   plan correctly excludes the Azure OpenAI realtime resource and shows the
   lean mock-mode resource set. `az bicep build --file infra/main.bicep
   --stdout` still compiles cleanly (only pre-existing BCP318/BCP422
   nullability warnings, no new errors).
- [ ] T008b [US1] Kitty: redeploy with these fixes (`azd up --no-prompt` again
      against the existing `all-clear-demo` env, which already has
      `MOCK_MODE=true`) and re-verify T009/T010.

**Checkpoint**: Live deployment either verified working, or a single clearly
diagnosed blocking failure is documented — not left ambiguous (SC-003).

---

## Phase 1b: Live phone / ACS provisioning (User Story 3, added mid-session) — owner: Kitty

User directive (2026-09-20): *"to test the calling feature, you'll need to
provision a phone number and setup acs."* Per `labs/06-deploy-with-azd/exercises/06b-azure-deployment.md`
line 226, phone is an explicit stretch goal: **"A team that elects to add it
must purchase and configure its own ACS number; it must never reuse another
deployment's number."** This deployment purchases its own number for this
test only.

- [ ] T007b [US3] Confirm the `acs` Communication Services resource exists
      from Phase 1's `azd up` (it's provisioned unconditionally in
      `infra/main.bicep`, mock mode or not).
      Evidence (2026-09-20 follow-up): ARM GET for
      `rg-all-clear-demo` returned `404 ResourceGroupNotFound` after cleanup, so
      there is currently **no live ACS resource to inspect** from Phase 1.
- [ ] T007c [US3] Purchase a real ACS phone number for **this deployment
      only**: use `az communication phonenumbers` (requires `az login` —
      device-code interactively, or reuse the `azd auth token` bearer against
      the ACS resource's own control-plane API if `az login` isn't available
      non-interactively) to search available toll-free/geographic numbers in
      a supported country/region and purchase one. Record the cost tier
      (numbers carry a monthly fee + per-minute charges).
      Evidence (2026-09-20 follow-up): `az account show` failed with
      `Please run 'az login' to setup account.` `az login --use-device-code`
      emitted a browser challenge (`https://login.microsoft.com/device`, code
      `AAXR2VESK`) and cannot complete without a human. Fallback attempt
      `azd auth token --scope https://communication.azure.com//.default`
      returned an empty token, so ACS control-plane REST was not available as a
      non-interactive substitute. **No number purchased; no billable phone
      number charges incurred.**
- [ ] T007d [US3] Update the `azd` environment: `azd env set MOCK_MODE false`,
      set the bicep `acsPhoneNumber` param to the purchased E.164 number, then
      `azd provision` (or `azd up`) again so the backend Container App picks
      up `AZURE_ACS_ENDPOINT`, `AZURE_ACS_CONNECTION_STRING`, and
      `ACS_PHONE_NUMBER` for real (per `backend/app/core/config.py` — these
      three plus `MOCK_MODE=false` are what flips `get_phone_service()` from
      `MockPhoneService` to the real `AzurePhoneService`).
      Note: flipping `MOCK_MODE=false` also affects Azure OpenAI/other
      integrations, not just phone — confirm nothing else in the deployment
      requires mock-only credentials before flipping it.
      Evidence (2026-09-20 follow-up): Blocked pending both a successful live
      deployment and a purchased ACS number. Verified the app wiring: in
      `backend/app/core/dependencies.py`, `get_phone_service()` uses
      `MockPhoneService` when `settings.use_mock_services` is true and
      `AzurePhoneService` otherwise; in `backend/app/core/config.py`,
      `use_mock_services` remains true whenever `mock_mode` is true, and
      `phone_enabled` auto-disables when `AZURE_ACS_ENDPOINT` is empty outside
      mock mode.
- [ ] T007e [US3] Verify the Event Grid `IncomingCall` subscription
      (`acsIncomingCallSubscription` in `infra/main.bicep`, only created when
      `!mockMode`) is wired to the backend's phone webhook.
      Evidence (2026-09-20 follow-up): Blocked. No current non-mock deployment
      exists, and the earlier failed provision showed this exact resource path
      (`acsIncomingCallSubscription`) is presently a deployment risk.
- [ ] T007f [US3] Place a real test call to the purchased number and confirm
      it reaches the backend's Call Automation webhook and a transcript
      appears on `/phone`.
      Evidence (2026-09-20 follow-up): Blocked. No purchased number, no live
      non-mock deployment, and no Event Grid subscription to receive
      `IncomingCall`.
- [ ] T007g [US3] Document the purchased number, its monthly cost, and a
      **teardown reminder** (release the number via `az communication
      phonenumbers release` when the demo/test is done, per the "must never
      reuse" / cleanup-conscious repo convention) in
      `.squad/identity/live-deploy.md`.
      Evidence (2026-09-20 follow-up): Updated `.squad/identity/live-deploy.md`
      with the Phase 1b blocker state, explicit note that no number was
      purchased, and the future release reminder command if a number is later
      acquired.

**Checkpoint**: A real phone call can reach the deployed app end-to-end, or
the specific blocker (e.g. no `az login`, no number inventory in region) is
clearly documented.

---

## Phase 2: Live eval suites (User Story 1) — owner: Forge, depends on Phase 1's URLs

- [ ] T011 [US1] Run `evals/quality/quality_eval.py` against the live backend URL; confirm Relevance/Coherence/Fluency clear threshold (≥3); upload to Foundry Evaluations tab if a project endpoint exists, else note fallback
- [ ] T012 [US1] Run `evals/red-team/red_team_scan.py` against the live backend URL; confirm ASR matches the 0.0% baseline in `evals/red-team/RESULTS.md`; upload to Foundry Red teaming tab if available
- [ ] T013 [US1] Run `evals/glass-box-audit/glass_box_eval.py` against the live deployment with Foundry upload (not `--skip-upload`) if `AZURE_AI_PROJECT_ENDPOINT` is available; otherwise re-confirm the local dry-run result from T004 and note why live upload wasn't possible

**Checkpoint**: All 3 Foundry eval suites have a recorded pass/fail result,
live or local-fallback (SC-004).

---

## Phase 3: Regression / QA sweep (User Story 2) — owner: Beast, parallel with Phase 1

- [x] T014 [US2] [P] Independently re-run backend pytest + frontend build as a second confirmation (catches any environment-specific flakiness)
- [x] T015 [US2] [P] Load `/`, `/phone`, `/?page=audit`, `/?page=clone` (local dev servers and/or the live Azure URLs once available) and confirm no console errors and expected content renders
- [x] T016 [US2] No defects found in T014/T015, so no fix/triage branch was required (FR-006)

**Beast's findings:** `cd backend && PYTHONPATH=. python -m pytest tests/ -q` re-confirmed the exact baseline at **347 passed**, 0 failed, 3 pre-existing warnings; `cd frontend && npm run build` stayed clean with only the pre-existing Tailwind gradient-syntax warnings. Playwright QA sweep against the local dev servers loaded `/`, `/phone`, `/?page=audit`, and `/?page=clone` with **0 console errors**, **0 page errors**, and **0 request failures**; screenshots saved to `/tmp/beast-screenshots/home.png`, `/tmp/beast-screenshots/phone.png`, `/tmp/beast-screenshots/audit.png`, and `/tmp/beast-screenshots/clone.png`. Verified `/` still has no capstone button, no live-calls button/toggle, and no overlapping header controls; `/phone` renders full-screen with generic **Caller line** language and no phone number displayed; `/?page=audit` renders its pipeline map, black-box/glass-box toggle, and findings view; `/?page=clone` renders meaningful clone/setup guidance.

**Checkpoint**: No regressions found, or every found regression is either
fixed-and-verified or explicitly logged with a recommendation.

---

## Phase 4: Readiness verdict (owner: Bishop, after Phases 1–3 complete)

- [ ] T017 Synthesize all results (T001–T016) into a single go/no-go verdict: ready to merge `020-glass-box-audit` to `main`, or not yet (with the specific blocking reasons)
- [ ] T018 Record the verdict at the bottom of this file under "## Final Verdict"

---

## Dependencies & Execution Order

- Phase 0 is complete and gates nothing further.
- Phase 1 (Kitty) and Phase 3 (Beast) run in parallel — no shared dependency.
- Phase 2 (Forge) depends on Phase 1's URLs (T009) before it can run live;
  it may start its local-only prep work in parallel but cannot complete T011–T013
  until Phase 1 finishes.
- Phase 4 (Bishop) depends on Phases 1–3 all reaching a checkpoint.

## Final Verdict

*(to be filled in after Phase 4 — do not recommend merging to `main` before
this section is completed)*
