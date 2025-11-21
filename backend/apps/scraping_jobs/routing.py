# Django Imports
from django.urls import path

# DRF imports
from rest_framework.routers import DefaultRouter

# App Imports
from .views import BrightDataWebhookAPIView, ScrapingJobViewSet


router = DefaultRouter()
router.register("", ScrapingJobViewSet.as_view(), basename="scraping-job")


webhook_urlpatterns = [
    path("brightdata/", BrightDataWebhookAPIView.as_view(), name="brightdata-webhook")
]

urlpatterns = router.urls
