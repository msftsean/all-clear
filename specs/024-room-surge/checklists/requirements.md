# Requirements and readiness checklist: Room Surge

**Branch**: `event/arlington-2026-11-18` | **Revision**: R6, 2026-11-17 12:42 ET
**Purpose**: Prevent specification/evidence drift before today's **13:00 ET** demo
**Source**: [spec](..\spec.md), [plan](..\plan.md), [tasks](..\tasks.md)
**Progress**: `████░░░░░` **4/9 primary-live gates**; checked requirement quality
below does **not** certify unfinished deployment.

**Final disposition**: primary live NO-GO; private network/identity succeeded
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

- [x] **CHK019** Shipped frontend revision/digest/bundle, runtime mock notices/
  neutral footer/sample text, independent browser and40 repeated-wording mock
  results, final protected CLOSED/zero cleanup and five-line handoff recorded.
  Mock40→4, zero errors, p95 all40=0.213s; physical cellular/live semantic
  acceptance remain explicitly unverified/NO-GO. Existing Board/Report lint
  baseline4warnings/1unused-disable reproduced unchanged; new modules strict PASS.

Unknown access/target/key/live mode/model/scale, untested verifier, wrong revision,
any safety/privacy regression, missing live coverage or failed acceptance
means **NO live GO**. Use only a verified, honestly labeled fallback.
