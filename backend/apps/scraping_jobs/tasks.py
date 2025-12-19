# Python Imports
from collections.abc import Sequence

# Django Imports
from django.conf import settings

# Third-party Imports
from celery import shared_task
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from langchain.messages import HumanMessage, SystemMessage
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from pydantic import ValidationError

# App Imports
from .models import ScrapingJob
from .prompts.gemini import gemini_prompt
from .schemas import SEOReportSchema
from .constants import ScrapingJobStatusChoices
from .consumers import ScrapingJoStatus

logger = get_task_logger(__name__)

channel_layer = get_channel_layer()


@shared_task(bind=True)
def analyze_scraped_data(self, job_id: str):
    """
    Analyze scraped data for the given ScrapingJob using Gemini.

    Args:
      job_id (str): The ID of the ScrapingJob whose scraped data
                      should be analyzed.

    """
    event_data: ScrapingJoStatus
    try:
        job: ScrapingJob = ScrapingJob.objects.get(id=job_id)
        user = job.user

        if not job.results or len(job.results) == 0:
            error_message = "No scraping data available for scraping job${0}"

            async_to_sync(ScrapingJob.objects.set_job_to_failed)(job.id, error_message.format(""))

            logger.error(error_message.format(f": {job.id}"))

            event_data = {
                "type": "job_status_update",
                "data": {
                    "status": ScrapingJobStatusChoices.FAILED.value,
                    "job_id": job_id,
                },
                "message": "Analyzing ScrapingJob has been failed",
            }
            async_to_sync(channel_layer.group_send)(f"user_{user.id}_jobs_status", event_data)
            return

        ScrapingJob.objects.set_job_to_analyzing(job.id)

        event_data = {
            "type": "job_status_update",
            "data": {
                "status": ScrapingJobStatusChoices.ANALYZING.value,
                "job_id": job_id,
            },
            "message": "ScrapingJob Analysis has been started",
        }
        async_to_sync(channel_layer.group_send)(f"user_{user.id}_jobs_status", event_data)

        scraping_data = job.results if isinstance(job.results, Sequence) else [job.results]
        analysis_prompt = gemini_prompt.build("USER", scraping_data)

        ScrapingJob.objects.save_analysis_prompt(job.id, analysis_prompt)

        model = ChatGoogleGenerativeAI(
            model=settings.GOOGLE_GEMINI_MODEL_IDENTIFIER,
            temperature=0.7,
            google_api_key=settings.GOOGLE_API_KEY,
        )

        structured_model = model.with_structured_output(SEOReportSchema, method="json_mode")
        messages = [
            SystemMessage(content=gemini_prompt.build("SYSTEM")),
            HumanMessage(content=analysis_prompt),
        ]

        result = structured_model.invoke(messages)

        ScrapingJob.objects.save_seo_report(job.id, result.model_dump())

        ScrapingJob.objects.set_job_to_completed(job.id)
        event_data = {
            "type": "job_status_update",
            "data": {
                "status": ScrapingJobStatusChoices.COMPLETED.value,
                "job_id": job_id,
            },
            "message": "ScrapingJob Analysis has been completed successfully",
        }
        async_to_sync(channel_layer.group_send)(f"user_{user.id}_jobs_status", event_data)

    except ScrapingJob.DoesNotExist:
        logger.error(f"No ScrapingJob found for given ID: {job_id}")
        event_data = {
            "type": "job_status_update",
            "data": {
                "status": ScrapingJobStatusChoices.FAILED.value,
                "job_id": job_id,
            },
            "message": "Analyzing ScrapingJob has been failed",
        }
        async_to_sync(channel_layer.group_send)(f"user_{user.id}_jobs_status", event_data)

    except ValidationError as e:
        logger.error("SEO report's schema validation falied", extra={"errors": e.errors()})
        event_data = {
            "type": "job_status_update",
            "data": {
                "status": ScrapingJobStatusChoices.FAILED.value,
                "job_id": job_id,
            },
            "message": "Analyzing ScrapingJob has been failed",
        }
        async_to_sync(channel_layer.group_send)(f"user_{user.id}_jobs_status", event_data)

    except Exception as e:
        async_to_sync(ScrapingJob.objects.set_job_to_failed)(job_id, str(e))

        logger.error(f"ScarpingJob {job_id} marked as failed due to analysis error")

        event_data = {
            "type": "job_status_update",
            "data": {
                "status": ScrapingJobStatusChoices.FAILED.value,
                "job_id": job_id,
            },
            "message": "Analyzing ScrapingJob has been failed",
        }
        async_to_sync(channel_layer.group_send)(f"user_{user.id}_jobs_status", event_data)
