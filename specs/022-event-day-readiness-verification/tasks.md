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
- [ ] T008 [US1] Run `azd up --no-prompt`; capture full output; on failure, diagnose + one retry, then stop and report if still failing (per spec Edge Cases)
- [ ] T009 [US1] Record `AZURE_CONTAINERAPP_URL`, `AZURE_FRONTEND_URL`, and `AZURE_AI_PROJECT_ENDPOINT` (if provisioned) to `.squad/identity/live-deploy.md`
- [ ] T010 [US1] Verify live: `/api/health` (backend), `/`, `/?page=audit`, `/phone` (frontend) all resolve healthy/200

**Checkpoint**: Live deployment either verified working, or a single clearly
diagnosed blocking failure is documented — not left ambiguous (SC-003).

---

## Phase 2: Live eval suites (User Story 1) — owner: Forge, depends on Phase 1's URLs

- [ ] T011 [US1] Run `evals/quality/quality_eval.py` against the live backend URL; confirm Relevance/Coherence/Fluency clear threshold (≥3); upload to Foundry Evaluations tab if a project endpoint exists, else note fallback
- [ ] T012 [US1] Run `evals/red-team/red_team_scan.py` against the live backend URL; confirm ASR matches the 0.0% baseline in `evals/red-team/RESULTS.md`; upload to Foundry Red teaming tab if available
- [ ] T013 [US1] Run `evals/glass-box-audit/glass_box_eval.py` against the live deployment with Foundry upload (not `--skip-upload`) if `AZURE_AI_PROJECT_ENDPOINT` is available; otherwise re-confirm the local dry-run result from T004 and note why live upload wasn't possible

**Checkpoint**: All 3 Foundry eval suites have a recorded pass/fail result,
live or local-fallback (SC-004).

---

## Phase 3: Regression / QA sweep (User Story 2) — owner: Beast, parallel with Phase 1

- [ ] T014 [US2] [P] Independently re-run backend pytest + frontend build as a second confirmation (catches any environment-specific flakiness)
- [ ] T015 [US2] [P] Load `/`, `/phone`, `/?page=audit`, `/?page=clone` (local dev servers and/or the live Azure URLs once available) and confirm no console errors and expected content renders
- [ ] T016 [US2] If any defect is found in T014/T015, triage: fix surgically + re-verify, or log as a known issue with a merge recommendation (FR-006)

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
