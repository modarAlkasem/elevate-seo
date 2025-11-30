import api from "@/lib/axios";
import type {
  GetScrapingJobsResponse,
  CreateScrapingJobPayload,
  CreateScrapingJobResponse,
  GetScrapingJobBySnapshotIDPayload,
  GetScrapingJobBySnapshotIDResponse,
} from "./types";

export const getScrapingJobs = async (): Promise<GetScrapingJobsResponse> => {
  const response = (await api.get(
    "/scraping-jobs/"
  )) as unknown as APIResponse<GetScrapingJobsResponse>;

  return response.data;
};

export const createScrapingJob = async ({
  prompt,
  country_code,
  existing_job_id,
}: CreateScrapingJobPayload): Promise<CreateScrapingJobResponse> => {
  const response = (await api.post("/scraping-jobs/", {
    prompt,
    country_code,
    existing_job_id,
  })) as unknown as APIResponse<CreateScrapingJobResponse>;

  return response.data;
};

export const getScrapingJobBySnapshotID = async ({
  snapshot_id,
}: GetScrapingJobBySnapshotIDPayload): Promise<GetScrapingJobBySnapshotIDResponse> => {
  const response = (await api.get(
    `/scraping-jobs/by-snapshot/${snapshot_id}/`
  )) as unknown as APIResponse<GetScrapingJobBySnapshotIDResponse>;

  return response.data;
};
