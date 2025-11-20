# REST Framework Imports
from rest_framework import status
from rest_framework.request import Request

# Project Imports
from core.responses import Response

# App Imports
from ..serializers import ScrapingJobCreationSerializer
from ..models import ScrapingJob


class ScrapingJobService:

    @staticmethod
    async def create(request: Request) -> Response:
        data = request.data
        user = request.user

        serializer = ScrapingJobCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            existing_job_id = validated_data.get("existing_job_id")

            if existing_job_id:
                retry_info = await ScrapingJob.objects.can_use_smart_retry(
                    existing_job_id, user.id
                )

                if retry_info.get("can_retry_analysis_only", False):
                    # Smart retry's logic goes here
                    pass

            else:
                scraping_job = await ScrapingJob.objects.acreate(
                    user=user, original_prompt=validated_data.get("original_prompt")
                )
