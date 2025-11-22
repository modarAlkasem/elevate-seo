# REST Framework Imports
from rest_framework import serializers

# Async REST Framework Imports
from adrf.serializers import ModelSerializer as AsyncModelSerializer

# App Imports
from .models import ScrapingJob


class ScrapingJobCreationSerializer(serializers.Serializer):
    prompt = serializers.CharField(min_length=2, max_length=255)
    country_code = serializers.CharField(min_length=2, max_length=2)
    existing_job_id = serializers.UUIDField(required=False)


class ScrapingJobModelSerializer(AsyncModelSerializer):

    class Meta:
        model = ScrapingJob
        fields = "__all__"
