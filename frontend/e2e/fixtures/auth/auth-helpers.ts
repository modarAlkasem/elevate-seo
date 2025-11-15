import { type Page, expect } from "@playwright/test";

export const openAuthForm = async (page: Page) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Sign in" }).click();

  await expect(page.locator('[role="dialog"]')).toBeVisible();
};

export const signIn = async ({
  page,
  email,
  password,
}: {
  page: Page;
  email: string;
  password: string;
}) => {
  await openAuthForm(page);

  await expect(
    page.getByRole("heading", { name: "Sign in to ElevateSEO" })
  ).toBeVisible({ timeout: 5000 });

  await page.fill('input[name="email"]', email);
  await page.fill('input[name="password"]', password);

  await page.click('button[type="submit"]:has-text("Sign In")');

  await expect(page.locator('[data-slot="dropdown-menu-trigger"]')).toBeVisible(
    {
      timeout: 5000,
    }
  );
};
