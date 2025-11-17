# Python Imports
from typing import Any, Optional
from uuid import uuid4

# Django Imports
from django.db import models
from django.core.validators import MinLengthValidator
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

# Project Imports
from core.models import CreatedAtMixin
from authentication.models import User

# App Imports
from .constants import ScrapingJobStatusChoices


class ScrapingJobQuerySet(models.QuerySet):
    def create(self, **kwargs: dict) -> ScrapingJob:
        user = kwargs.get("user")
        original_prompt = kwargs.get("original_prompt")

        if user is None:
            raise ValueError("ScrapingJob.create() requires 'user'.")

        if original_prompt is None:
            raise ValueError("ScrapingJob.create() requires 'original_prompt'.")

        data = {
            "user": user,
            "original_prompt": original_prompt,
            "status": ScrapingJobStatusChoices.PENDIN.value,
        }
        return super().create(**data)

    def update_job_with_snapshot_id(self, job_id: str, snapshot_id: str) -> None:
        if job_id is None:
            raise ValueError(
                "ScrapingJob.update_job_with_snapshot_id() requires 'job_id'."
            )

        if snapshot_id is None:
            raise ValueError(
                "ScrapingJob.update_job_with_snapshot_id() requires 'snapshot_id'."
            )

        self.filter(id=job_id).update(
            snapshot_id=snapshot_id,
            status=ScrapingJobStatusChoices.RUNNING.value,
            error=None,
        )

    def set_job_to_analyzing(self, job_id: str) -> None:

        if job_id is None:
            raise ValueError("ScrapingJob.set_job_to_analyzing() requires 'job_id'.")

        self.filter(id=job_id).update(
            status=ScrapingJobStatusChoices.ANALYZING.value,
            error=None,
        )

    def save_raw_scraping_data(self, job_id: str, raw_data: Any) -> None:
        if job_id is None:
            raise ValueError("ScrapingJob.save_raw_scraping_data() requires 'job_id'.")
        self.filter(id=job_id).update(
            results=raw_data,
            status=ScrapingJobStatusChoices.ANALYZING.value,
            error=None,
        )

    def save_seo_report(self, job_id: str, seo_report: Any) -> None:
        if job_id is None:
            raise ValueError("ScrapingJob.save_seo_report() requires 'job_id'.")

        if seo_report is None:
            raise ValueError("ScrapingJob.save_seo_report() requires 'seo_report'.")

        self.filter(id=job_id).update(
            seo_report=seo_report,
        )

    def save_analysis_prompt(self, job_id: str, prompt: str) -> None:
        if job_id is None:
            raise ValueError("ScrapingJob.save_analysis_prompt() requires 'job_id'.")

        if prompt is None:
            raise ValueError("ScrapingJob.save_analysis_prompt() requires 'prompt'.")

        self.filter(id=job_id).update(
            analysis_prompt=prompt,
        )

    def get_job_by_id(self, job_id: str) -> Optional[ScrapingJob]:

        if job_id is None:
            raise ValueError("ScrapingJob.get_job_by_id() requires 'job_id'.")

        return self.filter(id=job_id).first()

    def set_job_to_completed(self, job_id: str) -> None:

        if job_id is None:
            raise ValueError("ScrapingJob.set_job_to_completed() requires 'job_id'.")

        self.filter(id=job_id).update(
            status=ScrapingJobStatusChoices.COMPLETED.value,
            error=None,
            completed_at=timezone.now(),
        )

    def set_job_to_failed(self, job_id: str, error: str) -> None:

        if job_id is None:
            raise ValueError("ScrapingJob.set_job_to_failed() requires 'job_id'.")

        if error is None:
            raise ValueError("ScrapingJob.set_job_to_failed() requires 'error'.")

        self.filter(id=job_id).update(
            status=ScrapingJobStatusChoices.FAILED.value,
            error=error,
            completed_at=timezone.now(),
        )

    def retry_job(self, job_id: str) -> None:
        """Reset the job via reset it's status to PENDING and clear error, results and snapshotId"""
        if job_id is None:
            raise ValueError("ScrapingJob.retry_job() requires 'job_id'.")

        self.filter(id=job_id).update(
            status=ScrapingJobStatusChoices.PENDING.value,
            error=None,
            completed_at=None,
            results=None,
            seo_report=None,
            snapshot_id=None,
        )

    def can_use_smart_retry(self, job_id: str, user_id: int) -> dict:
        """
        Check if job can use smart retry (has scraping data and analysis promot)

        Args:
            job_id: scraping job ID
            user_id: User ID

        Returns:
        {
            "can_retry_analysis_only":bool,
            "has_scraping_data":bool,
            "has_analysis_prompt":bool
        }

        """

        if job_id is None:
            raise ValueError("ScrapingJob.can_use_smart_retry() requires 'job_id'.")

        if user_id is None:
            raise ValueError("ScrapingJob.can_use_smart_retry() requires 'user_id'.")

        job: ScrapingJob = self.filter(id=job_id).first()

        if not job or job.user.id != user_id:
            return {
                "can_retry_analysis_only": False,
                "has_scraping_data": False,
                "has_analysis_prompt": False,
            }

        has_scraping_data = job.results and len(job.results) > 0
        has_analysis_prompt = bool(job.analysis_prompt)
        can_retry_analysis_only = has_analysis_prompt and has_scraping_data

        return {
            "can_retry_analysis_only": can_retry_analysis_only,
            "has_scraping_data": has_scraping_data,
            "has_analysis_prompt": has_analysis_prompt,
        }


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

    objects = ScrapingJobQuerySet.as_manager()

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
