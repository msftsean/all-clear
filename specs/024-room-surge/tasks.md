# Tasks: Room Surge (024-room-surge)

**Input**: `spec.md`, `plan.md` in this directory.
**For the Copilot CLI**: the head-start patch is already applied. Your job is
verify → fix → finish. Do not weaken any Non-Negotiable in `CLAUDE.md`.

## Phase 0: Head-start patch (done, partly verified; see plan.md)

- [x] T001 `SurgeRoom` tally + unit tests (`backend/tests/test_surge_room.py`): 7/7 passed under a stdlib harness
- [x] T002 `/api/surge/{state,report,control}` router + settings + dependency wiring
- [x] T003 Route tests written (`backend/tests/test_surge_api.py`), **not yet run**
- [x] T004 Frontend: `/report`, `/surge`, `/surge/cards`, QR component, API client, vitest file
- [x] T005 `scripts/surge_rehearsal.py`: ran against a stand-in server, exit 0

## Phase 1: Verify the patch locally (Copilot CLI)

- [ ] T010 `cd backend && PYTHONPATH=. python -m pytest tests/test_surge_room.py tests/test_surge_api.py -q`, then fix any failures
- [ ] T011 Full backend suite stays green: `cd backend && PYTHONPATH=. python -m pytest tests/ -q`
- [ ] T012 `cd frontend && npm install && npm run build && npx vitest run src/allclear/surge`, then fix type errors (watch: `qrcode` types, `SEV` import, `ReactNode`)
- [ ] T013 Mock-mode smoke: run backend + `npm run dev`; open `/surge?coach=1`, Open; on a phone-sized viewport submit from `/report?card=A` twice with near-identical text → second shows "joined"; `/surge` updates; submit an injection from card R → "blocked by safety" increments
- [ ] T014 Screenshot `/surge` at 1920×1080, `/report` at 390×844 and `/surge/cards` print preview. Check readability from the back of a room (counter ≥ 96px, tiles legible)
- [ ] T015 Accessibility pass on `/report` (labels, focus ring, contrast, works with the keyboard mic)

## Phase 2: Live deployment and calibration (by Thu Nov 12)

- [ ] T020 `azd deploy`; pin backend to 1 replica; set `SURGE_COACH_KEY` secret
- [ ] T021 `python scripts/surge_rehearsal.py --base https://<frontend> --key $SURGE_COACH_KEY`, record the incident count per card and p95
- [ ] T022 If SC-001 fails, tune `DEDUP_THRESHOLD` (0.83 → 0.80 → 0.78), redeploy, rerun T021. Record the final value here. Make sure A to D don't merge into each other
- [ ] T023 Check quota/APIM headroom at 40 concurrency (no 429s or 503s in T021)
- [ ] T024 Real-phone test: 5+ people on cellular, not Wi-Fi

## Phase 3: Show readiness (by Fri Nov 13)

- [ ] T030 Short link for `/report`; print cards (`/surge/cards?copies=2`)
- [ ] T031 Dry run the 7-minute run of show with Adrian/Brian, including the fallback switch to the replay
- [ ] T032 Reset the room after the dry run; confirm `/api/surge/state` is empty on the morning of Nov 17
