import { z } from "zod";

//Base Schema
const evidenceSchema = z.object({
  url: z.string(),
  quote: z.string(),
  relevance_score: z.number().min(0).max(1),
});

const sourceSchema = z.object({
  title: z.string(),
  url: z.string(),
  description: z.string().nullable(),
});

// Main SEO report schema
export const seoReportSchema = z.object({
  meta: z.object({
    entity_name: z.string(),
    entity_type: z.enum([
      "person",
      "business",
      "product",
      "course",
      "website",
      "unknown",
    ]),
    analysis_data: z.string(),
    data_sources_count: z.number(),
    confidence_score: z.number().min(0).max(1),
  }),
  inventory: z.object({
    total_sources: z.number(),
    unique_domains: z.array(z.string()),
    source_types: z.object({
      social_media: z
        .array(
          z.object({
            domain: z.string(),
            url: z.string(),
            title: z.string(),
            description: z.string().nullable(),
            quality_score: z.number().min(0).max(1).optional(),
          })
        )
        .optional(),
      professional: z
        .array(
          z.object({
            domain: z.string(),
            url: z.string(),
            title: z.string(),
            description: z.string().nullable(),
            quality_score: z.number().min(0).max(1).optional(),
          })
        )
        .optional(),
      educational: z
        .array(
          z.object({
            domain: z.string(),
            url: z.string(),
            title: z.string(),
            description: z.string().nullable(),
            quality_score: z.number().min(0).max(1).optional(),
          })
        )
        .optional(),
      community: z
        .array(
          z.object({
            domain: z.string(),
            url: z.string(),
            title: z.string(),
            description: z.string().nullable(),
            quality_score: z.number().min(0).max(1).optional(),
          })
        )
        .optional(),
      news: z
        .array(
          z.object({
            domain: z.string(),
            url: z.string(),
            title: z.string(),
            description: z.string().nullable(),
            quality_score: z.number().min(0).max(1).optional(),
          })
        )
        .optional(),
      other: z
        .array(
          z.object({
            domain: z.string(),
            url: z.string(),
            title: z.string(),
            description: z.string().nullable(),
            quality_score: z.number().min(0).max(1).optional(),
          })
        )
        .optional(),
      official: z
        .array(
          z.object({
            domain: z.string(),
            url: z.string(),
            title: z.string(),
            description: z.string().nullable(),
            quality_score: z.number().min(0).max(1).optional(),
          })
        )
        .optional(),
      media: z
        .array(
          z.object({
            domain: z.string(),
            url: z.string(),
            title: z.string(),
            description: z.string().nullable(),
            quality_score: z.number().min(0).max(1).optional(),
          })
        )
        .optional(),
      review: z
        .array(
          z.object({
            domain: z.string(),
            url: z.string(),
            title: z.string(),
            description: z.string().nullable(),
            quality_score: z.number().min(0).max(1).optional(),
          })
        )
        .optional(),
    }),
    data_range: z.object({
      earliest: z.string().nullable(),
      latest: z.string().nullable(),
    }),
  }),

  content_analysis: z.object({
    content_themes: z.array(
      z.object({
        theme: z.string(),
        frequencey: z.number(),
        intent: z
          .enum(["informational", "navigational", "transactional"])
          .optional(),
        subthemes: z.array(z.string()).optional(),
        evidence: z.array(evidenceSchema),
      })
    ),
    sentiment: z.object({
      overall: z.enum(["positive", "neutral", "negative", "mixed"]),
    }),
  }),

  keywords: z.object({
    content_keywords: z
      .array(
        z.object({
          keyword: z.string(),
          intent: z
            .enum([
              "informational",
              "navigational",
              "transactional",
              "commercial",
            ])
            .optional(),
          evidence: z.array(evidenceSchema),
        })
      )
      .max(25),
    keyword_themes: z
      .array(
        z.object({
          theme: z.string(),
          keywords: z.array(z.string()).max(8),
          evidence: z.array(evidenceSchema),
        })
      )
      .max(8),
  }),

  competitors: z
    .array(
      z.object({
        name: z.string().nullable(),
        domain: z.string(),
        strength_score: z.number().min(0).max(1),
        overlap_keywords: z.array(z.string()),
        unique_advantages: z.array(z.string()),
        relationship: z.enum(["competitor", "employer", "partner", "unknown"]),
        evidence: z.array(evidenceSchema),
      })
    )
    .min(0)
    .max(15),
  social_presence: z.object({
    platforms: z.array(
      z.object({
        platform: z.string(),
        url: z.string().nullable(),
        evidence: z.array(evidenceSchema),
      })
    ),
  }),

  backlink_analysis: z.object({
    total_backlinks: z.number(),
    refeering_domains: z.number(),
    backlink_sources: z.array(
      z.object({
        source_type: z.enum([
          "direct_mentions",
          "professional_references",
          "educational_citations",
          "community_mentions",
          "press_coverage",
          "directory_listings",
          "social_shares",
          "other",
        ]),
        domain: z.string(),
        url: z.string(),
        title: z.string(),
        description: z.string().nullable(),
        link_type: z.enum(["dofollow", "nofollow", "unknown"]).optional(),
        evidence: z.array(evidenceSchema),
      })
    ),
  }),

  recommendations: z
    .array(
      z.object({
        category: z.enum([
          "content",
          "social_media",
          "community_building",
          "brand_development",
          "competitor_analysis",
          "educational_content",
        ]),
        priority: z.enum(["high", "medium", "low"]),
        title: z.string(),
        description: z.string(),
        expected_impact: z.enum(["high", "medium", "low"]),
        effort_required: z.enum(["high", "medium", "low"]),
        evidence: z.array(evidenceSchema),
        implementation_steps: z.array(z.string()),
        data_driven_insights: z.array(z.string()).optional(),
        specific_quotes: z.array(z.string()).optional(),
      })
    )
    .max(25)
    .optional(),

  summary: z
    .object({
      overall_score: z.number().min(0).max(100).optional(),
      key_strengths: z.array(z.string()).optional(),
      critical_issues: z.array(z.string()).optional(),
      quick_wins: z.array(z.string()).optional(),
      long_term_opportunities: z.array(z.string()).optional(),
    })
    .optional(),
});

// Type inference from schema - single source of truth
export type SeoReport = z.infer<typeof seoReportSchema>;

// Individual interface  exports for convenience
export type Meta = SeoReport["meta"];
export type Inventory = SeoReport["inventory"];
export type ContentAnalysis = SeoReport["content_analysis"];
export type Keywords = SeoReport["keywords"];
export type ContentKeyword = NonNullable<Keywords["content_keywords"]>[0];
export type Competitor = SeoReport["competitors"][0];
export type SocialPresence = SeoReport["social_presence"];
export type BacklinkAnalysis = SeoReport["backlink_analysis"];
export type Recommendation = NonNullable<SeoReport["recommendations"]>[0];
export type Summary = SeoReport["summary"];
export type Evidence = NonNullable<
  NonNullable<SeoReport["content_analysis"]["content_themes"]>[0]
>["evidence"][0];

export type SentimentAnalysis = SeoReport["content_analysis"]["sentiment"];
export type SourceType = SeoReport["inventory"]["source_types"];
export type EntityType = SeoReport["meta"]["entity_type"];
export type RecommendationCategory = Recommendation["category"];
export type CompetitorRelationship = Competitor["relationship"];
export type SocialPlatform = SeoReport["social_presence"]["platforms"][0];
export type BacklinkSource =
  SeoReport["backlink_analysis"]["backlink_sources"][0];
