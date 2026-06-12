# Tasks: Public SWA Site Redesign

**Input**: Design documents from `specs/013-site-redesign/`
**Prerequisites**: plan.md, spec.md, contracts/design-briefs.md

**Tests**: This feature reuses each site's existing Playwright e2e + build/typecheck. The objective design gate is `npx impeccable detect <site>/src` = 0. No new unit tests are written (presentation-only); existing suites must stay green.

**Organization**: Tasks grouped by user story. Stories are independent and shippable one-at-a-time in priority order (P1 → P2 → P3).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel (different files, no incomplete deps)
- **[Story]**: US1 = workshop, US2 = coach, US3 = hackathon

## Path Conventions

Each site is a standalone Vite app at repo root: `workshop-site/`, `coach-site/`, `hackathon-site/`.

---

## Phase 1: Setup (Shared)

- [ ] T001 Record Impeccable baseline counts for all three sites: run `npx --yes impeccable@2.3.2 detect workshop-site/src`, `... coach-site/src`, `... hackathon-site/src` and note findings (expected 30/3/1) in the PR description.
- [ ] T002 Confirm each site builds clean pre-change: `cd workshop-site && npm ci && npm run build`, repeat for `coach-site` (+ `npm run typecheck`) and `hackathon-site`.

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T003 Read `specs/013-site-redesign/contracts/design-briefs.md` and treat each site's brief as the source of truth for palette/type/spacing/component tokens.
- [ ] T004 Define the shared anti-pattern checklist (from design-briefs.md "Shared anti-pattern checklist") as the per-site exit criteria: detect=0, AA contrast, no `border-l-4`, no gradient text, real type hierarchy.

**Checkpoint**: Briefs understood, baselines captured — user-story phases can begin.

---

## Phase 3: User Story 1 — Workshop site redesign (Priority: P1) 🎯 MVP

**Goal**: Restyle workshop-site to a calm, restrained enterprise register (Linear/Vercel/Stripe), eliminating all 30 Impeccable tells (esp. `border-l-4` side-tabs and gray-on-color text).

**Independent Test**: `npx impeccable detect workshop-site/src` = 0; `npm run build` green; `npx playwright test` green; visual review shows preserved hierarchy and unchanged copy.

- [ ] T005 [US1] Update `workshop-site/tailwind.config.js` theme.extend.colors to the P1 palette (ink, surface, surface-muted, border, brand `#0F6CBD`, demoted accent) and confirm a type scale; remove reliance on flat `#F3F2F1`.
- [ ] T006 [US1] Update `workshop-site/src/index.css` base styles: type scale/leading, focus-visible, link/transition tokens; ensure body text uses `ink` not gray-on-color.
- [ ] T007 [P] [US1] Replace `border-l-4` side-tab treatment in `workshop-site/src/tabs/ResponsibleAI.tsx` with hairline card + top-rule/soft-fill per brief; also fix the `text-gray-600 on bg-blue-50` contrast at ResponsibleAI.tsx (~line 170) → `text-ink/80`.
- [ ] T008 [P] [US1] Replace `border-l-4` in `workshop-site/src/tabs/ReuseAcrossCampus.tsx` with the brief's accent treatment.
- [ ] T009 [P] [US1] Replace `border-l-4` in `workshop-site/src/tabs/Telephony.tsx`.
- [ ] T010 [P] [US1] Replace `border-l-4` in `workshop-site/src/tabs/TrustBoundaries.tsx`.
- [ ] T011 [P] [US1] Replace `border-l-4` in `workshop-site/src/tabs/VoiceAccessibility.tsx`.
- [ ] T012 [P] [US1] Replace `border-l-4` in `workshop-site/src/tabs/YourFirstAgent.tsx`.
- [ ] T013 [US1] Sweep remaining `workshop-site/src/**` for any other `border-l-4`, gray-on-color, pure-black/white, or flat-hierarchy tells flagged by the detector; apply card/spacing/elevation tokens from the brief.
- [ ] T014 [US1] Gate: run `npx impeccable detect workshop-site/src` and iterate until 0 anti-patterns.
- [ ] T015 [US1] Verify: `cd workshop-site && npm run build && npx playwright test` green; diff-review confirms no rendered-text/content changes.
- [ ] T016 [US1] Open PR (workshop-site only) → CI green → squash-merge → confirm `deploy-workshop-swa.yml` runs → curl https://red-mud-0ca867e10.7.azurestaticapps.net returns 200.

**Checkpoint**: Workshop redesign shipped and live — MVP complete.

---

## Phase 4: User Story 2 — Coach site redesign (Priority: P2)

**Goal**: Re-tone coach-site from cold Microsoft-blue Fluent to a warm, human, pastoral register (Notion/Headspace/Cal.com), eliminating the 3 `border-l-4` tells and dropping microsoft-blue as primary.

