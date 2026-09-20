# Implementation Plan: Briefing Room Demo Readiness

**Branch**: `020-glass-box-audit` | **Date**: 2026-09-20 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/021-briefing-room-demo-readiness/spec.md`

**Status**: Already implemented and pushed (commit `847a5f7` on
`020-glass-box-audit`). This plan documents the approach actually taken; there
is no forward-looking implementation work remaining for this record.

## Summary

Clean up the BriefingRoom demo surface ahead of the AI event: remove the
unfinished capstone lead-capture UI, fix a header layout bug where controls
overlapped the Canvas panel, remove a channel toggle that implied a live phone
call was active when it only tagged metadata, and relocate the real live
phone-call monitor to its own `/phone` route so it can be demoed on a separate
screen without cluttering or being confused with the main triage app.

## Technical Context

**Language/Version**: TypeScript 5, React 18
**Primary Dependencies**: Vite 5, Tailwind CSS (existing `frontend/` stack; no
new dependencies added)
**Storage**: N/A — no persistence changes; backend `channel` field and
capstone routes/service untouched
**Testing**: `frontend/tests/e2e/chat.spec.ts` (Playwright), `npx tsc --noEmit`,
`npm run build`; verified manually in-session with Playwright screenshots at
980px and 375px viewports (no new automated visual-regression test added)
**Target Platform**: Static web app served by nginx (`frontend/nginx.conf`) in
production, Vite dev server locally
**Project Type**: Web application (existing `backend/` + `frontend/` split;
this record only touches `frontend/`)
**Constraints**: Must not weaken PII/audit/escalation/RouterExecutor behavior;
must not require Azure credentials (mock mode); must not require a new
client-side router dependency
**Scale/Scope**: Single feature area (`frontend/src/allclear/BriefingRoom.tsx`,
`LiveCalls.tsx`, `Canvas.tsx`, `api.ts`, `types.ts`, `App.tsx`) plus one e2e
test file

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Data flow identifies PII handling, retention, audit events, and any
      embedding/external-service impact. → No PII/retention/audit change; the
      capstone form (client-side only) is removed, backend capstone
      routes/service and their data handling are untouched.
- [x] QueryAgent, RouterExecutor, and ActionAgent authority boundaries are
      unchanged or explicitly justified and tested. → Unchanged; zero backend
      Python files touched in this record.
- [x] Severity, statutory-clock, safety, PII, and human-request escalation
      behavior is preserved or expanded; no change weakens a trigger. →
      Preserved; the removed channel toggle never affected classification or
      escalation (confirmed by grep across `query_agent.py`, `router_agent.py`,
      `action_agent.py` — `channel` is passed through for audit only).
- [x] Mock mode validates the same authority boundaries without Azure
      credentials. → Unaffected; BriefingRoom and LiveCalls both continue to
      run fully in mock mode.
- [x] Sitreps or factual output identify their source-record/citation
      behavior. → N/A, no factual/citation output touched.
- [x] Relevant backend tests and frontend/companion typecheck-build commands
      are listed in the Verification Matrix. → See below.
- [x] The design uses the canonical terms in `CONTEXT.md` and introduces no
      retired support-domain concepts. → Confirmed; all UI copy uses
      "signal"/"incident"/"ClearBoard" language already in use.

## Project Structure

### Documentation (this feature)

```text
specs/021-briefing-room-demo-readiness/
├── spec.md   # User scenarios + requirements (this record)
├── plan.md   # This file
└── tasks.md  # Completed task ledger (Phase 2 output)
```

No `research.md`, `data-model.md`, `contracts/`, or `quickstart.md` were
produced — this is a small, already-shipped UI cleanup with no new data model,
API contract, or external integration.

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── App.tsx                      # added /phone standalone route
│   └── allclear/
│       ├── BriefingRoom.tsx         # removed capstone UI, channel toggle,
│       │                            # live-calls-toggle; restructured header
│       ├── LiveCalls.tsx            # removed hard-coded phone number/copy
│       ├── Canvas.tsx               # removed capstone-destination-link
│       ├── api.ts                   # removed submitCapstoneLead
│       └── types.ts                 # removed CapstoneLeadPayload/Entry
└── tests/
    └── e2e/
        └── chat.spec.ts             # removed capstone + channel-toggle tests
```

**Structure Decision**: Kept the existing `frontend/src/allclear/` structure;
no new files beyond this Spec Kit record and the route branch in `App.tsx`
(which follows the pre-existing `?page=clone` / `?page=audit` pattern already
used there — no new router dependency was introduced).

## Verification Matrix

| Surface | Command or check |
|---|---|
| Type safety | `cd frontend && npx tsc --noEmit` |
| Build | `cd frontend && npm run build` |
| No leftover capstone refs | `grep -rin capstone frontend/src frontend/tests` (expect no matches) |
| No leftover live-calls-in-app refs | `grep -rn "live-calls-toggle" frontend/src` (expect no matches) |
| `/phone` reachable | `curl -s -o /dev/null -w "%{http_code}" http://localhost:5173/phone` (expect 200, verified via Vite dev server and existing nginx SPA fallback `try_files $uri $uri/ /index.html;`) |
| Visual check | Playwright screenshots at 980px and 375px viewports (manual, in-session; no automated visual-regression test added) |

## Complexity Tracking

*No Constitution Check violations — this section is intentionally empty.*
