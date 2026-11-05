# Deploying All Clear

All Clear is a static Vite SPA. Build the site, publish the generated `dist/` directory to any static host, and configure an SPA navigation fallback to `index.html`.

```bash
cd hackathon-site
npm ci
npm run build
```

For Azure Static Web Apps, set the application location to `hackathon-site`, the output location to `dist`, and retain the included `staticwebapp.config.json`. Its navigation fallback lets direct visits to routes such as `/incidents/credential-spray` load the React application.

Before publishing, run:

```bash
npm run typecheck
npm run test:e2e
```