**Independent Test**: `npx impeccable detect coach-site/src` = 0; `npm run typecheck && npm run build` green; `npx playwright test` green including a11y + content-drift; warm palette visible.

- [ ] T017 [US2] Update `coach-site/tailwind.config.js` to the P2 warm palette (ink, paper, surface, warm border, terracotta `brand`, `accent-soft`) and humanist `fontFamily`; remove microsoft-blue as primary brand color.
- [ ] T018 [US2] Update `coach-site/src/index.css`: warm base background/type, humanist font load, focus-visible; replace the `border-l-4` rule (~line 40) with a soft-fill callout style.
- [ ] T019 [US2] Replace `border-l-4` in `coach-site/src/App.tsx` (~line 67) with the brief's treatment, preserving layout/landmarks.
- [ ] T020 [US2] Replace `border-l-4` callouts in `coach-site/src/components/ContentBlocks.tsx` (~line 64) with `bg-accent-soft rounded-lg` + icon, preserving info/warn/success tone mapping and all block content.
- [ ] T021 [US2] Sweep `coach-site/src/**` for remaining tells; apply warm card/spacing tokens; keep skip link, single `<main>`, `aria-current`, focus-visible intact.
- [ ] T022 [US2] Gate: run `npx impeccable detect coach-site/src` and iterate until 0.
- [ ] T023 [US2] Verify: `cd coach-site && npm run typecheck && npm run build && npx playwright test` all green (a11y + content `source:` drift tests must pass); no text changes.
- [ ] T024 [US2] Open PR (coach-site only) → CI green → squash-merge → confirm `deploy-coach-swa.yml` runs → curl https://gray-ground-07a6ae510.7.azurestaticapps.net returns 200.

**Checkpoint**: Coach redesign shipped and live; warm pastoral tone distinct from workshop.

---

## Phase 5: User Story 3 — Hackathon site refinement (Priority: P3)

**Goal**: Refine hackathon-site to an editorial-academic polish (Stripe Press/Linear Docs) while KEEPING maroon/gold/cream + Playfair Display identity; remove the 1 `border-l-4` tell and swap overused Inter body font.

**Independent Test**: `npx impeccable detect hackathon-site/src` = 0; `npm run build` green; `npx playwright test` green; brand identity (maroon/gold/Playfair) preserved.

- [ ] T025 [US3] Remove the `border-l-4` rule in `hackathon-site/src/index.css` (~line 52); replace with a refined `border`/top-rule + serif label treatment per brief.
- [ ] T026 [US3] Swap the overused Inter body font in `hackathon-site/src/index.css` / `tailwind.config.js` for a warmer text face (e.g. Source Serif 4 / Geist / Söhne); KEEP Playfair Display headings and JetBrains Mono code.
- [ ] T027 [US3] Sweep `hackathon-site/src/**` for any remaining tells; ensure gold is accent-only (not body text) and body contrast is AA on cream/white.
- [ ] T028 [US3] Gate: run `npx impeccable detect hackathon-site/src` and iterate until 0.
- [ ] T029 [US3] Verify: `cd hackathon-site && npm run build && npx playwright test` green; brand tokens preserved; no content changes.
- [ ] T030 [US3] Open PR (hackathon-site only) → CI green → squash-merge → confirm `deploy-hackathon-swa.yml` runs → curl https://white-ground-0c80a6f10.7.azurestaticapps.net returns 200.

**Checkpoint**: All three sites redesigned, detect=0, live and verified.

---

## Phase 6: Polish & Cross-Cutting

- [ ] T031 [P] Confirm all three sites still pass `detect=0` together (re-run on each src) and capture final before/after findings counts.
- [ ] T032 [P] Verify all three live URLs return expected status (200) post-deploy and no console/asset 404s.
- [ ] T033 Update `specs/013-site-redesign/spec.md` Success Criteria checkboxes and note final results.

---

## Dependencies & Execution Order

- **Setup (P1 tasks T001-T002)** → **Foundational (T003-T004)** → user stories.
- **US1 (T005-T016)**, **US2 (T017-T024)**, **US3 (T025-T030)** are mutually independent (separate site folders) and could be done in parallel by separate agents, but ship in priority order P1→P2→P3 for incremental delivery.
- Within a story: theme/config (tailwind + index.css) before component sweeps; all edits before the detect gate; gate before verify; verify before PR/deploy.
- **Polish (T031-T033)** after all shipped stories.

## Parallel Opportunities

- US1 component tasks T007-T012 are all `[P]` (different tab files).
- The three user stories touch disjoint folders → can be delegated to parallel agents if desired.

## Implementation Strategy

**MVP = User Story 1 (workshop-site)** — highest baseline tell count (30) and primary audience; deliver and ship it fully before starting US2. Then US2 (coach, tone fix), then US3 (hackathon, light refinement). Each story is a self-contained PR + deploy.
