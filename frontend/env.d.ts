declare namespace NodeJS {
  interface ProcessEnv {
    NEXT_PUBLIC_SITE_URL: string;
    NEXT_PUBLIC_BASE_API_URL: string;
    NEXT_PUBLIC_WEB_SOCKET_BASE_API_URL: string;

    GOOGLE_CLIENT_ID: string;
    GOOGLE_CLIENT_SECRET: string;

    NEXT_AUTHURL: string;
    AUTH_SECRET: string;
  }
}
