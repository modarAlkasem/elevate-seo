"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { LogIn, BarChart3 } from "lucide-react";
import { Button } from "./ui/button";
import { ThemeToggle } from "./theme-toggle";

export const Header = () => {
  const pathname = usePathname();
  const [isPricingPage, setIsPricingPage] = useState(false);

  useEffect(() => {
    const checkIsPricePage = () => {
      if (pathname.startsWith("/pricing")) setIsPricingPage(true);
    };
    checkIsPricePage();
  }, [pathname]);

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
          <Link href="/dashboard">
            <Button variant="outline">
              <BarChart3 className="size-4" />
              <span className="sr-only md:not-sr-only md:ml-2">
                {" "}
                Dashboard{" "}
              </span>
            </Button>
          </Link>

          <ThemeToggle />

          {/** Unauthenticated */}
          <Button variant="outline">
            <LogIn className="size-4" />
            <span className="sr-only md:not-sr-only md:ml-2"> Sign in</span>
          </Button>

          {/** Authenticated  */}
          {/* <Button variant="ghost"></Button> */}
        </div>
      </div>
    </header>
  );
};
