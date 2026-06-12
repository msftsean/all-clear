import { defineConfig, devices } from '@playwright/test';

const PORT = process.env.PORT ?? '4280';
const externalURL = process.env.BASE_URL?.trim() || undefined;
const baseURL = externalURL ?? `http://localhost:${PORT}`;

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: process.env.CI ? 'github' : 'list',
  use: {
    baseURL,
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['Pixel 5'] } },
  ],
  // When BASE_URL is provided, test the already-deployed site directly.
  // Otherwise build the production bundle and serve it locally (emulates
  // Azure SWA static hosting + SPA fallback).
  webServer: externalURL
    ? undefined
    : {
        command: 'npm run build && npx serve -s dist -l ' + PORT,
        url: baseURL,
        reuseExistingServer: true,
        timeout: 120_000,
      },
});
