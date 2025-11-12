"use client";

import { useState } from "react";
import { useSession } from "next-auth/react";
import type { Session } from "next-auth";

import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
} from "../ui/dropdown-menu";
import { UserAvatar } from "./user-avatar";
import { SignOutButton } from "./sign-out-button";
import { UserInfo } from "./user-info";

export const UserButton = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const { data: session } = useSession();
  const user = session?.user as Session["user"];

  return (
    <DropdownMenu open={isOpen} onOpenChange={setIsOpen}>
      <DropdownMenuTrigger asChild>
        <UserAvatar user={user} />
      </DropdownMenuTrigger>

      <DropdownMenuContent
        align="end"
        className="mt-[15px] w-[378px]  border-none p-0 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-slate-950 dark:via-blue-950 dark:to-purple-950"
      >
        {/* <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-pink-500/10 " /> */}
        <DropdownMenuItem className="p-0 focus:bg-transparent">
          <UserInfo user={user} />
        </DropdownMenuItem>
        <DropdownMenuSeparator className="bg-muted-foreground my-0" />
        <DropdownMenuItem className="p-0 focus:bg-transparent">
          <SignOutButton />
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};
