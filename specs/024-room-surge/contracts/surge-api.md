# Phase 1 Contract: Room Surge API and UI

**Branch**: `event/arlington-2026-11-18` | **Revision**: R9, 2026-11-17 15:00 ET
**Target**: Original 2026-11-17 13:00 Eastern elapsed; recovery | **Source**: current `api\surge.py`,
`services\surge_room.py`, `frontend\src\allclear\surge\surgeApi.ts`
**Status**: ✅ R9 source/deployment/accounting; ⛔ FINAL live NO-GO: semantic/latency FAIL; no cutover

## R9 reset/receipt contract — source tested; observed demo acceptance FAILED

Reviewed integration uses async Azure credentials and pre-lock embedding;
**atomic decision + persistence remain protected**. Generation guards isolate
the new room from requests admitted before reset:

- Late success is still domain-persisted and `accepted=true`, with
  **`room_counted=false`** and an explicit reset notice. Do not present it as a
  failed/lost report or retry solely because it is absent from the new board.
- Late blocks/errors do not increment the new room's tallies.
- Response **`room_counted` is optional**; frontend receipts remain backwards
  compatible when absent. `false` discloses non-counting/reset, not domain failure.
- This does not cancel in-flight work, promise exactly-once retries or remove
  the close/drain/reset operational requirement.

Immutable Linux backend
**sha256:318a475c91f3e21bb7b605052eb586a2a8c01192076a5dc71575961c0d36795a**
passed **all390 tests in one run**, using read-only README/docs/frontend-source
fixtures. Source frontend **14 tests / Node22 build PASS**. Built frontend
**sha256:b6711361acd28fe5ce6121312bbe871b8d4a2f49ad6531efb685c6f354ecf606**,
**index-CXbXlhpf.js**, hash
**46F1130F6BF45E9F70B4809149F51169B1CDDD100ED8B6263679CF5A63927412**.
Actual **--hybridr9 Healthy/one replica**, digest above verified, health
**false/memory**, keyless controls **403**. Untouched45/concurrency40:
**45/45 HTTP200**, **43 accepted signals→36 incidents**, **2 safety blocks**,
**0 errors/failed/escalated**, wall **19.7s**. A/B/C/D distinct
**10/7/6/10 =33** disjoint **FAIL4–6**; E3distinct/disjoint and complete/error-free
accounting **PASS**. Full45 median **16.32s**, p95 **17.97s FAIL<8s**.
Candidate finally reset **CLOSED/zero**; **no cutover**. Public mock named
**100% untouched**. R9 frontend **Healthy Single/latest**; actual hosted bundle
and full hash above match, public health **mock=true** after initial transient
old HTML then readiness+hosted-hash confirmation.
**FINAL NO-GO; no more paid load.** Actual semantic calibration/design **and
latency solutions required**, not inferred from async/reset fixes. Durable
blocked; no support case filed or physical-phone confirmation. Ordinary final
reset success does not by itself certify overlapping-generation behavior.

## Historical R8 acceptance/reset defect — before R9 source guards

--hybridr8 Healthy/1replica/false-memory/zero normal traffic, image
`sha256:0c755cd5a5dbb15ac5d7f1e93c2f9b94d10c0a1dc47e4590c64773f96afe7d7b`.
Untouched45/concurrency40 failed: HTTP41accepted→34incidents,2blocks,
2client timeouts(B,C), A–D31/E3disjoint; wall60.2s,median16.46s,p9518.22s on
43/45 HTTPsuccesses, **invalid complete acceptance**. All43pipeline+2block
completions logged, timed-out2 around82s, do not erase client failure.

Initial resetCLOSED/zero later became **CLOSED/2signals/2incidents/devices0**.
**Required pending fix**: record tally generation at admission and ignore
obsolete-generation tally updates after reset, while normal domain processing/
reports/audit finish. This describes the required epoch-isolation outcome,
not delivered acceptance. Confirm quiescence and repeat stable closed/zero
checks; never delete domain records. **14:24 ET cleanup verified**: all45
requests settled; second reset of only quiescent **--hybridr8** restored
**CLOSED/zero**. Stable public mock read-only verified **CLOSED/zero**, **not
reset**. This cleanup does not prove the pending epoch fix.

Reviewed Search SDK `k` fix/outside-atomic knowledge-sitrep/safe phase timing
passed Linux380runtime+4doc checks separately (Forge source384), but actual
sync-I/O/event-loop and epoch corrections remain in progress. **36 actual Azure
Search rows**, all **`vector_query=True` / results3**, verify live knowledge SDK
fix, not semantic/performance acceptance. Semantic
OPENmostly0.67–0.82 vs observedATTACH≥0.8308 is unresolved; no threshold,
taxonomy, fixture or card-routing change. Stable mock100%/frontendf688/
index-CNv7Cu5d.js unchanged. Cellular instruction delivery is not phone proof.

