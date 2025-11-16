# Python Imports
from uuid import uuid4

# Django Imports
from django.db import models
from django.core.validators import MinLengthValidator
from django.core.serializers.json import DjangoJSONEncoder

# Project Imports
from core.models import CreatedAtMixin
from authentication.models import User

# App Imports
from .constants import ScrapingJobStatusChoices


class ScrapingJob(CreatedAtMixin):
    id = models.UUIDField(primary_key=True, default=uuid4)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="scraping_jobs",
        related_query_name="scraping_job",
        blank=True,
    )
    original_prompt = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(1)],
        blank=True,
        help_text="User input",
    )

    analysis_prompt = models.TextField(
        blank=True,
        null=True,
        validators=[MinLengthValidator(1)],
        help_text="Saved Gemini analysis prompt for debugging",
    )

    snapshot_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[MinLengthValidator(1)],
        help_text="BrightData scraping job's ID for tracking",
    )

    status = models.CharField(
        max_length=10, choices=ScrapingJobStatusChoices.choices, blank=True
    )

    results = models.JSONField(
        encoder=DjangoJSONEncoder,
        blank=True,
        null=True,
        help_text="Optional, filled when webhook receives data from BrightData's scraper",
    )

    seo_report = models.JSONField(
        encoder=DjangoJSONEncoder,
        blank=True,
        null=True,
        help_text="Structured SEO report from AI analysis",
    )
    error = models.TextField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["created_at"], name="scraping_job_created_at_idx"),
            models.Index(fields=["status"], name="scraping_job_statust_idx"),
            models.Index(fields=["user"], name="scraping_job_user_idx"),
            models.Index(
                fields=["user", "created_at"], name="scraping_job_user_created_idx"
            ),
        ]
