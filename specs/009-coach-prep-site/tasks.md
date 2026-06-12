---
description: "Task list for Coach Prep Companion Site"
---

# Tasks: Coach Prep Companion Site

**Input**: Design documents from `/specs/009-coach-prep-site/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: INCLUDED — the spec + constitution (Principle V, light) require a Playwright e2e smoke. No agent/unit behaviors exist; tests are limited to render/nav/a11y and a content-drift check.

**Organization**: Tasks grouped by user story (US1 P1 → US2 P2 → US3 P3) for independent, incremental delivery. MVP = US1.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on incomplete tasks)
- **[Story]**: US1 / US2 / US3 (user-story phases only)
- All paths are relative to repo root; the new site lives in `coach-site/`.

## Path Conventions

New static site `coach-site/` (sibling to `workshop-site/`): `coach-site/src/`, `coach-site/public/`, `coach-site/tests/e2e/`. Deploy workflow in `.github/workflows/`. Provisioning docs in `docs/deployment/`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Stand up the Vite + React + TS + Tailwind project by mirroring `workshop-site/`.

- [x] T001 Scaffold `coach-site/` by copying and adapting the `workshop-site/` toolchain files: `package.json` (rename to `47doors-coach-site`, keep React 18 / Vite 5 / Tailwind 3.4 / TypeScript 5 / @heroicons/react deps and `dev`/`build`/`preview`/`typecheck` scripts), `vite.config.ts`, `tsconfig.json`, `tsconfig.node.json`, `tailwind.config.js`, `postcss.config.js`, and `index.html` (update `<title>`/description to "47 Doors Coach Prep"). Then run `cd coach-site && npm install`.
- [x] T002 [P] Create `coach-site/public/staticwebapp.config.json` exactly per `contracts/site-routes.md` (public/anonymous, `navigationFallback` → `/index.html`, security headers; NO `auth`/`routes` gating).
- [x] T003 [P] Add Playwright to `coach-site`: install `@playwright/test` as a devDependency, add a `test:e2e` script, and create `coach-site/playwright.config.ts` that builds + serves `dist/` (or runs `vite preview`) and targets a chromium project, mirroring `hackathon-site/playwright.config.ts`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: The content type system, app shell, and shared/nav components every section depends on.

**⚠️ CRITICAL**: No user-story section work can begin until this phase is complete.

- [x] T004 [P] Define the content model in `coach-site/src/content/types.ts`: `Section` (`id`, `title`, `order`, `summary`, `source`, `blocks`) and the `ContentBlock` discriminated union (`heading`/`paragraph`/`checklist`/`callout`/`troubleshoot`/`lane`/`link`) per `data-model.md`.
- [x] T005 [P] Create shared presentational components per `data-model.md`/plan: `coach-site/src/components/Checklist.tsx` (renders unchecked checklist items), `coach-site/src/components/CalloutCard.tsx` (info/warn/success tones), `coach-site/src/components/Footer.tsx`. Add a `coach-site/src/components/ContentBlocks.tsx` renderer that switches on `ContentBlock.kind`.
- [x] T006 [P] Create `coach-site/src/components/TabNavigation.tsx`: keyboard-accessible section nav (Tab/Enter/Space), `aria-current` on active item, inline labels at ≥640px and a hamburger menu at ≤640px that closes on selection (per `contracts/site-routes.md`).
- [x] T007 Create the app shell `coach-site/src/App.tsx`: skip link, semantic `<nav>` + single `<main>` landmark, `NavState` (activeSectionId default `prepare`, mobileMenuOpen), hash-anchor sync (`#<id>`), and a `sections` registry array (ordered) that renders the active section. Depends on T004–T006.
- [x] T008 Create `coach-site/src/main.tsx` and `coach-site/src/index.css` (Tailwind base/components/utilities, `:focus-visible` styles, no-horizontal-scroll base), mirroring `workshop-site/`.

**Checkpoint**: App builds and renders an empty shell + nav; sections can now be filled in per story.

---

## Phase 3: User Story 1 - A coach prepares the day before (Priority: P1) 🎯 MVP

**Goal**: A first-time coach lands on the site and can read the intro, the room/tech/pre-flight checklists, and the day timeline — on laptop or phone.

**Independent Test**: Serve `dist/` (no backend), land on Prepare, confirm intro + checklists + Timeline reachable in ≤2 clicks and the mobile nav works at 375px.

### Tests for User Story 1 ⚠️ (write first, expect fail)

- [x] T009 [P] [US1] Playwright e2e in `coach-site/tests/e2e/coach-site.spec.ts`: landing shows the intro + all six section labels; Prepare renders checklist items; Timeline reachable; at 375px the hamburger opens, a link navigates and the menu closes; single `main` landmark + skip link present; no horizontal scroll. (Sections US2/US3 assertions added in their phases.)

