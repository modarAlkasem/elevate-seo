import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/header/header";
import { ClientWrapper } from "@/wrappers/client-wrapper";
import { Toaster } from "sonner";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ElevateSEO - AI Powered SEO Optimization Platform",
  description:
    "Boost your website, product, YT channel, etc. rankings with ElevateSEO - an AI-driven SEO optimization tool that analyze your site, competitors, keywords to deliver actionable insights, reports, and strategies for better visibility and growth.",
  keywords: [
    "SEO",
    "AI SEO",
    "SEO optimization",
    "SEO analyzer",
    "SEO report generator",
    "keyword research",
    "competitor analysis",
    "website ranking",
    "AI marketing",
    "SEO tools",
  ],
  applicationName: "ElevateSEO",
  authors: [
    {
      name: "Mudar Alkasem",
      url: "https://mail.google.com/mail/?view=cm&fs=1&to=modaralkasem@gmail.com",
    },
  ],
  creator: "Mudar Alkasem",
  publisher: "Mudar Alkasem",
  openGraph: {
    title: "ElevateSEO – AI-Powered SEO Marketing Optimization",
    description:
      "Get data-driven SEO insights and competitor analysis powered by AI. Optimize your website performance and climb search rankings with ElevateSEO.",
    url: "https://elevateseo.com",
    siteName: "ElevateSEO",
    locale: "en_US",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ClientWrapper>
          <Header /> {children}
        </ClientWrapper>
        <Toaster />
      </body>
    </html>
  );
}
