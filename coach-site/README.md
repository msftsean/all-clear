# All Clear Facilitator Guide (`coach-site/`)

A standalone public static site for facilitators leading an All Clear
incident-triage exercise. It presents the materials in `coach-guide/` as a
mobile-friendly reference while retaining the existing React, Vite, TypeScript,
Tailwind, and accessibility toolchain.

## Sections

1. **Prepare** — accessible room setup and safe fictional exercise pre-flight
2. **Timeline** — a 90-minute surge-triage run of show
3. **Framing** — signals, incidents, reports, magnitude, severity, and SLA
4. **Facilitate** — interventions plus voice and phone intake practice
5. **Troubleshooting** — common triage, ClearBoard, safety, and device issues
6. **Debrief** — evidence-based assessment and next-action prompts

Each `src/content/*.ts` module declares the valid `coach-guide/*.md` source
that it summarizes. The content-map E2E test verifies that every source path
resolves to a non-empty file.

## Local development

```bash
cd coach-site
npm ci
npm run dev
```

## Build and verify

```bash
npm run typecheck
npm run build
npx playwright test
```

The build produces `dist/`; Vite copies
`public/staticwebapp.config.json` for SPA navigation and security headers.
