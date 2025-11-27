export type DataTableScrpingJob = Omit<
  ScrapingJob,
  "results" | "seo_report" | "error"
>;

export type GetScrapingJobsResponse = DataTableScrpingJob[];
