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

export const getProgressPercentage = (status: ScrapingJobStatus): string => {
  let progressPercentage = null;

  switch (status) {
    case "PENDING":
      progressPercentage = "0%";
      break;

    case "RUNNING":
      progressPercentage = "25%";
      break;

    case "ANALYZING":
      progressPercentage = "75%";
      break;

    case "COMPLETED":
      progressPercentage = "100%";
      break;

    default:
      progressPercentage = "0%";
  }

  return progressPercentage;
};

export const getProgressBarStyle = (status: ScrapingJobStatus): string => {
  let progressBarStyle = null;

  switch (status) {
    case "PENDING":
      progressBarStyle = "bg-yellow-500 w-0";
      break;

    case "RUNNING":
      progressBarStyle = "bg-blue-500 w-1/4";
      break;

    case "ANALYZING":
      progressBarStyle = "bg-purple-500 w-3/4";
      break;

    case "COMPLETED":
      progressBarStyle = "bg-green-500 w-full";
      break;

    default:
      progressBarStyle = "bg-red-500 w-full";
      break;
  }

  return progressBarStyle;
};

export const getReportTitle = (status: ScrapingJobStatus): string => {
  switch (status) {
    case "COMPLETED":
      return "Report Ready!";

    case "FAILED":
      return "Report Failed";

    default:
      return "Generating Report";
  }
};

export const getStatusMessage = (status: ScrapingJobStatus): string => {
  switch (status) {
    case "PENDING":
      return "Your report is queued and will start proccessing shortly.";

    case "RUNNING":
      return "We're scraping data from search engines. This may take a few minutes.";

    case "ANALYZING":
      return "We're analyzing your data and generate AI insights. This may take a few more minutes";

    case "COMPLETED":
      return "Your report is ready! You can now view and download your SEO insights.";

    case "FAILED":
      return "There was an error processing your report. Please try again.";

    default:
      return "Unknown status";
  }
};

export function formatDateTime(timestamp: string): string {
  return new Date(timestamp).toLocaleString();
}
