# Python Imports
import os

# Third Party Imports
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("elevate_seo")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
