# Python Imports
from typing import Optional, Tuple, List
from urllib.parse import quote
import httpx
import logging

# REST Framework Imports
from pydantic import ValidationError
from rest_framework import status

# Django Imports
from django.conf import settings

# Project Imports
from authentication.models import User


# App Imports
from ..serializers import ScrapingJobModelSerializer, ListScrapingJobModelSerializer
from ..models import ScrapingJob
from ..prompts.perplexity import perplexity_prompt as perplexity_prompt_obj


logger = logging.getLogger(__name__)


class ScrapingJobService:

    @staticmethod
    def retry_job(job_id: str, user: User):
        pass

    @staticmethod
    async def create_new_job(
        user: User,
        original_prompt: str,
        country_code: Optional["str"] = "US",
    ):

        scraping_job = await ScrapingJob.objects.acreate(
            user=user, original_prompt=original_prompt
        )

        webhook_url = f"{settings.API_BASE_URL}{settings.BRIGHTDATA_WEBHOOK_PATH}?job-id={scraping_job.id}"
        encoded_webhook_url = quote(webhook_url, safe="")

        url = (
            f"https://api.brightdata.com/datasets/v3/trigger"
            f"?dataset_id={settings.BRIGHTDATA_DATASET_ID}"
            f"&uncompressed_webhook=true"
            f"&format=json"
            f"&auth_header=Bearer {settings.BRIGHTDATA_WEBHOOK_SECRET}"
            f"&notify={encoded_webhook_url}"
            f"&include_errors=true"
        )

        perplexity_prompt = perplexity_prompt_obj.build(original_prompt)

        payload = {
            "input": [
                {
                    "url": "https://www.perplexity.ai",
                    "prompt": perplexity_prompt,
                    "country": country_code,
                    "index": 1,
                }
            ],
            "custom_output_fields": [
                "url",
                "prompt",
                "answer_text",
                "sources",
                "citations",
                "timestamp",
                "input",
            ],
        }

        headers = {
            "Authorization": f"Bearer {settings.BRIGHTDATA_API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload, headers=headers)

                if not response.is_success:
                    error_text = response.text or ""
                    error_msg = f"HTTP {response.status_code}: {error_text}"

                    logger.error(
                        f"BrightData API call's error for job {scraping_job.id}: {error_text}"
                    )

                    await ScrapingJob.objects.set_job_to_failed(
                        scraping_job.id, error_msg
                    )

                    return (
                        error_msg,
                        "UNKNOWN_ERROR",
                        status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                data = response.json()

                if data and data.get("snapshot_id"):
                    await ScrapingJob.objects.update_job_with_snapshot_id(
                        scraping_job.id, data.get("snapshot_id")
                    )

                    response_data = await ScrapingJobModelSerializer(
                        instance=scraping_job
                    ).adata
                    return (
                        response_data,
                        "CREATED",
                        status.HTTP_201_CREATED,
                    )

        except httpx.TimeoutException as e:
            error_msg = str(e)
            logger.error(
                f"BrightData API call timeout error for job {scraping_job.id}: {error_msg}"
            )

            await ScrapingJob.objects.set_job_to_failed(scraping_job.id, error_msg)

            return (
                error_msg,
                "UNKNOWN_ERROR",
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            error_msg = str(e)
            logger.error(
                f"BrightData API call's error for job {scraping_job.id}: {error_msg}"
            )

            await ScrapingJob.objects.set_job_to_failed(scraping_job.id, error_msg)

            return (
                error_msg,
                "UNKNOWN_ERROR",
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    async def list(user_id: int) -> Tuple[Optional[List[ScrapingJob]], str, int]:

        try:
            jobs = await ScrapingJob.objects.aget_user_jobs(user_id)
            response_data = ListScrapingJobModelSerializer(
                instance=jobs, many=True
            ).data
            return (
                response_data,
                "SUCCESS",
                status.HTTP_200_OK,
            )

        except ValidationError as e:
            logger.error(
                f"SEO report validation error when fetching jobs for user: {user_id}",
                extra={"validation_errors": e.errors()},
            )

            return (
                None,
                "BAD_REQUEST",
                status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(
                f"Error when fetching jobs for user: {user_id}",
                extra={"error_detail": str(e)},
            )

            return (
                None,
                "BAD_REQUEST",
                status.HTTP_400_BAD_REQUEST,
            )
