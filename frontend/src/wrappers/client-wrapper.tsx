"use client";

import { SessionProvider } from "next-auth/react";
import { ThemeProvider } from "next-themes";

import { AuthDialogProvider } from "@/contexts/auth-dialog-context";
import { QueryClientWrapper } from "./query-client-wrapper";

export const ClientWrapper = ({ children }: { children: React.ReactNode }) => {
  return (
    <ThemeProvider attribute="class" disableTransitionOnChange>
      <SessionProvider refetchInterval={5 * 60} refetchOnWindowFocus={true}>
        <QueryClientWrapper>
          {" "}
          <AuthDialogProvider>{children}</AuthDialogProvider>
        </QueryClientWrapper>
      </SessionProvider>
    </ThemeProvider>
  );
};
