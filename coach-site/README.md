# 47 Doors Coach Prep Companion Site (`coach-site/`)

A standalone, **public**, static site that gives hackathon **coaches** one
organized place to learn how to prepare for and help participants during the
47 Doors AJCU event. It re-presents existing repo content — `coach-guide/*.md`
and `docs/quickstart/HEADSTART.md` — as a calm, scannable, tab/section-based
reference usable on a laptop or phone, before and during the event.

It is a sibling to `workshop-site/` and reuses its exact toolchain
(React 18 + Vite 5 + TypeScript 5 + Tailwind 3.4 + @heroicons/react). No backend,
no auth, no agent code.

## Sections

1. **Prepare** — room / tech / materials / pre-flight checklists (`coach-guide/FACILITATION.md`)
2. **Timeline** — the 9:00–4:00 schedule + Coach Escalation Playbook (`coach-guide/FACILITATION.md`)
3. **Framing** — the 60-second mission pitch + six-intent rationale (`coach-guide/ajcu-framing.md`)
4. **Help Participants** — the three cold-start lanes + scenario-ready (`docs/quickstart/HEADSTART.md`)
5. **Troubleshooting** — common setup failures, symptom → fix (`coach-guide/TROUBLESHOOTING.md`)
6. **Assess** — rubric summary + phase-transition talking points (`coach-guide/ASSESSMENT_RUBRIC.md` + `coach-guide/TALKING_POINTS.md`)

Content is presented **faithfully** from those sources — the site does not
author new facilitation policy. Each `src/content/*.ts` module declares the
`source` file it derives from; a content-drift test verifies every source
resolves to a real repo file.

## Local development

```bash
cd coach-site
npm ci            # or: npm install
npm run dev       # Vite dev server at http://localhost:5173
```

## Build & verify

```bash
npm run typecheck # tsc --noEmit
npm run build     # tsc && vite build -> dist/
ls dist/          # index.html, assets/, staticwebapp.config.json
```

`dist/staticwebapp.config.json` is copied from `public/` by Vite and must be
present (public site, SPA navigation fallback, security headers).

## End-to-end tests

```bash
npx playwright install --with-deps chromium   # first time only
npx playwright test                           # tests/e2e/*.spec.ts
```

The smoke asserts: all six sections render their key content, mobile nav opens /
navigates / closes at 375px, single `main` landmark + skip link, no horizontal
scroll, and the content-map contract holds.

## Deploy

Auto-deploys to its own Azure Static Web App via
`.github/workflows/deploy-coach-swa.yml` on push to `coach-site/**`, but only
once its Azure resource + token secret (`AZURE_STATIC_WEB_APPS_API_TOKEN_COACH`)
exist. Until then the workflow no-ops with a warning. See
[`docs/deployment/SWA_PROVISIONING.md`](../docs/deployment/SWA_PROVISIONING.md)
(Site 4) for provisioning steps.
