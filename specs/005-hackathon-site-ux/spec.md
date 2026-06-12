# Feature Specification: Hackathon Site Mobile Nav, Accessibility & 404 Handling

**Feature Branch**: `005-hackathon-site-ux`
**Created**: 2026-05-31
**Status**: Draft
**Input**: User description: "Finish the remaining pre-hackathon frontend polish on the reference site (hackathon-site/): mobile navigation, an accessibility pass (skip link, landmarks, focus-visible), and a friendly SPA 404 page. Do not touch backend, docs, e2e/red-team/eval work owned by the other CLI."

## Scope & Boundaries

**In scope** (this feature ONLY touches `hackathon-site/`):

- `hackathon-site/src/components/**`
- `hackathon-site/src/pages/**`
- `hackathon-site/src/App.tsx`
- `hackathon-site/src/index.css`
- `hackathon-site/tests/e2e/site.spec.ts` (this feature's own spec file)

**Out of scope** (owned by a parallel effort — DO NOT modify):

- Anything under `backend/`, `labs/`, `specs/002-*`, `specs/004-*`
- Documentation files (`DEPLOYMENT.md`, `CHANGELOG.md`, READMEs)
- `hackathon-site/tests/e2e/coverage.spec.ts` (owned by the other CLI)
- Red-team suites and eval packs under `backend/tests/**`
- CI workflow deploy/eval logic (only smoke-test assertions for this feature's UI may be referenced, not rewritten)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Navigate the hub on a phone (Priority: P1)

A conference attendee opens the reference site on their phone during a session. From any hub page (Pattern, Intents, Rules, Schedule, or a card detail) they need to jump to another hub section without scrolling back to the landing page or editing the URL.

**Why this priority**: The site is described as "mobile-first", yet the header navigation is hidden on small screens (`hidden sm:flex`). On a phone the only navigation off an inner page is the "47 Doors" brand link back home. This is the single biggest usability gap before the hackathon and blocks the core "browse the doors on your phone" journey.

**Independent Test**: Load any inner route at a mobile viewport (e.g. 375px), open the menu control, and confirm all four hub links are reachable and navigate correctly. Delivers value on its own even if Stories 2 and 3 are not done.

**Acceptance Scenarios**:

1. **Given** the site at a ≤640px viewport on `/pattern`, **When** the user activates the menu toggle, **Then** a menu listing Pattern, Intents, Rules, and Schedule appears.
2. **Given** the mobile menu is open, **When** the user taps a hub link, **Then** the app navigates to that route and the menu closes.
3. **Given** the site at a ≥640px viewport, **When** the page renders, **Then** the existing inline header nav is shown and no hamburger toggle is shown (no visual regression on desktop).
4. **Given** the mobile menu is open, **When** the user presses `Escape`, **Then** the menu closes and focus returns to the toggle.

---

### User Story 2 - Keyboard & screen-reader access (Priority: P2)

A keyboard-only or screen-reader user works through the site. They need to skip repeated navigation, understand page landmarks, and always see where keyboard focus is.

**Why this priority**: Closes the open accessibility task (T027) for the reference site. Important for an inclusive demo and for AJCU/Jesuit accessibility values, but the site is still usable without it, so it ranks below the P1 navigation gap.

**Independent Test**: Tab through a page with the keyboard and confirm: a "Skip to content" link appears on first Tab and jumps focus to the main region; every interactive element shows a visible focus ring; landmarks (`header`/`nav`/`main`/`footer`) are labelled.

**Acceptance Scenarios**:

1. **Given** a freshly loaded page, **When** the user presses Tab once, **Then** a visible "Skip to main content" link is focused, and activating it moves focus to the main content region.
2. **Given** any interactive element (link, button), **When** it receives keyboard focus, **Then** a clearly visible focus indicator is shown.
3. **Given** assistive technology, **When** it lists landmarks, **Then** the header nav, mobile nav, main, and footer are present and distinguishable via accessible names.

---

### User Story 3 - Friendly handling of unknown URLs (Priority: P3)

A user follows a stale or mistyped link (e.g. `/cards/does-not-exist` or `/typo`). Instead of a blank page, they should see a friendly "not found" message with a way back to the hub.

**Why this priority**: Improves resilience and polish. Lowest priority because the SWA `navigationFallback` already returns HTTP 200 for unknown paths; the failure today is a silent empty layout, not an error page — a degraded but non-blocking experience.

**Independent Test**: Visit a non-existent route and confirm a clearly worded "page not found" message and a working link back to `/` render inside the normal site chrome.

**Acceptance Scenarios**:

1. **Given** an unknown path such as `/no-such-page`, **When** it loads, **Then** a 404 page with an explanatory message and a "Back to the doors" link to `/` is shown within the site layout.
2. **Given** an unknown card slug such as `/cards/not-real`, **When** it loads, **Then** the user sees the not-found page (or an equivalent in-card not-found message) rather than a blank page.

### Edge Cases

- Mobile menu open when the route changes via the brand link → menu must close.
- Resizing from mobile (menu open) up to desktop → desktop nav shows; the mobile panel must not remain visibly stuck open.
- Skip link must be visually hidden until focused (must not disrupt the visual design).
- 404 page must not break SWA deep-linking (server still returns index.html / 200).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: On viewports below the `sm` breakpoint, the site MUST provide an accessible menu control on inner (non-landing) pages that reveals navigation to Pattern, Intents, Rules, and Schedule.
- **FR-002**: The menu control MUST expose correct ARIA state (`aria-expanded`, `aria-controls`, accessible name) and MUST be operable by keyboard (Enter/Space to toggle, Escape to close).
- **FR-003**: Selecting a link in the mobile menu MUST navigate to the route and dismiss the menu; a route change MUST dismiss the menu.
- **FR-004**: Desktop (≥`sm`) navigation behaviour MUST remain unchanged (no new control visible, existing inline links intact).
- **FR-005**: Every page MUST provide a "skip to main content" link that is visually hidden until focused and that moves focus to the main content region when activated.
- **FR-006**: The main content region MUST be a labelled `main` landmark with a stable id usable as the skip-link target.
- **FR-007**: Header navigation and mobile navigation MUST be `nav` landmarks with distinct accessible names.
- **FR-008**: All interactive elements MUST display a visible focus indicator via `:focus-visible` styling consistent with the site theme (maroon/gold/cream tokens).
- **FR-009**: The application MUST render a friendly 404 page for any unmatched route, including a link back to the landing page, within the standard site layout.
- **FR-010**: All changes MUST be confined to `hackathon-site/` files listed in scope and MUST NOT alter backend, docs, eval, red-team, or the other CLI's e2e files.

### Non-Functional Requirements

- **NFR-001**: `npx tsc --noEmit` MUST report zero errors after the change (SC-002 parity for the site).
- **NFR-002**: `npm run build` MUST succeed.
- **NFR-003**: The existing Playwright suite (chromium + mobile projects) MUST continue to pass, with the mobile-nav test un-skipped to cover Story 1.
- **NFR-004**: No new runtime dependencies SHOULD be added; implement with React + existing Tailwind tokens.

## Success Criteria *(mandatory)*

- **SC-001**: From any inner route at a 375px viewport, a user can reach all four hub sections using only the on-screen menu (no URL editing, no returning home).
- **SC-002**: Keyboard-only traversal of any page reveals a working skip link and a visible focus indicator on every interactive element; landmarks are labelled.
- **SC-003**: Visiting an unknown URL shows a friendly 404 page with a working link home instead of a blank layout.
- **SC-004**: `tsc --noEmit` and `npm run build` succeed, and the Playwright suite passes (including an un-skipped mobile-nav test).
- **SC-005**: `git diff` for the feature touches only files under `hackathon-site/` and `specs/005-hackathon-site-ux/`.

## Assumptions

- The reference site on `main` is the source of truth; work is based off `origin/main` in an isolated worktree/branch to avoid the parallel CLI's in-flight branch.
- Tailwind theme tokens (maroon, deep-maroon, gold, light-gold, cream, deep-cream, ink) and fonts are available and should be reused rather than introducing new colors.
- "Schedule" is the header label for the `/run-of-show` route (matches existing header nav).
