# Python Imports
from enum import Enum
from typing import List, Optional, Literal
from datetime import datetime

# Third-party Imports
from pydantic import BaseModel, Field, field_validator


# Enums for better type safety
class EntityType(str, Enum):
    PERSON = "person"
    BUSINESS = "business"
    PRODUCT = "product"
    COURSE = "course"
    WEBSITE = "website"
    UNKNOWN = "unknown"


class Intent(str, Enum):
    INFORMATIONAL = "informational"
    NAVIGATIONAL = "navigational"
    TRANSACTIONAL = "transactional"
    COMMERCIAL = "commercial"


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    MIXED = "mixed"


class Priority(str, Enum):
    High = "high"
    MEDIUM = "medium"
    LOW = "low"


class RelationshipType(str, Enum):
    COMPETITOR = "competitor"
    EMPLOYER = "employer"
    PARTNER = "partner"
    UNKNOWN = "unknown"


class SourceTypeEnum(str, Enum):
    DIRECT_MENTIONS = "direct_mentions"
    PROFESSIONAL_REFERENCES = "professional_references"
    EDUCATIONAL_CITATIONS = "educational_citations"
    COMMUNITY_MENTIONS = "community_mentions"
    PRESS_COVERAGE = "press_coverage"
    DIRECTORY_LISTINGS = "directory_listings"
    SOCIAL_SHARES = "social_shares"
    OTHER = "other"


class LinkType(str, Enum):
    DEFOLLOW = "defollow"
    NOFOLLOW = "nofollow"
    UNKNOWN = "unknown"


class RecomendationCategory(str, Enum):
    CONTENT = "content"
    SOCIAL_MEDIA = "social_media"
    COMMUNITY_BUILDING = "community_building"
    BRAND_DEVELOPMENT = "brand_development"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    EDUCATIONAL_CONTENT = "educational_content"


# Base schemas
class EvidenceSchema(BaseModel):
    url: str
    quote: Optional[str] = None
    relevance_score: float = Field(ge=0, le=1)


class SourceSchema(BaseModel):
    title: str
    url: str
    description: Optional[str] = None


class SourceItemSchema(BaseModel):
    domain: str
    url: str
    title: str
    description: Optional[str] = None
    quality_score: Optional[float] = Field(None, ge=0, le=1)


# Meta Schema
class MetaSchema(BaseModel):
    entity_name: str
    entity_type: EntityType
    analysis_date: str
    data_source_count: int
    confidence_score: float = Field(ge=0, le=1)


# Inventory Schema
class DateRangeSchema(BaseModel):
    earliest: Optional[str] = None
    latest: Optional[str] = None


class SourceTypesSchema(BaseModel):
    social_media: Optional[List[SourceItemSchema]] = None
    professional: Optional[List[SourceItemSchema]] = None
    educational: Optional[List[SourceItemSchema]] = None
    community: Optional[List[SourceItemSchema]] = None
    news: Optional[List[SourceItemSchema]] = None
    other: Optional[List[SourceItemSchema]] = None
    official: Optional[List[SourceItemSchema]] = None
    media: Optional[List[SourceItemSchema]] = None
    review: Optional[List[SourceItemSchema]] = None


class InventorySchema(BaseModel):
    total_sources: int
    unique_domains: List[str]
    source_types: Optional[SourceTypesSchema] = None
    date_range: DateRangeSchema


# Content analysis schema
class ContentThemeSchema(BaseModel):
    theme: str
    frequency: int
    intent: Optional[Literal["informational", "navigational", "transactional"]] = None
    subthemes: Optional[List[str]] = None
    evidence: List[EvidenceSchema]


class SentimentSchema(BaseModel):
    overall: Sentiment


class ContentAnalysisSchema(BaseModel):
    content_themes: List[ContentThemeSchema]
    sentiment: SentimentSchema


# Keywords schema
class ContentKeywordSchema(BaseModel):
    keyword: str
    Intent: Optional[Intent] = None
    evidence: List[EvidenceSchema]


class KeywordThemeSchema(BaseModel):
    theme: str
    keywords: List[str] = Field(max_length=8)
    evidence: List[EvidenceSchema]

    @field_validator("keywords")
    @classmethod
    def validate_keywords_length(cls, v):
        if len(v) > 8:
            raise ValueError("Maximum 5 keywords allowed per theme")

        return v


class KeywordsSchema(BaseModel):
    content_keywords: List[ContentKeywordSchema] = Field(max_length=25)
    keyword_themes: List[KeywordThemeSchema] = Field(max_length=8)

    @field_validator("content_keywords")
    @classmethod
    def validate_content_keywords(cls, v):
        if len(v) > 25:
            raise ValueError("Maximum 25 content keywords allowed")

        return v

    @field_validator("keyword_themes")
    @classmethod
    def validate_keyword_themes_length(cls, v):
        if len(v) > 8:
            raise ValueError("Maximum 8 keyword themes allowed")

        return v


# Competitors schema
class CompetitorSchema(BaseModel):
    name: Optional[str] = None
    domain: str
    strength_score: float = Field(ge=0, le=10)
    overlap_keywords: List[str]
    unique_advantages: List[str]
    relationship: RelationshipType
    evidence: List[EvidenceSchema]


# Social presence schema
class PlatformSchema(BaseModel):
    platform: str
    url: Optional[str] = None
    evidence: List[EvidenceSchema]


class SocialPresenceSchema(BaseModel):
    platforms: List[PlatformSchema]


# Backlink analysis schema
class BacklinkSourceSchema(BaseModel):
    source_type: SourceTypeEnum
    domain: str
    url: str
    title: str
    description: Optional[str] = None
    link_type: Optional[LinkType] = None
    evidence: List[EvidenceSchema]


class BacklinkAnalysisSchema(BaseModel):
    total_backlinks: int
    referring_domains: int
    backlink_sources: List[BacklinkSourceSchema]


# Recommendations Schema
class RecommendationSchema(BaseModel):
    category: RecomendationCategory
    priority: Priority
    title: str
    description: str
    expected_impact: Priority
    effort_required: Priority
    evidence: List[EvidenceSchema]
    implementation_steps: List[str]
    data_driven_insights: Optional[List[str]] = None
    specific_quotes: Optional[List[str]] = None


# Summary Schema
class SummarySchema(BaseModel):
    overall_score: Optional[float] = Field(None, ge=0, le=100)
    key_strengths: Optional[List[str]] = None
    critical_issues: Optional[List[str]] = None
    quick_wins: Optional[List[str]] = None
    long_term_opportunities: Optional[List[str]] = None
