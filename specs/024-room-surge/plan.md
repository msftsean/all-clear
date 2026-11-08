# Implementation Plan: Room Surge (024-room-surge)

**Spec**: `specs/024-room-surge/spec.md`
**Event**: Azure Days Arlington, Tue Nov 17, 12:45 showcase. Code freeze target: **Fri Nov 13**.

## Approach

Add an admission and tally layer around the *unchanged* pipeline, plus three
frontend surfaces. No change to QueryAgent, RouterExecutor, ActionAgent, dedup,
severity, escalation, PII handling or audit.

```
phone (/report) --POST /api/surge/report--> admission (open? rate limit?)
                                            --> AllClearPipeline.process_signal(channel="report")
                                            --> SurgeRoom.record_result / record_blocked
room display (/surge) --GET /api/surge/state (1 s poll)--> counts + tiles (no raw text)
presenter --POST /api/surge/control + X-Surge-Key--> open | close | reset (tally only)
```

## Files

| File | Change |
|---|---|
| `backend/app/services/surge_room.py` | New. In-process tally, sliding-window rate limit, privacy-safe snapshot |
| `backend/app/api/surge.py` | New. `/state`, `/report`, `/control` |
| `backend/app/main.py` | Mount router at `/api/surge` |
| `backend/app/core/config.py` | `SURGE_COACH_KEY`, `SURGE_REPORTS_PER_WINDOW` (3), `SURGE_WINDOW_SECONDS` (60) |
| `backend/app/core/dependencies.py` | `get_surge_room()` singleton; cleared in `clear_service_caches()` |
| `backend/scripts/surge_rehearsal.py` | New. Live calibration verifier for SC-001/SC-002 (stdlib only) |
| `backend/tests/test_surge_room.py` | New. Tally unit tests |
| `backend/tests/test_surge_api.py` | New. Route tests on the mock pipeline |
| `frontend/src/App.tsx` | Routes `/report`, `/surge`, `/surge/cards` |
| `frontend/src/allclear/surge/*` | New. `SurgeReport`, `SurgeBoard`, `SurgeCards`, `Qr`, `cards.ts`, `surgeApi.ts`, `Surge.test.tsx` |
| `frontend/package.json` | Add `qrcode` and `@types/qrcode` (local QR generation, no external service) |

nginx already has an SPA fallback, so `/report` and `/surge` need no nginx change.

## Verification status (be honest about this on handoff)

The patch was written in a sandbox that could not install Python or npm packages.

| Check | Status |
|---|---|
| `test_surge_room.py` (7 tests) | **Passed** under a stdlib harness (same assertions, no pytest) |
| `surge_rehearsal.py` | **Ran** against a stand-in HTTP server that uses the real `SurgeRoom`: 45 reports, collapsed to 4 + 3, 2 blocked, exit 0 |
| Frontend helpers (cards, acknowledgments, category formatting) | **Passed** under `bun test` |
| All new TSX/TS files | Parse cleanly (`bun build --no-bundle`) |
| `test_surge_api.py`, full backend suite | **Not run** (no FastAPI or pytest available) |
| `npm run build` (tsc + vite), `Surge.test.tsx` under vitest | **Not run** (no node_modules) |
| Visual check of `/surge`, `/report`, `/surge/cards` | **Not done** |
| Live calibration | **Not done** (needs the Azure deployment) |

## Event-day configuration

1. **Pin one backend replica** (the tally is in-process):
   `az containerapp update -n <backend-app> -g <rg> --min-replicas 1 --max-replicas 1`
   Check: `/api/surge/state` shows the same `replica` on repeated calls.
2. **Set the coach key** as a Container Apps secret mapped to `SURGE_COACH_KEY`.
   Open the board as `/surge?key=<key>`. The key is moved to sessionStorage and
   stripped from the URL, so it never shows on the projector.
3. **Model capacity**: 40 reports in about 30 seconds means around 40 classify calls,
   plus a sitrep for each new Incident. Check the chat deployment's TPM/RPM quota
   and the APIM rate limit so the audience doesn't hit 429s. `with_rate_limit_retry`
   absorbs short bursts.
4. **Short join URL**: create a short link to `https://<frontend>/report` and pass it
   as `/surge?join=<short-url>` so the on-screen text is easy to type.
5. **Print cards**: `/surge/cards?copies=2` (A to D on most tables; one E and one R per room).

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Free-worded paraphrases don't collapse (the threshold was tuned on scripted text) | Run `surge_rehearsal.py` live; lower `DEDUP_THRESHOLD` in small steps. If one card splits across intent categories, that's a QueryAgent prompt issue, not a threshold issue. |
| Venue Wi-Fi or cell signal is poor | Most phones fall back to cellular. Fallback ladder: replay surge (`/?demo=loaded` → existing Muni Water surge) → backup demo (outbound call + multilingual) → mock mode |
| Fewer participants than expected | Coaches seed reports from their own phones. The rehearsal script can top up quietly (`--no-reset`), but say so on stage if you use it |
| Inappropriate text | Content safety blocks it (counted, never shown); the board shows no raw text anyway |
| Mock mode won't collapse paraphrases | Expected (bag-of-words mock embeddings). Rehearse the flow in mock mode, calibrate live |