## R7 storage/mode contract — retained; later R8 failure above

`SURGE_DEMO_MEMORY_STORAGE` is explicit opt-in, **defaultfalse**. With
MOCK_MODE=false it selects **cached memory incident AND session stores** while
chat, semantic embeddings and knowledge remain real Azure. Zero-LLM routing,
three-tool authority, PII/safety/escalation and audit calls are unchanged.
Memory-backed incident/report/session/audit data **is lost on restart**; reset
still clears only tally. Default flagfalse retains normal Cosmos live storage.

**GET `/api/health` adds `storage_mode: "memory"|"cosmos"` independently of
`mock_mode: boolean`**. Do not infer inference mode from storage mode.

| Runtime mode | Required UI behavior |
|---|---|
| mock_mode=true | Existing explicit Mock label and mock-only A–D sample flow; public currently verified in this mode |
| mock_mode=false, storage_mode=cosmos | Live own-word instructions; no mock sample button; durable readiness still separately verified |
| mock_mode=false, storage_mode=memory | **LIVE AZURE AI - TEMPORARY DEMO STORAGE**, own-word instructions, no mock sample button, explicit reports/session/audit restart-loss warning |

UI refreshes health every **10s**, independent of approximately1s board state
polls. Hybrid startup/source/image tests (382backend/14UI/image33/false-memory)
pass. Actual backend **--hybrid1340** is Healthy/Running/1replica, false/memory,
keyless403; untouched45/concurrency40 returned43accepted/34incidents/2blocked,
zeroerrors/failed/rate limits. A–D31disjoint IDs (10/7/6/8):SC-001 FAIL;
E3distinct/accounting PASS; p9516.81s (median15.67s/wall17.7s):SC-002 FAIL.
Candidate finally reset CLOSED/zero. Corrected semantic/UI/data-path acceptance
and retest remain pending; stable **--mockfallback100%**, no cutover.
Mode-aware frontend **--hybrid1340** Healthy, served **index-CNv7Cu5d.js**;
deployment is not semantic acceptance.
No inference tool/schema/pipeline routing change or durable-success claim.

## Historical R6 fallback UI delta — deployed and verified then

Report/board/cards use runtime **GET `/api/health`** mode for explicit mock
notices; footer must not unconditionally claim AI processing. In mock mode only,
A–D **Use sample report** prepopulates that scene's actual wording into the
normal report input. The existing POST/report contract and bounded pipeline
remain unchanged; card ID does not group or route. Live mode retains own-word
reporting without the mock-only button. **11 focused tests** including configured
API-origin, Node22 build/typecheck and new-module/cards/tests strict lint pass.
Deployed revision `allclear-sbuqtpuppifra-frontend--mocklabel1236` is Healthy/
Running100%traffic, bundle `index-DVUyNrL6.js`; public mock40-request run passes:
40 accepted→4 disjoint incidents/40devices, A–D10each, zero failures/blocks/
rate limits, p95 all40=0.213s, wall0.380s. Keyless controls403.
Two mobile-browser contexts and all3 runtime Mock labels/QRs/operator entry/
public-call credential separation pass. Final protected CLOSED/zero reset
retains domain reports/audit. Physical cellular scan is unverified.
This does not replace failed live semantic acceptance. `/?demo=loaded` remains
separately verified replay, not intake.

## Base and authorization

JSON over `/api/surge`, served through the public frontend nginx `/api` proxy.
GET state and POST report do not require attendee sign-in. POST control requires
`X-Surge-Key` when configured; compare is constant-time. In live mode missing
server key disables control (403). Mock-only unconfigured-key control is
permitted offline and **must not be published as live**.

Never put key values in examples, printed cards, join links, evidence or process
arguments. Board URL stripping is not secure credential delivery.

## GET `/api/surge/state`

200 JSON:

| Field | Type |
|---|---|
| `open` | boolean |
| `opened_at`, `closed_at` | epoch seconds or null |
| `signals`, `incidents`, `devices` | nonnegative integer |
| `ratio` | number rounded to one decimal or null when no tiles |
| `blocked`, `escalated_to_person`, `rate_limited`, `failed` | nonnegative integer |
| `by_card` | normalized card → result/block count |
| `replica` | process-host/replica string |
| `tiles` | array of tile objects below |

Tile fields: `incident_id: string`, `severity: SEV1|SEV2|SEV3|SEV4`,
`queue: string`, `category: string`, `location: string|null` (redacted, ≤40
characters), `escalated: boolean`, `room_reports: integer`, `magnitude: integer`.
No raw report, attendee message, secret, device ID or session ID.

`signals` excludes blocks/failures; `incidents` counts distinct room-represented
IDs, including existing incidents; `devices` counts admitted distinct IDs.
Global `escalated_to_person` counts no-incident escalations only; tiles carry
incident-bearing escalation. See [model](..\data-model.md).

## POST `/api/surge/report`

Request:

