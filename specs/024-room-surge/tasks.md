# Tasks: Room Surge recovery

**Branch**: `event/arlington-2026-11-18` | **Revision**: R9, 2026-11-17 15:00 ET
**Original deadline**: **2026-11-17 13:00 Eastern** elapsed | **Progress**: `████░░░░░` **4/9 baseline primary-live gates**; hybrid release/acceptance pending
**Sources**: [spec](spec.md), [plan/evidence/gates](plan.md), user live-test
authorization; patch `e1eca20` on `7bed125`.

✅ means observed completion, not a task merely specified. 🛑 means STOP until
the prerequisite is evidenced. This pass edits documentation only; subsequent
implementation/deployment belongs to the parent/assigned operator. Preserve
zero-LLM routing, three action tools, PII/audit/SEV1/statutory escalation and
every operational signal/report.

**FINAL EVENT BOUNDARY**: primary live deployment/acceptance **BLOCKED / NO-GO**.
12:10 cutoff passed; no further speculative infra before showcase. Corrective
network succeeded but private backend terminal Failed; use T045–T049's bounded
frontend-only authorized fallback. Live tasks remain unchecked, not “passed by mock.”
**12:42 update**: fallback deployment/browser/40-report mock flow now **PASS**;
T047–T049 complete. Physical cellular scan and primary live acceptance remain
unchecked. Final protected CLOSED/zero cleanup confirmed.

## R9 current boundary — observed FINAL NO-GO; no more paid load

- [x] **T066** Integration reviewed: async Azure credential, embedding before
  lock, **atomic decision + persistence retained**, reset generation guards.
  Late success remains domain-persisted/accepted with optional
  **`room_counted=false`** and explicit reset notice; late blocks/errors cannot
  pollute new room. Frontend receipt field backwards compatible.
  Built Linux backend
  **sha256:318a475c91f3e21bb7b605052eb586a2a8c01192076a5dc71575961c0d36795a**
  passed **all390 tests in one run**, read-only README/docs/frontend-source
  fixtures. Source frontend **14 tests / Node22 build PASS**.
  Frontend **sha256:b6711361acd28fe5ce6121312bbe871b8d4a2f49ad6531efb685c6f354ecf606**;
  bundle **index-CXbXlhpf.js**, hash
  **46F1130F6BF45E9F70B4809149F51169B1CDDD100ED8B6263679CF5A63927412**.
  This is source/image proof, not semantic acceptance. **Depends: T062**.
- [x] **T067** Actual **--hybridr9 Healthy/one replica**, backend digest above
  verified; health **false/memory**, keyless controls **403**. R9 frontend
  **Healthy Single/latest**, actual hosted **index-CXbXlhpf.js** and hash above
  exact match; public health **mock=true**. Initial transient old HTML preceded
  readiness+hosted-hash confirmation. Candidate finally reset **CLOSED/zero**;
  no cutover, public mock named **100% untouched**. This does not certify
  overlapping reset behavior or demo acceptance. **Depends: T066**.
- [x] **T068** Record actual untouched45/concurrency40 **FAILED**:
  **45/45 HTTP200**, **43 accepted signals→36 incidents**, **2 safety blocks**,
  **0 errors/failed/escalated**, wall **19.7s**. A/B/C/D distinct
  **10/7/6/10 =33** disjoint **FAIL4–6**; E3distinct/disjoint **PASS**.
  Complete/error-free accounting **PASS**. Full45 median **16.32s**,
  p95 **17.97s FAIL<8s**. **FINAL NO-GO; no more paid load**.
  Semantic calibration/design **and latency need actual solutions**; async/reset
  fixes are not full demo acceptance. Durable blocked, no support case or
  physical-phone confirmation. T054/T055/T065 remain open. **Depends: T067**.

**Historical R8**: --hybridr8 Healthy/false-memory/1replica/zero normal traffic,
but actual45 fixture failed two client timeouts, A–D31 grouping and latency;
late completions then polluted candidate reset. At14:24 ET all45 settled;
second reset of only quiescent --hybridr8 restored CLOSED/zero. Stable public
mock read-only CLOSED/zero, not reset. Public mock100%/frontendf688/index-CNv7Cu5d.js unchanged; source
sync-I/O/epoch fixes underway. Earlier mock/R7 cleanup is historical evidence.

## R8 failure ledger and corrective gate — source now tested, runtime pending

