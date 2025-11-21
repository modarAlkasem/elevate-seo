# REST Framework Imports
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.serializers import ValidationError
from rest_framework import status

# Project Imports
from core.responses import Response

# App Imports
from .services import ScrapingJobService, BrightDataWebhookService
from .serializers import ScrapingJobCreationSerializer


class ScrapingJobViewSet(ViewSet):

    async def create(request: Request) -> Response:
        data = request.data
        user = request.user
        serializer = ScrapingJobCreationSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            existing_job_id = validated_data.get("existing_job_id")
            if existing_job_id:
                ScrapingJobService.retry_job(job_id=existing_job_id, user=user)
            else:
                response_data, status_text, status_code = (
                    await ScrapingJobService.create_new_job(
                        user,
                        validated_data.get("original_prompt"),
                        validated_data.get("country_code"),
                    )
                )
        except ValidationError as e:
            response_data, status_text, status_code = (
                e.detail,
                None,
                status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data=response_data, status_text=status_text, status_code=status_code
        )


class BrightDataWebhookAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    async def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        response_data, status_text, status_code = await BrightDataWebhookService.handle(
            request
        )

        return Response(
            data=response_data, status_text=status_text, status_code=status_code
        )
