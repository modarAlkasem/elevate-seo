/// <reference types="./next-auth.d.ts" />

import type { AuthOptions, User } from "next-auth";
import type { JWT } from "next-auth/jwt";
import CredentialsProvider from "next-auth/providers/credentials";
import GoogleProvider from "next-auth/providers/google";
import type { GoogleProfile } from "next-auth/providers/google";

import { DateTime } from "luxon";
import { SignInPayload, SignInSocialPayload } from "../api/auth/types";
import { refreshToken, signIn, signInSocial } from "../api/auth/fetchers";
import { ErrorCode } from "./error-codes";
import { useSecureCookies, formatSecureCookieName } from "./utils";

export const NEXT_AUTH_OPTIONS: AuthOptions = {
  secret: process.env.AUTH_SECRET,
  session: {
    strategy: "jwt",
  },

  providers: [
    GoogleProvider<GoogleProfile>({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
      async profile(profile, token) {
        const paylaod: SignInSocialPayload = {
          id_token: token.id_token as string,
          access_token: token.access_token as string,
          email: profile.email,
          provider: "GOOGLE" as const,
        };

        const result = await signInSocial(paylaod);

        return {
          id: result.user.id,
          name: result.user.name,
          email: result.user.email,
          email_verified: result.user.email_verified,
          last_signed_in: result.user.last_signed_in as string,
          is_active: result.user.is_active,
          avatar: result.user.avatar,
          access: result.tokens.access,
          refresh: result.tokens.refresh,
        } satisfies User;
      },
    }),
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: {
          type: "email",
          label: "Email",
          placeholder: "Enter Your Email",
        },
        password: {
          label: "Password",
          type: "password",
          placeholder: "Enter Your Password",
        },
      },
      async authorize(credentials) {
        if (!credentials) {
          throw new Error(ErrorCode.CREDENTIALS_NOT_FOUND);
        }

        const payload: SignInPayload = {
          email: credentials.email,
          password: credentials.password,
        };

        try {
          const result = await signIn(payload);

          return {
            id: result.user.id,
            name: result.user.name,
            email: result.user.email,
            email_verified: result.user.email_verified,
            last_signed_in: result.user.last_signed_in as string,
            is_active: result.user.is_active,
            avatar: result.user.avatar,
            access: result.tokens.access,
            refresh: result.tokens.refresh,
          } satisfies User;
        } catch (err: any) {
          throw Error(err?.status_text);
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ user, token, isNewUser, trigger, account, profile }) {
      let resultToken: JWT = { ...token };

      if (user) {
        resultToken = {
          id: user.id as number,
          name: user.name as string,
          email: user.email,
          email_verified: user.email_verified,
          last_signed_in: user.last_signed_in,
          is_active: user.is_active,
          avatar: user.avatar,
          access: user.access,
          refresh: user.refresh,
          expires: DateTime.now().toUTC().plus({ minutes: 5 }).toString(),
        };
      }

      if (
        DateTime.fromISO(resultToken.expires as string).toUTC() <=
        DateTime.now().toUTC()
      ) {
        const payload = {
          refresh: resultToken.refresh as string,
        };
        const result = await refreshToken(payload);
        resultToken.access = result.access;
        resultToken.refresh = result.refresh;
        resultToken.expires = DateTime.now()
          .toUTC()
          .plus({ minutes: 5 })
          .toString();
      }

      return resultToken;
    },
    session({ session, token }) {
      session.user = {
        id: token.id as number,
        name: token.name as string,
        email: token.email as string,
        email_verified: token.email_verified as boolean,
        last_signed_in: token.last_signed_in as string,
        is_active: token.is_active as boolean,
        avatar: token.avatar as string,
      };

      session.access = token.access as string;
      session.refresh = token.refresh as string;
      session.expires = token.expires as string;

      return session;
    },
  },

  cookies: {
    sessionToken: {
      name: formatSecureCookieName("next-auth.session-token"),
      options: {
        httpOnly: true,
        sameSite: useSecureCookies ? "none" : "lax",
        path: "/",
        secure: useSecureCookies,
      },
    },
    callbackUrl: {
      name: formatSecureCookieName("next-auth.callback-url"),
      options: {
        sameSite: useSecureCookies ? "none" : "lax",
        path: "/",
        secure: useSecureCookies,
      },
    },
    csrfToken: {
      // Default to __Host- for CSRF token for additional protection if using useSecureCookies
      // NB: The `__Host-` prefix is stricter than the `__Secure-` prefix.
      name: formatSecureCookieName("next-auth.csrf-token"),
      options: {
        httpOnly: true,
        sameSite: useSecureCookies ? "none" : "lax",
        path: "/",
        secure: useSecureCookies,
      },
    },
    pkceCodeVerifier: {
      name: formatSecureCookieName("next-auth.pkce.code_verifier"),
      options: {
        httpOnly: true,
        sameSite: useSecureCookies ? "none" : "lax",
        path: "/",
        secure: useSecureCookies,
      },
    },
  },
};
