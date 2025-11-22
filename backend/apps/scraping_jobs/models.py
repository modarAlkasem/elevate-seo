# Python Imports
from typing import Any, Optional, Self, List
from uuid import uuid4

# Django Imports
from django.db import models
from django.core.validators import MinLengthValidator
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

# Third-Party Imports
from pydantic import ValidationError

# Project Imports
from core.models import CreatedAtMixin
from authentication.models import User

# App Imports
from .constants import ScrapingJobStatusChoices
from .schemas import SEOReportSchema


class ScrapingJobQuerySet(models.QuerySet):
    async def acreate(self, **kwargs: dict) -> ScrapingJob:
        """Create and return a new ScrapingJob instance

        Expected kwargs:
            user(User | str): The user instance or user ID
            original_prompt (str): The original prompt provided by user

        Returns:
            ScrapingJob: The created ScrapingJob instance.

        """
        user = kwargs.get("user")
        original_prompt = kwargs.get("original_prompt")

        data = {
            "user": user,
            "original_prompt": original_prompt,
            "status": ScrapingJobStatusChoices.PENDING.value,
        }
        return await super().acreate(**data)

    async def update_job_with_snapshot_id(self, job_id: str, snapshot_id: str) -> None:
        """
        Update a ScrapingJob instance's snapshot_id, status, and error fields.

        Args:
            job_id (str): JobScraping's ID
            snapshot_id (str): BrightData task ID for tracking.

        Return:
            None

        """
        await self.filter(id=job_id).aupdate(
            snapshot_id=snapshot_id,
            status=ScrapingJobStatusChoices.RUNNING.value,
            error=None,
        )

    def set_job_to_analyzing(self, job_id: str) -> None:
        """
        Set a ScrapingJob instance's status to ANALYZING and clear its error field.

        Args:
            job_id (str): JobScraping's ID

        Return:
            None
        """

        self.filter(id=job_id).update(
            status=ScrapingJobStatusChoices.ANALYZING.value,
            error=None,
        )

    async def save_raw_scraping_data(self, job_id: str, raw_data: Any) -> None:
        """
        Set a ScrapingJob instance's `results` field with received scraping data from BrightData,
        set the `status` field to ANALYZING, and clear the `error` field.


        Args:
            job_id (str): JobScraping's ID
            raw_data (Any): scraping data received from BrightData

        Return:
            None

        """

        await self.filter(id=job_id).aupdate(
            results=raw_data,
            status=ScrapingJobStatusChoices.ANALYZING.value,
            error=None,
        )

    def save_seo_report(self, job_id: str, seo_report: Any) -> None:
        """
        Set a ScrapingJob instance's 'seo_report' with structured data received from Gemini.

        Raises pydantic.ValidationError exception for invalid schema - caller must handle it.

        Args:
            job_id (str): The ScrapingJob instance's ID.
            seo_report (Any): The structured SEO report data.

        Return:
            None

        """

        validated = SEOReportSchema(**seo_report)
        self.filter(id=job_id).update(
            seo_report=validated.model_dump(),
        )

    def save_analysis_prompt(self, job_id: str, prompt: str) -> None:
        """
        Save or update the analysis_prompt field of a ScrapingJob instance.

        Args:
            job_id (str): The ID of the ScrapingJob instance to update.
            prompt (str): The analysis prompt text to save.

        Returns:
            None
        """

        self.filter(id=job_id).update(
            analysis_prompt=prompt,
        )

    async def get_job_by_id(self, job_id: str) -> Optional[ScrapingJob]:
        """
        Retrieve a ScrapingJob instance by its ID.

        Raises pydantic.ValidationError exception for invalid schema - caller must handle it.

        Args:
            job_id (str): The ID of the ScrapingJob instance to retrieve.

        Returns:
            Optional[ScrapingJob]: The ScrapingJob instance if found, otherwise None.
        """

        job: ScrapingJob = await self.filter(id=job_id).afirst()

        if job and job.seo_report:
            SEOReportSchema(**job.seo_report)

        return job

    def set_job_to_completed(self, job_id: str) -> None:
        """
        Mark a ScrapingJob instance as completed by updating its status, clearing errors,
        and setting the completion timestamp.

        Args:
            job_id (str): The ID of the ScrapingJob instance to update.

        Returns:
            None
        """
        self.filter(id=job_id).update(
            status=ScrapingJobStatusChoices.COMPLETED.value,
            error=None,
            completed_at=timezone.now(),
        )

    async def set_job_to_failed(self, job_id: str, error: str) -> None:
        """
        Mark a ScrapingJob instance as failed by updating its status, setting the error message,
        and recording the completion timestamp.

        Args:
            job_id (str): The ID of the ScrapingJob instance to update.
            error (str): The error message explaining why the job failed.

        Returns:
            None
        """
        await self.filter(id=job_id).aupdate(
            status=ScrapingJobStatusChoices.FAILED.value,
            error=error,
            completed_at=timezone.now(),
        )

    def retry_job(self, job_id: str) -> None:
        """
        Reset a ScrapingJob instance to allow it to be retried by setting its status
        to PENDING and clearing error, results, SEO report, snapshot_id, and completion timestamp.

        Args:
            job_id (str): The ID of the ScrapingJob instance to reset.

        Returns:
            None
        """

        self.filter(id=job_id).update(
            status=ScrapingJobStatusChoices.PENDING.value,
            error=None,
            completed_at=None,
            results=None,
            seo_report=None,
            snapshot_id=None,
        )

    async def can_use_smart_retry(self, job_id: str, user_id: int) -> dict:
        """
        Check whether a ScrapingJob can use smart retry based on available scraping data
        and analysis prompt.

        Args:
            job_id (str): The ID of the ScrapingJob instance.
            user_id (int): The ID of the user attempting the retry.

        Returns:
            dict: A dictionary containing the following keys:
                - "can_retry_analysis_only" (bool): True if both scraping data and analysis prompt exist.
                - "has_scraping_data" (bool): True if the job has scraping results.
                - "has_analysis_prompt" (bool): True if the job has an analysis prompt.
        """

        job: ScrapingJob = self.filter(id=job_id).afirst()

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

    def reset_job_for_analyzing_retry(self, job_id: str) -> None:
        """
        Reset a ScrapingJob instance for analysis retry.
        This clears analysis-related fields but preserves the scraping data.

        Args:
            job_id (str): The ID of the ScrapingJob instance to reset.

        Returns:
            None
        """

        self.filter(id=job_id).update(
            status=ScrapingJobStatusChoices.ANALYZING.value,
            error=None,
            completed_at=None,
            seo_report=None,
        )

    def get_job_by_snapshot_id(
        self, user_id: int, snapshot_id: str
    ) -> Optional[ScrapingJob]:
        """
        Retrieve a ScrapingJob instance by its BrightData snapshot ID and user ID.

        Raises pydantic.ValidationError exception for invalid schema - caller must handle it.

        Args:
            user_id (int): The ID of the user who owns the job.
            snapshot_id (str): BrightData's scraping job ID.

        Returns:
            Optional[ScrapingJob]: The ScrapingJob instance if found, otherwise None.
        """
        job: ScrapingJob = self.filter(snapshot_id=snapshot_id, user=user_id).first()
        if job and job.seo_report:
            SEOReportSchema(**job.seo_report)

        return job

    def get_user_jobs(self, user_id: int) -> Self:
        """
        Return a queryset of ScrapingJob instances belonging to a specific user.

        Raises pydantic.ValidationError exception for invalid schema - caller must handle it.

        Args:
            user_id (int): The ID of the user whose jobs should be fetched.

        Returns:
            Self: A ScrapingJobQuerySet filtered to the specified user's jobs.
        """

        jobs: List[ScrapingJob] = self.filter(user=user_id)

        for job in jobs:
            if job and job.seo_report:
                SEOReportSchema(**job.seo_report)

        return jobs

    def delete_job(self, job_id: str) -> bool:
        """
        Remove a specific ScrapingJob instance.

        Args:
            job_id (str): The ID of the ScrapingJob instance to delete.

        Returns:
            bool: True if the ScrapingJob was successfully deleted, False if it does not exist.
        """

        try:
            self.get(id=job_id).delete()
            return True
        except self.model.DoesNotExist:
            return False


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

    objects: ScrapingJobQuerySet = ScrapingJobQuerySet.as_manager()

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