```json
{"message":"Water main break on Wilson Blvd near Clarendon","device_id":"device-example-0001","card":"A"}
```

- `message`: 1–500 characters; UI trims before send.
- `device_id`: `[A-Za-z0-9-]`, 8–64 characters.
- `card`: optional/null, max 8; normalized A/B/C/D/E/R or `?`, tally only.
- Valid admitted request runs the normal pipeline on `channel="report"`.

| Result | HTTP / shape |
|---|---|
| Opened/joined | 200: `accepted=true`, `outcome="opened"|"joined"`, `incident_id`, `room_reports`, `severity`, `message` |
| No incident | 200: `accepted=true`, `outcome="escalated"|"received"`, `incident_id=null`, `room_reports=0`, `severity`, `message` |
| Actual content-safety block | 200: `accepted=false`, `outcome="blocked"`, `message`; blocked tally increments |
| Room closed | 409 with string `detail`; no processing |
| Per-device limit exceeded | 429 with string `detail`; rate-limited tally increments |
| Invalid input | 422 validation response |
| Other pipeline exception | 503 friendly `detail`; failed tally increments |

R9 adds optional `room_counted: boolean` to report receipts. Late accepted
results crossing reset retain normal domain success but return
`room_counted=false` and explicit reset notice; stale blocks/errors do not
increment the new-generation tallies. The tally-increment descriptions above
apply only to the matching room generation. Overlapping-generation runtime
verification is not inferred from the ordinary final reset or full-fixture run.

Receipts may contain existing user-facing pipeline messages and are **not**
public board content. Privacy guarantees must also hold on receipt/output
surfaces. Network/client timeout is not proof a report was not processed; do not
blindly retry and claim exactly-once behavior.

## POST `/api/surge/control`

Request `{"action":"open"}`, `{"action":"close"}`, or `{"action":"reset"}`;
private `X-Surge-Key` header. 200 returns current state; wrong/missing live key
403; invalid action 422. Reset is tally-only and leaves intake closed.
Close does not cancel in-flight processing; drain before reset/empty-state
certification. R8 showed stale completions repopulate tally after reset; epoch
guards are source-tested in R9, with actual staged behavior pending. Require
quiescence/repeated stable state; do not infer runtime acceptance.
No endpoint deletes incidents/reports/audit; a timeout is not cancellation.

## Browser routes

| Route | Contract |
|---|---|
| `/report?card=A` | No sign-in; optional A–R card selection; ≤500-character textarea; keyboard dictation is phone capability; accessible receipt/error status |
| `/surge` | Locally generated QR to join URL; approximately 1s state polls; retain last good state + reconnecting on errors |
| `/surge?join=<public-report-url>` | Optional non-secret join destination; verify origin before publication |
| `/surge` operator entry | Expand Operator controls, enter masked Coach key, Set key; UI visibility grants no API authority |
| `/surge/cards?copies=2` | A/B/C/D/E/R printable cards and local PNG QR generation |
| Card options | `only=ABCD`, `copies` bounded 1–10, `origin` override for QR target; never override to an unverified host |

Current board credential-query ingestion is **not approved for live delivery**.
Implemented/tested operator path: masked non-URL password input,
credential retained only in private memory/session and sent solely in
`X-Surge-Key`; test no key in address/join/QR/cards/logs and invalid control still
403 on the deployed target remains a G5 check. Forge reports 6 UI tests and
typecheck/build pass. Legacy query-key support remains but must not be used;
no existing-server-secret change is implied.
Frontend client state timeout is 5s,
report/control 30s; nginx API proxy read timeout is 90s. Live SC-002 remains <8s;
a 30s client timeout is not an acceptable success target.

## Rehearsal contract (implemented/tested verifier, not new runtime API)

- Existing fixture remains 45 requests: A–D ten each; E three; R two; 40 workers.
- All 40 A–D results must be accepted with IDs; 4–6 IDs union, per-card coverage,
  pairwise-disjoint A–D sets. E three IDs distinct from each other and A–D.
- Account for every request; fail on HTTP/transport/timeout/invalid response,
  server failed count or unexpected rate-limit count. Zero/missing coverage
  and all cards merged into one never pass.
- R may block or follow normal safe routing; actual outcome and unchanged rules
  matter, not a synthetic mandatory refusal.
- Preserve HTTP-200 latency population including blocked responses and existing
  p95 index `max(0, int(n * 0.95) - 1)`; errors fail overall. Report full population
  and errors to prevent selective-success p95 claims.
- Implemented `--key-env <environment-variable-name>` intake (default
  `SURGE_COACH_KEY`) avoids exposed key values in arguments; pass only variable
  name. Forge's 11 new verifier tests /26 focused backend tests pass, without
  new packages. Live execution still waits for verified deployment/readiness.
- Baseline/candidate/revisions/replica, sanitized aggregates and cleanup are
  evidence; raw submissions, response bodies, device/session IDs and keys are not.
