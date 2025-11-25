# Django Imports
from django.urls import path, re_path

# DRF imports
from rest_framework.routers import DefaultRouter

# App Imports
from .views import BrightDataWebhookAPIView, ScrapingJobViewSet
from .consumers import ScrapingJoStatusWebsocketConsumer


router = DefaultRouter()
router.register("", ScrapingJobViewSet, basename="scraping-job")


webhook_urlpatterns = [
    path("brightdata/", BrightDataWebhookAPIView.as_view(), name="brightdata-webhook")
]

websocket_patterns = [
    re_path(
        r"^ws/scraping-jobs/(?P<job_id>[\w-]+)/$",
        ScrapingJoStatusWebsocketConsumer.as_asgi(),
    )
]


urlpatterns = router.urls
