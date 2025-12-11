# Python Imports
from typing import Optional, Tuple, List, TypedDict
from urllib.parse import quote
import httpx
import logging

# REST Framework Imports
from pydantic import ValidationError
from rest_framework import status

# Third-Party Imports
from asgiref.sync import sync_to_async

# Django Imports
from django.conf import settings

# Project Imports
from authentication.models import User


# App Imports
from ..serializers import ScrapingJobModelSerializer, ListScrapingJobModelSerializer
from ..models import ScrapingJob
from ..prompts.perplexity import perplexity_prompt as perplexity_prompt_obj
from ..tasks import analyze_scraped_data


logger = logging.getLogger(__name__)


class StartBrightDataScrapingReturn(TypedDict):
    snapshot_id: Optional[str]
    message: Optional[str]
    code: int


class ScrapingJobService:

    @classmethod
    async def retry_job(cls, job_id: str, user: User):
        retry_info = await ScrapingJob.objects.can_use_smart_retry(job_id, user.id)

        job = await ScrapingJob.objects.get_job_by_id(job_id)
        if retry_info.get("can_retry_analysis_only"):
            await ScrapingJob.objects.reset_job_for_analyzing_retry(job.id)
            analyze_scraped_data.delay(job_id)

        elif not retry_info.get("has_scraping_data"):
            bt_scraping_result = await cls.start_brightdata_scraping(job)

            if (
                not bt_scraping_result.get("success")
                and bt_scraping_result.get("code")
                == status.HTTP_500_INTERNAL_SERVER_ERROR
            ):
                return (
                    bt_scraping_result.get("message"),
                    "UNKNOWN_ERROR",
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            snapshot_id = bt_scraping_result.get("snapshot_id")

            await ScrapingJob.objects.update_job_with_snapshot_id(job.id, snapshot_id)

        response_data = await ScrapingJobModelSerializer(instance=job).adata
        return (
            response_data,
            "SUCCESS",
            status.HTTP_200_OK,
        )

    @staticmethod
    async def start_brightdata_scraping(
        job: ScrapingJob, original_prompt: Optional[str], country_code: Optional[str]
    ) -> StartBrightDataScrapingReturn:
        webhook_url = (
            f"{settings.API_BASE_URL}{settings.BRIGHTDATA_WEBHOOK_PATH}?job-id={job.id}"
        )
        encoded_webhook_url = quote(webhook_url, safe="")

        url = (
            f"https://api.brightdata.com/datasets/v3/trigger"
            f"?dataset_id={settings.BRIGHTDATA_DATASET_ID}"
            f"&uncompressed_webhook=true"
            f"&format=json"
            f"&auth_header=Bearer {settings.BRIGHTDATA_WEBHOOK_SECRET}"
            f"&endpoint={encoded_webhook_url}"
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
                        f"BrightData API call's error for job {job.id}: {error_text}"
                    )

                    await ScrapingJob.objects.set_job_to_failed(job.id, error_msg)

                    return {
                        "message": error_msg,
                        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    }

                data = response.json()

                return {
                    "message": "success",
                    "snapshot_id": data.get("snapshot_id"),
                    "code": status.HTTP_200_OK,
                }

        except httpx.TimeoutException as e:
            error_msg = str(e)
            logger.error(
                f"BrightData API call timeout error for job {job.id}: {error_msg}"
            )

            await ScrapingJob.objects.set_job_to_failed(job.id, error_msg)

            return {
                "message": error_msg,
                "snapshot_id": None,
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }

        except Exception as e:
            error_msg = str(e)
            logger.error(
                f"Error happened while updating job status to failed (Job ID:  {job.id}): {error_msg}"
            )

            return {
                "message": error_msg,
                "snapshot_id": None,
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }

    @classmethod
    async def create_new_job(
        cls,
        user: User,
        original_prompt: str,
        country_code: Optional["str"] = "US",
    ):

        scraping_job = await ScrapingJob.objects.acreate(
            user=user, original_prompt=original_prompt
        )

        bt_scraping_result = await cls.start_brightdata_scraping(
            scraping_job, original_prompt, country_code
        )

        if (
            not bt_scraping_result.get("success")
            and bt_scraping_result.get("code") == status.HTTP_500_INTERNAL_SERVER_ERROR
        ):
            return (
                bt_scraping_result.get("message"),
                "UNKNOWN_ERROR",
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        snapshot_id = bt_scraping_result.get("snapshot_id")

        await ScrapingJob.objects.update_job_with_snapshot_id(
            scraping_job.id, snapshot_id
        )

        await sync_to_async(scraping_job.refresh_from_db)(fields=["snapshot_id"])
        response_data = await ScrapingJobModelSerializer(instance=scraping_job).adata
        return (
            response_data,
            "CREATED",
            status.HTTP_201_CREATED,
        )

    @staticmethod
    async def list(user_id: int) -> Tuple[Optional[List[ScrapingJob]], str, int]:

        try:
            jobs = await ScrapingJob.objects.aget_user_jobs(user_id)

            return (
                jobs,
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

    @staticmethod
    async def retrieve_by_snapshot_id(
        user_id: int, snapshot_id: str
    ) -> Tuple[Optional[ScrapingJob], str, int]:

        try:
            job = await ScrapingJob.objects.aget_job_by_snapshot_id(
                user_id, snapshot_id
            )

            if not job:
                logger.error(
                    f"No scraping job found with given snapshot ID ({snapshot_id}) for user ({user_id})",
                )

                return (
                    None,
                    "NOT_FOUND",
                    status.HTTP_404_NOT_FOUND,
                )

            return (
                job,
                "SUCCESS",
                status.HTTP_200_OK,
            )

        except ValidationError as e:
            logger.error(
                f"SEO report validation error when fetching job with given snapshot ID ({snapshot_id}) for user ({user_id})",
                extra={"validation_errors": e.errors()},
            )

            return (
                None,
                "BAD_REQUEST",
                status.HTTP_400_BAD_REQUEST,
            )
