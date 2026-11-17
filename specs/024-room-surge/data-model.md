# Phase 1 Data Model: Room Surge

**Branch**: `event/arlington-2026-11-18` | **Revision**: R3, 2026-11-17 10:15 ET
**Target**: 2026-11-17 13:00 Eastern | **Source**: `api\surge.py`,
`services\surge_room.py`, pipeline and [spec](spec.md)
**Status**: ✅ Repository model documented; deployed configuration unverified

## Canonical records (unchanged)

| Entity | Relationship / authority |
|---|---|
| Signal | Inbound communication, processed through existing pipeline; channel `report`, session `surge-<device_id>`; card never passed to pipeline |
| Report | Attributable association of a processed signal to an incident; dedup attaches rather than deletes |
| Incident | Existing ID, severity, queue, SLA, magnitude, status, category/embedding; RouterExecutor decides, ActionAgent acts through its three tools |
| Audit entry | Existing mutation record with actor/time/cause; never cleared by room reset |

Live durable records use existing services; offline records use mock twins.
No persistence migration, new container, retention policy or embedding model is
introduced. Safety-blocked attempts do not become incidents/reports.

## Admission request (transient)

| Field | Validation / use |
|---|---|
| `message` | Required string length 1–500; UI trims whitespace; existing pipeline safety/PII flow |
| `device_id` | Required `^[A-Za-z0-9-]{8,64}$`; random localStorage identifier, not verified identity |
| `card` | Optional string ≤8 characters; trim/uppercase/first character → A/B/C/D/E/R or `?`; tally only |

Device ID participates in session/rate metadata but is not exposed by public
state. Client IDs are not abuse-resistant authentication. No raw message is
stored in SurgeRoom. Existing pipeline classifies original text, redacts
downstream embedding/persistence text, and retains existing audit boundaries.

## SurgeRoom (one backend process)

| Fields | Meaning |
|---|---|
| `is_open`, `opened_at`, `closed_at` | Intake state and nullable epoch-second timestamps |
| `signals` | Successful pipeline results, including no-incident human escalation; excludes blocks/failures/rate-limit rejections |
| `_tiles` | Incident ID → room tile; `incidents` is number of distinct IDs represented this room session, **not number newly created** |
| `blocked`, `failed`, `rate_limited` | Content-safety blocks, pipeline failures, admission refusals respectively |
| `escalated_to_person` | Escalated results **without incident ID** only; incident-bearing escalation is on tile |
| `by_card` | Successful results + safety blocks by normalized card; excludes pipeline failures/rate limits |
| `_devices` | Distinct admitted IDs; includes attempts later blocked/failed; public `devices` is cardinality only |
| `_recent` | Per-device monotonic timestamps; default sliding window three attempts /60 seconds |
| `reports_per_window`, `window_seconds` | Existing settings configure admission; not changed for event rehearsal |
| `replica` (snapshot) | `CONTAINER_APP_REPLICA_NAME` or hostname; troubleshooting metadata, not proof of a single worker |

Public `ratio = round(signals / incidents, 1)` when incidents>0, otherwise null.
No-incident escalations mean ratio is not exclusively a dedup metric.

## Tile projection

`incident_id`, `severity` (SEV1–SEV4), `queue`, `category`, nullable `location`,
`escalated`, `room_reports`, `magnitude`.

- `room_reports` counts successful results for that ID since tally reset.
- `magnitude` reflects retained incident report history supplied by routing;
  it can exceed `room_reports`, especially after rehearsals.
- Location is whitespace-normalized, PII-redacted and capped to 40 characters.
- Initial category/severity/queue/location are observed from the first result
  for the room tile; escalation is OR'd across subsequent results.
- Tiles sort by room reports descending, then first-seen time. Internal
  `first_seen`/`last_seen` are not public tile fields.
- No transcript, user message, raw report, device/session ID or card-based
  routing bucket is a tile field.

## State transitions and cleanup

```text
startup/reset → CLOSED, empty tally
CLOSED --authorized open--> OPEN
OPEN --admitted result--> tally/tiles updated
OPEN --authorized close--> CLOSED, existing tally retained
any --authorized reset--> CLOSED, empty tally; operational records untouched
```

Open stamps `opened_at` and clears `closed_at` but does not clear tallies.
Close refuses **new** reports; already admitted pipeline work can still update
state. Reset is not a cancellation barrier: **close, drain, reset, close, then
read repeated closed/zero state**. Restart/revision change loses tally/rate
metadata but must not delete live incidents/reports/audit.

## Deployment and acceptance consequences

One replica **and one serving process**, with correct revision traffic, is
required; repeated stable hostname alone cannot prove this. Reset does not
isolate a new durable incident dataset. Live rehearsal records baseline/reused
incident IDs and grades grouping within the run; it never purges earlier
signals to obtain four newly opened incidents.
