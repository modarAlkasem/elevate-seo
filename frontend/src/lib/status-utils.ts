import {
  Clock,
  CheckCircle,
  XCircle,
  BarChart3,
  HardDriveDownload,
} from "lucide-react";

export type StatusConfig = {
  icon: any;
  label: "Pending" | "Scraping" | "Analyzing" | "Completed" | "Failed";
  variant: "default" | "secondary" | "destructive";
  className: string;
};

export const getStatusConfig = (status: ScrapingJobStatus): StatusConfig => {
  let config: StatusConfig;

  switch (status) {
    case "PENDING":
      config = {
        label: "Pending",
        icon: Clock,
        variant: "secondary",
        className:
          "bg-yellow-50 text-yellow-700 border-yellow-200 hover:bg-yellow-100 dark:bg-yellow-900/20 dark:text-yellow-300 dark:border-yellow-800 dark:hover:bg-yellow-900/30",
      };
      break;

    case "RUNNING":
      config = {
        label: "Scraping",
        icon: HardDriveDownload,
        variant: "secondary",
        className:
          "bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100 dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-800 dark:hover:bg-blue-900/30",
      };
      break;

    case "ANALYZING":
      config = {
        label: "Analyzing",
        icon: BarChart3,
        variant: "secondary",
        className:
          "bg-purple-50 text-purple-700 border-purple-200 hover:bg-purple-100 dark:bg-purple-900/20 dark:text-purple-300 dark:border-purple-800 dark:hover:bg-purple-900/30",
      };
      break;

    case "COMPLETED":
      config = {
        label: "Completed",
        icon: CheckCircle,
        variant: "default",
        className:
          "bg-green-50 text-green-700 border-green-200 hover:bg-green-100 dark:bg-green-900/20 dark:text-green-300 dark:border-green-800 dark:hover:bg-green-900/30",
      };
      break;

    case "FAILED":
      config = {
        label: "Failed",
        icon: XCircle,
        variant: "destructive",
        className:
          "bg-red-50 text-red-700 border-red-200 hover:bg-red-100 dark:bg-red-900/20 dark:text-red-300 dark:border-red-800 dark:hover:bg-red-900/30",
      };
      break;
  }

  return config;
};

export const formateDate = (date: string): string => {
  return new Date(date).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
};

export const getSpinnerColor = (status: ScrapingJobStatus): string => {
  let spinnerColor: string = "";

  switch (status) {
    case "PENDING":
      spinnerColor = "text-yellow-600 dark:text-yellow-400";
      break;

    case "RUNNING":
      spinnerColor = "text-blue-600 dark:text-blue-400";
      break;

    case "ANALYZING":
      spinnerColor = "text-purple-600 dark:text-purple-400";
      break;
  }

  return spinnerColor;
};
