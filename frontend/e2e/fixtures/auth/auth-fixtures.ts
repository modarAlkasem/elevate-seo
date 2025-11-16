/* eslint-disable react-hooks/rules-of-hooks */

import { test } from "@playwright/test";

import { TEST_USER } from "./test-data";

interface AuthFixtures {
  testUser: { email: string; password: string };
}

export const testUser = test.extend<AuthFixtures>({
  testUser: async ({ request }, use) => {
    const credentials = {
      name: TEST_USER.NAME,
      email: TEST_USER.EMAIL,
      password: TEST_USER.PASSWORD,
    };
    try {
      await request.post(
        `${process.env.NEXT_PUBLIC_BASE_API_URL}/auth/signup/`,
        {
          data: credentials,
        }
      );
      await use(credentials);
    } catch (e) {
      await use(credentials);
    }
  },
});
