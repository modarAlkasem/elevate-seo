"use client";

import { use } from "react";
import { useQuery } from "@tanstack/react-query";
import { AlertTriangle, Loader2 } from "lucide-react";

import { getScrapingJobBySnapshotID } from "@/lib/api/scrapingJob/fetchers";
import { scrapingJobKeys } from "@/lib/query-keys";
import {
  KeyMetricsGrid,
  OverallScoreCard,
  SourceDistributionChart,
  SummaryHeader,
  CompetitorStrengthCard,
  RecommendationsCard,
  KeywordAnalysisGrid,
  KeyInsightsGrid,
  AdditionalAnalysisGrid,
} from "./ui";

interface ReportSummaryPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default function ReportSummaryPage({ params }: ReportSummaryPageProps) {
  // const { id } = use(params);
  // const { data, isPending, error } = useQuery({
  //   queryKey: scrapingJobKeys.bySnapshot(id),
  //   queryFn: () => getScrapingJobBySnapshotID({ snapshot_id: id }),
  // });

  //   if (isPending) {
  //     return (
  //       <div className="flex items-center justify-center min-h-screen">
  //         <div className="text-center">
  //           <Loader2 className="w-8 h-8 animate-spin text-primary mx-auto mb-4" />
  //           <p className="text-muted-foreground ">Loading SEO report...</p>
  //         </div>
  //       </div>
  //     );
  //   }

  //   if (error || !data?.seo_report) {
  //     return (
  //       <div className="flex items-center justify-center min-h-screen">
  //         <div className="text-center">
  //           <AlertTriangle className="w-12 h-12 text-destructive mx-auto mb-4" />
  //           <h2 className="text-2xl font-bold mb-2"> Report Not Found</h2>
  //           <p className="text-muted-foreground ">
  //             The requested report could not be found.
  //           </p>
  //         </div>
  //       </div>
  //     );
  //   }

  return (
    <div className="min-h-screen bg-gradient-t-br from-background via-background to-muted/20">
      <SummaryHeader />

      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 lg:py-12 space-y-8 lg:space-y-12">
        <OverallScoreCard />
        <KeyMetricsGrid />

        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6 lg:gap-8">
          <SourceDistributionChart />
          <CompetitorStrengthCard />
        </div>

        <RecommendationsCard />
        <KeywordAnalysisGrid />
        <KeyInsightsGrid />
        <AdditionalAnalysisGrid />
      </div>
    </div>
  );
}
