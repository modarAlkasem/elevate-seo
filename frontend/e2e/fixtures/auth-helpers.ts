import { type Page, expect } from "@playwright/test";

export const openAuthForm = async (page: Page) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Sign in" }).click();

  await expect(page.locator('[role="dialog"]')).toBeVisible();
};
