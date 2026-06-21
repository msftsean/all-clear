import { test, expect } from "@playwright/test";

test.describe("All Clear chat smoke", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("renders the briefing room shell", async ({ page }) => {
    await expect(page.getByRole("banner").getByText("All Clear", { exact: true })).toBeVisible();
    await expect(page.getByTestId("signal-input")).toBeVisible();
    await expect(page.getByTestId("send-signal")).toBeVisible();
  });

  test("submits a signal and shows an agent response", async ({ page }) => {
    await page.getByTestId("signal-input").fill("Downed power line sparking on Oak Street.");
    await page.getByTestId("send-signal").click();

    await expect(page.getByTestId("caller-message").filter({ hasText: "Downed power line sparking on Oak Street." })).toBeVisible();
    await expect(page.getByTestId("agent-message").first()).toBeVisible({ timeout: 30000 });
  });

  test("supports channel toggling", async ({ page }) => {
    const toggle = page.getByTestId("channel-toggle");
    await expect(toggle).toContainText("chat");
    await toggle.click();
    await expect(toggle).toContainText("phone");
  });

  test("renders trust controls and doc links", async ({ page }) => {
    await expect(page.getByTestId("trust-view")).toBeVisible();
    await expect(page.getByTestId("trust-map-link")).toBeVisible();
    await expect(page.getByTestId("lab-to-production-link")).toBeVisible();
  });

  test("renders capstone capture + export controls", async ({ page }) => {
    await expect(page.getByTestId("capstone-capture")).toBeVisible();
    await expect(page.getByTestId("capstone-name")).toBeVisible();
    await expect(page.getByTestId("capstone-submit")).toBeVisible();
    await expect(page.getByTestId("capstone-export-csv")).toBeVisible();
    await expect(page.getByTestId("capstone-export-json")).toBeVisible();
  });
});