- [x] **T060** Reviewed source Search SDK `k` fix, knowledge/sitrep outside
  atomic dedup section, privacy-safe phase instrumentation. **Linux380 backend/
  runtime checks PASS +4 repo-doc checks separately PASS** with read-only
  fixtures; Forge source384PASS. **36 actual Azure Search rows**, all
  **`vector_query=True` / results3**, verify live knowledge SDK fix, not
  semantic/performance or future-fix acceptance.
- [x] **T061** Actual R8 image
  **sha256:0c755cd5a5dbb15ac5d7f1e93c2f9b94d10c0a1dc47e4590c64773f96afe7d7b**,
  --hybridr8 Healthy/1replica/false-memory/zero normal traffic. Untouched45/
  concurrency40 **FAILED**: HTTP41accepted→34incidents +2blocks +2client
  timeouts(B,C); A–D31/E3disjoint, wall60.2s/median16.46s/p9518.22s from43/45
  HTTPsuccesses, **invalid complete acceptance**. Logs prove43pipeline+2block
  completion, timed-out2 around82s; test still fails. This task records attempt,
  not passing T054/T055.
- [x] **T062** R9 integration/source correction reviewed and built Linux image
  passed all390 tests in one run; async credential, pre-lock embedding and
  reset generation guards, with atomic decision+persistence retained.
  Initial R8 resetCLOSED/zero was
  polluted to **CLOSED/2signals/2incidents/devices0** by late completions.
  Guard tally generations without canceling/dropping domain reports/audit.
  No threshold/taxonomy/fixture/card-routing changes. **Runtime/performance/
  semantic acceptance remains pending**, not implied by source completion.
  **Depends: T061**.
- [x] **T063** At **14:24 ET**, all45 requests had settled; second reset of
  **only quiescent --hybridr8 tally** restored **CLOSED/zero**, never deleting
  domain records. Stable public mock read-only verified **CLOSED/zero**, **not
  reset**. This cleanup does not prove epoch isolation or live acceptance.
  **Depends: T061**; source epoch guards now tested in T062, runtime proof pending.
- [ ] **T064** Diagnose semantic evidence: OPENmostly0.67–0.82 vs observed
  ATTACH≥0.8308, categories/similarity and phase timing. Scores are not a new
  configured threshold or proof of resolution. Correct/retest one evidenced
  cause; no weaker gates. **Depends: T061**.
- [ ] **T065** Verify corrected source/tests, release guarded candidate and
  rerun untouched45/concurrency40 with zero client/network/server errors,
  complete coverage/disjoint grouping and unchanged full-response latency
  population. Timeouts fail even if server eventually completes. Promote only
  after full pass and stable cleanup; old mock remains100%. **Depends: T062,
  T063, T064**. R9 actual run recorded in T068 **failed** grouping/latency;
  **ON HOLD: no more paid load**. Needs actual semantic/design and latency
  solutions, not another blind run or weaker acceptance.

## R7 — approved parallel recovery; deployed hybrid canary FAILED acceptance

Historical R7 attempt follows; R8 attempt/reset defect above is newer.

- [x] **T050** User approved parallel temporary-memory demo and durable recovery:
  “can you do both in parallel.” Document default-false
  `SURGE_DEMO_MEMORY_STORAGE`, explicit restart-loss tradeoff and no durable GO.
- [x] **T051** Implemented explicit opt-in: with MOCK_MODE=false, cached memory
  incident **and session** stores while Azure chat/embeddings/knowledge and
  zero-LLM router/PII/safety/escalation/audit calls remain unchanged. Health adds
  independent storage_mode memory/cosmos. UI health poll10s; false/memory label
  **LIVE AZURE AI - TEMPORARY DEMO STORAGE**, own-word instructions/no mock samples.
  Reports/session/audit records lost on restart; reset still tally-only.
  **Depends: T050**.
- [x] **T052** Implementation tests only: **382 backend /14 UI PASS**, real
  Linux backend-image **33 focused PASS**, local startup **false/memory PASS**.
  No deployed hybrid/model-call/semantic/load success inferred. **Depends: T051**.
