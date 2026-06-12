# Quickstart — 005 Hackathon Site UX

All commands run inside the isolated worktree.

```bash
cd /workspaces/47doors-polish/hackathon-site
npm install                 # first time only

# Type check (must be clean)
npx tsc --noEmit -p tsconfig.json

# Production build (must succeed)
npm run build

# Dev server for manual checks
npm run dev                 # then open the printed URL, narrow to 375px

# E2E (use a free port to avoid clashes with the parallel CLI)
PORT=4399 npx playwright test --project=chromium
PORT=4399 npx playwright test            # all projects incl. mobile (Pixel 5)
```

## Manual verification checklist

- [ ] At 375px on `/pattern`, a menu button is visible; opening it lists Pattern/Intents/Rules/Schedule; tapping one navigates and closes the menu; Escape closes and refocuses the button.
- [ ] At ≥640px, no menu button; inline header nav present (desktop unchanged).
- [ ] First Tab on any page focuses a visible "Skip to main content" link; activating it jumps to main.
- [ ] Every link/button shows a visible focus ring when tabbed to.
- [ ] Visiting `/no-such-page` shows a friendly 404 with a working link home.
- [ ] `git -C /workspaces/47doors-polish diff --name-only origin/main` lists only `hackathon-site/**` and `specs/005-hackathon-site-ux/**`.
