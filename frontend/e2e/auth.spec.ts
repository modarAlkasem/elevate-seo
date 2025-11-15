import { test, expect } from "@playwright/test";

test.describe("Authentication", () => {
  const timestamp = Date.now();
  const email = `test${timestamp}@example.com`;
  const password = "TestPassword123!";

  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("should sign up with new account", async ({ page }) => {
    await page.getByRole("button", { name: "Sign in" }).click();

    await expect(page.locator('[role="dialog"]')).toBeVisible();

    await page.getByRole("button", { name: "Sign Up" }).click();

    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password"]', password);

    await page.click('button[type="submit"]:has-text("Sign Up")');

    await expect(
      page.getByRole("heading", { name: "Sign in to ElevateSEO" })
    ).toBeVisible({ timeout: 5000 });
  });

  test("should sign in with existing account", async ({ page }) => {
    await page.getByRole("button", { name: "Sign in" }).click();

    await expect(page.locator('[role="dialog"]')).toBeVisible();

    await page.getByRole("button", { name: "Sign Up" }).click();

    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password"]', password);

    await page.click('button[type="submit"]:has-text("Sign Up")');

    await expect(
      page.getByRole("heading", { name: "Sign in to ElevateSEO" })
    ).toBeVisible({ timeout: 5000 });

    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password"]', password);

    await page.click('button[type="submit"]:has-text("Sign In")');

    await expect(page.locator('[data="dropdown-menu-trigger"]')).toBeVisible({
      timeout: 5000,
    });
  });
});