### Implementation for User Story 1

- [x] T010 [P] [US1] Author `coach-site/src/content/prepare.ts` (`source: 'coach-guide/FACILITATION.md'`): Room Setup (Physical), Technical Environment, Materials, and Pre-Flight Verification as `checklist` blocks, with a short intro paragraph. Content faithful to FACILITATION.md.
- [x] T011 [P] [US1] Author `coach-site/src/content/timeline.ts` (`source: 'coach-guide/FACILITATION.md'`): the 7-Hour Timeline (9:00–4:00) and the Coach Escalation Playbook as `heading`/`paragraph`/`callout` blocks.
- [x] T012 [US1] Create `coach-site/src/sections/Prepare.tsx` rendering `prepare` blocks via `ContentBlocks`. Depends on T005, T010.
- [x] T013 [US1] Create `coach-site/src/sections/Timeline.tsx` rendering `timeline` blocks. Depends on T005, T011.
- [x] T014 [US1] Add a landing/intro region (top of `App.tsx` or a `Landing` block on the default section) with "what this is / how to use it" copy and the six-section overview, per US1 acceptance scenario 1.
- [x] T015 [US1] Register `prepare` (order 1) and `timeline` (order 2) in the `App.tsx` sections registry and nav; make `prepare` the default. Run the T009 e2e (US1 assertions) to green.

**Checkpoint**: MVP — site is independently usable for night-before prep; deployable.

---

## Phase 4: User Story 2 - A coach unblocks a stuck participant (Priority: P2)

**Goal**: Mid-event triage — common setup failures with quick fixes, plus the three cold-start lanes to keep blocked teams moving.

**Independent Test**: From the site, open Troubleshooting and Help; confirm the Azure conditional-access fix and the three head-start lanes are findable in <30s via section anchors.

### Tests for User Story 2 ⚠️

- [x] T016 [P] [US2] Extend `coach-site/tests/e2e/coach-site.spec.ts`: Troubleshooting renders symptom→fix entries (incl. an Azure/conditional-access entry); Help renders the three lanes + the "scenario-ready" definition and a link to HEADSTART.

### Implementation for User Story 2

- [x] T017 [P] [US2] Author `coach-site/src/content/troubleshooting.ts` (`source: 'coach-guide/TROUBLESHOOTING.md'`): common Lab 00+ issues as `troubleshoot` blocks (symptom/cause/fix), including Python/Node versions, Azure conditional access, subscription/RBAC, `azd up` registration.
- [x] T018 [P] [US2] Author `coach-site/src/content/help.ts` (`source: 'docs/quickstart/HEADSTART.md'`): the three lanes (shared backend / self-serve azd / mock) as `lane` blocks, the "scenario-ready" definition, and a `link` block to the full HEADSTART guide.
- [x] T019 [US2] Create `coach-site/src/sections/Troubleshooting.tsx` rendering `troubleshoot` blocks. Depends on T005, T017.
- [x] T020 [US2] Create `coach-site/src/sections/HelpParticipants.tsx` rendering `lane`/`link` blocks. Depends on T005, T018.
- [x] T021 [US2] Register `help` (order 4) and `troubleshooting` (order 5) in the `App.tsx` sections registry and nav. Run the T016 e2e to green.

**Checkpoint**: US1 + US2 both work independently; the site now covers prep and in-event aid.

---

## Phase 5: User Story 3 - A coach frames and assesses the build sprint (Priority: P3)

**Goal**: The 60-second mission pitch + six-intent rationale to open the sprint, plus rubric and talking-point transitions.

**Independent Test**: Open Framing and Assess; confirm the mission pitch, six-intent rationale, rubric summary, and talking points render with links to the full guides.

### Tests for User Story 3 ⚠️

- [x] T022 [P] [US3] Extend `coach-site/tests/e2e/coach-site.spec.ts`: Framing renders the 60-second pitch and six-intent rationale; Assess renders rubric criteria + talking points with links.

### Implementation for User Story 3

- [x] T023 [P] [US3] Author `coach-site/src/content/framing.ts` (`source: 'coach-guide/ajcu-framing.md'`): the 60-second mission pitch (as a `callout`) and the six-intent rationale paragraphs.
- [x] T024 [P] [US3] Author `coach-site/src/content/assess.ts` (`source: 'coach-guide/ASSESSMENT_RUBRIC.md'` + `coach-guide/TALKING_POINTS.md`): rubric criteria summary + phase-transition talking points, with `link` blocks to the full guides.
- [x] T025 [US3] Create `coach-site/src/sections/Framing.tsx` rendering `framing` blocks. Depends on T005, T023.
- [x] T026 [US3] Create `coach-site/src/sections/Assess.tsx` rendering `assess` blocks. Depends on T005, T024.
- [x] T027 [US3] Register `framing` (order 3) and `assess` (order 6) in the `App.tsx` sections registry and nav. Run the T022 e2e to green.

