import NextAuth from "next-auth";

import { NEXT_AUTH_OPTIONS } from "@/lib/next-auth/auth-options";
import { signOut } from "@/lib/api/auth/fetchers";

const auth = async (req: any, ctx: any) => {
  return await NextAuth(req, ctx, {
    ...NEXT_AUTH_OPTIONS,
    pages: {
      signIn: "/",
      signOut: "/",
      error: "/",
      newUser: "/",
    },
    events: {
      async signOut({ token }) {
        await signOut({ refresh: token.refresh as string });
      },
    },
  });
};

export { auth as GET, auth as POST };
