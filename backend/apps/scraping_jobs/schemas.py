# Python Imports
from enum import Enum
from typing import List, Optional, Literal
from datetime import datetime

# Third-party Imports
from pydantic import BaseModel, Field, field_validator


class EntityType(str, Enum):
    PERSON = "person"
    BUSINESS = "business"
    PRODUCT = "product"
    COURSE = "course"
    WEBSITE = "website"
    UNKNOWN = "unknown"


class Entent(str, Enum):
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
