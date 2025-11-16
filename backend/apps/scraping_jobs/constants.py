# Django Imports
from django.db.models import TextChoices


class ScrapingJobStatusChoices(TextChoices):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    ANALYZING = "ANALYZING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
