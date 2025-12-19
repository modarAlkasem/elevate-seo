# Django Imports
from django.views.decorators.csrf import csrf_exempt

# REST Framework Imports
from rest_framework.request import Request
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework.decorators import action

# Async REST Framework Imports
from adrf.views import APIView
from adrf.viewsets import ViewSet

# Project Imports
from core.responses import Response

# App Imports
from .services import ScrapingJobService, BrightDataWebhookService
from .serializers import (
    ScrapingJobCreationSerializer,
    ListScrapingJobModelSerializer,
    ScrapingJobModelSerializer,
)


class ScrapingJobViewSet(ViewSet):

    async def create(self, request: Request) -> Response:
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
                response_data, status_text, status_code = await ScrapingJobService.create_new_job(
                    user,
                    validated_data.get("prompt"),
                    validated_data.get("country_code"),
                )
        except ValidationError as e:
            response_data, status_text, status_code = (
                e.detail,
                None,
                status.HTTP_400_BAD_REQUEST,
            )

        return Response(data=response_data, status_text=status_text, status_code=status_code)

    async def list(self, request: Request) -> Response:
        user = request.user
        jobs, status_text, status_code = await ScrapingJobService.list(user.id)
        response_data = []

        if jobs:
            response_data = await ListScrapingJobModelSerializer(instance=jobs, many=True).adata

        return Response(data=response_data, status_text=status_text, status_code=status_code)

    @action(methods=["GET"], detail=False, url_path=r"by-snapshot/(?P<snapshot_id>[^/.]+)")
    async def retrieve_by_snapshot_id(self, request: Request, snapshot_id: str) -> Response:
        user = request.user
        job, status_text, status_code = await ScrapingJobService.retrieve_by_snapshot_id(
            user.id, snapshot_id
        )

        if job:
            job = await ScrapingJobModelSerializer(instance=job).adata

        return Response(data=job, status_text=status_text, status_code=status_code)

    @action(methods=["POST"], detail=True)
    async def retry(self, request: Request, pk: str) -> Response:
        user = request.user
        job, status_text, status_code = await ScrapingJobService.retry_job(pk, user)

        return Response(data=job, status_text=status_text, status_code=status_code)


class BrightDataWebhookAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @csrf_exempt
    async def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        response_data, status_text, status_code = await BrightDataWebhookService.handle(request)

        return Response(data=response_data, status_text=status_text, status_code=status_code)
