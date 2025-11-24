# Third-party Imports
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True)
async def analyze_scraped_data(self, job_id: str):
    """
    Analyze scraped data for the given ScrapingJob using Gemini.

    Args:
      job_id (str): The ID of the ScrapingJob whose scraped data
                      should be analyzed.

    """
    pass
