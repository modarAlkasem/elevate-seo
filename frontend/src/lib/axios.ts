import axios from "axios";
import { getSession } from "next-auth/react";
import { getServerSession } from "next-auth/next";

import { NEXT_AUTH_OPTIONS } from "./next-auth/auth-options";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BASE_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  async (config) => {
    let accessToken;

    // Client-side
    if (typeof window !== "undefined") {
      const session = await getSession();
      accessToken = session?.access;
    } else if (!config.url?.includes("/api/auth/token/refresh/")) {
      const session = await getServerSession(NEXT_AUTH_OPTIONS);
      accessToken = session?.access;
    }

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    return config;
  },
  (err) => Promise.reject(err)
);

api.interceptors.response.use(
  (response) => response.data,
  (err) => Promise.reject(err.response.data || err.message)
);

export default api;
