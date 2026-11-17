import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

/** Accessibility checks for the current All Clear BriefingRoom. */

test.describe('Accessibility Compliance', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should not have any automatically detectable accessibility issues', async ({ page }) => {
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('should expose one page-level h1', async ({ page }) => {
    const h1 = await page.locator('h1').count();
    expect(h1).toBe(1);
    await expect(page.getByRole('heading', { level: 1, name: 'All Clear' })).toBeVisible();
  });

  test('should have sufficient color contrast in default mode', async ({ page }) => {
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['cat.color'])
      .analyze();

    // Filter for color contrast violations
    const contrastViolations = accessibilityScanResults.violations.filter(
      v => v.id === 'color-contrast'
    );

    expect(contrastViolations).toHaveLength(0);
  });

  test('should maintain accessibility in forced-colors mode', async ({ page }) => {
    await page.emulateMedia({ forcedColors: 'active' });
    // Contrast is tested in default mode; forced-colors remaps the palette.
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .disableRules(['color-contrast'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('should have proper focus indicators', async ({ page }) => {
    const input = page.getByRole('textbox', { name: /describe the signal/i });
    const inputBox = await input.boundingBox();
    expect(inputBox).not.toBeNull();

    const readIndicatorStyles = () => input.evaluate((el) => {
      const styles = window.getComputedStyle(el);
      return {
        outline: styles.outline,
        outlineStyle: styles.outlineStyle,
        boxShadow: styles.boxShadow,
        borderColor: styles.borderColor,
      };
    });
    const beforeFocus = await readIndicatorStyles();
    await input.focus();
    const afterFocus = await readIndicatorStyles();

    const hasFocusIndicator =
      (afterFocus.outline !== beforeFocus.outline && afterFocus.outlineStyle !== 'none') ||
      (afterFocus.boxShadow !== beforeFocus.boxShadow && afterFocus.boxShadow !== 'none') ||
      afterFocus.borderColor !== beforeFocus.borderColor;
    expect(hasFocusIndicator).toBe(true);
  });

  test('should support keyboard-only navigation', async ({ page }) => {
    const input = page.getByRole('textbox', { name: /describe the signal/i });
    for (let i = 0; i < 20; i++) {
      if (await input.evaluate((element) => element === document.activeElement)) break;
      await page.keyboard.press('Tab');
    }
    await expect(input).toBeFocused();
  });

  test('should have proper ARIA landmarks', async ({ page }) => {
    // Check for main landmark
    const main = page.getByRole('main');
    await expect(main).toBeVisible();

    // Check for banner (header)
    const banner = page.getByRole('banner');
    await expect(banner).toBeVisible();
  });

  test('should have descriptive button labels', async ({ page }) => {
    // All buttons should have accessible names
    const buttons = await page.getByRole('button').all();

    for (const button of buttons) {
      const label =
        (await button.getAttribute('aria-label')) ?? (await button.innerText()).trim();
      expect(label).toBeTruthy();
    }
  });

  test('should announce dynamic content changes', async ({ page }) => {
    const transcript = page.getByRole('log');
    await expect(transcript).toBeVisible();
    await expect(transcript).toHaveAttribute('aria-live', 'polite');
    await expect(transcript).toHaveAttribute('aria-relevant', 'additions');
  });
});

test.describe('Screen Reader Support', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should have alt text for all images', async ({ page }) => {
    const images = await page.locator('img').all();

    for (const img of images) {
      const alt = await img.getAttribute('alt');
      const role = await img.getAttribute('role');

      // Image should have alt text or be marked as decorative
      const hasAltText = alt !== null && alt.length > 0;
      const isDecorative = alt === '' || role === 'presentation';

      expect(hasAltText || isDecorative).toBe(true);
    }
  });

  test('should have proper form labels', async ({ page }) => {
    const inputs = await page.locator('input, textarea').all();

    for (const input of inputs) {
      const id = await input.getAttribute('id');
      const ariaLabel = await input.getAttribute('aria-label');
      const ariaLabelledBy = await input.getAttribute('aria-labelledby');

      // Check for associated label
      let hasLabel = false;

      if (id) {
        const label = page.locator(`label[for="${id}"]`);
        hasLabel = (await label.count()) > 0;
      }

      const hasAriaLabel = ariaLabel !== null && ariaLabel.length > 0;
      const hasAriaLabelledBy = ariaLabelledBy !== null;

      expect(hasLabel || hasAriaLabel || hasAriaLabelledBy).toBe(true);
    }
  });

  test('should provide status messages for actions', async ({ page }) => {
    const input = page.getByRole('textbox', { name: /describe the signal/i });
    const transcript = page.getByRole('log');
    await input.fill('A water main break is flooding the intersection at 5th and Main.');
    await page.getByRole('button', { name: /send/i }).click();

    await expect(transcript).toContainText('A water main break is flooding the intersection at 5th and Main.');
    await expect(transcript.locator('[data-testid="agent-message"]')).toHaveCount(2, {
      timeout: 30000,
    });
  });
});

test.describe('Responsive Accessibility', () => {
  test('should maintain accessibility at different viewport sizes', async ({ page }) => {
    const viewports = [
      { width: 1920, height: 1080, name: 'Desktop' },
      { width: 1024, height: 768, name: 'Tablet' },
      { width: 375, height: 667, name: 'Mobile' },
    ];

    for (const viewport of viewports) {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto('/');

      const accessibilityScanResults = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa'])
        .analyze();

      expect(
        accessibilityScanResults.violations,
        `Accessibility violations at ${viewport.name} (${viewport.width}x${viewport.height})`
      ).toEqual([]);
    }
  });

  test('should have touch-friendly targets on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    // Keep interactive targets at least 44x44 pixels for touch use.
    const buttons = await page.getByRole('button').all();

    for (const button of buttons) {
      const box = await button.boundingBox();
      if (box) {
        const label = await button.innerText();
        expect(box.width, `button "${label}" should be at least 44px wide`).toBeGreaterThanOrEqual(44);
        expect(box.height, `button "${label}" should be at least 44px tall`).toBeGreaterThanOrEqual(44);
      }
    }
  });
});
