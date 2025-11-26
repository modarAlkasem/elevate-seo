"use client";

import { Badge } from "./ui/badge";
import { getStatusConfig } from "@/lib/status-utils";

interface StatusBadgeProps {
  status: ScrapingJobStatus;
  showIcon?: boolean;
}

export const StatusBadge = ({ status, showIcon = false }: StatusBadgeProps) => {
  const config = getStatusConfig(status);
  const IconComponent = config.icon;

  return (
    <Badge variant={config.variant} className={config.className}>
      {showIcon && <IconComponent className="w-3 h-3 mr-1" />}
      {config.label}
    </Badge>
  );
};
