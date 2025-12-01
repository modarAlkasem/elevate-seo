"use client";

import { useState, useTransition, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";

import {
  Loader2,
  CheckCircle,
  XCircle,
  BarChart3,
  Calendar,
  FileText,
  AlertCircle,
} from "lucide-react";

import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { StatusBadge } from "@/components/status-badge";
import { getScrapingJobBySnapshotID } from "@/lib/api/scrapingJob/fetchers";
import { scrapingJobKeys } from "@/lib/query-keys";
import {
  getSpinnerColor,
  getReportTitle,
  getStatusMessage,
  getProgressBarStyle,
  getProgressPercentage,
  formatDateTime,
} from "@/lib/status-utils";

const ReportPage = () => {
  const [id, setId] = useState<string | null>(null);
  const [retryError, setRetryError] = useState<string | null>(null);

  const [transitionIsPending, startTransition] = useTransition();

  const router = useRouter();

  const snapshotId = useParams<{ id: string }>().id;

  const { data, isPending, error } = useQuery({
    queryKey: scrapingJobKeys.bySnapshot(snapshotId),
    queryFn: () => getScrapingJobBySnapshotID({ snapshot_id: snapshotId }),
  });

  const handleRetry = () => {
    console.log("handleRetry function is called");
  };

  if (isPending) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-6 h-6 animate-spin mr-2" />
        <span className="text-muted-foreground"> Loading report status...</span>
      </div>
    );
  }

  if (error && (error as unknown as ErrorAPIResponse)?.status_code === 404) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <AlertCircle className="w-6 h-6 text-destructive mr-2" />
        <span className="text-destructive"> Report not found</span>
      </div>
    );
  }

  const job: {
    status: ScrapingJobStatus;
    original_prompt: string;
    created_at: string;
    completed_at: string;
    snapshot_id: string;
    error: string;
    results: {}[];
  } = {
    status: "FAILED",
    original_prompt: "Google",
    created_at: "2025-11-30 00:28:25.291901+00",
    completed_at: "2025-11-30 00:28:25.291901+00",
    snapshot_id: "sx234x_12s",
    error: "Something went wrong",
    results: [{}],
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/20">
      <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="space-y-6">
          {/** Header */}

          <div className="text-center">
            <h1 className="text-3xl font-bold tracking-tight sm:text-4xl mb-4">
              Report Status
            </h1>
            <p className="text-lg text-muted-foreground">
              Track the progress of your SEO report generation
            </p>
          </div>

          {/** Status Card */}
          <Card className="w-full">
            <CardHeader className="text-center">
              <div className="flex flex-col items-center justify-center mb-4">
                {(job.status === "PENDING" ||
                  job.status === "RUNNING" ||
                  job.status === "ANALYZING") && (
                  <Loader2
                    className={`w-5 h-5 animate-spin mb-2 ${getSpinnerColor(
                      job.status
                    )}`}
                  />
                )}
                <StatusBadge status={job.status} showIcon={true} />
              </div>
              <CardTitle className="text-base">
                {getReportTitle(job.status)}
              </CardTitle>
              <CardDescription className="text-base">
                {getStatusMessage(job.status)}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/** Progress Indicator */}
              <div className="space-y-4">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground"> Progress</span>
                  <span className="font-medium">
                    {" "}
                    {getProgressPercentage(job.status)}
                  </span>
                </div>

                <div className="w-full bg-muted rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-500 ${getProgressBarStyle(
                      job.status
                    )}`}
                  />
                </div>
              </div>

              {/** Job Details */}
              <div className="space-y-4 pt-4 border-t">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="flex items-center gap-3">
                    <FileText className="w-4 h-4 text-muted-foreground" />
                    <div>
                      <p className="text-sm font-medium"> Original Query</p>
                      <p className="text-sm text-muted-foreground truncate">
                        {job.original_prompt}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <Calendar className="w-4 h-4 text-muted-foreground" />
                    <div>
                      <p className="text-sm font-medium">Created</p>
                      <p className="text-sm text-muted-foreground">
                        {formatDateTime(job.created_at)}
                      </p>
                    </div>
                  </div>
                </div>

                {job.completed_at && (
                  <div className="flex items-center gap-3">
                    <CheckCircle className="w-4 h-4 text-muted-foreground" />
                    <div>
                      <p className="text-sm font-medium">Completed</p>
                      <p className="text-sm text-muted-foreground">
                        {formatDateTime(job.completed_at)}
                      </p>
                    </div>
                  </div>
                )}

                {job.snapshot_id && (
                  <div className="flex items-center gap-3">
                    <BarChart3 className="w-4 h-4 text-muted-foreground" />
                    <div>
                      <p className="text-sm font-medium">Snapshot ID</p>
                      <p className="text-sm text-muted-foreground">
                        {formatDateTime(job.snapshot_id)}
                      </p>
                    </div>
                  </div>
                )}

                {job.error && (
                  <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                    <div className="flex items-start gap-2">
                      <XCircle className="w-4 h-4 text-red-600 mt-0.5 shrink-0" />
                      <div>
                        <p className="text-sm font-medium text-red-800 dark:text-red-200">
                          Error Details
                        </p>
                        <p className="text-sm text-red-700 dark:text-red-300 mt-1">
                          {job.error}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/** Results Preview */}
              {job.status === "COMPLETED" &&
                job.results &&
                job.results.length > 0 && (
                  <div className="pt-4 border-t">
                    <div className="flex items-center gap-2 mb-3">
                      <BarChart3 className="w-4 h-4 text-green-600" />
                      <p className="text-sm font-medium text-green-800 dark:text-green-200">
                        Results Available
                      </p>
                    </div>
                    <div className="p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
                      <p className="text-sm text-green-700 dark:text-green-300">
                        Your SEO report is ready for analysis.
                      </p>
                    </div>
                  </div>
                )}
            </CardContent>
          </Card>

          {/** Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            {job.status === "COMPLETED" && (
              <Link href={`/dashboard/report/${job.snapshot_id}/summary`}>
                <Button
                  variant="default"
                  size="lg"
                  className="cursor-pointer bg-green-600 hover:bg-green-700 text-white "
                >
                  View Full Report
                </Button>
              </Link>
            )}

            {job.status === "FAILED" && (
              <div className="flex flex-col items-center gap-2">
                <Button
                  variant="default"
                  size="lg"
                  className="cursor-pointer"
                  onClick={handleRetry}
                  disabled={isPending}
                >
                  {transitionIsPending ? (
                    <>
                      {" "}
                      <Loader2 className="w-4 h-4 animate-spin mr-2" />
                      Retrying...
                    </>
                  ) : (
                    "Retry Report"
                  )}
                </Button>
              </div>
            )}
            <Link href="/dashboard">
              <Button variant="outline" size="lg" className="cursor-pointer">
                Back to Dashboard
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportPage;
