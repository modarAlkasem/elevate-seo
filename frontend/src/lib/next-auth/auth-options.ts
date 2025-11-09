/// <reference types="./next-auth.d.ts" />

import type { AuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import GoogleProvider from "next-auth/providers/google";
import type { GoogleProfile } from "next-auth/providers/google";

import { DateTime } from "luxon";

export const NEXT_AUTH_OPTIONS: AuthOptions = {};
