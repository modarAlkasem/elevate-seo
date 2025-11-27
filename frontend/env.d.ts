declare namespace NodeJS {
  interface ProcessEnv {
    NEXT_PUBLIC_SITE_URL: string;
    NEXT_PUBLIC_BASE_API_URL: string;
    NEXT_PUBLIC_BASE_WEBSOCKET_URL: string;

    GOOGLE_CLIENT_ID: string;
    GOOGLE_CLIENT_SECRET: string;

    NEXTAUTH_URL: string;
    AUTH_SECRET: string;
  }
}
