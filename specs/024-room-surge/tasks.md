# Tasks: Room Surge recovery

**Branch**: `event/arlington-2026-11-18` | **Revision**: R3, 2026-11-17 10:15 ET
**Deadline**: **2026-11-17 13:00 Eastern** | **Progress**: `███░░░░░░` **3/9 gates**
**Sources**: [spec](spec.md), [plan/evidence/gates](plan.md), user live-test
authorization; patch `e1eca20` on `7bed125`.

✅ means observed completion, not a task merely specified. 🛑 means STOP until
the prerequisite is evidenced. This pass edits documentation only; subsequent
implementation/deployment belongs to the parent/assigned operator. Preserve
zero-LLM routing, three action tools, PII/audit/SEV1/statutory escalation and
every operational signal/report.

## Phase 0 — Applied artifacts and observed baseline (retain completion)

- [x] **T001** `backend\app\services\surge_room.py` + tally tests delivered.
- [x] **T002** `backend\app\api\surge.py`, settings/dependency wiring delivered.
- [x] **T003** `backend\tests\test_surge_api.py` delivered **and run**.
- [x] **T004** `frontend\src\App.tsx`, `src\allclear\surge\*`, QR/client/tests delivered.
- [x] **T005** `backend\scripts\surge_rehearsal.py` delivered; historical stand-in
  run is **not** live acceptance or verifier correctness evidence.
- [x] **T010** Focused backend verification: **15 passed in 1.83s**.
- [x] **T011** Full backend with `MOCK_MODE=true`: **364 passed in 8.22s**.
- [x] **T012** Surge Vitest **5 passed** and frontend production build passed;
  QR `act` / existing Browserslist/gradient warnings recorded.
- [x] **T013a** Actual local Chromium flow: `/report?card=A` at 390×844 → joined
  receipt; `/surge` updated 1 signal / 1 incident; local QR and six card PNGs.
  This does not certify accessibility, projection, or real phones.
- [x] **T013b** Real mock HTTP rehearsal, 40 workers: 45 requests, 43 signals →
  43 incidents; A–D 10 distinct each, E=3, R=2 blocked, failed=0; median
  0.13s/p95 0.22s. SC-001 **FAIL** as expected for broad bag-of-words paraphrases;
  SC-002 **PASS** locally, not live.
- [x] **T013c** Local reset verified closed/signals=0/incidents=0; local servers
  stopped; incidents/reports/audit were **not** deleted.
- [x] **T006** Refresh the nine feature docs for today's deadline, evidence and
  full recovery loop; design Constitution checks pass (G0/G1).
- [ ] **T007** Parent mechanically reviews links/status/claims, runs
  `.specify\scripts\powershell\update-agent-context.ps1 -AgentType copilot`
  with `SPECIFY_FEATURE=024-room-surge`, and **commits/pushes this plan FIRST**
  on the existing branch before implementation/deployment execution.
  **Depends: T006**. No setup-plan rerun/branch checkout. Record published SHA.
  Update 10:23 ET: agent-context updater succeeded; generated root commands/
  paths corrected by parent. Commit/push publication remains pending.
- [ ] **T008** Parent reviews/checkpoints already generated
  `frontend\package-lock.json` alignment for `qrcode` and `@types/qrcode`.
  **Depends: T012**. Bishop does not edit this file; required for Docker `npm ci`.

## Phase 1 — Approved subscription, separate audience resource plan (G2)

- [x] **T016a** User selected **MCAPS-2026-segayle**
  (`9f8986ed-ceb2-414d-8fcb-46d5cfc70618`) for today's **separate audience app**.
  Corporate-tenant TAP/membership repair is deferred until today's demo works.
- [x] **T016b** At 10:15 ET user explicitly approved NEW separate audience
  resources and NEW app-scoped secrets, including coach key: “yes create away.
  the goal is to get this complete.” No more elicitation for ordinary isolated
  creation within approved subscription. No existing-secret change/rotation,
  private redteam reuse or deployment before technical handoff.
- [x] **T016c** Explicit-subscription CLI confirms selected subscription Enabled,
  actual tenant **`16b3c013-d300-468d-ac64-7eda0820b6d3`**. Wrong-context CNE/MCP
  failures are not evidence MCAPS 2026 is inaccessible. Exact CLI inventory
  and deployed target readiness remain T016/T020b, not completed.
- [ ] **T016** 🛑 Kitty completes read-only approved-subscription inventory,
  identifying separate audience resources/names/FQDN, eligible dependencies and
  permissions in local ignored [deployment plan](..\..\.azure\deployment-plan.md).
  Historical [spec 022](..\022-event-day-readiness-verification\tasks.md) target
  is reference only; never reuse `ca-allclear-redteam-20261001` or its secrets.
  Parent mirrors non-secret decisions into `research.md`. **Depends: T016a**.
