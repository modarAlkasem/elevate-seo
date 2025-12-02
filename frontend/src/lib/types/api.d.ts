import type { SeoReport } from "../seo-schema";

type JsonPrimitives =
  | string
  | number
  | boolean
  | Date
  | symbol
  | undefined
  | null;

type JsonArray = Json[];

type JsonRecord<T> = {
  [Property in keyof T]: Json;
};

type Json<T = any> = JsonPrimitives | JsonArray | JsonRecord<T>;

interface APIResponse<T = any> {
  data: T;
  status_text: string;
  status_code: number;
}

interface ErrorAPIResponse extends Omit<APIResponse, "data"> {
  errors: Json;
}

interface APIUser {
  id: number;
  name: string;
  email: string;
  email_verified: boolean;
  last_signed_in: string | null;
  is_active: boolean;
  avatar: string | null;
  created_at: string;
  updated_at: string;
}

type ScrapingJobStatus =
  | "PENDING"
  | "RUNNING"
  | "ANALYZING"
  | "COMPLETED"
  | "FAILED";

interface ScrapingJob {
  id: string;
  user: number;
  status: ScrapingJobStatus;
  original_prompt?: string;
  analysis_prompt?: string;
  snapshot_id: string;
  results?: Array;
  seo_report?: SeoReport;
  error?: string;
  completed_at?: string;
  created_at: string;
}
