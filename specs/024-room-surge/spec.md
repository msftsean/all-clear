# Feature Specification: Room Surge

**Feature ID**: `024-room-surge` | **Working branch**: `event/arlington-2026-11-18`
**Created**: 2026-11-08 | **Revision**: R4, 2026-11-17 11:27 ET
**Target**: **TODAY, Tuesday 2026-11-17, 13:00 Eastern**, seven-minute showcase
**Status**: ⛔ Azure images deployed, live run failed; policy-compliant network correction in progress
**Readiness**: `████░░░░░` **4/9 gates**; G5 partial, G6 failed ([gate definitions](plan.md#completion-gates))
**Source**: msftsean request and live-test follow-up; Cowork patch commit `e1eca20`
on `7bed125`; repository inspection and observed tests in [plan.md](plan.md).

## Objective and scope lock

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
may be needed, but no new model architecture, data retention scheme, platform, or
telemetry payload is introduced. Tally/rate metadata is process-local.

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

## Out of scope

Day 2 curriculum changes; outbound/multilingual backup implementation; broad
refactors; cross-replica tally; new platforms; hardcoded card grouping; blanket
threshold lowering. Alternate demos are fallback candidates only if independently
verified, not assumed available.
