import { test, expect, Page } from '@playwright/test'

// E2E smoke for the Coach Prep Companion Site.
// Covers US1 (landing + Prepare + Timeline + mobile nav + a11y), US2
// (Troubleshooting + Help), and US3 (Framing + Assess).
//
// Navigation uses the always-visible landing intro list (the "About this site"
// region) so the same helper works at every viewport.

const SECTION_LABELS = [
  'Prepare',
  'Timeline',
  'Framing',
  'Help Participants',
  'Troubleshooting',
  'Assess',
]

async function gotoSection(page: Page, label: string) {
  const intro = page.getByRole('region', { name: 'About this site' })
  await intro.getByRole('button', { name: new RegExp('^' + label) }).click()
}

test.describe('Coach Prep Companion Site', () => {
  // ---- US1: prepare the day before ------------------------------------------

  test('landing shows the intro and all six section labels', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveTitle(/Coach Prep/)
    await expect(page.getByRole('heading', { level: 1, name: '47 Doors Coach Prep' })).toBeVisible()

    const intro = page.getByRole('region', { name: 'About this site' })
    await expect(intro).toBeVisible()
    await expect(intro.getByText(/calm, scannable companion/i)).toBeVisible()

    for (const label of SECTION_LABELS) {
      await expect(intro.getByRole('button', { name: new RegExp('^' + label) })).toBeVisible()
    }
  })

  test('Prepare (default section) renders checklist items', async ({ page }) => {
    await page.goto('/')
    // Prepare is the default active section.
    await expect(page.getByRole('heading', { name: 'Prepare', exact: true })).toBeVisible()
    await expect(page.getByText('Projector/screen tested and working')).toBeVisible()
    await expect(page.getByText('Wi-Fi credentials posted visibly')).toBeVisible()
    await expect(page.getByText('Run azd up end-to-end on a fresh account')).toBeVisible()
  })

  test('Timeline is reachable and renders the schedule + escalation playbook', async ({ page }) => {
    await page.goto('/')
    await gotoSection(page, 'Timeline')
    await expect(page.getByRole('heading', { name: 'Timeline', exact: true })).toBeVisible()
    await expect(page.getByText(/Run of Show/)).toBeVisible()
    await expect(page.getByText(/Build sprint 1/).first()).toBeVisible()
    await expect(page.getByText(/Coach Escalation Playbook/)).toBeVisible()
    await expect(page.getByText(/AADSTS53003/)).toBeVisible()
  })

  test('deep-link via hash activates the section on load', async ({ page }) => {
    await page.goto('/#troubleshooting')
    await expect(page.getByRole('heading', { name: 'Troubleshooting', exact: true })).toBeVisible()
  })

  test('a11y: a single main landmark and a working skip link are present', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByRole('main')).toHaveCount(1)

    await page.keyboard.press('Tab')
    const skipLink = page.getByRole('link', { name: 'Skip to main content' })
    await expect(skipLink).toBeFocused()
    await expect(skipLink).toBeVisible()
    await skipLink.press('Enter')
    await expect(page.locator('#main-content')).toBeFocused()
  })

  test('mobile nav opens, navigates, and closes at 375px', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')

    const toggle = page.getByRole('button', { name: 'Open menu' })
    await expect(toggle).toBeVisible()
    await expect(toggle).toHaveAttribute('aria-expanded', 'false')

    await toggle.click()
    await expect(page.getByRole('button', { name: 'Close menu' })).toHaveAttribute(
      'aria-expanded',
      'true'
    )

    const menu = page.getByRole('navigation', { name: 'Sections' })
    await expect(menu).toBeVisible()
    for (const label of SECTION_LABELS) {
      await expect(menu.getByRole('button', { name: label, exact: true })).toBeVisible()
    }

    // Selecting a section navigates and closes the menu.
    await menu.getByRole('button', { name: 'Assess', exact: true }).click()
    await expect(page.getByRole('navigation', { name: 'Sections' })).toBeHidden()
    await expect(page.getByRole('button', { name: 'Open menu' })).toHaveAttribute(
      'aria-expanded',
      'false'
    )
    await expect(page.getByRole('heading', { name: 'Assess', exact: true })).toBeVisible()
  })

  test('no horizontal scroll at 375px', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    await page.goto('/')
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth > document.documentElement.clientWidth
    )
    expect(overflow).toBe(false)
  })

  // ---- US2: unblock a stuck participant -------------------------------------

  test('Troubleshooting renders symptom → fix entries incl. Azure conditional access', async ({
    page,
  }) => {
    await page.goto('/')
    await gotoSection(page, 'Troubleshooting')
    await expect(page.getByRole('heading', { name: 'Troubleshooting', exact: true })).toBeVisible()

    // An Azure conditional-access entry with a fix.
    await expect(page.getByText(/AADSTS53003/).first()).toBeVisible()
    await expect(page.getByText(/Conditional Access blocks user-interactive Azure CLI login/)).toBeVisible()
    // The symptom → fix shape is rendered (Fix: labels present).
    await expect(page.getByText('Fix:').first()).toBeVisible()
    // Other common setup failures are present.
    await expect(page.getByText(/Node\.js version < 18/)).toBeVisible()
  })

  test('Help renders the three lanes, scenario-ready, and a HEADSTART link', async ({ page }) => {
    await page.goto('/')
    await gotoSection(page, 'Help Participants')
    await expect(page.getByRole('heading', { name: 'Help Participants', exact: true })).toBeVisible()

    await expect(page.getByText(/Shared backend/)).toBeVisible()
    await expect(page.getByText(/Self-serve azd/)).toBeVisible()
    await expect(page.getByText(/Mock \/ offline/)).toBeVisible()
    await expect(page.getByText(/Definition of scenario-ready/)).toBeVisible()

    const headstartLink = page.getByRole('link', { name: /HEADSTART/ })
    await expect(headstartLink).toBeVisible()
    await expect(headstartLink).toHaveAttribute('href', /HEADSTART\.md/)
  })

  // ---- US3: frame and assess the build sprint -------------------------------

  test('Framing renders the 60-second pitch and the six-intent rationale', async ({ page }) => {
    await page.goto('/')
    await gotoSection(page, 'Framing')
    await expect(page.getByRole('heading', { name: 'Framing', exact: true })).toBeVisible()

    await expect(
      page.getByRole('heading', { name: 'The 60-second mission pitch' })
    ).toBeVisible()
    await expect(page.getByText(/build the door behind the door/)).toBeVisible()
    await expect(page.getByText(/Why these six intents/)).toBeVisible()
  })

  test('Assess renders rubric criteria and talking points with links', async ({ page }) => {
    await page.goto('/')
    await gotoSection(page, 'Assess')
    await expect(page.getByRole('heading', { name: 'Assess', exact: true })).toBeVisible()

    await expect(page.getByText(/Strong demo qualities/)).toBeVisible()
    await expect(page.getByText(/Correct intent routing across at least three of the six intents/)).toBeVisible()
    await expect(page.getByText(/Talking points for phase transitions/)).toBeVisible()
    await expect(page.getByText(/Coach script for deployment blockers/)).toBeVisible()

    await expect(page.getByRole('link', { name: /Assessment Rubric/ })).toBeVisible()
    await expect(page.getByRole('link', { name: /Talking Points/ })).toBeVisible()
  })
})
