"use client";

import { createContext, useContext, useState } from "react";

export const authFormModes = {
  SIGN_IN: "SIGN_IN",
  SIGN_UP: "SIGN_UP",
} as const;

export type AuthFormModes = (typeof authFormModes)[keyof typeof authFormModes];

interface AuthDialogContext {
  showDialog: boolean;
  authFormMode: AuthFormModes;
  setShowDialog: (show: boolean) => void;
  setAuthFormMode: (mode: AuthFormModes) => void;
}

const authDialogContext = createContext<AuthDialogContext | undefined>(
  undefined
);

export const AuthDialogProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [authFormMode, setAuthFormMode] = useState<AuthFormModes>(
    authFormModes.SIGN_IN
  );
  const [showDialog, setShowDialog] = useState(false);

  return (
    <authDialogContext.Provider
      value={{
        showDialog: showDialog,
        authFormMode: authFormMode,
        setShowDialog: (show: boolean) => setShowDialog(show),
        setAuthFormMode: (mode: AuthFormModes) => setAuthFormMode(mode),
      }}
    >
      {children}
    </authDialogContext.Provider>
  );
};

export const useAuthDialog = () => {
  const context = useContext(authDialogContext);
  if (!context) {
    throw new Error("useAuthDialog must be used within AuthDialogProvider");
  }

  return context;
};