- [x] **T053** App-only candidate **`--hybrid1340`** on original public backend
  deployed **Healthy/Running/1replica**, actual health **false/memory**, keyless
  control403. Mode-aware frontend **`--hybrid1340`** Healthy, served bundle
  **`index-CNv7Cu5d.js`**. This records deployment/runtime evidence, not full UI/
  audit/semantic certification. Stable backend **`--mockfallback`100%**;
  no cutover or existing-secret/private-redteam change. **Depends: T052**.
- [ ] **T054** Run **untouched45-request fixture /concurrency40** on hybrid
  canary: all original coverage, disjoint A–D/E grouping, actual safe R outcomes,
  zero HTTP/network/server errors and full-denominator p95<8s. Record actual
  counts/latency/model/storage/revision evidence only after observed.
  Original45/43 failures and mock40→4 remain distinct. **Depends: T053**.
  **ACTUAL ATTEMPT FAILED**:43accepted signals→34incidents,2safety blocks,
 0errors/failed/rate limits, complete accounting PASS. A10/B7/C6/D8 distinct
  IDs =31disjoint A–D incidents: **SC-001 FAIL** (needs4–6); E3distinct PASS.
  Median15.67s/p9516.81s/wall17.7s: **SC-002 FAIL**. Candidate finally reset
  CLOSED/zero. Task remains unchecked until unchanged full retest passes.
- [ ] **T055** Promote only after T054 complete pass and protected
  close/drain/reset evidence; retain temporary-storage/restart-loss disclosure.
  Otherwise keep original mock100%. Physical cellular/human acceptance remains
  separate. **Depends: T054 passing**.
- [x] **T056** Kitty prepared durable support packet, **no actual ticket filed**.
  Terminal Container Apps rollout root cause remains unknown; private backend
  not verified ready. Packet preparation is not resolution or service acceptance.
- [ ] **T057** Durable track independently establishes actual case status,
  evidence-backed cause and healthy private app/connectivity/report/persistent
  audit proof before durable GO. Do not equate hybrid memory success with
  Cosmos repair. **Depends: T056**.
- [ ] **T058** Forge diagnoses actual hybrid semantic/performance failure using
  sanitized category/similarity/embedding and measured latency evidence; one
  bounded tested correction at a time. No thresholds/fixture weakening, card
  grouping, safety reduction or assumed lock bottleneck. **Depends: T054 attempted**.
  R8 confirms sync-I/O/event-loop and reset-epoch defects; T062/T064 own current
  correction. Semantic resolution is not established by reviewed lock changes.
- [ ] **T059** Parent retests corrected canary with untouched45/concurrency40,
  records complete outcome/latency/cleanup evidence and promotes only if all
  original gates pass. Until then stable --mockfallback stays100%; current
  source382/UI14/image33 passes do not waive acceptance. **Depends: T058**.

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
- [x] **T007** Parent mechanically reviewed links/status/claims, ran
  `.specify\scripts\powershell\update-agent-context.ps1 -AgentType copilot`
  with `SPECIFY_FEATURE=024-room-surge`, and **commits/pushes this plan FIRST**
  on the existing branch before implementation/deployment execution.
  **Depends: T006**. No setup-plan rerun/branch checkout. Record published SHA.
  Update 10:23 ET: agent-context updater succeeded; generated root commands/
  paths corrected by parent. Published checkpoint **`00141cd`**.
- [x] **T008** Parent reviewed/checkpointed
  `frontend\package-lock.json` alignment for `qrcode` and `@types/qrcode`.
  **Depends: T012**. Bishop does not edit this file; required for Docker `npm ci`.
  Published minimal **88-package Linux lock** in `00141cd`; Node 22.23.5 build passed.

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
- [x] **T016** Kitty completed initial approved-subscription inventory,
  identifying separate audience resources/names/FQDN, eligible dependencies and
  permissions in local ignored [deployment plan](..\..\.azure\deployment-plan.md).
  Historical [spec 022](..\022-event-day-readiness-verification\tasks.md) target
  is reference only; never reuse `ca-allclear-redteam-20261001` or its secrets.
  Parent mirrors non-secret decisions into `research.md`. **Depends: T016a**.
  Audience **`rg-allclear-surge-20261117`** deployed; corrective target/new-app
  usable URL remains unverified.
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
- [x] **T026** Frontend locked production build, Surge Vitest,
  `npm run typecheck`, `npm run build`; check every exit code. Record lock/build
  evidence and parent checkpoint.   **Depends: T008, T019d, T019e**. Earlier T012 remains
  completed; no install churn beyond required lock alignment.
  **6 UI tests /typecheck /Node 22.23.5 build PASS**; minimal Linux lock and
  immutable images built/pushed/deployed from **`00141cd`**.
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
  **PARTIAL**: initial 19-resource preview passed; both immutable images deployed;
  models GPT-5.1 cap150/embedding cap50 Succeeded; backend MI OpenAI User,
  one replica, frontend health mock=false, key configured/keyless403 confirmed.
  Report503 means G5 NOT complete. Preserve initial apps during correction.