- [ ] **T017** Review/validate concrete separate audience resource plan and
  target-specific azd/deployment mapping. If audience apps exist, capture
  versions/traffic/config; if new, validate Bicep/what-if before creation.
  Plan frontend external ingress+`BACKEND_URL`, backend 1/1 single process and
  required live dependencies; no blind provision or existing-secret changes.
  **Depends: T007, T016, T016b**.
- [ ] **T018** Establish key presence/secretRef mapping **status only**, private coach
  delivery, live `mock_mode=false`, real chat/semantic embedding deployments,
  content-safety/knowledge/store/audit access, capacity/quota and public
  `/api/health` + `/api/surge/state`.   **Depends: T017**. For new resources, approve configuration/verification plan
  now and prove runtime checks in T020b; do not require nonexistent endpoints
  before approved creation. Key state is UNKNOWN; creating a NEW audience-app
  coach key is explicitly approved by T016b. Do not print key or secret list.
  Never change existing secrets; technical validation remains required (G2).

## Phase 2 — Repair verification, not the architecture (G3)

May proceed locally while the operator resolves G2. No live traffic yet.
**Owner: Forge**, limited to known verifier false passes, protected `--key-env`
intake and small password operator-entry UI/tests. No new packages, card
grouping, threshold or mock changes. Kitty deployment/exposure waits for G3/G4.

- [x] **T019a** Forge added **11 verifier regression tests** in
  `backend\tests\test_surge_rehearsal.py` for the known false-pass/error cases;
  focused verifier+tally+API run **26 passed**. Local implementation occurred
  before publication; parent checkpoint must precede deployment.
- [x] **T019b** Repaired `backend\scripts\surge_rehearsal.py` against T019a: all
  45 requests accounted for, A–D 10 accepted incident-bearing receipts each,
  union 4–6 and pairwise-disjoint card sets; three distinct E incidents outside
  A–D; zero request/network/server failures. Preserve fixture texts/order,
  40-worker setting and HTTP-200 latency population (including blocks), existing
  percentile calculation and flag compatibility. Explicit nonzero failures;
  never count zero incidents as semantic success. **Depends: T019a**.
- [x] **T019c** Added/tested protected `--key-env <environment-variable-name>`
  intake, default `SURGE_COACH_KEY`, in the same script;
  safe summaries contain counts/incident IDs/latencies/revisions only, never raw
  response bodies, report text, device IDs, coach-key URLs or secrets. Do not
  change Azure secrets. R probes grade actual safe authority, not universal
  blocking. **Depends: T019a**.
- [x] **T019d** Focused verifier+tally+API verification **26 passed**;
  parent full backend rerun **375 passed in 8.15s**. Earlier actual mock HTTP
  rehearsal remains baseline, not a post-fix/live claim.
  **Depends: T019b, T019c**.
- [x] **T019e** Forge added masked **Operator controls → Coach key → Set key**
  in `frontend\src\allclear\surge\SurgeBoard.tsx`, retaining private memory/
  session and existing control headers. **6 UI tests**, typecheck/build pass.
  Legacy key-query support remains compatibility only, forbidden for live
  credential delivery. Real deployed authorized/unauthorized control remains G5.
  Actual keyed mock browser integration PASS: missing key 403; input=password;
  Set key →Open; 390×844 report A →board polls 1 signal; QR PNG; observed
  no key URL or `X-Surge-Key` on public calls. Reset closed/zero and helpers
  stopped. This is not live semantic acceptance.

## Phase 3 — Release candidate verification (G4)

