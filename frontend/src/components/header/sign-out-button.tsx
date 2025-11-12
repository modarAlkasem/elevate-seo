"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signOut } from "next-auth/react";
import { LogOut } from "lucide-react";
import { toast } from "sonner";

import { Button } from "../ui/button";

export const SignOutButton = () => {
  const [isSigningOut, setIsSigningOut] = useState(false);
  const router = useRouter();

  const onButtonClick = async () => {
    try {
      setIsSigningOut(true);
      await signOut({
        redirect: false,
        callbackUrl: "/",
      });
      setIsSigningOut(false);

      router.replace("/");
    } catch (err) {
      toast.error("An unknown error occured", {
        description:
          "We encountered an error while trying to sign you out. please try again later.",
        duration: 5000,
        position: "top-right",
      });
    }
  };

  return (
    <Button
      variant="outline"
      className=" w-full flex justify-start items-start  gap-x-6 px-4.5 py-4  border-none hover:cursor-pointer h-12.5 bg-transparent hover:bg-transparent hover:opacity-100 group"
      disabled={isSigningOut}
      onClick={onButtonClick}
    >
      <LogOut className=" font-semibold h-full ml-3 mr-2 group-hover:scale-110 group-hover:translate-x-2 transition-transform duration-300 " />
      <span className=" font-semibold text-sm ">Sign Out</span>
    </Button>
  );
};
