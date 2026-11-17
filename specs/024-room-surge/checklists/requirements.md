# Requirements and readiness checklist: Room Surge

**Branch**: `event/arlington-2026-11-18` | **Revision**: R9, 2026-11-17 15:00 ET
**Purpose**: Preserve showcase evidence and gate approved post-showcase hybrid/durable recovery
**Source**: [spec](..\spec.md), [plan](..\plan.md), [tasks](..\tasks.md)
**Progress**: `████░░░░░` **4/9 primary-live gates**; checked requirement quality
below does **not** certify unfinished deployment.

**R9 current FINAL NO-GO**: reviewed async Azure credential, embedding
before lock, atomic decision+persistence retained, reset generation guards.
Late success domain-persisted/accepted with optional **`room_counted=false`**
and explicit reset notice; late blocks/errors do not pollute new room.
Frontend receipt field backwards compatible. Immutable Linux backend
**sha256:318a475c91f3e21bb7b605052eb586a2a8c01192076a5dc71575961c0d36795a**
passed **all390 tests in one run** with read-only README/docs/frontend-source
fixtures; source frontend **14 tests / Node22 build PASS**. Built frontend
**sha256:b6711361acd28fe5ce6121312bbe871b8d4a2f49ad6531efb685c6f354ecf606**,
**index-CXbXlhpf.js**, hash
**46F1130F6BF45E9F70B4809149F51169B1CDDD100ED8B6263679CF5A63927412**.
Actual **--hybridr9 Healthy/one replica**, digest verified, health
**false/memory**, keyless controls **403**. Untouched45/concurrency40:
**45/45 HTTP200**, **43 accepted signals→36 incidents**, **2 safety blocks**,
**0 errors/failed/escalated**, wall **19.7s**. A/B/C/D distinct
**10/7/6/10 =33** disjoint **FAIL4–6**; E3distinct/disjoint **PASS**.
Complete/error-free accounting **PASS**; full45 median **16.32s**,
p95 **17.97s FAIL<8s**. Candidate finally reset **CLOSED/zero**, **no cutover**.
Public mock named **100% untouched**; frontend R9 **Healthy Single/latest**,
actual hosted **index-CXbXlhpf.js** and full hash above match; publichealthmock=true.
Initial transient old HTML preceded readiness+hosted-hash confirmation.
**No more paid load.** Semantic calibration/design **and latency need actual
solutions**; async/reset fixes are not full demo acceptance. Durable blocked,
no support case filed or physical-phone confirmation.

**Historical R8 BLOCKED**: --hybridr8 Healthy/1replica/false-memory/zero normal
traffic; actual45/concurrency40:HTTP41accepted→34incidents,2blocks,2timeouts(B,C),
A–D31/E3disjoint. Wall60.2s/median16.46s/p9518.22s on43/45successes **invalid
complete acceptance**. Eventual43pipeline+2blocks logged (timed-out2~82s) still
fails. Initial reset polluted toCLOSED/2signals/2incidents/devices0; **14:24 ET**,
all45 requests settled, second reset of only quiescent **--hybridr8** restored
**CLOSED/zero**, with no domain deletion. Stable public mock read-only verified
**CLOSED/zero**, **not reset**. Sync-I/O/epoch fixes/retest pending. **36 actual
Azure Search rows**, all **`vector_query=True` / results3**, verify live knowledge
SDK fix, not semantic/performance acceptance. Public mock100%/
frontendf688/index-CNv7Cu5d.js unchanged. Linux380runtime+4doc separatelyPASS/
Forge source384PASS is not readiness. Cellular instructions sent, no confirmation.

**R7.1**: Hybrid **--hybrid1340 deployed Healthy/Running/1replica,false-memory,
keyless403**, but actual45/concurrency40 **FAILED**:43accepted→34incidents,
2blocked,0errors/failed/rate limits; A–D31disjoint IDs (10/7/6/8),SC-001 FAIL;
E3distinct/accounting PASS; median15.67s,p9516.81s,wall17.7s,SC-002 FAIL.
Candidate reset CLOSED/zero. **No cutover: --mockfallback100%**; frontend
--hybrid1340 Healthy, served index-CNv7Cu5d.js. Source382/UI14/image33 stay green,
not acceptance. Forge investigates without threshold/fixture weakening.
Durable cause unknown/private backend unready; packet prepared, no actual ticket.

**Historical R6 fallback disposition**: primary live NO-GO; private network/identity succeeded
but corrected backend terminal Failed 12:17:52, no usable private app/frontend.
No more speculative infra before stage. Original backend mock=true/CLOSED/zero
confirmed 12:20:26; replay browser verified, not reporting. Mock disclosure/sample
frontend now Healthy/Running100%traffic at `allclear-sbuqtpuppifra-frontend--mocklabel1236`.
**11 UI tests/Node22 build/typecheck/new-module strict lint PASS**; deployed
browser and 40 repeated-wording mock reports PASS. Primary live remains NO-GO;
physical cellular scan remains unverified.

## Requirement quality / design

- [x] **CHK001** Deadline is 2026-11-17 13:00 Eastern; existing event branch and
  feature ID are distinct; no past freeze or conflicting stage time remains.
- [x] **CHK002** Scope is admission/tally plus existing pages; no card routing,
  new platform or broad refactor.
- [x] **CHK003** QueryAgent, zero-LLM RouterExecutor, three ActionAgent tools,
  PII/audit, SEV1/statutory and mandatory escalation are explicitly preserved.
- [x] **CHK004** Signal/report retention, tally-only reset, in-flight work,
  room-vs-durable magnitude and public-state privacy are specified.
- [x] **CHK005** Mock near-duplicate flow and live semantic acceptance are
  separate; actual 43→43 mock result is not misrepresented.
