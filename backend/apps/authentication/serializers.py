# Python Imports
from typing import Any

# Django Imports
from django.contrib.auth.hashers import make_password, check_password
from django.db.transaction import atomic
from django.utils import timezone

# REST Framework Imports
from rest_framework import serializers

# Third-party Imports
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

# App Imports
from .models import User, Account
from .constants import (
    SignUpErrorCodeChoices,
    AccountProviderChoices,
    AccountTypeChoices,
)


class UserModelSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data: Any = None):

        if isinstance(data, dict):
            email = data.get("email")

            if email:
                data["email"] = email.strip().lower()

        return super().to_internal_value(data)

    def validate_password(self, value: str) -> str:
        hashed_password = make_password(value)
        return hashed_password

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs: {"password": {"write_only": True, "required": True}}


class SignUpModelSerializer(UserModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, email: str) -> str:

        try:
            User.objects.get(email=email)
            return email

        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email already exists",
                code=SignUpErrorCodeChoices.EMAIL_ALREADY_EXISTS.value,
            )

    def create(self, validated_data: dict) -> User:
        with atomic(durable=True):
            user = User.objects.create(**validated_data)

            account_data = {
                "type": AccountTypeChoices.CREDENTIALS.value,
                "provider": AccountProviderChoices.CREDENTIALS.value,
                "provider_account_id": user.id,
                "user": user,
            }
            Account.objects.create(**account_data)

            return user
