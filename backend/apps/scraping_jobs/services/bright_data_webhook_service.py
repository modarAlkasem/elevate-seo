# Python Imports
import hmac
import hashlib
import logging

# Django Imports
from django.conf import settings


# REST Framework Imports
from rest_framework import status
from rest_framework.request import Request

# Third-party Imports
from pydantic import ValidationError


# App Imports
from ..models import ScrapingJob


logger = logging.Logger(__name__)


class BrightDataWebhookService:

    @staticmethod
    async def handle(request: Request):
        try:

            data = request.data
            signature = request.headers.get("X-BrightData-Signature")
            secret: str = settings.BRIGHTDATA_WEBHOOK_SECRET

            computed = hmac.new(
                secret.encode(), request.body, hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(computed or "", signature):
                logger.error(
                    "Unauthorized BrightData webhook access", extra={"data": data}
                )
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

            # Here where should schedule AI analysis as Celery task

            return None, "SUCCESS", status.HTTP_200_OK

        except ValidationError as e:
            logger.error(
                "SEO report's schema validation falied", extra={"errors": e.errors()}
            )
            return e.errors(), "UNKNOWN_ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR
