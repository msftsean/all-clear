# Phase 0 Research: Coach Prep Companion Site

The spec has **no open `NEEDS CLARIFICATION` markers** — the request ("a site to explain to coaches how
to prepare to help folks") plus the existing `coach-guide/` content and the `workshop-site/` precedent
fully constrain the design. Research below records the key technical decisions and the alternatives
weighed.

## D1 — Stack & tooling

- **Decision**: React 18 + Vite 5 + TypeScript 5 + Tailwind CSS 3.4 + @heroicons/react, identical to
  `workshop-site/`.
- **Rationale**: A sibling site already proves this exact stack builds and deploys cleanly in this repo
  (verified: 373 modules → `dist/`, ~73 kB gz JS). Reusing it means zero new toolchain risk, consistent
  look/feel, and easy maintenance. Coaches get the same calm, scannable, tab-based UX.
- **Alternatives considered**:
  - *Plain HTML in `docs/`*: rejected — the docs SWA is AAD-login-gated and not mobile-first/scannable;
    coaches need a public, phone-friendly site.
  - *Add tabs to `workshop-site/`*: rejected — different audience (coaches vs executives), different
    lifecycle, and would bloat the executive briefing.
  - *A heavier framework (Next.js/Astro)*: rejected — no SSR/data needs; Vite static is simplest.

## D2 — Content sourcing & drift control

- **Decision**: Each section's prose lives in a single TS module under `src/content/` that mirrors one
  `coach-guide/*.md` source. Content is presented faithfully (no new policy). A short "source:" note in
  each content module names the markdown file it derives from.
- **Rationale**: Spec edge case "stale content drift" requires a single source per section and easy
  updates. Embedding as TS modules (vs fetching markdown at runtime) keeps the site fully static with no
  runtime dependency (FR-003) and no markdown-parser bundle.
- **Alternatives considered**:
  - *Runtime fetch/parse of `coach-guide/*.md`*: rejected — adds a backend/fetch dependency and a
    markdown parser; violates "no runtime backend dependency".
  - *Build-time markdown import (vite-plugin-md)*: viable but adds a plugin; deferred. Hand-curated TS
    content is simpler for the ~6 sections and lets us tighten wording for the web.

## D3 — Section information architecture

- **Decision**: Six sections mapping to coach intents and existing guides:
  Prepare (FACILITATION room/tech/pre-flight) · Timeline (FACILITATION 7-hr schedule) · Framing
  (ajcu-framing 60-sec pitch + six intents) · Help Participants (HEADSTART three lanes + escalation
  playbook) · Troubleshooting (TROUBLESHOOTING symptom→fix) · Assess (ASSESSMENT_RUBRIC + TALKING_POINTS).
- **Rationale**: Directly satisfies FR-001 and the three prioritized user stories (P1 prepare, P2 help,
  P3 frame/assess). Ordering puts the night-before MVP first and the in-event aid second.
- **Alternatives considered**: A single long-scroll page — rejected for SC-001/SC-002 (2-clicks / <30s
  findability); tabs/sections give fast jump-to.

## D4 — Navigation, accessibility & mobile

- **Decision**: Keyboard-accessible tab/section nav with a mobile menu (hamburger) at ≤640px, semantic
  landmarks (`<nav>`, `<main>`, headings), visible focus, no horizontal scroll at 375px. Mirror the
  accessibility bar `hackathon-site` adopted (skip link, focus-visible).
- **Rationale**: Constitution Principle VI (WCAG AA, keyboard nav, mobile) applies; spec FR-004/SC-005
  require phone usability.
- **Alternatives considered**: Desktop-only inline nav — rejected (coaches use phones on the floor).

## D5 — Deployment

- **Decision**: New guarded GitHub Actions workflow `deploy-coach-swa.yml`, triggered on push to
  `coach-site/**` + `workflow_dispatch`, building `app_location: coach-site` → `output_location: dist`,
  deploying with its **own** secret `AZURE_STATIC_WEB_APPS_API_TOKEN_COACH`. Public
  `staticwebapp.config.json` placed in `coach-site/public/` so Vite copies it into `dist/`. Guard step
  no-ops with a clear message until the secret is set.
- **Rationale**: Exactly mirrors the just-merged `deploy-workshop-swa.yml` pattern (PR #7). Per a stored
  repo lesson, **each SWA needs its own deployment token** — reusing one deploys into the wrong site, so
  a distinct secret name is mandatory.
- **Alternatives considered**: OIDC auto-discovery (like the hackathon OIDC workflow) — more robust but
  more setup; deferred to a follow-up. Token-based is simplest for a one-time event site.

## D6 — Testing

- **Decision**: A Playwright e2e smoke (`coach-site/tests/e2e/coach-site.spec.ts`) asserting: all six
  sections reachable/render, mobile nav opens and navigates at 375px, and basic a11y (skip link / single
  main landmark / keyboard reach). Plus `tsc --noEmit` and `vite build` as build gates.
- **Rationale**: Constitution Principle V (test-first, light — no agent behaviors) and the sibling sites'
  Playwright convention. Validates the measurable success criteria (SC-004/SC-005).
- **Alternatives considered**: Unit tests of content modules — low value for static prose; the e2e
  render assertion covers "sections present" (SC-004).

**Phase 0 result**: All decisions resolved; no blocking unknowns. Proceed to Phase 1.