- [x] **CHK006** SC-001 rejects zero coverage and cross-event merging; SC-002
  keeps fixture/latency denominator and fails on request/server errors.
- [x] **CHK007** Red-card results reflect actual routing; no mandatory live
  poison block or fake refusal.
- [x] **CHK008** API/model/quickstart/research/plan/tasks agree on key control,
  private credential delivery, unknown deployed status, operational blockers,
  tests, rollback, rehearsal and safe freeze.
- [x] **CHK009** Baseline test/build/browser passes remain completed; browser
  smoke is not substituted for accessibility/projection/real-phone acceptance.
- [x] **CHK010** Live test is authorized after target/access/configuration gates;
  NEW audience-app coach-key creation is approved; existing-secret changes and
  private redteam target explicitly excluded.
- [x] **CHK018** Today's separate audience target is in approved MCAPS 2026;
  corporate-tenant auth is deferred. Exact inventory/resource-write scope,
  resource/NEW app-secret creation approved at 10:15 ET. Exact inventory,
  technical validation and candidate image build remain gates; Docker daemon
  29.9.3/linux readiness is verified by version + info at 10:20 ET.

## Execution evidence (must remain open until observed)

- [ ] **CHK011** Parent mechanical review/context update and GitHub publication
  FIRST; aligned npm lock captured (T007/T008); execution waits for published SHA.
  Base code/IaC/Linux lock published as `00141cd`; fallback runtime revision/
  digest recorded in plan; parent final source/docs publication follows.
- [ ] **CHK012** Authorized access, exact audience target/environment, public
  health/proxy, private key presence/control, live services/quota and one backend
  process/replica verified (G2).
- [ ] **CHK013** Hardened verifier has focused false-pass/error/pass tests and
  private environment-key support and masked non-URL coach UI; full release
  tests/typecheck/build pass (G3/G4).
  Verified: 11 new regressions /26 focused, full backend 375 in 8.15s, UI 6,
  typecheck/build PASS. G3/G4 base candidate complete; fallback adds11 focused
  UI/API-origin tests, Node22 build/typecheck/new-module strict lint and actual
  deployed mock browser/concurrency PASS, not live semantic acceptance.
  Actual keyed mock browser also passed operator entry/403, mobile report/
  board/QR and public-call credential separation; closed/zero cleanup confirmed.
- [ ] **CHK014** Preview/approval, previous revisions/rollback and actual deployed
  candidate image/revision/traffic/health confirmed (G5).
- [ ] **CHK015** Authorized public-frontend 45-request/40-worker live rehearsal
  passes full semantic/error/coverage/latency/safety gates with sanitized evidence (G6).
- [ ] **CHK016** Five cellular phones, QR printouts, accessibility/contrast,
  projector readability and seven-minute show/fallback rehearsed (G7).
- [ ] **CHK017** Close/drain/reset/close yields stable closed/zero tally while
  incidents/reports/audit remain; exact tested revision frozen and GO/NO-GO
  recorded before stage time (G7/G8).

## Stop conditions

- [x] **CHK020** Defaultfalse explicit SURGE_DEMO_MEMORY_STORAGE opt-in selects
  cached incident **and session** memory stores with real Azure chat/embeddings/
  knowledge when mock=false; zero-LLM router/safety/PII/audit calls unchanged.
  Health storage_mode independent of mock_mode; 10s UI health refresh,
  **LIVE AZURE AI - TEMPORARY DEMO STORAGE**, own words/no mock sample, explicit
  restart loss of reports/session/audit documented.
- [ ] **CHK021** Actual app-only hybrid canary revision/health false-memory/UI
  disclosure/control/report/model/knowledge/audit path verified; public old
  mock100% until untouched45-fixture/concurrency40 fully passes.
  R9 revision/health/1replica/403 and hosted frontend now verified; do not infer
  full UI/audit/overlapping-reset proof. Actual R9 fixture failed grouping/latency;
  no cutover, keep composite gate open.
- [ ] **CHK022** Actual hybrid semantic/error/latency evidence, cleanup and
  promotion decision recorded; no source/startup/mock pass substituted.
  Actual R9 full accounting and CLOSED/zero cleanup recorded; semantic/latency
  FAIL, no promotion. No more paid load; actual design/latency solutions required.
- [ ] **CHK024** R8 blocking-I/O/epoch fixes have focused regressions; obsolete
  results cannot repopulate reset tally, domain records/audit preserved;
  quiescent cleanup is stably CLOSED/zero and untouched45/concurrency40 has no
  timeouts/errors plus full grouping/latency acceptance. Eventual completion
  must not be reclassified as successful client response.
  R9 source/image checks pass all390 in one run and final reset CLOSED/zero;
  actual full-fixture accounting passes but semantic/latency **FAIL**. Keep this
  composite gate open; source fixes and ordinary reset do not certify live GO.
- [ ] **CHK023** Durable track proves actual case status, evidence-backed cause,
  healthy private backend and persistent report/audit path; support packet alone
  is not a ticket, fix or service readiness.

- [x] **CHK019** Shipped frontend revision/digest/bundle, runtime mock notices/
  neutral footer/sample text, independent browser and40 repeated-wording mock
  results, final protected CLOSED/zero cleanup and five-line handoff recorded.
  Mock40→4, zero errors, p95 all40=0.213s; physical cellular/live semantic
  acceptance remain explicitly unverified/NO-GO. Existing Board/Report lint
  baseline4warnings/1unused-disable reproduced unchanged; new modules strict PASS.

Unknown access/target/key/live mode/model/scale, untested verifier, wrong revision,
any safety/privacy regression, missing live coverage or failed acceptance
means **NO live GO**. Use only a verified, honestly labeled fallback.