- [x] **T025** Parent ran full backend mock suite after verifier fixes using
  [verification commands](plan.md#verification-matrix). Preserve authority,
  PII, audit and escalation tests. Record candidate/test evidence in `plan.md`.
  **375 passed in 8.15s**. **Depends: T019d**. Earlier T010/T011 remain completed baseline facts.
- [ ] **T026** In `frontend`, run `npm ci --ignore-scripts`, Surge Vitest,
  `npm run typecheck`, `npm run build`; check every exit code. Record lock/build
  evidence and parent checkpoint.   **Depends: T008, T019d, T019e**. Earlier T012 remains
  completed; no install churn beyond required lock alignment.
  Update: **6 UI tests /typecheck /build PASS**; parent confirms locked install/
  lock checkpoint before marking the aggregate task complete.
- [ ] **T014** Capture/check 1920×1080 `/surge`, 390×844 `/report`, print preview
  `/surge/cards`; certify projector/back-of-room counters/tiles/readability.
  **Depends: T026**. Existing route smoke is insufficient.
- [ ] **T015** Check labels, keyboard/focus, contrast, sending/error/receipt
  announcements and real-phone keyboard dictation on `/report`; address only
  demonstrated blockers with focused test/build rerun. **Depends: T026**.

## Phase 4 — Separate audience release (G5)

- [x] **T020c** Image-build engine blocker resolved at 10:20 ET: parent verified
  Docker daemon **29.9.3**, **linux**, using `docker version` + `docker info`
  after starting Desktop PID 30064. azd 1.37.3 installed; retain existing
  `remoteBuild:false` local build path. No new packages or build-default change.
  Engine readiness is independent of T017 and does not certify image build,
  application tests or deployment.
- [ ] **T020a** 🛑 Capture healthy prior audience backend/frontend revision IDs, image
  digests/traffic/configuration metadata and rollback sequence; review tested
  candidate diff, exact environment, frontend proxy and key mapping preservation.
  Preview writes within T016b approval; validate Bicep/what-if and complete
  azure-validate/preflight/deploy handoff before execution. Record in `research.md`.   For first release record no prior revision and verified fallback instead of
  fictitious rollback. **Depends: T018, T025, T026**.
- [ ] **T020b** Operator creates only approved separate audience resources,
  then deploys tested images using target-specific mapping. Prefer application-
  only updates if audience apps already exist; no blind `azd up`/provision:
  infra lacks coach-key mapping and may erase manual configuration. Create
  a NEW app-scoped coach key under T016b approval; preserve existing secrets.
  Verify expected image/revision/traffic, healthy frontend/backend,
  direct SPA routes and frontend `/api` proxy, live models, stable single
  backend process/replica, unauthenticated control=403 and private authorized
  control. Record G5 in `plan.md`. **Depends: T020a, T020c**. STOP/rollback on mismatch.

## Phase 5 — Authorized live rehearsal, diagnose, rerun (G6)

- [ ] **T021** 🛑 User's follow-up **authorizes live testing**; no further generic
  "go" is awaited. Target/access/key/configuration G2 and deployed candidate G5
  must pass first. Run repaired script against public frontend, 40 workers,
  45-request fixture with private environment credential. Record sanitized
  time/commit/revisions/replica/card sets/coverage/errors/blocked/escalated/failed,
  median/p95 and SC-001/002 in `research.md`. **Depends: T019d, T020b**.
- [ ] **T022** If T021 fails, classify failure: transport/auth/proxy, quota/429/
  503, category drift, semantic embedding/similarity, retained-incident reuse,
  or serialized dedup-lock live latency. Measure rather than assume lock
  bottleneck. Author one evidence-backed fix/test task at a time; update spec,
  rerun affected tests/preview/deploy and identical T021. No blanket threshold
  lowering/card grouping/safety weakening. If T021 passes, mark this task
  not-needed with evidence. **Depends: T021 attempted**.
- [ ] **T023** Confirm capacity/headroom and zero request/server errors in live
  evidence; every A–D report covered, 4–6 separated incidents, E separation,
  p95 <8s, no rule bypass. Parent records G6/checkpoint only on passing evidence.
  **Depends: T021 passing, T022 disposition**.

## Phase 6 — Human checks, cleanup, freeze (G7/G8)

- [ ] **T024** Five or more real phones on cellular scan correct production
  cards, submit/receive receipts and see board updates; no PII entered. Open
  only for the test window; confirm true live mode and safe controls.
  **Depends: T023**.
- [ ] **T030** Confirm public join URL/short link and print A–D plus E/R cards
  from correct origin; scan actual printouts. No key-bearing printed/shared URL.
  **Depends: T024**.
- [ ] **T031** Presenter/operator run [seven-minute show](run-of-show.md),
  review a safe decision receipt/citations, practice fallback to a working
  `/?demo=loaded` replay or verified sanitized capture, and disclose any seeds.
  Never assume outbound/multilingual backup works. **Depends: T014, T015, T030**.
- [ ] **T032** Close intake; wait for in-flight work to settle; reset tally,
  close and read state repeatedly: `open=false`, all counters=0, tiles empty,
  stable replica. Verify operational incidents/reports/audit remain; do not
  purge stores. Record cleanup evidence. **Depends: T031**.
- [ ] **T033** By 12:30 ET parent freezes exact tested/deployed checkpoint,
  records GO/NO-GO and rollback/fallback, updates all affected docs/statuses and
  checkpoints. At 12:45 repeat safe closed-board, target version, QR, projector
  and fallback checks. **Depends: T007, T023, T032**. Unmet gate → verified
  fallback at **13:00**, not an unverified late live change.

## Checkpoint discipline

Every attempt updates its task, sanitized result and commit/revision reference;
failure stays unchecked with blocker and next action. Reopen affected **release**
gates after a fix, but never erase completed baseline observations. Five-to-fifteen
minutes is an existing-app update estimate only after prerequisites; no
reprovisioning or resource-readiness promise is made.
