"use client";

import { SessionProvider } from "next-auth/react";
import { ThemeProvider } from "next-themes";

import { AuthDialogProvider } from "@/context/auth-dialog-context";

export const ClientWrapper = ({ children }: { children: React.ReactNode }) => {
  return (
    <ThemeProvider attribute="class" disableTransitionOnChange>
      <SessionProvider refetchInterval={5 * 60} refetchOnWindowFocus={true}>
        <AuthDialogProvider>{children}</AuthDialogProvider>
      </SessionProvider>
    </ThemeProvider>
  );
};