**Checkpoint**: All six sections live and independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Drift safety net, deployment wiring, docs, and full validation.

- [x] T028 [P] Add a content-drift check (`coach-site/tests/e2e/content.spec.ts` or a small node test) per `contracts/content-map.md`: each `Section.source` resolves to an existing repo file, every section's `blocks` is non-empty, and all six section ids appear exactly once.
- [x] T029 [P] Create `.github/workflows/deploy-coach-swa.yml` mirroring `deploy-workshop-swa.yml`: triggers on push to `coach-site/**` + `workflow_dispatch`; guard step no-ops with a `::warning::` if `AZURE_STATIC_WEB_APPS_API_TOKEN_COACH` is unset; otherwise build `app_location: coach-site`, `output_location: dist` and deploy with that secret.
- [x] T030 [P] Extend `docs/deployment/SWA_PROVISIONING.md`: add the coach site as "Site 4" with `az staticwebapp create --name swa-47doors-coach` (capture URL), `secrets list` → `gh secret set AZURE_STATIC_WEB_APPS_API_TOKEN_COACH`, and the dispatch step; update the sites table at the top.
- [x] T031 [P] Add `coach-site/README.md` (purpose, local dev, build, deploy pointer) and a `.gitignore` (node_modules, dist) mirroring `workshop-site/`.
- [x] T032 Run quickstart validation per `quickstart.md`: `cd coach-site && npm run typecheck && npm run build` (assert `dist/` includes `staticwebapp.config.json`) and `npx playwright test` (all e2e green). Fix any failures.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies — start immediately.
- **Foundational (Phase 2)**: depends on Setup — **BLOCKS all user stories**.
- **User Stories (Phase 3–5)**: depend on Foundational. US1 → US2 → US3 in priority order; each is independently testable and can be staffed in parallel after Phase 2.
- **Polish (Phase 6)**: T028/T032 depend on sections existing; T029–T031 (deploy/docs) are independent and may be done any time after Setup.

### User Story Dependencies

- **US1 (P1)**: after Phase 2. No dependency on other stories. = MVP.
- **US2 (P2)**: after Phase 2. Adds sections + extends the shared e2e spec; otherwise independent of US1.
- **US3 (P3)**: after Phase 2. Independent of US1/US2.

> Note: US1/US2/US3 each register sections in `App.tsx` and extend the single e2e spec file — if run in parallel by different people, serialize those two touch-points (registry + spec) to avoid merge conflicts.

### Within Each User Story

- Write the story's e2e assertions first (expect fail) → author content module(s) → build section component(s) → register in nav → make e2e green.

### Parallel Opportunities

- Setup: T002, T003 in parallel after T001.
- Foundational: T004, T005, T006 in parallel; T007 after them; T008 in parallel with T004–T006.
- Within a story, the `content/*.ts` modules ([P]) can be authored in parallel; section components depend on their content module + shared components.
- Polish: T028–T031 largely parallel.

---

## Parallel Example: User Story 1

```bash
# After Phase 2, author US1 content modules in parallel:
Task: "Author coach-site/src/content/prepare.ts from FACILITATION.md"
Task: "Author coach-site/src/content/timeline.ts from FACILITATION.md"
# Then build sections (each depends on its content module):
Task: "Create coach-site/src/sections/Prepare.tsx"
Task: "Create coach-site/src/sections/Timeline.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Phase 1 Setup → 2. Phase 2 Foundational → 3. Phase 3 US1 → 4. **STOP & VALIDATE** (serve `dist/`, run US1 e2e at 375px) → 5. Deploy/demo.

### Incremental Delivery

Setup + Foundational → US1 (MVP, deploy) → US2 (deploy) → US3 (deploy) → Polish. Each story adds value without breaking the prior ones.

---

## Notes

- [P] = different files, no dependency on incomplete tasks.
- Content is presented faithfully from `coach-guide/*.md` / HEADSTART — no new facilitation policy (FR-002).
- Site is fully static: no backend, no API calls, no auth (public SWA).
- Commit after each task or logical group; the deploy workflow is merge-safe before Azure is provisioned.
- Build/implement on branch `009-coach-prep-site` in its own worktree; do not touch `backend/`, `labs/`, or the other sites.
