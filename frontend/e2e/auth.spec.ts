import { test, expect } from "@playwright/test";

import { openAuthForm } from "./fixtures/auth/auth-helpers";
import { signIn } from "./fixtures/auth/auth-helpers";
import { testUser } from "./fixtures/auth/auth-fixtures";

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
});

test.describe("Sign In", () => {
  testUser(
    "should sign in with existing account",
    async ({ page, testUser }) => {
      await signIn({
        page,
        email: testUser.email,
        password: testUser.password,
      });
    }
  );

  testUser(
    "should show error for wrong password",
    async ({ page, testUser }) => {
      await signIn({
        page,
        email: testUser.email,
        password: "WrongPassword!",
        withExpecting: false,
      });

      await expect(page.getByText("Unable to sign in")).toBeVisible({
        timeout: 5000,
      });
    }
  );
});

test.describe("Protected Routes", () => {
  test("should redirect to home page when accessing to protected route without auth", async ({
    page,
  }) => {
    await page.goto("/dashboard");

    await page.waitForURL(
      "/?open-auth-dialog=true&auth-context=SIGN_IN&callbackUrl=%2Fdashboard"
    );
    await expect(page.locator('[role="dialog"]')).toBeVisible();
    await expect(
      page.getByRole("heading", { name: "Sign in to ElevateSEO" })
    ).toBeVisible({ timeout: 5000 });
  });

  testUser(
    "should access protected route when authenticated",
    async ({ page, testUser }) => {
      await signIn({
        page,
        email: testUser.email,
        password: testUser.password,
      });

      await page.goto("/dashboard");
      await expect(page).toHaveURL("/dashboard");
    }
  );
});

testUser.describe("Sign Out", () => {
  testUser("should sign authenticaed user out", async ({ page, testUser }) => {
    await signIn({
      page,
      email: testUser.email,
      password: testUser.password,
    });

    await page.locator("#user-button").click();

    await page.getByRole("button", { name: "Sign Out" }).click();

    await expect(page.getByRole("button", { name: "Sign in" })).toBeVisible();
  });
});
