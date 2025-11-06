# Django Imports
from django.db import models


class AccountTypeChoices(models.TextChoices):
    CREDENTIALS = "CREDENTIALS"
    OAUTH = "OAUTH"


class AccountProviderChoices(models.TextChoices):
    CREDENTIALS = "CREDENTIALS"
    GOOGLE = "GOOGLE"


class SignUpErrorCodeChoices(models.TextChoices):
    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
