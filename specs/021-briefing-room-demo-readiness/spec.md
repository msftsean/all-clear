# Feature Specification: Briefing Room Demo Readiness

**Feature Branch**: `020-glass-box-audit` (documented retroactively; no new
branch was created — see Note below)
**Created**: 2026-09-20
**Status**: Implemented
**Input**: User description: "remove the capstone option from the ui. on the
live calls page, remove the phone number as each participant's number will be
different. adjust the language" followed by iterative follow-ups: fix the
BriefingRoom header overlapping the Canvas panel, center-justify the header
rows, clarify or remove the confusing chat/phone channel toggle, and move the
Live Calls phone-transcript monitor to its own standalone URL so it is not
part of the main triage app during the event.

**Note on branch**: This record was authored after the described changes were
already implemented and pushed directly to `020-glass-box-audit` (commit
`847a5f7`), continuing that branch's existing pattern of accumulating related
increments rather than creating a new per-increment branch. No `021-*` branch
exists; the `021-` prefix here only orders this Spec Kit record after
`020-glass-box-audit`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Presenter runs the main triage demo without dead-end UI (Priority: P1)

A facilitator runs the BriefingRoom app in front of an audience (state/local
government hackathon participants) to demonstrate signal intake, dedup, and
incident routing. Every visible control must do something real and legible at
a glance — no half-finished lead-capture form, no header buttons that overlap
the ClearBoard/Canvas panel, and no toggle whose two states are unexplained.

**Why this priority**: This is the primary demo surface for the event. Visible
clutter, dead controls, or a broken layout directly undermines trust in the
product during a live audience demo.

**Independent Test**: Load the BriefingRoom app in a browser at various widths
(desktop ~980px, mobile ~375px). Confirm: (a) no "capstone" button/form is
present anywhere, (b) the header's two button rows are centered and never
overlap or bleed into the right-hand Canvas panel, (c) the "Live channel
strip" only shows Muni Water surge / Clear board — no channel toggle.

**Acceptance Scenarios**:

1. **Given** the BriefingRoom app is loaded, **When** the presenter looks at
   the header, **Then** they see History, Trust, and Live Calls status/health
   badges arranged in two centered rows with no visual overlap with the
   ClearBoard/Canvas panel, at both desktop and mobile widths.
2. **Given** the BriefingRoom app is loaded, **When** the presenter searches
   the UI for a "capstone" control, **Then** none exists — the feature and its
   dead API/type plumbing have been removed.
3. **Given** the presenter is typing a signal into the compose box, **When**
   they look at the "Live channel strip," **Then** they see only "Muni Water
   surge" and "Clear board" — no chat/phone tagging control that implied an
   active call was in progress.

---

### User Story 2 - AV/demo operator runs the live phone-call demo independently (Priority: P1)

During the event, a presenter wants to actually call into the All Clear phone
line and have the audience watch the live transcript stream in on a second
screen or browser tab, decoupled from the main BriefingRoom demo so the two
can run side by side (e.g., one laptop showing chat/incident triage, a second
screen/projector showing the live call).

**Why this priority**: The live phone-call demo is the most compelling part of
the presentation ("dial in and watch the transcript appear"), and it must be
reliably reachable on its own URL so it can be opened on a dedicated
screen/projector without any BriefingRoom chrome getting in the way.

**Independent Test**: Navigate directly to `/phone` (no prior navigation
through the main app required). Confirm the live call monitor renders
full-screen with no phone number displayed, and that the main BriefingRoom app
(`/`) no longer has any control that opens it in-app.

**Acceptance Scenarios**:

1. **Given** a browser is pointed at `/phone`, **When** the page loads,
   **Then** the full-screen live call monitor appears showing a generic
   "Caller line" label (no specific phone number) and a "waiting for a call"
   empty state that doesn't reference any number.
2. **Given** a real call comes in on the All Clear voice line, **When** the
   operator is viewing `/phone`, **Then** the transcript streams in in real
   time exactly as it did when this view was reachable from inside the main app.
3. **Given** a presenter is in the main BriefingRoom app (`/`), **When** they
   look at the header, **Then** there is no "Live Calls" button — the feature
   is only reachable by navigating to `/phone` directly.

---

### Edge Cases

