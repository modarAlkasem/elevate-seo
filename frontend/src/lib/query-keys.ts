export const scrapingJobKeys = {
  all: ["scraping-jobs"] as const,
  list: () => [...scrapingJobKeys.all, "list"] as const,
  detail: (id: string) => [...scrapingJobKeys.all, "detail", id] as const,
  bySnapshot: (snapshotId: string) =>
    [...scrapingJobKeys.all, "by-snapshot", snapshotId] as const,

  create: () => [...scrapingJobKeys.all, "create"] as const,
  delete: (id: string) => [...scrapingJobKeys.all, "delete", id] as const,
  retry: (id: string) => [...scrapingJobKeys.all, id, "retry"],
};
