# Django Imports
from django.db import models


class AccountTypeChoices(models.TextChoices):
    CREDENTIALS = "CREDENTIALS"
    OAUTH = "OAUTH"


class AccountProviderChoices(models.TextChoices):
    CREDENTIALS = "CREDENTIALS"
    GOOGLE = "GOOGLE"
