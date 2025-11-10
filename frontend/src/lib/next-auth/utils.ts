export const useSecureCookies =
  process.env.NODE_ENV === "production" &&
  String(process.env.NEXTAUTH_URL).startsWith("https://");

const secureCookiePrefix = useSecureCookies ? "__Secure-" : "";

export const formatSecureCookieName = (name: string) =>
  `${secureCookiePrefix}${name}`;
