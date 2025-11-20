# REST Framework Imports
from rest_framework.request import Request
from rest_framework.views import APIView

# Project Imports
from core.responses import Response

# App Imports
from .services import ScrapingJobService, BrightDataWebhookService


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
