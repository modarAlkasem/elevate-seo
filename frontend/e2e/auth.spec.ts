import { test, expect } from "@playwright/test";

test.describe("Authentication", () => {
  test("should sign up with new account", async ({ page }) => {
    await page.goto("/");

    await page.getByRole("button", { name: "Sign in" }).click();

    await expect(page.locator('[role="dialog"]')).toBeVisible();

    await page.getByRole("button", { name: "Sign Up" }).click();

    const timestamp = Date.now();
    await page.fill('input[name="email"]', `test${timestamp}@example.com`);
    await page.fill('input[name="password"]', "TestPassword123!");

    await page.click('button[type="submit"]:has-text("Sign Up")');

    await page.waitForTimeout(2000);

    await expect(
      page.getByRole("heading", { name: " Sign in to ElevateSEO" })
    ).toBeVisible();
  });
});
