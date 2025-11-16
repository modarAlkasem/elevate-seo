"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";

import { LogIn, BarChart3 } from "lucide-react";
import { useSession } from "next-auth/react";

import { Button } from "../ui/button";
import { ThemeToggle } from "../theme-toggle";
import {
  useAuthDialog,
  authFormModes,
  type AuthFormModes,
} from "@/contexts/auth-dialog-context";
import { Dialog, DialogTrigger, DialogContent } from "../ui/dialog";
import { AuthForm } from "../forms/auth-form";
import { UserButton } from "./user-button";

export const Header = () => {
  const pathname = usePathname();
  const [isPricingPage, setIsPricingPage] = useState(false);
  const { data: session } = useSession();

  const { setAuthFormMode, setShowDialog, showDialog, authFormMode } =
    useAuthDialog();

  const searchParams = useSearchParams();

  useEffect(() => {
    const checkIsPricePage = () => {
      if (pathname.startsWith("/pricing")) setIsPricingPage(true);
    };
    checkIsPricePage();
  }, [pathname]);

  useEffect(() => {
    if (
      searchParams.get("open-auth-dialog") &&
      searchParams.get("auth-context") &&
      Object.values(authFormModes).includes(
        searchParams.get("auth-context") as AuthFormModes
      ) &&
      searchParams.get("callbackUrl")
    ) {
      setAuthFormMode("SIGN_IN");
      setShowDialog(true);
    }
  }, [searchParams, authFormMode, setShowDialog, setAuthFormMode]);
  return (
    <header
      className={`sticky top-0 w-full border-b bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60 ${
        isPricingPage ? "z-0 bg-transparent" : "z-50"
      }`}
    >
      <div className="mx-auto flex h-14 max-w-7xl items-center gap-2 px-4">
        <div className="flex flex-1 items-center gap-3">
          <Link
            href="/"
            className="flex items-center gap-2 justify-center rounded-md bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent font-semibold  text-lg"
          >
            ElevateSEO
          </Link>
        </div>

        <div className="flex flex-1 items-center justify-end gap-2">
          {session && (
            <Link href="/dashboard">
              <Button variant="outline" name="Dashboard">
                <BarChart3 className="size-4" />
                <span className="sr-only md:not-sr-only md:ml-2">
                  {" "}
                  Dashboard{" "}
                </span>
              </Button>
            </Link>
          )}

          <ThemeToggle />

          {/** Unauthenticated */}
          {session ? (
            <UserButton />
          ) : (
            <Dialog open={showDialog} onOpenChange={setShowDialog}>
              <DialogTrigger asChild>
                <Button variant="outline">
                  <LogIn className="size-4" />
                  <span className="sr-only md:not-sr-only md:ml-2">
                    {" "}
                    Sign in
                  </span>
                </Button>
              </DialogTrigger>
              <DialogContent
                className="sm:max-w-md bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-slate-950 dark:via-blue-950 dark:to-purple-950 "
                showCloseButton={false}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-pink-500/10 " />
                <AuthForm />
              </DialogContent>
            </Dialog>
          )}

          {/** Authenticated  */}
          {/* <Button variant="ghost"></Button> */}
        </div>
      </div>
    </header>
  );
};
