# Django Imports
from django.urls import path, re_path

# DRF imports
from rest_framework.routers import DefaultRouter

# App Imports
from .views import BrightDataWebhookAPIView, ScrapingJobViewSet
from .consumers import ScrapingJobsStatusWebsocketConsumer


router = DefaultRouter()
router.register("api/scraping-jobs", ScrapingJobViewSet, basename="scraping-job")


webhook_urlpatterns = [
    path(
        "webhooks/brightdata/",
        BrightDataWebhookAPIView.as_view(),
        name="brightdata-webhook",
    )
]

websocket_patterns = [
    path(
        "ws/scraping-jobs/status/",
        ScrapingJobsStatusWebsocketConsumer.as_asgi(),
    )
]


urlpatterns = router.urls + webhook_urlpatterns
