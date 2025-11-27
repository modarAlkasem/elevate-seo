export const scrapingJobKeys = {
  all: ["scraping-jobs"] as const,
  list: () => [...scrapingJobKeys.all, "list"] as const,
  detail: (id: string) => [...scrapingJobKeys.all, "detail", id] as const,

  mutations: {
    create: ["create-scraping-job"] as const,
    delete: (id: string) => ["delete-scraping-job", id] as const,
  },
};
