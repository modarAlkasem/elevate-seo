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
  disabled: boolean;
  avatar: string | null;
  created_at: string;
  updated_at: string;
}
