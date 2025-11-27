export type DataTableScrpingJob = Omit<
  ScrapingJob,
  "results" | "seo_report" | "error"
>;

export type GetScrapingJobsResponse = DataTableScrpingJob[];

export type CreateScrapingJobPayload = {
  country_code: string;
  prompt: string;
  existing_job_id?: string;
};

export type CreateScrapingJobResponse = ScrapingJob;
