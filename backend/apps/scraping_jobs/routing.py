# Django Imports
from django.urls import path

# App Imports
from .views import BrightDataWebhookAPIView

webhook_urlpatterns = [
    path("brightdata/", BrightDataWebhookAPIView.as_view(), name="brightdata-webhook")
]
