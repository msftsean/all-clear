import { test, expect } from '@playwright/test';

test.describe('All Clear incident-triage site', () => {
  test('landing page loads with the triage hero and all six scenarios', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/All Clear/);
    await expect(page.getByRole('heading', { level: 1, name: 'All Clear' })).toBeVisible();
    await expect(page.getByText('Turn noisy surge signals into safe, owned incidents.')).toBeVisible();
    await expect(page.locator('a[href^="/incidents/"]')).toHaveCount(6);
    await expect(page.getByText(/signal → incident → owner → sitrep/)).toBeVisible();
  });

  test('navigating into a scenario shows its triage detail', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('link', { name: /Credential spray/ }).click();
    await expect(page).toHaveURL(/\/incidents\/credential-spray$/);
    await expect(page.getByRole('heading', { name: 'Credential spray' })).toBeVisible();
  });

  test('header navigation routes between reference pages', async ({ page, isMobile }) => {
    test.skip(isMobile, 'Header nav is hidden on small screens');
    await page.goto('/incidents/credential-spray');
    for (const [label, route] of [['Workflow', '/workflow'], ['Queues', '/queues'], ['Policy', '/policy'], ['Shift plan', '/shift-plan']] as const) {
      await page.getByRole('link', { name: label, exact: true }).click();
      await expect(page).toHaveURL(new RegExp(`${route}$`));
    }
  });

  test('SPA fallback supports direct reference routes', async ({ page }) => {
    const response = await page.goto('/workflow');
    expect(response?.status()).toBe(200);
    await expect(page.locator('#root')).not.toBeEmpty();
    await page.getByRole('link', { name: 'All Clear' }).first().click();
    await expect(page).toHaveURL(/\/$/);
  });

  test('mobile nav opens, routes, and closes', async ({ page, isMobile }) => {
    test.skip(!isMobile, 'Mobile nav only renders below the sm breakpoint');
    await page.goto('/workflow');
    const toggle = page.getByRole('button', { name: 'Open menu' });
    await toggle.click();
    const mobileNav = page.getByRole('navigation', { name: 'Mobile' });
    await expect(mobileNav.getByRole('link', { name: 'Queues', exact: true })).toBeVisible();
    await mobileNav.getByRole('link', { name: 'Queues', exact: true }).click();
    await expect(page).toHaveURL(/\/queues$/);
    await expect(page.getByRole('navigation', { name: 'Mobile' })).toBeHidden();
  });

  test('skip link and layout landmarks are accessible', async ({ page }) => {
    await page.goto('/workflow');
    await page.keyboard.press('Tab');
    await expect(page.getByRole('link', { name: 'Skip to main content' })).toBeFocused();
    await page.keyboard.press('Enter');
    await expect(page.locator('#main-content')).toBeFocused();
    await expect(page.getByRole('banner')).toBeVisible();
    await expect(page.getByRole('main')).toBeVisible();
    await expect(page.getByRole('contentinfo')).toBeVisible();
  });

  test('unknown routes render a friendly not-found page', async ({ page }) => {
    await page.goto('/no-such-page');
    await expect(page.getByText(/not on the board/i)).toBeVisible();
    await expect(page.locator('a[href="/"]').first()).toBeVisible();
  });
});
