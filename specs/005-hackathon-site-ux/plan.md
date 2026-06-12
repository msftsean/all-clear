# Implementation Plan: Hackathon Site Mobile Nav, Accessibility & 404 Handling

**Branch**: `005-hackathon-site-ux` | **Date**: 2026-05-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-hackathon-site-ux/spec.md`

## Summary

Close the three remaining pre-hackathon UX gaps in the reference site (`hackathon-site/`):
(1) an accessible mobile navigation menu so phones can reach hub pages from any inner route,
(2) an accessibility pass (skip link, labelled landmarks, `:focus-visible` styles) closing task T027,
and (3) a friendly SPA 404 catch-all route. Implementation is pure client-side React + existing
Tailwind tokens — no new dependencies, no backend changes. Work is isolated on a worktree branch off
`origin/main` so it never collides with the parallel CLI's docs/e2e/red-team/eval effort.

## Technical Context

**Language/Version**: TypeScript 5, React 18
**Primary Dependencies**: react-router-dom (existing), Tailwind CSS (existing). No new runtime deps.
**Storage**: N/A (static SPA)
**Testing**: Playwright (chromium + Pixel 5 mobile projects), `tsc --noEmit`, `npm run build`
**Target Platform**: Static Web App (Azure SWA), modern mobile + desktop browsers
**Project Type**: Web frontend (single Vite SPA in `hackathon-site/`)
**Performance Goals**: No regression; no added bundle deps; menu interaction < 100ms perceived
**Constraints**: Changes confined to `hackathon-site/` in-scope files; reuse theme tokens; no visual regression on desktop
**Scale/Scope**: 1 new component, 1 new page, edits to `Layout.tsx`, `App.tsx`, `index.css`, 1 e2e spec

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Bounded Agent Authority** — N/A. Static marketing/reference UI; introduces no agent, tool, or API surface.
- **II. Human Escalation for Policy Decisions** — N/A. No decisioning logic added.
- **III. Privacy-First Data Handling** — N/A. No student data, no PII, no logging, no audio. Purely presentational navigation.
- **IV. Stateful Context Preservation** — N/A. No session/conversation state involved.
- **V. Test-First Development** — **APPLIES.** Acceptance scenarios for Stories 1–3 are encoded as Playwright assertions before/with implementation; the existing mobile-nav test is un-skipped to drive Story 1. `tsc --noEmit` + build gate every change.

**Result**: PASS. Only Principle V is engaged and is satisfied by the test-first task ordering below.

## Project Structure

### Documentation (this feature)

```text
specs/005-hackathon-site-ux/
├── spec.md              # Feature spec (done)
├── plan.md              # This file
├── research.md          # Phase 0 — decisions
├── data-model.md        # Phase 1 — nav-link model (lightweight)
├── quickstart.md        # Phase 1 — how to run/verify
├── contracts/
│   └── ui-behavior.md   # Phase 1 — UI behavior "contracts" (a11y/nav)
└── tasks.md             # Phase 2 (/speckit.tasks output)
```

### Source Code (repository root)

```text
hackathon-site/
├── src/
│   ├── App.tsx                      # add <Route path="*"> catch-all
│   ├── index.css                    # add .skip-link + :focus-visible styles
│   ├── components/
│   │   ├── Layout.tsx               # skip link, labelled landmarks, mount MobileNav
│   │   └── MobileNav.tsx            # NEW — accessible disclosure menu
│   └── pages/
│       └── NotFound.tsx             # NEW — friendly 404 page
└── tests/
    └── e2e/
        └── site.spec.ts             # un-skip mobile-nav test; add a11y + 404 assertions
```

**Structure Decision**: Single existing Vite SPA. No restructuring; additive components + targeted edits only.

## Complexity Tracking

No constitution violations; no complexity deviations to justify.
