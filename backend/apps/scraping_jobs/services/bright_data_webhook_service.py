# Python Imports
import logging
from typing import Optional, Tuple

# Django Imports
from django.conf import settings

# REST Framework Imports
from rest_framework import status
from rest_framework.request import Request

# App Imports
from ..models import ScrapingJob
from ..tasks import analyze_scraped_data

logger = logging.getLogger(__name__)


class BrightDataWebhookService:

    @staticmethod
    async def handle(request: Request) -> Tuple[Optional[str], str, int]:

        data = request.data
        auth_header = request.headers.get("Authorization", "")
        expected_auth = f"Bearer {settings.BRIGHTDATA_WEBHOOK_SECRET}"

        if auth_header != expected_auth:
            logger.error("Unauthorized BrightData webhook access", extra={"data": data})
            return (
                "Unauthorized to do this action",
                "FORBIDDEN",
                status.HTTP_403_FORBIDDEN,
            )

        job_id = request.query_params.get("job-id")
        if not job_id:
            logger.error("No job ID found with Webhook URL", extra={"data": data})
            return (
                "No job ID found",
                "BAD_REQUEST",
                status.HTTP_400_BAD_REQUEST,
            )

        job = await ScrapingJob.objects.get_job_by_id(job_id)
        if not job:
            logger.error("No job found for job ID", extra={"job_id": job_id})
            return "No job found for job ID", "NOT_FOUND", status.HTTP_404_NOT_FOUND

        if not isinstance(data, list):
            data = [data]

        await ScrapingJob.objects.save_raw_scraping_data(job_id, data)

        analyze_scraped_data.delay(job_id)

        return None, "SUCCESS", status.HTTP_200_OK
