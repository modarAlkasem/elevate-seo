import React from "react";

const DashboardLayout = ({ children }: { children: React.ReactNode }) => {
  const isInStarterPlan = true;
  const isInProPlan = true;
  const isPaidMember = isInStarterPlan || isInProPlan;

  if (!isPaidMember) {
    return <div>You must be a paid member to access this page</div>;
  }

  return <>{children}</>;
};

export default DashboardLayout;
