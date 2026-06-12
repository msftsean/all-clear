# Feature Specification: Coach Prep Companion Site

**Feature Branch**: `009-coach-prep-site`
**Created**: 2026-06-01
**Status**: Draft
**Input**: User description: "A site to be created to explain to the coaches how to prepare to help folks in the hackathon."

## Overview

A standalone, public companion website that gives **coaches/facilitators** a single, well-organized place to learn how to prepare for and run the 47 Doors AJCU hackathon. It surfaces the material that already exists in `coach-guide/` (FACILITATION.md, TALKING_POINTS.md, TROUBLESHOOTING.md, ASSESSMENT_RUBRIC.md, ajcu-framing.md) plus the cold-start head-start guidance (`docs/quickstart/HEADSTART.md`), presented as a calm, scannable, tab-based reference a coach can use on a laptop or phone before and during the event.

This mirrors the existing **`workshop-site/`** (React + Vite + Tailwind, tab-based) in look, tooling, and deploy pattern, but is aimed at coaches (how to prepare and help), not at executives (the value pitch) or participants (the labs).

## Scope & Boundaries

**In scope** (this feature adds a NEW site directory, e.g. `coach-site/`):

- A new static site (React + Vite + TypeScript + Tailwind), built to `dist/`.
- Content sourced from existing `coach-guide/*.md` and `docs/quickstart/HEADSTART.md` — re-presented for the web, not rewritten in substance.
- Its own `staticwebapp.config.json` (public site) and Azure SWA deploy workflow, following the pattern just established for `workshop-site/` in `deploy-workshop-swa.yml` (guarded, own token secret).
- A short README and provisioning note appended to `docs/deployment/SWA_PROVISIONING.md`.

**Out of scope** (DO NOT modify):

- `backend/`, `labs/`, agent code, evals, red-team suites.
- The existing `hackathon-site/`, `workshop-site/`, `docs/` site behavior.
- The substance of the coach guidance (this surfaces it; it does not author new policy).
- Any login/auth gating — this site is public.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A coach prepares the day before (Priority: P1)

A volunteer coach who has not run this hackathon before opens the site the night before. They need a clear, ordered picture of what to do to be ready: the room/tech pre-flight checklist, the day's timeline, the mission framing, and where the cold-start head-start fits so participants don't get stuck in setup.

**Why this priority**: Preparation is the entire point of the request ("how to prepare to help folks"). A coach who lands on the site cold must reach "I know what to do tomorrow" without reading raw markdown in the repo. This is the MVP — if only this ships, the site already delivers its core value.

**Independent Test**: Load the deployed site, land on a "Prepare" view, and confirm a coach can read the pre-flight checklist, the timeline, and the framing without leaving the site or opening the repo. Delivers value even if Stories 2–3 are absent.

**Acceptance Scenarios**:

1. **Given** the site home/landing, **When** a coach arrives, **Then** they see a concise "what this is / how to use it" intro and clearly labeled sections (e.g. Prepare, Timeline, Framing, Help Participants, Troubleshooting, Assess).
2. **Given** the Prepare section, **When** the coach reads it, **Then** they see the room-setup + technical + pre-flight checklists (from FACILITATION.md) rendered as readable, scannable lists.
3. **Given** any inner section on a ≤640px phone viewport, **When** the page renders, **Then** navigation between sections is reachable (mobile nav), matching the accessibility bar set for the other sites.

---

### User Story 2 - A coach unblocks a stuck participant during the event (Priority: P2)

Mid-event, several participants hit the same Azure/setup error. The coach needs a fast triage reference: the common failures and their <5-minute fixes, plus the cold-start lanes (shared backend / azd / mock) so a blocked team can keep moving toward the scenarios.

**Why this priority**: The request is specifically about helping *folks* in the hackathon, not just self-prep. The troubleshooting + head-start content is the highest-leverage in-event aid, but it builds on the Prepare MVP.

**Independent Test**: From the deployed site, open a "Troubleshooting / Help" view and confirm a coach can find the Azure conditional-access escalation playbook and the three cold-start lanes quickly (search or clear section anchors).

**Acceptance Scenarios**:

