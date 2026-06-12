import { test, expect } from '@playwright/test';

// US1 (spec 004) coverage: every challenge card deep-links without a 404,
// and the six Jesuit intents are all present on /intents (SC-005).

const CARDS: Array<{ slug: string; title: string }> = [
  { slug: 'quiet-crisis', title: 'The Quiet Crisis' },
  { slug: 'aid-cliff', title: 'The Aid Cliff' },
  { slug: 'discernment', title: 'The Discernment' },
  { slug: 'phishing-storm', title: 'The Phishing Storm' },
  { slug: 'holy-spirit', title: 'Mass of the Holy Spirit' },
  { slug: 'multilingual-family', title: 'The Multilingual Family' },
];

const INTENT_KEYS = [
  'financial_aid',
  'registrar',
  'campus_ministry',
  'it',
  'student_wellness',
  'general',
];

const HUB_ROUTES = ['/', '/pattern', '/intents', '/rules', '/run-of-show'];

test.describe('AJCU site — full route coverage', () => {
  for (const card of CARDS) {
    test(`card deep-link /cards/${card.slug} renders (no 404)`, async ({ page }) => {
      const response = await page.goto(`/cards/${card.slug}`);
      expect(response?.status()).toBe(200);
      await expect(
        page.getByRole('heading', { name: card.title })
      ).toBeVisible();
    });
  }

  for (const route of HUB_ROUTES) {
    test(`hub route ${route} renders content`, async ({ page }) => {
      const response = await page.goto(route);
      expect(response?.status()).toBe(200);
      await expect(page.locator('#root')).not.toBeEmpty();
    });
  }

  test('/intents lists all six Jesuit intents', async ({ page }) => {
    await page.goto('/intents');
    // The page renders the intents twice: a desktop table (hidden below `sm`)
    // and mobile cards (hidden at/above `sm`). Assert the key is visible in
    // whichever view is active for the current viewport, not the first DOM match.
    for (const key of INTENT_KEYS) {
      await expect(
        page.getByText(key, { exact: false }).filter({ visible: true }).first()
      ).toBeVisible();
    }
  });
});
