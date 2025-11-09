import type { AuthOptions } from "next-auth";

declare module "next-auth" {
  interface User {
    id: number;
    name: string | null;
    email: string;
    email_verified: boolean;
    last_signed_in: string;
    disabled: boolean;
    avatar: string | null;
    access: string;
    refresh: string;
  }

  interface Session {
    user: Omit<User, "access" | "refresh">;
    access: string;
    refresh: string;
    expires: string;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    id: number;
    name: string;
    email: string;
    email_verified: boolean;
    last_signed_in: string;
    access: string;
    refresh: string;
    expires: string;
  }
}
