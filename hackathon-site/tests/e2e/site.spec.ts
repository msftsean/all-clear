import { test, expect } from '@playwright/test';

test.describe('47 Doors hackathon site', () => {
  test('landing page loads with hero and all 6 door cards', async ({ page }) => {
    await page.goto('/');

    await expect(page).toHaveTitle(/47 Doors/);
    await expect(
      page.getByRole('heading', { level: 1, name: '47 Doors' })
    ).toBeVisible();
    await expect(page.getByText('Pick a door. Build the agent behind it.')).toBeVisible();

    // Each card is a link to /cards/:slug
    const cardLinks = page.locator('a[href^="/cards/"]');
    await expect(cardLinks).toHaveCount(6);

    await expect(page.getByText(/AJCU IT Conference/)).toBeVisible();
  });

  test('navigating into a card shows its detail', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('link', { name: /The Quiet Crisis/ }).click();

    await expect(page).toHaveURL(/\/cards\/quiet-crisis$/);
    await expect(
      page.getByRole('heading', { name: 'The Quiet Crisis' })
    ).toBeVisible();
  });

  test('header nav links route between hub pages', async ({ page, isMobile }) => {
    test.skip(isMobile, 'Header nav is hidden on small screens (sm:flex)');

    await page.goto('/cards/quiet-crisis');

    await page.getByRole('link', { name: 'Pattern', exact: true }).click();
    await expect(page).toHaveURL(/\/pattern$/);

    await page.getByRole('link', { name: 'Intents', exact: true }).click();
    await expect(page).toHaveURL(/\/intents$/);

    await page.getByRole('link', { name: 'Rules', exact: true }).click();
    await expect(page).toHaveURL(/\/rules$/);

    await page.getByRole('link', { name: 'Schedule', exact: true }).click();
    await expect(page).toHaveURL(/\/run-of-show$/);
  });

  test('SPA fallback: deep-linking directly to a route works (SWA navigationFallback)', async ({
    page,
  }) => {
    const response = await page.goto('/pattern');
    expect(response?.status()).toBe(200);
    await expect(page.locator('#root')).not.toBeEmpty();

    // Brand link back to home is present on non-home pages.
    await page.getByRole('link', { name: '47 Doors' }).first().click();
    await expect(page).toHaveURL(/\/$/);
  });

  test('deep-linking directly to a card detail works', async ({ page }) => {
    const response = await page.goto('/cards/quiet-crisis');
    expect(response?.status()).toBe(200);
    await expect(
      page.getByRole('heading', { name: 'The Quiet Crisis' })
    ).toBeVisible();
  });

  // C1 — Mobile nav (Story 1): mobile viewport behavior
  test('mobile nav: toggle opens/closes a disclosure menu with the 4 hub links', async ({
    page,
    isMobile,
  }) => {
    test.skip(!isMobile, 'Mobile nav disclosure only renders below the sm breakpoint');

    await page.goto('/pattern');

    const toggle = page.getByRole('button', { name: 'Open menu' });
    await expect(toggle).toBeVisible();
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');

    // Desktop inline nav links are not visible on mobile.
    const primaryNav = page.getByRole('navigation', { name: 'Primary' });
    await expect(primaryNav).toBeHidden();

    // Open the menu.
    await toggle.click();
    await expect(page.getByRole('button', { name: 'Close menu' })).toHaveAttribute(
      'aria-expanded',
      'true'
    );

    const mobileNav = page.getByRole('navigation', { name: 'Mobile' });
    await expect(mobileNav).toBeVisible();
    await expect(mobileNav.getByRole('link', { name: 'Pattern', exact: true })).toBeVisible();
    await expect(mobileNav.getByRole('link', { name: 'Intents', exact: true })).toBeVisible();
    await expect(mobileNav.getByRole('link', { name: 'Rules', exact: true })).toBeVisible();
    await expect(mobileNav.getByRole('link', { name: 'Schedule', exact: true })).toBeVisible();

    // Activating a panel link navigates and closes the panel.
    await mobileNav.getByRole('link', { name: 'Intents', exact: true }).click();
    await expect(page).toHaveURL(/\/intents$/);
    await expect(page.getByRole('navigation', { name: 'Mobile' })).toBeHidden();
    await expect(page.getByRole('button', { name: 'Open menu' })).toHaveAttribute(
      'aria-expanded',
      'false'
    );
  });

  test('mobile nav: Escape closes the panel and returns focus to the toggle', async ({
    page,
    isMobile,
  }) => {
    test.skip(!isMobile, 'Mobile nav disclosure only renders below the sm breakpoint');

    await page.goto('/pattern');
    const toggle = page.getByRole('button', { name: 'Open menu' });
    await toggle.click();
    await expect(page.getByRole('navigation', { name: 'Mobile' })).toBeVisible();

    await page.keyboard.press('Escape');
    await expect(page.getByRole('navigation', { name: 'Mobile' })).toBeHidden();
    await expect(page.getByRole('button', { name: 'Open menu' })).toBeFocused();
  });

  test('mobile nav: toggle is hidden and inline nav visible on desktop', async ({
    page,
    isMobile,
  }) => {
    test.skip(isMobile, 'Desktop-only: inline nav replaces the mobile disclosure at >= sm');

    await page.goto('/pattern');
    await expect(page.getByRole('button', { name: 'Open menu' })).toBeHidden();
    const primaryNav = page.getByRole('navigation', { name: 'Primary' });
    await expect(primaryNav).toBeVisible();
    await expect(primaryNav.getByRole('link', { name: 'Pattern', exact: true })).toBeVisible();
  });

  // C2 — Accessibility (Story 2)
  test('a11y: first Tab focuses the skip link and activating it moves focus to main', async ({
    page,
  }) => {
    await page.goto('/pattern');

    await page.keyboard.press('Tab');
    const skipLink = page.getByRole('link', { name: 'Skip to main content' });
    await expect(skipLink).toBeFocused();
    await expect(skipLink).toBeVisible();

    await page.keyboard.press('Enter');
    await expect(page.locator('#main-content')).toBeFocused();
  });

  test('a11y: header, main, and footer landmarks render around the page', async ({ page }) => {
    await page.goto('/pattern');
    await expect(page.getByRole('banner')).toBeVisible();
    await expect(page.getByRole('main')).toBeVisible();
    await expect(page.getByRole('contentinfo')).toBeVisible();
  });

  test('a11y: mobile nav landmark has an accessible name when open', async ({
    page,
    isMobile,
  }) => {
    test.skip(!isMobile, 'Mobile nav landmark only renders below the sm breakpoint');

    await page.goto('/pattern');
    await page.getByRole('button', { name: 'Open menu' }).click();
    await expect(page.getByRole('navigation', { name: 'Mobile' })).toBeVisible();
  });

  // C3 — 404 (Story 3)
  test('404: unknown route renders a friendly not-found page within site chrome', async ({
    page,
  }) => {
    await page.goto('/no-such-page');

    await expect(page.getByText(/not found/i)).toBeVisible();
    await expect(page.locator('a[href="/"]').first()).toBeVisible();

    // Site chrome still renders around the 404 content.
    await expect(page.getByRole('banner')).toBeVisible();
    await expect(page.getByRole('contentinfo')).toBeVisible();
  });
});
