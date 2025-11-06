# Django Imports
from django.db import models


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField("created at", blank=True, auto_now_add=True)

    class Meta:
        abstract = True


class TimeStampMixin(CreatedAtMixin):
    updated_at = models.DateTimeField("updated at", blank=True, auto_now=True)

    class Meta:
        abstract = True