1. **Given** the Troubleshooting section, **When** a coach scans it, **Then** common issues (Python/Node versions, Azure conditional access, subscription/RBAC, `azd up` registration) appear with symptom → quick fix.
2. **Given** the Help/Head-start section, **When** a coach reads it, **Then** the three cold-start lanes (shared backend, self-serve azd, mock) and the "scenario-ready" definition are presented, linking to `docs/quickstart/HEADSTART.md` for depth.

---

### User Story 3 - A coach frames and assesses the build sprint (Priority: P3)

A coach wants the 60-second mission pitch (cura personalis, the six intents) to open the sprint, plus the assessment rubric and talking points for phase transitions.

**Why this priority**: Valuable for coaching quality and consistency, but a coach can run a successful day with Stories 1–2 alone. This rounds out the site.

**Independent Test**: From the deployed site, open Framing/Assess views and confirm the mission pitch, six-intent rationale, talking points, and rubric summary are present.

**Acceptance Scenarios**:

1. **Given** the Framing section, **When** the coach reads it, **Then** the 60-second mission pitch and the six-intent rationale (from ajcu-framing.md) are shown faithfully.
2. **Given** the Assess section, **When** the coach reads it, **Then** the assessment rubric criteria and talking-point transitions are summarized with a link to the full guides.

### Edge Cases

- **Stale content drift**: the site re-presents `coach-guide/` content; if a guide changes, the site must be easy to update (single content source per section, not scattered copies).
- **Offline/flaky venue Wi-Fi**: the site is static and self-contained (no runtime API calls), so it loads from the CDN/edge without a backend.
- **Phone-only coach**: must be readable and navigable at 375px.
- **Deploy-before-Azure**: the deploy workflow must no-op safely until its token secret is set (same guard as `workshop-site`).
- **Deep-link/refresh on an inner route**: SPA navigation fallback must serve `index.html` (no 404 on refresh).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The site MUST present coach-preparation content organized into clearly labeled sections covering, at minimum: Prepare (checklists), Timeline, Framing, Help Participants (head-start), Troubleshooting, and Assess.
- **FR-002**: The site MUST source its substance from the existing `coach-guide/*.md` and `docs/quickstart/HEADSTART.md` material, presented faithfully (no invented policy).
- **FR-003**: The site MUST be a self-contained static build with no runtime backend dependency.
- **FR-004**: The site MUST be responsive and navigable on phone (≤640px) and desktop, with accessible navigation (keyboard reachable, semantic landmarks), consistent with the other sites' accessibility bar.
- **FR-005**: The site MUST deploy to its own Azure Static Web App via a guarded GitHub Actions workflow that no-ops with a clear message until its own deployment-token secret is set (NOT reusing another site's token).
- **FR-006**: The site MUST include a public `staticwebapp.config.json` (anonymous access) with SPA navigation fallback and the standard security headers used by the sibling sites.
- **FR-007**: Provisioning steps to create the SWA, capture its URL, and set the token secret MUST be documented (extend `docs/deployment/SWA_PROVISIONING.md`).
- **FR-008**: The build MUST be verifiable locally (`npm ci && npm run build` produces `dist/` including `staticwebapp.config.json`).

### Key Entities

- **Section**: a coach-facing topic area (Prepare, Timeline, Framing, Help, Troubleshooting, Assess) with a title, ordering, and rendered content derived from a coach-guide source.
- **Checklist item**: a single actionable pre-flight/setup task with a checked/unchecked visual (from FACILITATION.md).
- **Troubleshooting entry**: symptom → cause → quick fix (from TROUBLESHOOTING.md).
- **Head-start lane**: one of the three cold-start paths (shared backend / azd / mock) with its "scenario-ready" outcome.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A first-time coach can, from the landing view, reach the full pre-flight checklist and the day timeline in **2 clicks or fewer**.
- **SC-002**: During the event, a coach can locate the fix for a given setup error (e.g. Azure conditional access) in **under 30 seconds** via clear section anchors or search.
- **SC-003**: The site loads and is fully usable with **no backend/API** running (verified by serving the static `dist/` alone).
- **SC-004**: All six required sections (FR-001) are present and render their content faithfully from the coach-guide sources.
- **SC-005**: The site is usable at a **375px** viewport: all sections reachable, no horizontal scroll, navigation operable by keyboard.
- **SC-006**: The deploy workflow is merge-safe before Azure exists (no-ops cleanly without its token secret) and, once provisioned, publishes the site at its SWA URL.