## Phase 5 — Authorized live rehearsal, diagnose, rerun (G6)

- [ ] **T021** 🛑 User's follow-up **authorizes live testing**; no further generic
  "go" is awaited. Target/access/key/configuration G2 and deployed candidate G5
  must pass first. Run repaired script against public frontend, 40 workers,
  45-request fixture with private environment credential. Record sanitized
  time/commit/revisions/replica/card sets/coverage/errors/blocked/escalated/failed,
  median/p95 and SC-001/002 in `research.md`. **Depends: T019d, T020b**.
  **ATTEMPTED / FAILED**: 45 attempts, 0 accepted signals/0 incidents,
  2 safety blocks/43 failed; single report503. p95 **2.75s from only two HTTP
  successes is invalid acceptance evidence**. Reset confirmed CLOSED/zero.
- [ ] **T022** If T021 fails, classify failure: transport/auth/proxy, quota/429/
  503, category drift, semantic embedding/similarity, retained-incident reuse,
  or serialized dedup-lock live latency. Measure rather than assume lock
  bottleneck. Author one evidence-backed fix/test task at a time; update spec,
  rerun affected tests/preview/deploy and identical T021. No blanket threshold
  lowering/card grouping/safety weakening. If T021 passes, mark this task
  not-needed with evidence. **Depends: T021 attempted**.
  **ROOT CAUSE CONFIRMED** in Activity Log: inherited `MCAPSGovDeployPolicies`,
  `CosmosDB_PublicNetwork_Modify` + `CosmosDB_LocalAuth_Modify`; public/local
  auth Disabled, no Cosmos PE, initial ACA has no VNet. Follow T040–T044;
  no policy bypass or app/threshold changes.
- [ ] **T023** Confirm capacity/headroom and zero request/server errors in live
  evidence; every A–D report covered, 4–6 separated incidents, E separation,
  p95 <8s, no rule bypass. Parent records G6/checkpoint only on passing evidence.
  **Depends: T021 passing, T022 disposition**.

## Phase 5b — Bounded policy-compliant recovery (G2/G5/G6)

- [x] **T039** Existing Search seed script completed **12/12 All Clear articles**,
  **1536-dimensional vectors**, using scoped operator OpenAI User on the new
  audience account. No repository secrets; runtime Search consumption still
  needs proof in successful report/knowledge flow.
- [ ] **T040** Kitty prepares corrective network/identity delta in owned
  deployment artifacts: NEW VNet-integrated ACA environment, Cosmos private
  endpoint/private DNS, backend MI **SQL Built-in Data Contributor**, NEW
  backend/frontend apps. Reuse audience models/Cosmos/Search/ACR and tested
  immutable images. Parent validates/previews before any execution.
  **Depends: T022 diagnosis**. Preserve initial apps and private redteam unchanged.
  Preparation/network retry executed; approved provider feature registration
  allowed network Succeeded. App completion remains failed; no further retry now.
- [ ] **T041** After parent validation, deploy only isolated corrective
  network/identity resources and new apps; verify private Cosmos DNS/resolution,
  private connectivity and MI data-plane read/write/audit access; public and
  local-auth restrictions stay Disabled. Record revisions/traffic and
  first-release fallback. **Depends: T040 validated**.
  **PARTIAL / TERMINAL APP FAILURE**: Cosmos SQL PE Approved; DNS10.77.2.4/.5;
  UAI/bootstrap/AcrPull and DB-scoped data roles verified. At **12:17:52 ET**
  `allclear-surge-live-backend` Failed (`ContainerAppOperationError`, empty
  provider error), no revision/FQDN/log stream; private frontend never created.
  Correlation **f851acdb-4556-456c-bbd4-71f5c7bd0a1e**. Network success is not
  app success. Further speculative execution stopped before showcase.
