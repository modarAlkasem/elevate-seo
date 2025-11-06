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


class SignInErrorCodeChoices(models.TextChoices):
    INCORRECT_EMAIL_PASSWORD = "INCORRECT_EMAIL_PASSWORD"
    USER_MISSING_PASSWORD = "USER_MISSING_PASSWORD"
    CREDENTIALS_NOT_FOUND = "CREDENTIALS_NOT_FOUND"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    INCORRECT_PASSWORD = "INCORRECT_PASSWORD"
    UNVERIFIED_EMAIL = "UNVERIFIED_EMAIL"
    ACCOUNT_DISABLED = "ACCOUNT_DISABLED"
