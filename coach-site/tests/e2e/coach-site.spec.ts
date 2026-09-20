import { test, expect, Page } from '@playwright/test'

const SECTION_LABELS = ['Prepare', 'Timeline', 'Framing', 'Facilitate', 'Troubleshooting', 'Debrief']

async function gotoSection(page: Page, label: string) {
  const intro = page.getByRole('region', { name: 'About this site' })
  await intro.getByRole('button', { name: new RegExp('^' + label) }).click()
}

test.describe('All Clear Facilitator Guide', () => {
  test('landing shows the facilitator guide and all six sections', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveTitle(/All Clear Facilitator Guide/)
    await expect(page.getByRole('heading', { level: 1, name: 'All Clear Facilitator Guide' })).toBeVisible()
    const intro = page.getByRole('region', { name: 'About this site' })
    await expect(intro.getByText(/incident-triage exercise/i).first()).toBeVisible()
    for (const label of SECTION_LABELS) await expect(intro.getByRole('button', { name: new RegExp('^' + label) })).toBeVisible()
  })

  test('Prepare renders safe fictional-exercise preflight', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByText('Shared demo workspace opens directly to ClearBoard')).toBeVisible()
    await expect(page.getByText(/fictional All Clear exercise/i)).toBeVisible()
  })

  test('Timeline teaches surge triage and the 90-minute flow', async ({ page }) => {
    await page.goto('/')
    await gotoSection(page, 'Timeline')
    await expect(page.getByRole('heading', { name: 'Surge triage prompts' })).toBeVisible()
    await expect(page.getByText(/signal, an incident, or a report/i)).toBeVisible()
  })

  test('Framing explains severity, SLA, and the safety boundary', async ({ page }) => {
    await page.goto('/')
    await gotoSection(page, 'Framing')
    await expect(page.getByText(/severity.*SLA/i).first()).toBeVisible()
    await expect(page.getByText(/Safety overrides pace/)).toBeVisible()
  })

  test('Facilitate covers accessible voice and phone intake', async ({ page }) => {
    await page.goto('/')
    await gotoSection(page, 'Facilitate')
    await expect(page.getByText('Voice and phone checklist')).toBeVisible()
    await expect(page.getByText(/Offer a text alternative/)).toBeVisible()
  })

  test('Troubleshooting renders symptom to fix entries', async ({ page }) => {
    await page.goto('/#troubleshooting')
    await expect(page.getByText(/Two records describe the same event/)).toBeVisible()
    await expect(page.getByText('Fix:').first()).toBeVisible()
  })

  test('Debrief renders ClearBoard and safety assessment criteria', async ({ page }) => {
    await page.goto('/')
    await gotoSection(page, 'Debrief')
    await expect(page.getByText(/Uses ClearBoard to show owner/)).toBeVisible()
    await expect(page.getByText(/Escalates safety-critical content/)).toBeVisible()
  })

  test('a11y: a single main landmark and working skip link are present', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByRole('main')).toHaveCount(1)
    await page.keyboard.press('Tab')
    const skipLink = page.getByRole('link', { name: 'Skip to main content' })
    await expect(skipLink).toBeFocused()
    await skipLink.press('Enter')
    await expect(page.locator('#main-content')).toBeFocused()
  })

  test('mobile navigation opens, selects, and closes without horizontal scroll', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    await page.getByRole('button', { name: 'Open menu' }).click()
    const menu = page.getByRole('navigation', { name: 'Sections' })
    await menu.getByRole('button', { name: 'Debrief', exact: true }).click()
    await expect(menu).toBeHidden()
    expect(await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth)).toBe(false)
  })
})
