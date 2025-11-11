"use client";

import * as React from "react";

import { Avatar, AvatarImage, AvatarFallback } from "../ui/avatar";
import type { Session } from "next-auth";

export const UserAvatar = React.forwardRef<
  React.ElementRef<typeof Avatar>,
  React.ComponentPropsWithRef<typeof Avatar> & { user: Session["user"] }
>(({ user, ...props }, ref) => {
  return (
    <Avatar
      {...props}
      ref={ref}
      className="w-10 h-10 ring-2 dark:ring-blue-800 hover:dark:ring-blue-400 ring-blue-200 hover:ring-blue-500 "
    >
      <AvatarImage src={user.avatar ?? undefined} alt="user's avatar" />
      <AvatarFallback className="font-bold ">
        {user.name
          ? user.name.split(" ").map((text) => text[0].toUpperCase())
          : [user?.email[0], user?.email[1]]
              .map((text) => text[0].toUpperCase())
              .join("")}
      </AvatarFallback>
    </Avatar>
  );
});

UserAvatar.displayName = "UserButtonAvatar";
