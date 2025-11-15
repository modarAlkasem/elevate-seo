import { test, expect } from "@playwright/test";

import { openAuthForm } from "./fixtures/auth-helpers";

test.describe("Sign Up", () => {
  test("should sign up with new account", async ({ page }) => {
    const timestamp = Date.now();
    const email = `test${timestamp}@example.com`;
    const password = "TestPassword123!";

    await openAuthForm(page);
    await page.getByRole("button", { name: "Sign Up" }).click();
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password"]', password);

    await page.click('button[type="submit"]:has-text("Sign Up")');

    await expect(
      page.getByRole("heading", { name: "Sign in to ElevateSEO" })
    ).toBeVisible({ timeout: 5000 });
  });

  test("should show validation errors for invalid email", async ({ page }) => {
    await openAuthForm(page);
    await page.getByRole("button", { name: "Sign Up" }).click();
    await page.fill('input[name="email"]', "invalid-email");
    await page.fill('input[name="password"]', "Test123!");
    await page.click('button[type="submit"]:has-text("Sign Up")');

    await expect(page.locator('p[data-slot="form-message"]')).toBeVisible({
      timeout: 5000,
    });
  });

  test("should sign out successfully", async ({ page }) => {
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

    await page.click('[data="dropdown-menu-trigger"]');
    await page.getByRole("button", { name: "Sign Out" }).click();
    await expect(page.getByRole("button", { name: "Sign in" })).toBeVisible({
      timeout: 5000,
    });
  });
});

test.describe("Sign In", () => {
  const name = "E2E Test User";
  const email = "e2e-test@example.com";
  const password = "TestPassword123!";
  test.beforeAll(async ({ request }) => {
    await request.post(`${process.env.NEXT_PUBLIC_BASE_API_URL}/auth/signup/`, {
      data: {
        name: name,
        email: email,
        password: password,
      },
    });
  });

  test("should sign in with existing account", async ({ page }) => {
    await openAuthForm(page);
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

  test("should show error for wrong password", async ({ page }) => {
    await openAuthForm(page);
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="password"]', "WrongPassword!");

    await page.click('button[type="submit"]:has-text("Sign In")');

    await expect(
      page
        .locator("[data-sonner-toast]")
        .filter({ hasText: "Unable to sign in" })
    ).toBeVisible({ timeout: 5000 });
  });
});
