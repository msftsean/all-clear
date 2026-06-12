# 47 Doors — Hackathon Reference Site

Mobile-first static reference site for the AJCU IT Conference AI hackathon at Fordham Lincoln Center.

## Quick Start

```bash
cd hackathon-site
npm install
npm run dev        # http://localhost:5173
```

## Build

```bash
npm run build      # outputs to dist/
npm run preview    # preview the build locally
```

## Tech Stack

- **Vite** + **React 18** + **TypeScript 5** + **Tailwind CSS 3**
- **React Router v6** for client-side SPA routing
- Pure static output — no backend, no API, no database

## Deploy to Azure Static Web Apps

1. Create an Azure Static Web App resource in the Azure Portal
2. Copy the deployment token
3. Add it as a GitHub secret: `AZURE_STATIC_WEB_APPS_API_TOKEN_HACKATHON_SITE`
4. Push to `main` — the workflow at `.github/workflows/deploy-hackathon-swa.yml` handles CI/CD

The `staticwebapp.config.json` provides a navigation fallback so deep links (e.g., `/cards/quiet-crisis`) resolve correctly.

## Routes

| Path | Description |
|------|-------------|
| `/` | Landing — hero + card gallery + hub nav |
| `/cards/:slug` | Card detail (6 cards: A–F) |
| `/pattern` | The three-agent pattern |
| `/intents` | The six doors (intent table) |
| `/rules` | Escalation & routing rules |
| `/run-of-show` | 1:00–4:00 timeline |

## Design

Jesuit Light Version palette: maroon headings, gold accents, cream backgrounds. Playfair Display serif headings, Inter sans body.

## Card Data

All six challenge cards are defined in `src/data/cards.ts`. Edit that single file to update card content across the gallery and detail pages.

<!-- deploy trigger: 2026-05-31T06:27:07Z -->
