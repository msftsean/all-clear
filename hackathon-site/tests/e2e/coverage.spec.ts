import { test, expect } from '@playwright/test';

const INCIDENTS = [
  { slug: 'credential-spray', title: 'Credential spray' },
  { slug: 'checkout-latency', title: 'Checkout latency' },
  { slug: 'possible-exposure', title: 'Possible data exposure' },
  { slug: 'warehouse-offline', title: 'Warehouse offline' },
  { slug: 'unsafe-content-report', title: 'Unsafe content report' },
  { slug: 'api-error-noise', title: 'API error noise' },
];

const QUEUE_KEYS = ['identity_security', 'payments_reliability', 'privacy_security', 'network_operations', 'safety_response', 'platform_observability'];
const HUB_ROUTES = ['/', '/workflow', '/queues', '/policy', '/shift-plan', '/runbook'];

test.describe('All Clear route coverage', () => {
  for (const incident of INCIDENTS) {
    test(`incident deep-link /incidents/${incident.slug} renders`, async ({ page }) => {
      const response = await page.goto(`/incidents/${incident.slug}`);
      expect(response?.status()).toBe(200);
      await expect(page.getByRole('heading', { name: incident.title })).toBeVisible();
    });
  }

  for (const route of HUB_ROUTES) {
    test(`reference route ${route} renders content`, async ({ page }) => {
      const response = await page.goto(route);
      expect(response?.status()).toBe(200);
      await expect(page.locator('#root')).not.toBeEmpty();
    });
  }

  test('/queues lists each response queue', async ({ page }) => {
    await page.goto('/queues');
    for (const key of QUEUE_KEYS) {
      await expect(page.getByText(key, { exact: false }).filter({ visible: true }).first()).toBeVisible();
    }
  });
});
