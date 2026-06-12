# UI Behavior Contracts — 005 Hackathon Site UX

These are observable behavior contracts verified by Playwright (`tests/e2e/site.spec.ts`).

## C1 — Mobile nav (Story 1)

- **Given** viewport width ≤ 640px on a non-home route
  - A control with an accessible name ("Open menu") and `aria-expanded="false"` is visible.
  - The desktop inline nav links are NOT visible.
- **When** the control is activated
  - `aria-expanded` becomes `"true"`; a `nav` panel with links Pattern, Intents, Rules, Schedule is visible.
- **When** a panel link is activated
  - The app navigates to that route AND the panel is no longer visible.
- **When** `Escape` is pressed while open
  - The panel closes and focus returns to the toggle.
- **Given** viewport width ≥ 640px
  - The toggle is NOT visible; the inline header nav IS visible (desktop unchanged).

## C2 — Accessibility (Story 2)

- The first Tab from page load focuses a visible "Skip to main content" link.
- Activating the skip link moves focus to `#main-content`.
- `header`, mobile `nav`, `main`, and `footer` landmarks exist with accessible names.
- Focused interactive elements show a visible focus indicator (`:focus-visible`).

## C3 — 404 (Story 3)

- Navigating to `/no-such-page` renders text matching /not found/i and a link with href `/`.
- The site `header`/`footer` chrome still renders around the 404 content.

## Non-regression contracts

- Landing (`/`) still shows 6 cards and the HubNav.
- Card deep-links (`/cards/:slug`) still render the corresponding card.
- `tsc --noEmit` clean; `npm run build` succeeds.
