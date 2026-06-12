# Implementation Plan: Coach Prep Companion Site

**Branch**: `009-coach-prep-site` | **Date**: 2026-06-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/009-coach-prep-site/spec.md`

## Summary

Build a standalone, **public**, static companion website (`coach-site/`) that gives hackathon
**coaches** one organized place to learn how to prepare for and help participants during the 47 Doors
AJCU event. It re-presents existing repo content — `coach-guide/*.md` and `docs/quickstart/HEADSTART.md`
— as a calm, tab/section-based reference usable on a laptop or phone, before and during the event.

Technical approach: clone the proven **`workshop-site/`** stack and conventions (React 18 + Vite 5 +
TypeScript 5 + Tailwind 3.4, tab navigation, `public/staticwebapp.config.json`), give it its own
guarded Azure SWA deploy workflow (`deploy-coach-swa.yml`) with its own deployment-token secret, and
document provisioning in `docs/deployment/SWA_PROVISIONING.md`. No backend, no auth, no agent code.

## Technical Context

**Language/Version**: TypeScript 5.3, Node.js 18+
**Primary Dependencies**: React 18, Vite 5, Tailwind CSS 3.4, @heroicons/react (mirrors `workshop-site/`)
**Storage**: N/A — fully static; content embedded as TS/TSX modules sourced from `coach-guide/*.md`
**Testing**: Playwright (e2e smoke, mirroring `hackathon-site/tests/e2e/`), `tsc --noEmit` typecheck, `vite build`
**Target Platform**: Azure Static Web Apps (CDN/edge); modern browsers, mobile + desktop
**Project Type**: Static web front-end (single new site directory `coach-site/`)
**Performance Goals**: Static, no runtime API; first paint from edge cache; bundle comparable to workshop-site (~270 kB JS gz ~73 kB) or smaller
**Constraints**: Offline-of-backend (no API calls); usable at 375px; WCAG AA; deploy must no-op until token secret set
**Scale/Scope**: ~6 content sections, single audience (coaches), one deploy target; low-traffic event site

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The constitution (v1.1.0) governs the **agent system** (bounded authority, escalation, privacy, voice).
This feature is a **static content site with no agents, no backend, no PII, and no data persistence**, so
the agent/privacy/voice principles are **Not Applicable**. Two principles do apply:

| Principle | Applies? | How this plan complies |
|-----------|----------|------------------------|
| I. Bounded Agent Authority | N/A | No agents; no code paths touch the pipeline. |
| II. Human Escalation | N/A | No automated decisions. |
| III. Privacy-First Data Handling | N/A | No student data, no PII, no logging, no storage. Content is public facilitation material. |
| IV. Stateful Context | N/A | No sessions. |
| **V. Test-First Development** | **Yes (light)** | A Playwright e2e smoke test asserting the six sections render + mobile nav works is written before/with the components, mirroring sibling sites. No agent behaviors to test. |
| **VI. Accessibility as Requirement** | **Yes** | WCAG AA: keyboard-navigable section nav, semantic landmarks, focus-visible, mobile responsive at 375px, no horizontal scroll. Verified in e2e. |
| VII. Graceful Degradation | N/A (trivially satisfied) | Static site has no external runtime deps; deploy workflow guards on its token secret and no-ops safely until provisioned. |

**Quality Gates (from Development Workflow):** changes reviewed via PR; CI must pass; accessibility
checks for UI; no coverage decrease (new isolated site, no backend coverage impact). **No violations.**

**Gate result: PASS** (no Complexity Tracking entries required).

## Project Structure

### Documentation (this feature)

```text
specs/009-coach-prep-site/
├── plan.md              # This file (/speckit.plan output)
├── spec.md              # Feature spec (input)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (content/section model)
├── quickstart.md        # Phase 1 output (build/run/deploy steps)
└── contracts/           # Phase 1 output
    ├── content-map.md   # Section → source coach-guide file mapping (the "API" of a content site)
    └── site-routes.md   # Route/navigation + SWA config contract
```

### Source Code (repository root)

```text
coach-site/                         # NEW — mirrors workshop-site/ tooling
├── index.html
├── package.json
├── vite.config.ts
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
├── public/
│   └── staticwebapp.config.json    # public site, SPA fallback, security headers
└── src/
    ├── main.tsx
    ├── App.tsx                     # tab/section shell + mobile nav
    ├── index.css
    ├── components/
    │   ├── TabNavigation.tsx       # keyboard-accessible, mobile-friendly
    │   ├── Checklist.tsx           # renders FACILITATION pre-flight items
    │   ├── CalloutCard.tsx
    │   └── Footer.tsx
    ├── content/                    # content sourced from coach-guide/*.md (single source per section)
    │   ├── prepare.ts
    │   ├── timeline.ts
    │   ├── framing.ts
    │   ├── help.ts
    │   ├── troubleshooting.ts
    │   └── assess.ts
    └── sections/
        ├── Prepare.tsx
        ├── Timeline.tsx
        ├── Framing.tsx
        ├── HelpParticipants.tsx
        ├── Troubleshooting.tsx
        └── Assess.tsx

coach-site/tests/e2e/
└── coach-site.spec.ts              # Playwright smoke: 6 sections render + mobile nav + a11y basics

.github/workflows/
└── deploy-coach-swa.yml            # NEW — guarded; secret AZURE_STATIC_WEB_APPS_API_TOKEN_COACH

docs/deployment/SWA_PROVISIONING.md # EXTEND — add the coach SWA (Site 4) provisioning steps
```

**Structure Decision**: New top-level `coach-site/` directory, a sibling to `workshop-site/`, reusing
its exact toolchain and deploy pattern. This keeps the coach site fully isolated from `backend/`,
`labs/`, and the other sites, and lets it deploy independently to its own SWA. Chosen over adding pages
to `workshop-site/` (different audience and lifecycle) and over a docs-folder static page (the docs SWA
is AAD-login-gated; coaches need a public, mobile-first, scannable site).

## Complexity Tracking

> No Constitution violations — section intentionally empty.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |
