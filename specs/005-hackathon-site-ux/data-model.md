# Phase 1 Data Model — 005 Hackathon Site UX

This feature is presentational; the only "data" is the static hub navigation link set,
shared between the desktop header nav and the new mobile nav.

## Entity: HubLink

| Field | Type   | Notes                                         |
|-------|--------|-----------------------------------------------|
| to    | string | Router path (e.g. `/pattern`)                 |
| label | string | Visible text (e.g. `Pattern`, `Schedule`)     |

### Canonical link set (must match existing header order)

| to              | label    |
|-----------------|----------|
| `/pattern`      | Pattern  |
| `/intents`      | Intents  |
| `/rules`        | Rules    |
| `/run-of-show`  | Schedule |

### Notes

- Defined once (e.g. exported `HUB_LINKS` const) and consumed by both navs to prevent drift.
- No persistence, no API, no derived state beyond the boolean `open` UI flag in `MobileNav`.
