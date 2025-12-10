"use client";

import { useState } from "react";

import { Loader2, FileText, Plus, Trash2, TrendingUp } from "lucide-react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

import {
  Table,
  TableBody,
  TableHeader,
  TableRow,
  TableHead,
  TableCell,
} from "./ui/table";
import { Button } from "./ui/button";
import { StatusBadge } from "./status-badge";
import { formateDate, getSpinnerColor } from "@/lib/status-utils";
import { getScrapingJobs } from "@/lib/api/scrapingJob/fetchers";
import { scrapingJobKeys } from "@/lib/query-keys";
import { useScrapingJobsStatus } from "@/lib/websocket/hooks/use-scraping-jobs-status";
import type { ScrapingJobStatusUpdateEventPayload } from "@/lib/websocket/scraping-job-status-websocket";

export const ReportsTable = () => {
  const { data, isPending, isSuccess, error, isError, status } = useQuery({
    queryKey: scrapingJobKeys.list(),
    queryFn: getScrapingJobs,
  });

  const [deletingJobId, setDeletingJobId] = useState<string | null>(null);

  const queryClient = useQueryClient();
  useScrapingJobsStatus(async (data: ScrapingJobStatusUpdateEventPayload) => {
    if (data.type === "job_status_update")
      queryClient.setQueryData(
        scrapingJobKeys.list(),
        (oldJobs: ScrapingJob[]) => {
          if (!oldJobs) return oldJobs;

          return oldJobs.map((job) =>
            job.id === data?.data?.job_id
              ? { ...job, status: data.data?.status }
              : job
          );
        }
      );
  });

  if (isPending) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-center">
        <div className="p-3 bg-muted/50 rounded-full mb-4">
          <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold mb-2"> Loading Reports</h3>
        <p className="text-muted-foreground">
          Fetching your latest analysis reports...
        </p>
      </div>
    );
  }

  if (error) {
    console.error(error);
    return;
  }

  if (data?.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-center">
        <div className="p-4 bg-muted/50 rounded-full mb-6">
          <FileText className="w-8 h-8 animate-spin text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold mb-2"> Np Reports Yet.</h3>
        <p className="text-muted-foreground mb-6 max-w-md">
          Get started by creating your first SEO analysis report. Enter a
          business name, product, or website above to begin.
        </p>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Plus className="w-4 h-4 " />
          <span>Create your first report to see it here</span>
        </div>
      </div>
    );
  }

  const handleRowClick = (jobId: string) => {
    console.log(`handleRowClick has been clicked with Job ID: ${jobId}`);
  };

  const handleDelete = (e: React.MouseEvent, jobId: string) => {
    e.stopPropagation();
    console.log(`handleDelete has been clicked with Job ID: ${jobId}`);
  };

  return (
    <div className="w-full">
      <div className="rounded-lg border bg-card/50 backdrop-blur-sm">
        <Table>
          <TableHeader>
            <TableRow className="border-b border-border/50">
              <TableHead className="font-semibold text-foreground">
                Report
              </TableHead>
              <TableHead className="font-semibold text-foreground">
                Status
              </TableHead>
              <TableHead className="font-semibold text-foreground">
                Created
              </TableHead>
              <TableHead className="font-semibold text-foreground">
                Completed
              </TableHead>
              <TableHead className="font-semibold text-foreground w-20">
                Actions
              </TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data?.map((job) => (
              <TableRow
                key={job.id}
                className="cursor-pointer hover:muted/30 transition-colors border-b border-border/30 last:border-b-0"
                onClick={() => handleRowClick(job.id)}
              >
                <TableCell className="font-medium py-4">
                  <div className="flex items-center gap-3">
                    <div className="p-1.5 bg-muted/50 rouned-md">
                      <FileText className="w-4 h-4 text-muted-foreground" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        {(job.status === "PENDING" ||
                          job.status === "RUNNING" ||
                          job.status === "ANALYZING") && (
                          <Loader2
                            className={` w-4 h-4 animate-spin ${getSpinnerColor(
                              job.status
                            )}`}
                          />
                        )}
                        <span className="truncate font-medium text-foreground">
                          {job.original_prompt}
                        </span>
                      </div>
                      {job.snapshot_id && (
                        <p className="text-xs text-muted-foreground mt-1 font-mono ">
                          ID: {job.snapshot_id.slice(0, 8)}...
                        </p>
                      )}
                    </div>
                  </div>
                </TableCell>
                <TableCell className="py-4">
                  <StatusBadge status={job.status} showIcon={true} />
                </TableCell>
                <TableCell className="py-4">
                  {formateDate(job.created_at)}
                </TableCell>
                <TableCell className="py-4">
                  {job.completed_at ? (
                    formateDate(job.completed_at)
                  ) : (
                    <span className="text-muted-foreground/60">-</span>
                  )}
                </TableCell>
                <TableCell className="py-4">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => handleDelete(e, job.id)}
                    disabled={deletingJobId === job.id}
                    className="h-8 w-8 p-0 hover:bg-destructive/10 hover:text-destructive"
                  >
                    {deletingJobId === job.id ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <Trash2 className="h-4 w-4" />
                    )}
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {/** Summary */}
      <div className="mt-6 flex items-center justify-between text-sm text-muted-foreground">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-4 h-4" />
            <span>
              {" "}
              {data?.length} total report {data?.length !== 1 ? "s" : ""}
            </span>
          </div>
          {data?.filter((job) => job.status === "COMPLETED").length > 0 && (
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full" />
              <span> {data?.length} completed</span>
            </div>
          )}
        </div>
        <div className="text-xs">Click any report to view details</div>
      </div>
    </div>
  );
};
