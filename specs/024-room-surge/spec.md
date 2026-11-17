# Feature Specification: Room Surge

**Feature ID**: `024-room-surge` | **Working branch**: `event/arlington-2026-11-18`
**Created**: 2026-11-08 | **Revision**: R9, 2026-11-17 15:00 ET
**Target**: Original showcase **2026-11-17 13:00 Eastern** (elapsed); bounded recovery continues
**Status**: ✅ R9 source/deployment/accounting verified; ⛔ FINAL live NO-GO: grouping and latency FAIL; no cutover
**Readiness**: `████░░░░░` **4/9 primary-live gates**; G5 blocked, G6 failed; fallback does not satisfy live acceptance ([gates](plan.md#completion-gates))
**Source**: msftsean request and live-test follow-up; Cowork patch commit `e1eca20`
on `7bed125`; repository inspection and observed tests in [plan.md](plan.md).

## Objective and scope lock

### R9 — observed rehearsal FAILED; FINAL NO-GO

Reviewed integration uses async Azure credentials, computes embeddings before
the lock, and retains **atomic decision + persistence**. Reset generation guards
keep late successes domain-persisted/accepted with **`room_counted=false`** and
an explicit reset notice; late blocks/errors cannot pollute the new room.
The optional frontend receipt field is backwards compatible.

Immutable Linux backend
**`sha256:318a475c91f3e21bb7b605052eb586a2a8c01192076a5dc71575961c0d36795a`**
passed **all390 tests in one run**, with read-only README/docs/frontend-source
fixtures. Source frontend **14 tests / Node22 build PASS**. Frontend image
**`sha256:b6711361acd28fe5ce6121312bbe871b8d4a2f49ad6531efb685c6f354ecf606`**,
bundle **`index-CXbXlhpf.js`**, hash
**`46F1130F6BF45E9F70B4809149F51169B1CDDD100ED8B6263679CF5A63927412`**.
These are built/source checks, **not deployed semantic/performance acceptance**.

Actual **--hybridr9** backend Healthy/one replica, digest above verified,
health **false/memory**, keyless control **403**. Untouched45/concurrency40:
**45/45 HTTP200**, **43 accepted signals→36 incidents**, **2 safety blocks**,
**0 errors/failed/escalated**, wall **19.7s**. A/B/C/D distinct
**10/7/6/10 =33**, pairwise disjoint: **SC-001 FAIL** against4–6.
E3 distinct/disjoint and complete/error-free accounting **PASS**.
Full45 latency median **16.32s**, p95 **17.97s**: **SC-002 FAIL**, requires<8s.
Candidate finally reset **CLOSED/zero**; **no cutover**. Public mock remains
named **100% traffic pin**, untouched.

R9 frontend now **Healthy, Single/latest**; actual hosted
**index-CXbXlhpf.js** and full hash above match exactly; public health **mock=true**.
Initial readiness briefly served old HTML; subsequent readiness plus hosted-hash
verification confirms deployment, not semantic acceptance.
**No more paid load.** Semantic calibration/design **and latency require actual
solutions**; async/reset source fixes are not full demo acceptance. Durable
blocked; no support case filed or physical-phone confirmation.

### Historical R8 — actual failed canary and reset-generation defect

Reviewed changes include the Search SDK `k` fix, knowledge/sitrep work outside
the **atomic dedup** critical section, and privacy-safe phase instrumentation.
Verification: **Linux380 backend/runtime checks PASS plus4 repository-document
checks PASS separately with read-only fixtures**; Forge's source run
**384 PASS**. These are implementation evidence, not acceptance of current fixes.

Image **`sha256:0c755cd5a5dbb15ac5d7f1e93c2f9b94d10c0a1dc47e4590c64773f96afe7d7b`**,
candidate **`--hybridr8`**, Healthy/one replica, health false/memory,
**zero normal traffic**. Untouched45/concurrency40 **FAILED**: HTTP
**41 accepted signals→34 incidents**,2safety blocks,2client timeouts (B,C);
A–D31/E3disjoint observed IDs. Wall **60.2s**, median **16.46s**, p95 **18.22s**
from **43/45 HTTP successes**: incomplete and **invalid acceptance**, not a pass.
The two timed-out reports eventually completed around82s; all43 pipeline
completions plus2blocks are logged, but eventual completion cannot undo timeouts.

The initial finally-reset CLOSED/zero was **polluted by late completions**:
**CLOSED /2signals /2incidents /devices0**. This confirms a reset-generation
defect, not clean final state from that first reset. **14:24 ET cleanup verified**:
all45 requests had settled; a second reset of only quiescent **--hybridr8**
restored **CLOSED/zero**. Stable public mock was read-only verified **CLOSED/zero**,
not reset. Domain records were not deleted; cleanup does not fix the epoch defect.
Forge is fixing actual synchronous-I/O/event-loop blocking and reset epoch
handling. No threshold, taxonomy, fixture or card-routing changes. Observed
OPEN similarities mostly **0.67–0.82**, ATTACH observations **≥0.8308** require
further semantic diagnosis; these are observations, not a new threshold value
or proof the semantic problem is fixed.

Stable public mock remains100%; frontend artifact **f688**, served
**`index-CNv7Cu5d.js`**, unchanged. Cellular QR instructions were sent, **no
actual user confirmation**. Actual Azure Search evidence: **36 rows**, all
**`vector_query=True` / results3**, verifies the live knowledge SDK fix, not
semantic/performance acceptance. Fixed source and complete
unchanged-fixture retest remain pending; do not claim readiness.

### R7 — explicit hybrid demo opt-in (canary deployed; acceptance FAILED)

User approved parallel temporary-demo and durable recovery tracks: **“can you
do both in parallel.”** New **`SURGE_DEMO_MEMORY_STORAGE=false` by default**;
with `MOCK_MODE=false`, opting in selects **cached memory incident AND session
stores** while retaining real Azure chat, semantic embeddings and knowledge.
This is **not mock mode**. QueryAgent authority, zero-LLM RouterExecutor,
three ActionAgent tools, safety/PII/escalation and audit calls remain unchanged.

Health reports **`storage_mode="memory"|"cosmos"` independently of `mock_mode`**.
The R7 UI polls health every **10 seconds** (separate from board state polling)
and shows **LIVE AZURE AI - TEMPORARY DEMO STORAGE** for false/memory, with
own-word instructions and **no mock sample button**. Incident/report/session/
audit data in the memory stores **is lost on restart**; no durable-storage or
production-readiness claim is permitted. Reset remains tally-only, not deletion.

**Implementation evidence**: source backend **382 PASS**, UI **14 PASS**;
real Linux backend-image focused tests **33 PASS**; local startup health
**mock_mode=false /storage_mode=memory PASS**. These did not establish acceptance.

**Actual canary evidence, 13:46 ET**: backend candidate **`--hybrid1340`**
Healthy/Running, one replica, real Azure AI +memory, health **false/memory**,
keyless control403. Untouched45-request/concurrency40 rehearsal:
**43 accepted signals →34 incidents**,2safety blocks,0errors/failed/rate limits.
A10/B7/C6/D8 distinct IDs: **31 pairwise-disjoint A–D incidents**, so
**SC-001 FAIL** (requires4–6); E3distinct and complete accounting PASS.
Median **15.67s**, p95 **16.81s**, wall **17.7s**: **SC-002 FAIL**.
Candidate protected reset CLOSED/zero. **NO cutover**: stable backend
**`--mockfallback` keeps100% traffic**. New mode-aware frontend **`--hybrid1340`**
deployed Healthy, served bundle **`index-CNv7Cu5d.js`**; this does not promote
the hybrid backend. Forge investigates actual semantic/performance failure;
no threshold/fixture/card-grouping weakening permitted. Fixed retest pending.

Durable track: Kitty prepared a support packet, **no actual ticket filed**.
The private backend is not verified ready; the terminal Container Apps rollout
failure's root cause remains **unknown**. Earlier policy-caused Cosmos
reachability evidence remains valid but does not explain that terminal rollout.

**Final event decision, 12:42 ET**: the 12:10 live/fallback cutoff passed.
Corrected private backend rollout terminally failed at 12:17:52 ET; no usable
private revision/FQDN or frontend exists. No more speculative infrastructure
before the 13:00 showcase. Preserve policy, existing secrets and private redteam.
The original public backend is now intentionally **MOCK_MODE=true**, coach key
unchanged; at 12:20:26 health confirmed mock mode and CLOSED/zero tally.
`/?demo=loaded` is browser-verified **replay, not audience reporting**.
Mock audience fallback is now deployed and independently verified: **40 concurrent
repeated-wording reports →40 accepted signals /4 disjoint incidents**, zero
failures/blocks/rate limits, p95 **0.213s across all 40 attempts**, wall **0.380s**.
This is mock flow, not semantic acceptance. Two isolated mobile-browser contexts
also passed the sample/report/receipt/board path; physical cellular scan remains
unverified. Final protected reset confirmed CLOSED/zero without deleting reports/audit.
See the [five-line decision record](run-of-show.md#five-line-gono-go-record).

The audience supplies the surge: many signals, few incidents, one clear board.
An admission/tally wrapper and three pages exercise the existing bounded
pipeline. Recover, verify, deploy a **separate audience app in the user-approved
`MCAPS-2026-segayle` subscription `9f8986ed-ceb2-414d-8fcb-46d5cfc70618`**,
rehearse, reset/close, and freeze before 13:00. Do not treat local mock results
as live semantic-dedup evidence.

This refresh is **documentation only**. No branch switch, runtime change,
deployment, Azure setting/secret change, or commit/push is performed by this
planning pass. The parent owns agent-context refresh and checkpoints. The user's
follow-up authorizes a live Azure test **after** target/access/configuration
gates pass; it does not authorize changing secrets or using the private redteam
deployment. [Tasks](tasks.md) are the executable recovery backlog, not completed
implementation merely because they are written.

**Target decision update**: Today's subscription choice is confirmed; Kitty's
read-only inventory will determine exact audience resources/FQDN and populate
the local, ignored [deployment plan](..\..\.azure\deployment-plan.md).
Do not require historical corporate-tenant sign-in for today; that path is
deferred until today's demo works. Never reuse the private redteam adapter.
**Creation permission granted, 10:15 ET**: User said “yes create away. the goal
is to get this complete,” explicitly authorizing new separate audience resources
and NEW app-scoped secrets, including the coach key, in that subscription.
No further elicitation is needed for ordinary isolated creation within this
scope. Never modify/rotate existing app secrets or reuse the private redteam
adapter. Parent must publish this Spec Kit checkpoint to GitHub **first**;
implementation and validated deployment follow. Technical preflight/preview
gates remain, not a renewed generic permission request.

## User Scenarios & Testing

### US1 — Report from a phone (P1)

An attendee scans a card, opens `/report?card=A` without sign-in, and types or
uses the phone keyboard's dictation. Acknowledgment identifies an opened/joined
incident and its **room** report count, or truthfully reports a blocked,
escalated, received, or failed outcome.

**Independent test**: A phone-sized browser submits while open; receipt and board
agree. A real-phone cellular check remains required.

1. A valid 1–500 character message uses `process_signal(channel="report")`.
2. Closed intake returns 409 without processing; the fourth attempt by one device
   within the default 60-second/three-report window returns 429.
3. If the content-safety service actually blocks, receipt says blocked and only
   the blocked tally increments; no incident is created for that attempt.
4. A crisis/harm signal follows the existing human-escalation safety net.
5. Red-card input is **not guaranteed to be blocked in live mode**. Inspect the
   actual safety/routing outcome; no rule, severity, SLA, or tool authority may
   be overridden. Never fabricate a refusal for the stage.

### US2 — Watch the room board (P1)

`/surge` shows a locally generated QR, join URL, signals/incidents, ratio,
participating devices, safety blocks, no-incident human escalations, and incident
tiles weighted by room reports. Incident-bearing escalations are marked on tiles;
the current global escalation counter is not a count of every escalation.

**Independent test**: Submit near-duplicates and observe counts update on the
approximately one-second poll. Keep the last good state and show reconnecting
when polling fails. Projection readability, contrast, and keyboard accessibility
require separate verification; browser route smoke alone does not certify them.

Tiles contain only incident ID, severity, queue, category, redacted/capped
machine-extracted location, escalation flag, room reports, and magnitude. No raw
attendee text or device identifiers appear in public state.

### US3 — Coach controls and safe reset (P1)

`POST /api/surge/control` accepts `open`, `close`, or `reset` with `X-Surge-Key`.
Live mode with missing/wrong key returns 403; mock mode permits a missing key
only when no key is configured. Hiding controls is not authorization.
Masked **Operator controls → Coach key → Set key** is now implemented/tested.
Use that non-URL entry path; legacy URL ingestion is not safe credential delivery.

**Independent test**: Verify unauthenticated control fails and authorized control
works on the confirmed live target; reset, then read `open=false`, all tally
counters zero, and no tiles. Incidents, reports, and audit records remain intact.
Wait for in-flight reports to finish before resetting; close alone does not
cancel already admitted work.

### US4 — Distribute truthful scenario cards (P2)

`/surge/cards` prints A–D (four Arlington events), E (distinct small issues), and
R (guardrail probes). QR opens the matching report page. E does not force SEV4;
severity always follows deterministic rules. Card letters never affect routing.
Print only after the actual public join origin and real-phone scanning work.

## Requirements

- **FR-001**: All accepted reports use the unchanged bounded pipeline. Card ID
  affects tally only; no card-based grouping or demo-only routing.
- **FR-002**: Preserve zero-LLM RouterExecutor, ActionAgent's exact three tools
  (`create_incident`, `search_knowledge`, `generate_sitrep`), PII filtering,
  audit, crisis/SEV1/statutory and other mandatory human escalation.
- **FR-003**: Preserve per-device admission defaults (three reports / 60 seconds).
  LocalStorage device ID is rate-limit metadata, not authenticated identity.
- **FR-004**: Public state is counts and safe tiles only. Evidence must exclude
  raw attendee text, device/session IDs, secrets, and coach-key URLs.
- **FR-005**: Mock mode stays viable offline. Bag-of-words embeddings do not
  collapse broad free-typed paraphrases; use near-duplicates for offline dedup
  flow tests and **live semantic embeddings** for semantic acceptance.
- **FR-006**: One backend replica **and one serving process** for the in-process
  tally; inspect actual scale/revision traffic and repeated replica IDs.
  Repository defaults are not deployed-state proof.
- **FR-007**: Confirm exact subscription/resource group/apps, accessible public
  frontend with `/api` proxy, `mock_mode=false`, operational chat/embedding,
  stores/knowledge/audit dependencies, quota, and authorized coach control
  before live load. Use masked non-URL coach entry and private script credential
  intake, not key URLs/arguments. Creating a NEW audience-app coach key is
  approved; changing existing secrets is not. Do not publish keyless mock
  controls as a live deployment.
- **FR-008**: Harden rehearsal verification before using its exit code as a gate:
  full fixture coverage, no request/network errors or server failures,
  positive incident coverage, and no A–D cross-event merges. Preserve the
  45-request fixture and documented latency denominator; record actual red-card
  outcomes without requiring universal blocking.
- **FR-009**: Deploy only a tested, checkpointed candidate through existing
  infrastructure after preview/approval. Verify image/revision and traffic,
  public health/routes, authorized live 40-worker rehearsal, reset/closed state,
  real phones, seven-minute run-through, and a tested fallback.
- **FR-010 — disclosed mock fallback**: Report/board/cards read runtime
  `/api/health` mode and disclose mock/replay honestly; use a neutral footer
  without an unconditional AI-processing claim. Only in mock mode, A–D may offer
  **Use sample report**, prepopulating the actual scene wording for deterministic
  token-overlap flow. The resulting text still follows normal admission and
  pipeline processing; no card-based server grouping, dedup/threshold change or
  hidden shortcut. Live own-word behavior remains unchanged. This demonstrates
  repeated-wording mock flow, **not live semantic acceptance**.
- **FR-011 — temporary demo storage**: `SURGE_DEMO_MEMORY_STORAGE` MUST default
  false. Its explicit opt-in selects cached memory incident and session stores,
  not mock Azure clients. With `MOCK_MODE=false`, chat/embedding/knowledge remain
  real Azure; routing/safety/audit-call behavior is unchanged. Normal false/flag-
  false operation keeps Cosmos storage. Public health separates `storage_mode`
  from `mock_mode`; UI health refresh is10s and discloses false/memory using
  **LIVE AZURE AI - TEMPORARY DEMO STORAGE**, own-word reporting, no mock samples,
  and restart loss. This approved demo-only retention tradeoff is not a waiver
  of audit calls, attributable reports or safety and is not durable acceptance.
- **FR-012 — reset-generation isolation**: A result admitted before a tally reset
  MUST NOT repopulate the new tally after reset; domain pipeline processing,
  reports and audit must still complete normally. R8 observed the violation;
  R9 source guards are reviewed/tested, **deployed acceptance still pending**.
  Late success remains accepted/domain-persisted, with optional
  `room_counted=false` and explicit reset notice; late blocks/errors must not
  affect new-room tallies. Close/drain/reset after quiescence remains required.

### Incident-triage and safety constraints

**Authority/escalation**: QueryAgent classifies only; RouterExecutor decides
dedup/severity/SLA/escalation; ActionAgent cannot bypass decisions. No safety
trigger is weakened to pass a demo. Every processed signal remains attributable;
dedup creates a report, never deletes a signal. Safety-blocked attempts do not
become incidents; tally reset never erases operational records.

**Data/external services**: Existing classification/content-safety flow is
unchanged. Pipeline redacts downstream text before embedding/persistence;
public location is redacted again and capped to 40 characters. Live mode uses
the existing Azure integration design; approved audience resource provisioning
may be needed, but no new model architecture/platform/telemetry payload is
introduced. **R7 explicitly changes demo retention only when opted in**:
incident/report/session/audit records use cached memory stores and are lost on
restart. Audit calls and PII filtering remain; disclose and never represent
ephemeral records as durable. Default Cosmos path is unchanged. Tally/rate
metadata remains process-local in all modes.

**Grounding**: Board facts come from pipeline results, not raw submissions.
Sitreps retain source-record citations; never project an unreviewed receipt or
claim observed live behavior without an evidence record.

### Key entities

Signal → report → incident remain canonical. SurgeRoom observes results, not
authority; its incident tile is a room projection, not a second incident store.
See [data-model.md](data-model.md) and [API contract](contracts/surge-api.md).

## Success criteria and release evidence

- **SC-001**: In a live 40-worker rehearsal, all 40 A–D fixture reports (10/card)
  receive accepted incident-bearing receipts. Their union is **4–6 incidents**
  (target four), each card has coverage, and card incident sets are pairwise
  disjoint. Zero incidents or cross-event merging is a failure, not a collapse.
  Three E fixtures remain distinct from one another and A–D; R outcomes are
  assessed separately.
- **SC-002**: p95 report-to-acknowledgment <8 seconds at concurrency 40.
  Preserve the existing HTTP-200 latency population (including safety blocks)
  and percentile calculation for comparability; report all 45 request outcomes
  and require zero errors/failed before calling it a pass.
- **SC-003**: Zero raw attendee text on board/state; PII, authority, severity/SLA,
  audit, and escalation regression tests stay green.
- **SC-004**: Focused/full mock backend tests, Surge UI tests, frontend typecheck
  and production build pass on the release candidate with aligned npm lock.
- **SC-005**: Confirmed audience deployment serves that candidate; live gates,
  real-phone/accessibility/projection checks, cleanup, rehearsal, and fallback
  are recorded before the freeze. Unknowns block live GO.

**Current disposition**: SC-001/002 live acceptance remains failed/unproven.
Latest observed rehearsal R8 adds two client timeouts and a reset-generation
failure; partial HTTP-response latency and eventual completion are not a pass.
R9 source/image checks pass and actual full accounting passes, but
43accepted→36incidents/A–D33 fails grouping and full45 p9517.97s fails latency.
FINAL live NO-GO; no cutover or more paid load. Semantic/design and latency
solutions remain required, not established by async/reset fixes.
R7 source/image/startup checks remain green; actual real-Azure/memory canary ran
without request errors but **failed both semantic grouping and latency**.
Promotion is blocked pending evidence-backed fix and unchanged full-fixture
retest; public stable mock retains100%. Earlier failed durable45/43errors and
mock40→4 remain separate historical runs.
Historical R6 fallback **11 focused UI tests** (including configured API-origin), Node22
build/typecheck, new-module/cards/tests strict lint and deployed browser/mock
flow checks passed. Frontend revision
`allclear-sbuqtpuppifra-frontend--mocklabel1236` was Healthy/Running, 100% traffic,
bundle `index-DVUyNrL6.js` then; current mode-aware frontend is **--hybrid1340**,
served **index-CNv7Cu5d.js**, with stable **backend --mockfallback100%**.
Physical cellular scan, full accessibility/projection
and live semantic/load criteria remain unverified/NO-GO; original 43 failures
in 45 live attempts are not superseded by mock success.

## Out of scope

Day 2 curriculum changes; outbound/multilingual backup implementation; broad
refactors; cross-replica tally; new platforms; hardcoded card grouping; blanket
threshold lowering. Alternate demos are fallback candidates only if independently
verified, not assumed available.
