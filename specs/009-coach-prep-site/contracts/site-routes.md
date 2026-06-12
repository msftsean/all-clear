# Contract: Site Routes, Navigation & SWA Config

A single-page app with in-page section navigation (no server routes). This contract defines the
navigation surface and the Static Web App hosting config.

## Navigation contract

- The app renders six sections (see content-map.md). Exactly one is active at a time.
- Default active section on load: `prepare`.
- Navigation control:
  - **Desktop (≥640px)**: inline tab/section nav, all six labels visible.
  - **Mobile (≤640px)**: a toggle (hamburger) opens a menu listing all six sections; selecting one
    activates that section and closes the menu.
- Each section is addressable via a hash anchor `#<id>` (e.g. `#troubleshooting`) so coaches can deep-link
  / bookmark and so a refresh on a deep link still resolves (combined with SPA fallback below).
- All nav controls MUST be operable by keyboard (Tab to focus, Enter/Space to activate) with visible
  focus, and the active item MUST be programmatically determinable (e.g. `aria-current`).

## SWA hosting contract (`coach-site/public/staticwebapp.config.json`)

Public site (anonymous). Mirrors the workshop site config:

```json
{
  "navigationFallback": {
    "rewrite": "/index.html",
    "exclude": ["/assets/*", "*.{css,scss,js,png,gif,ico,jpg,jpeg,svg,json,woff,woff2,ttf,eot,webp,map}"]
  },
  "globalHeaders": {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Content-Security-Policy": "default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; script-src 'self'; connect-src 'self'"
  }
}
```

- **No `auth` / `routes` role gating** — every route is anonymous (contrast the docs SWA, which is
  AAD-gated).
- `navigationFallback` → `/index.html` guarantees deep-link/refresh on `#section` does not 404 (spec edge
  case).
- The file lives in `coach-site/public/` so Vite copies it to `dist/staticwebapp.config.json` (verified
  pattern from workshop-site).

## Deploy contract (`.github/workflows/deploy-coach-swa.yml`)

- Triggers: `push` to `coach-site/**` on `main`, plus `workflow_dispatch`.
- Builds with the SWA action: `app_location: coach-site`, `output_location: dist`.
- Auth token: `secrets.AZURE_STATIC_WEB_APPS_API_TOKEN_COACH` (its **own** secret — never reuse another
  site's token).
- Guard step: if the secret is empty, emit a `::warning::` and **no-op** (skip checkout/build/deploy), so
  the workflow is merge-safe before Azure is provisioned.
