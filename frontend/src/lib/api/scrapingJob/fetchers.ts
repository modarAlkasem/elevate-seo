import api from "@/lib/axios";
import type { GetScrapingJobsResponse } from "./types";

export const getScrapingJobs = async (): Promise<GetScrapingJobsResponse> => {
  const response = (await api.get(
    "/scraping-jobs/"
  )) as unknown as APIResponse<GetScrapingJobsResponse>;

  return response.data;
};
