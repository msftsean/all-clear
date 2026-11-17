# Phase 1 Contract: Room Surge API and UI

**Branch**: `event/arlington-2026-11-18` | **Revision**: R6, 2026-11-17 12:42 ET
**Target**: 2026-11-17 13:00 Eastern | **Source**: current `api\surge.py`,
`services\surge_room.py`, `frontend\src\allclear\surge\surgeApi.ts`
**Status**: ✅ Deployed mock/browser/load contract PASS; ⛔ live AI/semantic NO-GO

## Authorized fallback UI delta — deployed and verified

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

Receipts may contain existing user-facing pipeline messages and are **not**
public board content. Privacy guarantees must also hold on receipt/output
surfaces. Network/client timeout is not proof a report was not processed; do not
blindly retry and claim exactly-once behavior.

## POST `/api/surge/control`

Request `{"action":"open"}`, `{"action":"close"}`, or `{"action":"reset"}`;
private `X-Surge-Key` header. 200 returns current state; wrong/missing live key
403; invalid action 422. Reset is tally-only and leaves intake closed.
Close does not cancel in-flight processing; drain before reset/empty-state
certification. No endpoint deletes incidents/reports/audit.

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
