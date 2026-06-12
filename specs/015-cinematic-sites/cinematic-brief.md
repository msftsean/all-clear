# 015 — Cinematic / TED-Talk Site Redesigns

## Mission

Transform the public sites into **stunning, cinematic, TED-talk-grade experiences** — graphical, animated, immersive. Each site adopts a specific curated design system from `designs/` (Refero-derived). **Follow each design's guidance for layout, type, color, components, and motion — do NOT keep the old layouts.** Reimagine each site's structure to match its design reference while preserving all existing copy/content.

## Workspace & Git rules (CRITICAL)

- Work **only** in this worktree: `/workspaces/47doors-cinematic` (branch `015-cinematic-sites`).
- **Never** touch `/workspaces/47doors` (a different worktree on another branch).
- Commit per site on `015-cinematic-sites` with clear messages + the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer. Do **not** open PRs, merge, or deploy — the orchestrator handles PR + deploy.
- Do not edit other sites' deploy workflows except the docs one (see docs task).

## Site → Design assignments

| Site | Design ref (`designs/`) | Theme | Notes |
|------|------------------------|-------|-------|
| **workshop-site** | `design-sequel.md` (primary) + `design-monoposaigon.md` (second version) | dark | Two switchable themes (see below) |
| **coach-site** | `design-gi-company.md` | light (dark hero) | Architectural night-sky |
| **docs** → migrate to **docs-site/** | `design-mercury.md` | dark | React migration + AAD preserved |
| hackathon-site | — | — | **OUT OF SCOPE this round; do not modify** |

Read the full assigned `designs/design-*.md` for each site — they contain exact color tokens, type scales, spacing, radii, shadows, component specs, do's/don'ts, layout guidance, and a Quick-Start CSS/Tailwind block. Treat them as the source of truth.

## Cinematic / motion requirements (all sites)

- **Atmospheric hero**: full-bleed, large display type, entrance animation (fade/slide/scale-in), per-design background (Sequel: stark black gallery; Monopo Saigon: shifting organic gradient on frosted glass; Mercury: twilight command-center w/ violet-blue accent; GI Company: illustrative night-sky cityscape over light UI).
- **Scroll-reveal**: IntersectionObserver-driven reveal/stagger as sections enter the viewport.
- **Motion graphics**: animated gradients, parallax, animated SVG diagrams/data viz, number count-ups, smooth tab/section transitions, hover micro-interactions per each design's elevation/interaction model.
- **Accessibility (non-negotiable)**: honor `prefers-reduced-motion: reduce` — gate every non-essential animation behind it (no parallax/auto-motion when reduced). Maintain WCAG AA contrast, visible focus, keyboard nav, skip links, single `<main>`, semantic landmarks.
- **Performance**: prefer CSS transforms/opacity; lazy/init observers; no layout thrash; keep bundles reasonable.

## Fonts (proprietary → Google substitutes)

Proprietary faces are unavailable; use distinctive Google Font substitutes (avoid plain Inter/Roboto as the sole body font):
- **Sequel**: headline serif (Bradford) → `Fraunces`; body sans (VisueltPro) → `Geist` (fallback `Familjen Grotesk`).
- **Monopo Saigon**: Roobert → `Familjen Grotesk` (or `Geist`); `Raleway` (Google) for accent headings.
- **Mercury**: arcadia / arcadiaDisplay → `Manrope` (light weights for display).
- **GI Company**: PPMondwest serif → `Instrument Serif` (or `Fraunces`); `af` sans → `Geist` (fallback `Inter Tight`).
Load via `<link>` in index.html (and reflect in the docs CSP, which already allows fonts.googleapis.com / fonts.gstatic.com).

## Fluent 2 icons

- Install `@fluentui/react-icons` and use **Fluent 2** (Fluent System Icons) for UI + any Azure-concept icons (e.g. cloud, search, phone, shield, server). Style them to each theme (stroke/fill, color).
- For the **GitHub** and **Azure** brand marks specifically, use a clean inline SVG consistent with Fluent 2's geometry/stroke; do not use mismatched third-party logo packs.

## workshop-site — two versions (Sequel + Monopo Saigon)

- Default theme = **Sequel** (black canvas, Fraunces serif display, pill buttons, gallery layout, cinematic reveals).
- Add a **second version = Monopo Saigon**, switchable via a header **theme toggle** persisted to `localStorage`, applied via a `data-theme="sequel|saigon"` attribute on `<html>`. The Saigon theme swaps the token set (organic shifting **Deep Ocean gradient** background `linear-gradient(90deg, rgb(160,224,171), rgb(255,172,46) 50%, rgb(165,45,37))`, frosted-glass translucent surfaces, 75px pill radius, Familjen Grotesk/Raleway type).
- Both themes share the same cinematic layout + content; tokens/treatments differ. All 12 tabs' content (Overview, The Problem, Chatbots→Agents, Trust & Boundaries, Architecture, Voice & Accessibility, Phone Integration, Demo Walkthrough, Responsible AI, Reuse Across Campus, Your First Agent, Presenter Script) and their copy are preserved.
- Animate the existing `DiagramSVG` content cinematically.

## coach-site — GI Company

- Light, architectural theme with an **illustrative dark "night-sky" hero** (`#1f1f29`) and serif display (`Instrument Serif`/PPMondwest substitute) over a clean `Canvas White` body with soft multi-layered shadows and a single `Cofounder Blue #0081c0` accent.
- Preserve ALL section content and the discriminated-union content blocks. **Coach has e2e tests that MUST stay green**: a11y (skip link, single `<main>`, `aria-current`, focus-visible) and a **content-drift test** asserting each section's `source:` declarations resolve — do not alter content/`source:` data. Layout/visuals may be fully reimagined.

## docs → docs-site/ migration — Mercury

- Create a new **`docs-site/`** React 18 + Vite 5 + TS + Tailwind 3.4 app (mirror workshop-site/coach-site config: tsconfig, vite.config.ts, tailwind.config.js, postcss, index.html, src/main.tsx, src/App.tsx, src/index.css).
- Port the **entire runbook content** from `docs/index.html` (all sections/text — it's the "47 Doors — Voice Feature Demo Runbook") into the React app, restyled to **Mercury** (Midnight Slate `#1e1e2a` bg, Starlight `#ededf3` text, single Mercury Blue `#5266eb` CTA accent, Manrope light-weight display, pill buttons, cinematic command-center hero + scroll reveals).
- **Preserve AAD gating**: copy `docs/staticwebapp.config.json` into `docs-site/public/staticwebapp.config.json` unchanged (so it ships in the build output). It already includes a CSP allowing Google Fonts — keep it; if you add other origins, update the CSP accordingly.
- **Update `.github/workflows/deploy-docs-swa.yml`**: change `paths:` trigger from `docs/**` to `docs-site/**`; replace the `skip_app_build: true` / `output_location: ""` SWA inputs with the Vite build pattern used by `deploy-workshop-swa.yml` (`app_location: "docs-site"`, `output_location: "dist"`, no skip_app_build). Keep the token guard + secret name `AZURE_STATIC_WEB_APPS_API_TOKEN_DOCS`.
- Leave existing `docs/*.md` and subdirectories in place (repo documentation — not part of the served site). You may keep `docs/index.html` or note it's superseded; do not delete other docs content.
- Add a Playwright smoke test if convenient (optional), mirroring coach's setup.

## Per-site verification gates (must pass before declaring a site done)

For each site dir:
1. `npm ci`
2. `npm run typecheck` (where the script exists)
3. `npm run build` → succeeds
4. `npx playwright test` where tests exist (coach mandatory: a11y + content-drift green)
5. Manual check: `prefers-reduced-motion` disables motion; AA contrast; keyboard nav; no console errors.

Report per site: files changed/created, fonts + Fluent icons used, how cinematic motion was implemented, how reduced-motion is handled, and gate results.
