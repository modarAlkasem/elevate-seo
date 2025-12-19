# Python Imports
from uuid import uuid4

# Django Imports
from django.db import models

# App Imports
from .constants import AccountProviderChoices, AccountTypeChoices

# Project Imports
from core.models import CreatedAtMixin, TimeStampMixin


class User(TimeStampMixin):
    name = models.CharField("name", max_length=150, blank=True, null=True)
    email = models.EmailField("email", unique=True)
    password = models.CharField("password", max_length=128, blank=True, null=True)
    email_verified = models.BooleanField(
        "email verified",
        blank=True,
        default=True,
        help_text="""
        Specify whether user's email is confirmed or not.
        Note: for now it defaults to True after until
        User Email Confirmation mechanism being applied.
        """,
    )
    last_signed_in = models.DateTimeField("last signed in", null=True)
    is_active = models.BooleanField(
        "is active",
        blank=True,
        default=True,
        help_text="""
        Define the activity status of user,
        set it to 'False' to disable user instead of deleting it.
        """,
    )
    avatar = models.CharField(
        "avatar",
        blank=True,
        null=True,
        help_text="User's avatar obtained from social login provider.",
    )

    REQUIRED_FIELDS = []  # Used by Django Simple JWT package
    USERNAME_FIELD = "email"  # Used by Django Simple JWT package

    @property
    def is_anonymous(self):
        """
        Implemented since used by Django Simple JWT package but
        it'wont has any effect on authenticated process
        """
        return False

    @property
    def is_authenticated(self):
        """
        Implemented since used by Django Simple JWT package but
        it'wont has any effect on authenticated process
        """
        return True


class Account(CreatedAtMixin):
    id = models.UUIDField("id", primary_key=True, default=uuid4)
    user = models.ForeignKey(
        User,
        verbose_name="user",
        on_delete=models.CASCADE,
        related_name="accounts",
        related_query_name="account",
    )

    type = models.CharField("type", max_length=15, choices=AccountTypeChoices.choices)
    provider = models.CharField("provider", max_length=15, choices=AccountProviderChoices.choices)
    provider_account_id = models.CharField("provider account id", max_length=255)
    token_type = models.CharField("token type", max_length=10, blank=True, null=True)
    scope = models.TextField("scope", blank=True, null=True)
    id_token = models.TextField("id token", blank=True, null=True)
    expires_at = models.DateTimeField("Expires at", null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "provider_account_id"],
                name="provider_account_id_unique",
            )
        ]
