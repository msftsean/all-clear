---
description: "Task list for 005 Hackathon Site UX (mobile nav, a11y, 404)"
---

# Tasks: Hackathon Site Mobile Nav, Accessibility & 404 Handling

> ✅ **STATUS: COMPLETE (2026-05-31).** All 19 tasks implemented, live, and verified.
> The work landed on `main` (PR #3, `c934567`), not a separate `005-` branch.
> Evidence: `HUB_LINKS` shared nav, `MobileNav.tsx` disclosure, `Layout.tsx` skip-link +
> `#main-content` + labelled landmarks, `index.css` `.skip-link`/`:focus-visible`,
> `App.tsx` `path="*"` → `NotFound.tsx`. Playwright (chromium + mobile) green for all
> three stories (mobile nav, a11y skip-link/landmarks, 404). Full suite 43 passed / 5 skipped.

**Input**: Design documents from `/specs/005-hackathon-site-ux/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ui-behavior.md

**Tests**: Included. Per Constitution Principle V (Test-First), Playwright assertions for each
story's acceptance scenarios are written/un-skipped before or alongside implementation.

**Working dir (isolated worktree)**: `/workspaces/47doors-polish` on branch `005-hackathon-site-ux`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 = mobile nav, US2 = a11y, US3 = 404
- All paths are under `hackathon-site/`.

## Scope guard (applies to EVERY task)

- ✅ Allowed: `hackathon-site/src/**`, `hackathon-site/src/App.tsx`, `hackathon-site/src/index.css`, `hackathon-site/tests/e2e/site.spec.ts`, `specs/005-hackathon-site-ux/**`
- ⛔ Forbidden: `backend/**`, `labs/**`, `specs/002-*`, `specs/004-*`, any docs (`*.md` outside this spec dir), `hackathon-site/tests/e2e/coverage.spec.ts`, CI deploy/eval workflow logic.

---

## Phase 1: Setup (Shared Infrastructure)

- [x] T001 Confirm worktree + deps: `cd hackathon-site && npm install`; baseline `npx tsc --noEmit -p tsconfig.json` and `npm run build` succeed before changes.
- [x] T002 Extract canonical hub link set into a shared const `HUB_LINKS` (in `src/components/Layout.tsx` or a tiny `src/data/nav.ts`) matching data-model.md order: Pattern, Intents, Rules, Schedule. Refactor existing header nav to consume it (no behavior change).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Layout landmarks/skip-link target that both nav and a11y stories build on.

- [x] T003 In `src/components/Layout.tsx`, give `<main>` a stable `id="main-content"` and an `aria-label` (e.g. "Main content"); add `aria-label` to the existing `<header>` nav ("Primary"). (Foundational for US1 mount point + US2 target.)

---

## Phase 3: User Story 1 — Mobile navigation (Priority: P1) 🎯 MVP

**Goal**: Reach all four hub sections from any inner route on a ≤640px viewport.
**Independent test**: Playwright mobile project — open menu on `/pattern`, all links present, tapping navigates + closes, Escape closes + refocuses.

### Tests for US1

- [x] T004 [P] [US1] In `tests/e2e/site.spec.ts`, un-skip the existing mobile-nav test and assert C1 from contracts: toggle visible+`aria-expanded=false` on mobile, opens to show 4 links, link nav closes panel, Escape closes + returns focus, and toggle hidden / inline nav visible on desktop.

### Implementation for US1

- [x] T005 [US1] Create `src/components/MobileNav.tsx`: controlled disclosure per research D1 — `<button>` toggle (`sm:hidden`, `aria-expanded`, `aria-controls`, accessible name "Open menu"/"Close menu"), conditionally rendered `<nav aria-label="Mobile">` panel listing `HUB_LINKS`. Close on route change (`useLocation`), Escape (return focus to button). Use Tailwind theme tokens (maroon/gold/cream).
- [x] T006 [US1] Mount `<MobileNav />` in `Layout.tsx` header (only on non-home pages, alongside the brand link); keep existing inline `<nav className="hidden sm:flex">` untouched for desktop (FR-004).
- [x] T007 [US1] Verify: `npx tsc --noEmit`; `PORT=4399 npx playwright test` mobile + chromium projects green for US1 assertions.

**Checkpoint**: US1 independently demoable — phones can navigate the hub.

---

## Phase 4: User Story 2 — Keyboard & screen-reader access (Priority: P2)

**Goal**: Skip link, labelled landmarks, visible focus indicators.
**Independent test**: Playwright — first Tab focuses skip link; activating moves focus to `#main-content`; focus-visible indicator present; landmarks labelled.

### Tests for US2

- [x] T008 [P] [US2] In `tests/e2e/site.spec.ts`, add C2 assertions: Tab once → "Skip to main content" link focused + visible; activate → focus within `#main-content`; assert `header`/`main`/`footer`/mobile `nav` landmark roles/names exist.

### Implementation for US2

- [x] T009 [US2] In `Layout.tsx`, add a `.skip-link` anchor (`href="#main-content"`) as the first child of the root, before the header.
- [x] T010 [P] [US2] In `src/index.css`, add `.skip-link` styles (visually hidden until `:focus`, on-brand when focused) and a global `:focus-visible` outline using the gold token (research D3/D4).
- [x] T011 [US2] Ensure all interactive controls (links, MobileNav button) inherit/declare a visible `:focus-visible` indicator; add `focus-visible:ring` where the global outline is insufficient.
- [x] T012 [US2] Verify: keyboard pass manually per quickstart; `npx tsc --noEmit`; Playwright US2 assertions green.

**Checkpoint**: US1 + US2 deliver an accessible, mobile-navigable site.

---

## Phase 5: User Story 3 — Friendly 404 (Priority: P3)

**Goal**: Unknown routes render a friendly not-found page inside the layout.
**Independent test**: Playwright — `/no-such-page` shows /not found/i text + link to `/` within site chrome.

### Tests for US3

- [x] T013 [P] [US3] In `tests/e2e/site.spec.ts`, add C3 assertions: visit `/no-such-page` → text matches /not found/i and a link with href `/` is present; header/footer chrome still rendered.

### Implementation for US3

- [x] T014 [US3] Create `src/pages/NotFound.tsx`: friendly message + "Back to the doors" `<Link to="/">`, styled with theme tokens.
- [x] T015 [US3] In `src/App.tsx`, add `<Route path="*" element={<NotFound />} />` inside the `Layout` route. (Optionally render NotFound for unknown card slugs in `CardDetail`.)
- [x] T016 [US3] Verify: `npx tsc --noEmit`; Playwright US3 assertions green.

**Checkpoint**: All three stories complete.

---

## Phase 6: Polish & Cross-Cutting

- [x] T017 Full regression: `npm run build` + `npx tsc --noEmit` clean; `PORT=4399 npx playwright test` (all projects) green including non-regression contracts (6 cards on landing, card deep-links).
- [x] T018 Scope check (SC-005): `git diff --name-only origin/main` lists ONLY `hackathon-site/**` and `specs/005-hackathon-site-ux/**`.
- [x] T019 Commit `feat(hackathon-site): mobile nav + a11y pass + 404 page`, push branch `005-hackathon-site-ux`, open PR → main. Verify CI (Build/Deploy + Playwright Smoke) green; confirm live production URL after merge.

---

## Dependencies & Execution Order

- Setup (T001–T002) → Foundational (T003) → then stories.
- **US1 (T004–T007)** is the MVP and should land first.
- US2 (T008–T012) depends on T003 (main id) and ideally T005 (button to style) but can proceed in parallel on `index.css` (T010 is [P]).
- US3 (T013–T016) is independent of US1/US2 and can run anytime after Setup.
- Polish (T017–T019) last.

## Parallelizable

- T004, T008, T013 (test authoring in the same file — coordinate edits) and T010 (`index.css`) are marked [P] relative to component work in `.tsx` files.