- What happens when `/phone` is visited with no call in progress? → Existing
  "Pane of glass — waiting for a call" empty state renders; copy no longer
  references a specific phone number (see FR-004).
- What happens on narrow (mobile) viewports where the header would otherwise
  wrap awkwardly? → Both header rows use `flex-wrap` and `justify-center`
  inside an `overflow-hidden` column, so status pills (e.g., the model badge,
  which is intentionally `sm:`-only) hide or wrap without visually bleeding
  into the adjacent Canvas panel.
- What happens to conversation-history/audit records that were tagged with a
  `channel` of `"phone"` before this change? → Not affected; this change only
  removes the *UI* control for tagging future demo signals. The backend
  `channel` field, schemas, and audit behavior are untouched (see FR-006).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The BriefingRoom UI MUST NOT present any capstone lead-capture
  control (toggle button, form, or CSV/JSON export links).
- **FR-002**: The BriefingRoom header MUST render its controls (History,
  Trust, Live Calls status pills) across two `flex-wrap`, center-justified
  rows that never visually overlap the adjacent Canvas/ClearBoard panel, at
  both desktop and mobile viewport widths.
- **FR-003**: The BriefingRoom UI MUST NOT present a chat/phone "channel"
  toggle in the Live channel strip; signals submitted through the compose box
  MUST continue to be tagged with channel `"chat"` by default.
- **FR-004**: The Live Calls page MUST NOT display any specific phone number
  (header or empty-state copy); it MUST instead use a generic label (e.g.
  "Caller line") and describe waiting for a call without naming a number.
- **FR-005**: The Live Calls experience MUST be reachable at a standalone
  `/phone` route, and MUST NOT be reachable via any control inside the main
  BriefingRoom app (`/`).
- **FR-006**: None of the above UI changes MAY alter backend classification,
  routing, severity, escalation, or audit behavior — the `channel` field
  continues to exist end-to-end (API contract unchanged), only the UI control
  for setting it to `"phone"` is removed.

### Incident-Triage and Safety Constraints *(mandatory when behavior touches the pipeline)*

- **Authority impact**: None. QueryAgent, RouterExecutor, and ActionAgent
  boundaries are untouched — every change in this record is presentational
  (React components) or removes an unused UI control. No backend Python file
  changed.
- **Escalation impact**: Unchanged. SEV1/statutory-clock/PII/safety escalation
  triggers do not depend on any of the removed UI (capstone form, channel
  toggle) or the moved Live Calls page.
- **Data impact**: No new PII surface. The capstone removal deletes a demo
  lead-capture form that collected name/agency/free-text fields client-side;
  no retained data or audit trail is affected since the backend capstone
  routes/service were intentionally left in place (frontend-only removal).
- **Mock-mode impact**: No change — all affected surfaces (BriefingRoom,
  LiveCalls) already run fully in mock mode without Azure credentials, and
  continue to do so.
- **Grounding impact**: N/A — no factual/citation-bearing output changed.

### Key Entities *(include if feature involves data)*

- **Signal/`channel` field**: Existing backend field (`"chat"` | `"phone"` |
  `"voice"` | `"report"`) recording how a signal was reported; unchanged by
  this record. Only the frontend control that let a demo operator manually set
  it to `"phone"` while typing was removed, since it never captured or
  simulated a real call.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Loading `/` shows zero elements with `capstone` in their
  `data-testid`, verified by `grep -rin capstone frontend/src frontend/tests`
  returning no matches.
- **SC-002**: At both 980px and 375px viewport widths, the BriefingRoom header
  renders with no bounding-box overlap between the button rows and the Canvas
  panel (verified visually via Playwright screenshot in this session; no
  automated visual-regression test added).
- **SC-003**: Loading `/phone` directly (no prior navigation) renders the live
  call monitor; loading `/` shows no control that opens it in-app, verified by
  `grep -rn "live-calls-toggle\|LiveCalls" frontend/src` showing only the
  component definition and the `/phone` route wiring.
- **SC-004**: `cd frontend && npm run build` completes with no TypeScript or
  build errors after all changes (verified in-session, multiple times).
- **SC-005**: Verification commands — `cd frontend && npx tsc --noEmit` and
  `cd frontend && npm run build` — both exit 0.
