"use client";

import { SessionProvider } from "next-auth/react";
import { ThemeProvider } from "next-themes";

export const ClientWrapper = ({ children }: { children: React.ReactNode }) => {
  return (
    <ThemeProvider attribute="class" disableTransitionOnChange>
      <SessionProvider refetchInterval={5 * 60} refetchOnWindowFocus={true}>
        {children}
      </SessionProvider>
    </ThemeProvider>
  );
};
