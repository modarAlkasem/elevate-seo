"use client";

/// <reference types="./next-auth.d.ts" />

import type { Session } from "next-auth";

import { UserAvatar } from "./user-avatar";

export const UserInfo = ({ user }: { user: Session["user"] }) => {
  <div className="w-full flex  gap-x-4 px-4.5 py-4">
    <UserAvatar user={user} />

    <div className="flex flex-col gap-y-1">
      {user.name && <span className="font-semibold "> {user.name}</span>}

      <span className="text-sm text-muted-foreground ">{user.email}</span>
    </div>
  </div>;
};
