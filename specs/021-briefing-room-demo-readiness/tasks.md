---

description: "Task ledger for Briefing Room Demo Readiness — retroactive record of already-completed work"
---

# Tasks: Briefing Room Demo Readiness

**Input**: Design documents from `/specs/021-briefing-room-demo-readiness/`
**Prerequisites**: plan.md, spec.md (both in this directory)

**Status**: All tasks below are already complete, implemented and pushed as
commit `847a5f7` on branch `020-glass-box-audit`. This ledger is a retroactive
record (per the repo's Spec Kit convention of tracking behavior changes),
not a forward-looking backlog.

**Tests**: Manual verification via `npx tsc --noEmit`, `npm run build`, grep
checks, and Playwright screenshots at 980px/375px viewports (see plan.md's
Verification Matrix). One e2e test file was updated to drop assertions for
removed controls.

## Phase 1: Remove capstone lead-capture UI (User Story 1)

- [x] T001 [US1] Remove `capstone-toggle` button, `capstoneForm/capstoneBusy/capstoneSaved/capstoneOpen` state, `CAPSTONE_INITIAL`, `submitCapstone()`, and the `CapstoneCapture` component from `frontend/src/allclear/BriefingRoom.tsx`
- [x] T002 [P] [US1] Remove `capstone-destination-link` anchor from `frontend/src/allclear/Canvas.tsx`
- [x] T003 [P] [US1] Remove `submitCapstoneLead` from `frontend/src/allclear/api.ts`
- [x] T004 [P] [US1] Remove `CapstoneLeadPayload`/`CapstoneLeadEntry` from `frontend/src/allclear/types.ts`
- [x] T005 [US1] Remove "renders capstone capture + export controls" test from `frontend/tests/e2e/chat.spec.ts`

**Checkpoint**: No `capstone` reference remains anywhere under `frontend/src`
or `frontend/tests` (verified via grep). Backend `capstone_leads.py` and
routes intentionally untouched (out of scope per user decision).

---

## Phase 2: Fix header overlap + center-justify rows (User Story 1)

- [x] T006 [US1] Split the single non-wrapping header row in `frontend/src/allclear/BriefingRoom.tsx` into two `flex flex-wrap` rows (nav buttons; status pills) so content wraps inside the fixed-width column instead of bleeding into the Canvas panel
- [x] T007 [P] [US1] Add `overflow-hidden` to the column container and `whitespace-nowrap` to `ModelStatusBadge` text as layout safety nets
- [x] T008 [US1] Change both header rows from left/`ml-auto`-right split to `justify-center` per explicit follow-up request; remove the now-unneeded `ml-auto` wrapper span
- [x] T009 [US1] Verify via Playwright screenshots at 980px and 375px viewports — no overlap, both rows centered

**Checkpoint**: Header renders cleanly at desktop and mobile widths with no
visual overlap with the Canvas/ClearBoard panel.

---

## Phase 3: Remove the confusing chat/phone channel toggle (User Story 1)

- [x] T010 [US1] Remove `channel` state, the `channel-toggle` button, `Msg.channel` field, and the dead `m.channel === "phone"` tag rendering in `frontend/src/allclear/BriefingRoom.tsx`
- [x] T011 [US1] Hardcode `"chat"` as the literal channel argument to `submitSignal` (backend contract/behavior unchanged — `channel` was never used for classification/routing/escalation, only recorded as `input_modality` for audit; confirmed via grep across `backend/app/agents/query_agent.py`, `router_agent.py`, `action_agent.py`)
- [x] T012 [P] [US1] Repurpose the `Waveform` animation in the live-channel strip to reflect `busy` (pipeline actively processing) instead of the removed channel state
- [x] T013 [US1] Remove "supports channel toggling" test from `frontend/tests/e2e/chat.spec.ts`

**Checkpoint**: The Live channel strip shows only "Muni Water surge" / "Clear
board" — no control implying an active/simulated phone call.

---

## Phase 4: Move Live Calls to a standalone `/phone` route (User Story 2)

- [x] T014 [US2] Remove the hard-coded `PHONE_DISPLAY` constant (`+1 (844) 207-0169`) and its three usages (header badge, empty-state heading, "dial ... to watch" copy) from `frontend/src/allclear/LiveCalls.tsx`
- [x] T015 [US2] Replace the header phone display with a generic "Caller line" label; reword the empty state to "transcripts will appear here the moment a participant calls in" (no number referenced)
- [x] T016 [US2] Add a `window.location.pathname === "/phone"` branch in `frontend/src/App.tsx` (following the existing `?page=clone`/`?page=audit` pattern already used there — no new router dependency) rendering `<LiveCalls onExit={() => window.location.assign("/")} />` as a standalone full-screen page
- [x] T017 [US2] Remove the "📞 live calls" button, `liveOpen` state, the `<LiveCalls onExit=.../>` overlay block, and the now-unused `LiveCalls` import from `frontend/src/allclear/BriefingRoom.tsx` — Live Calls is no longer reachable from inside the main app
- [x] T018 [US2] Confirm `/phone` resolves via the existing SPA fallback (`frontend/nginx.conf`: `try_files $uri $uri/ /index.html;` in production; Vite dev server's default SPA fallback locally) — no server config changes needed
- [x] T019 [US2] Verify via Playwright screenshots that `/` shows no live-calls control and `/phone` renders the full standalone live call monitor

**Checkpoint**: Live Calls is reachable only at `/phone`, independent of the
main BriefingRoom app, ready to be projected on a separate screen during the
event.

---

## Phase 5: Final verification (cross-cutting)

- [x] T020 `cd frontend && npx tsc --noEmit` — clean, no type errors
- [x] T021 `cd frontend && npm run build` — clean build (only pre-existing,
  unrelated Tailwind CSS gradient-syntax warnings)
- [x] T022 `git add` the seven changed source/test files (screenshot dump
  folders explicitly excluded), commit, and push to `origin/020-glass-box-audit`
  (commit `847a5f7`)

---

## Dependencies & Execution Order

Phases 1–4 each map to independently-testable slices of User Story 1 (Phases
1–3) or User Story 2 (Phase 4); all were completed sequentially in a single
session and landed together in commit `847a5f7`. Phase 5 (verification) gates
the commit/push and was re-run after every phase.

## Notes

- This ledger intentionally has no open/pending tasks — it exists so future
  contributors and any AI agent working this repo during the event can see
  *why* capstone, the channel toggle, and the in-app Live Calls button are
  gone, and *where* the live phone demo now lives (`/phone`), without needing
  to re-derive it from chat history.
- If further changes are needed (e.g., adding automated visual-regression
  coverage for the header layout), open a new Spec Kit record rather than
  reopening this one.