- [ ] **T042** Prove new frontend/proxy/new backend live mode, one replica,
  safe coach control, then **one synthetic report →valid receipt +board +
  durable report/incident/audit +knowledge flow**. Health alone is insufficient.
  No usable URL claim until this passes. **Depends: T041**. Close/drain/reset
  tally afterward, preserving operational data.
- [ ] **T043** Rerun unchanged **45-request /40-worker** live fixture against
  the proven NEW audience frontend. Require all coverage/error/separation/
  semantic/latency gates; no selective-success p95. Record safe evidence and
  cleanup; only then close T021/T023 and G5/G6. **Depends: T042**.
- [x] **T044** At **12:10 ET**, choose live only if T043 passes with time for
  human rehearsal/freeze; otherwise rehearse **loaded replay or explicitly
  labeled mock** on a working build. Keep 13:00 stage time. No policy exemption,
  public-Cosmos/local-auth re-enable, unsafe URL or untested live claim.
  **Depends: T040 attempted**; do not wait indefinitely for provisioning.
  Decision boundary is in force: primary NO-GO; disclosed mock fallback and
  replay verified. Final fallback handoff now recorded in T049; primary live
  acceptance remains unchecked.

## Phase 5c — Authorized bounded fallback, not live semantic acceptance

- [x] **T045** Original public audience backend changed only **MOCK_MODE=true**;
  protected key unchanged. **12:20:26** health mock=true and tally CLOSED/zero
  confirmed. No new private URL available; keep public frontend
  `https://allclear-sbuqtpuppifra-frontend.gentlesand-926708e1.eastus2.azurecontainerapps.io`.
- [x] **T046** Browser verified public **`/?demo=loaded` replay**. This is
  replay, **not audience reporting**; do not count it as SC-001/002 or phone proof.
- [x] **T047** Parent shipped **frontend only**: runtime health-driven
  mock notices on report/board/cards, neutral no-AI footer, mock-only A–D
  **Use sample report** prepopulating actual scene wording. Live own-word
  behavior/pipeline unchanged; no card grouping/threshold shortcut.
  **11 focused UI tests PASS** including configured API-origin; Node22
  build/typecheck and new modules/cards/tests strict lint PASS. Existing
  Board/Report HEAD baseline reproduced unchanged: four fast-refresh warnings,
  one unused-disable error. Revision
  **`allclear-sbuqtpuppifra-frontend--mocklabel1236` Healthy/Running /100% traffic**,
  public bundle **`index-DVUyNrL6.js`**, immutable digest
  **`sha256:9a7eb0ed665c595e59c7fb7f13e89554b196a9a9eddc463bc9bc91e48a60cb56`**.
  **Depends: T045**.
- [x] **T048** Independent deployed browser/mock-flow proof PASS: public frontend
  **40 concurrent repeated-wording reports →40 accepted signals /4 disjoint
  incidents /40 devices, A–D 10 each; failures/blocks/rate limits all0**;
  **p95 all40 attempts0.213s, wall0.380s**; keyless control403.
  Two isolated 390×844 Chromium contexts used generic `/report` →A →Use sample
  report →send receipt; board polled **2 signals /1 incident /2 devices**.
  Runtime Mock labels on all3 pages, neutral footer, one board +six printable
  PNG QRs, masked Set key/Open, no key URL/public-call key leak, zero JS errors/
  mobile overflow. Protected final reset **CLOSED/0signals/0incidents**;
  reports/audit not deleted. **Mock flow only, not physical cellular or live
  semantic acceptance. Depends: T047**.
- [x] **T049** Final [five-line decision record](run-of-show.md#five-line-gono-go-record)
  distinguishes **mock PASS** from **live AI/semantic NO-GO**, exact available
  URL/operator/sample steps, closed/zero cleanup, replay and unverified physical
  cellular scan. **Depends: T046, T048**. Parent publishes final checkpoint.

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
  Primary live remains NO-GO. Fallback freeze/decision uses T049 instead of
  pretending T023/T024 passed; preserve these unmet primary completion gates.

## Checkpoint discipline

Every attempt updates its task, sanitized result and commit/revision reference;
failure stays unchecked with blocker and next action. Reopen affected **release**
gates after a fix, but never erase completed baseline observations. Five-to-fifteen
minutes is an existing-app update estimate only after prerequisites; no
reprovisioning or resource-readiness promise is made.
