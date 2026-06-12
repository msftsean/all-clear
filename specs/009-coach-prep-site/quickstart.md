# Quickstart: Coach Prep Companion Site (`coach-site/`)

How to build, run, test, and deploy the coach prep site once implemented (per `/speckit.tasks`).

## Prerequisites

- Node.js 18+ and npm.

## Local development

```bash
cd coach-site
npm ci
npm run dev          # Vite dev server (hot reload) at http://localhost:5173
```

## Build & verify (the FR-008 gate)

```bash
cd coach-site
npm run typecheck    # tsc --noEmit
npm run build        # tsc && vite build  ->  dist/
ls dist/             # expect: index.html, assets/, staticwebapp.config.json
```

`dist/staticwebapp.config.json` must be present (copied from `coach-site/public/`).

## End-to-end smoke (the SC-004/SC-005 gate)

```bash
cd coach-site
npx playwright install --with-deps chromium   # first time only
npx playwright test                           # runs tests/e2e/coach-site.spec.ts
```

The smoke asserts: all six sections render, mobile nav (375px) opens and navigates, and basic a11y
(single `main` landmark, keyboard-reachable nav).

## Deploy (Azure Static Web App — Site 4)

The site auto-deploys via `.github/workflows/deploy-coach-swa.yml` on push to `coach-site/**`, but only
once its Azure resource + token secret exist. Until then the workflow no-ops with a warning.

```bash
# Where you have Azure access (see docs/deployment/SWA_PROVISIONING.md):
az login
az account set --subscription 098ef2f6-cea4-4839-8093-ef90622e1b8c
RG=rg-ajcu-hackathon

# 1) Create the SWA — defaultHostname IS the public URL:
az staticwebapp create --name swa-47doors-coach -g $RG -l eastus2 \
  --query defaultHostname -o tsv

# 2) Capture its deploy token into the repo secret:
TOKEN=$(az staticwebapp secrets list --name swa-47doors-coach -g $RG \
  --query properties.apiKey -o tsv)
gh secret set AZURE_STATIC_WEB_APPS_API_TOKEN_COACH --body "$TOKEN" \
  --repo EstablishedCorp/47doors

# 3) Trigger the deploy:
gh workflow run deploy-coach-swa.yml --repo EstablishedCorp/47doors
```

Open `https://<defaultHostname>` — the public coach site loads immediately (no login).

## What "done" looks like (maps to Success Criteria)

- SC-001: From the landing (Prepare) view, the pre-flight checklist and Timeline are ≤2 clicks away.
- SC-002: A setup error fix (e.g. Azure conditional access) is findable in <30s via section anchors.
- SC-003: Serving `dist/` alone (no backend) is fully usable.
- SC-004: All six sections present and faithful to `coach-guide/` sources.
- SC-005: Usable at 375px — all sections reachable, no horizontal scroll, keyboard-operable nav.
- SC-006: Workflow no-ops cleanly pre-Azure; publishes at the SWA URL once provisioned.

## Next step

Run `/speckit.tasks` to generate the dependency-ordered `tasks.md` for implementation.
