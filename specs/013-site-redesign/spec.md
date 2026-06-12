# Feature Specification: Public SWA Site Redesign

**Feature Branch**: `013-site-redesign`
**Created**: 2026-06-01
**Status**: Draft
**Input**: User description: "Redesign the three public SWA sites (workshop, coach, hackathon) to eliminate AI-slop design tells and fit each audience, using the Impeccable detector as the acceptance gate and Refero-style references."

## Context

Three public Azure Static Web Apps are live (React 18 + Vite 5 + Tailwind 3.4 + TypeScript):

- **workshop-site/** — executive briefing / workshop companion. Microsoft Fluent palette (blue `#0078D4` + IU crimson `#990000`) + Segoe UI.
- **coach-site/** — coach prep companion for facilitators. Currently inherits workshop's cold corporate Fluent palette — a mismatch for pastoral, supportive content.
- **hackathon-site/** — architecture reference site. Maroon/gold/cream + Playfair Display serif (already distinctive).

A baseline scan with `npx impeccable detect` found AI-generated design "tells": **workshop-site 30**, **coach-site 3**, **hackathon-site 1**. The dominant tell across all three is the left-accent-border card (`border-l-4`), Impeccable's #1 slop signal; workshop also has gray-on-color contrast issues.

This feature restyles each site to fit its audience and pass the Impeccable detector with **0 anti-patterns**, without changing content, breaking the build/deploy, or regressing accessibility. The AAD-gated internal `docs/` site is out of scope.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Workshop site reads as premium enterprise, not AI-generated (Priority: P1)

An executive or workshop attendee opens the workshop companion site. Instead of generic Microsoft-Fluent cards with thick left-accent borders, they see a calm, restrained, credibly-enterprise interface (Linear/Vercel/Stripe register): hairline borders, soft elevation, generous whitespace, a single restrained accent, and corrected text contrast.

**Why this priority**: workshop-site has by far the most anti-patterns (30) and is the most generic, so it delivers the largest objective and perceptual improvement. It is the executive-facing artifact where credibility matters most.

**Independent Test**: Run `npx impeccable detect workshop-site/src` → 0 anti-patterns; `npm run build` + Playwright e2e green; all 10 tab contents unchanged; site deploys via `deploy-workshop-swa.yml`.

**Acceptance Scenarios**:

1. **Given** the redesigned workshop site, **When** `npx impeccable detect workshop-site/src` runs, **Then** it reports 0 anti-patterns (exit 0).
2. **Given** the redesign, **When** the build and Playwright suite run, **Then** both pass and no tab's text content changed.
3. **Given** any card previously using `border-l-4`, **When** rendered, **Then** it uses a subtler treatment (hairline border, soft fill, or top rule) instead.
4. **Given** the previous `gray-600 on bg-blue-50` text, **When** rendered, **Then** contrast meets WCAG AA.

---

### User Story 2 - Coach site feels warm and human (Priority: P2)

A faculty/staff coach opens the coach prep site to prepare to support students. The interface feels warm, calm, and supportive (Notion/Headspace/Cal.com register) — a humane palette and type that reflect *cura personalis*, not a cold corporate dashboard.

**Why this priority**: the cold Fluent palette is an audience/tone mismatch; fixing it changes how the site *feels* for its specific users. Only 3 anti-patterns, so it is also a fast, visible win.

**Independent Test**: `npx impeccable detect coach-site/src` → 0 anti-patterns; `npm run typecheck` + `npm run build` + Playwright e2e green; all six sections' content unchanged; deploys via `deploy-coach-swa.yml`.

**Acceptance Scenarios**:

1. **Given** the redesigned coach site, **When** `npx impeccable detect coach-site/src` runs, **Then** 0 anti-patterns.
2. **Given** the redesign, **When** typecheck/build/Playwright run, **Then** all pass and the six sections' text + `source:` declarations are unchanged.
3. **Given** the new palette, **When** the page loads, **Then** it no longer uses Microsoft blue as the primary brand color.

---

### User Story 3 - Hackathon site refined while keeping its identity (Priority: P3)

A developer/attendee opens the architecture reference site. Its existing editorial-academic identity (maroon/gold/cream serif) is preserved but refined (Stripe Press / Linear Docs register): the one side-tab tell is removed and the overused body font is replaced with a warmer text face.

**Why this priority**: only 1 anti-pattern and the identity is already strong, so this is the smallest-effort polish, done last.

**Independent Test**: `npx impeccable detect hackathon-site/src` → 0 anti-patterns; `npm run build` + existing e2e green; brand palette + serif identity retained; deploys via `deploy-hackathon-swa.yml`.

**Acceptance Scenarios**:

1. **Given** the refined hackathon site, **When** `npx impeccable detect hackathon-site/src` runs, **Then** 0 anti-patterns.
2. **Given** the refinement, **When** the build and e2e run, **Then** both pass and the maroon/gold editorial identity is retained.

---

### Edge Cases

- What happens if a redesign would change rendered text or remove content? → Not allowed; only presentation (color, type, spacing, borders, elevation, motion) may change.
- What happens if removing `border-l-4` reduces an element's semantic emphasis? → Replace with an accessible alternative (heading, soft fill, top rule) that preserves the information hierarchy.
- What happens if a new palette reduces contrast? → Reject; all text/UI must keep WCAG AA contrast.
- What happens if Impeccable flags a new tell introduced by the redesign? → Iterate until detect = 0 before the site is considered done.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Each in-scope site MUST pass `npx impeccable detect <site>/src` with 0 anti-patterns.
- **FR-002**: The redesign MUST NOT change any rendered text/content, including coach-site section `source:` declarations and content-map drift contract.
- **FR-003**: Each site MUST continue to pass its existing build (`npm run build`), typecheck where present, and Playwright e2e suite.
- **FR-004**: All text and interactive elements MUST meet WCAG AA contrast (Constitution Principle VI).
- **FR-005**: The `border-l-4` side-tab pattern MUST be eliminated from all in-scope sites.
- **FR-006**: workshop-site MUST fix the `gray-600 on bg-blue-50` (gray-on-color) contrast finding.
- **FR-007**: coach-site MUST adopt a warm, human palette/type distinct from Microsoft Fluent blue.
- **FR-008**: hackathon-site MUST retain its maroon/gold/cream + serif editorial identity while removing its one tell and replacing the overused body font.
- **FR-009**: Each site's deploy artifact (incl. `staticwebapp.config.json`) and deploy workflow MUST remain intact and functional.
- **FR-010**: Changes MUST be limited to each site's own folder (no cross-site or backend/labs changes).

### Key Entities

- **Per-site DESIGN.md brief**: the target visual system for a site (palette tokens, type scale, spacing, component treatments, motion), anchored to a named Refero reference. Produced in the plan.
- **Impeccable finding**: a detected anti-pattern (rule id, file, line) used as the objective gate; target count per site is 0.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `npx impeccable detect` reports 0 anti-patterns for each in-scope site (down from 30 / 3 / 1).
- **SC-002**: 100% of each site's existing automated tests (build, typecheck, Playwright e2e) pass after redesign.
- **SC-003**: 0 rendered-text/content diffs versus pre-redesign (presentation-only changes).
- **SC-004**: 0 WCAG AA contrast violations in changed UI.
- **SC-005**: Each redesigned site deploys successfully via its existing workflow.
