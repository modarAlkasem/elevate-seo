# Python Imports
from typing import Any
import logging

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
    SignInErrorCodeChoices,
)

logger = logging.Logger(__name__)


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
            account = Account.objects.create(**account_data)

            logger.info(
                f"New user & account has been created successfully: User ID={user.id} Account ID={account.id}"
            )
            return user

    class Meta(UserModelSerializer.Meta):
        pass


class SignInModelSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    ip_address = serializers.IPAddressField(required=False)
    user_agent = serializers.CharField()

    def to_internal_value(self, data: Any = None):

        if isinstance(data, dict):
            email = data.get("email")

            if email:
                data["email"] = email.strip().lower()

        return super().to_internal_value(data)

    def validate(self, attrs: dict):
        try:
            user = User.objects.get(email=attrs.get("email"))

            if not user.password:
                logger.error(
                    f"Wrong sign in method: Email{attrs.get("email") } IP Adress:{attrs.get("ip_address",None)} User Agent:{attrs.get("user_agent")}"
                )
                raise serializers.ValidationError(
                    {"non_field_error": "Invalid sign in method"},
                    code=SignInErrorCodeChoices.USER_MISSING_PASSWORD.value,
                )

            if not check_password(attrs.get("password"), user.password):
                raise ValueError("Invalid Password")

            if not user.email_verified:
                logger.error(
                    f"Unverified user's sign in attempt: Email{attrs.get("email") } IP Adress:{attrs.get("ip_address",None)} User Agent:{attrs.get("user_agent")}"
                )
                raise serializers.ValidationError(
                    {"email": "Unverified email"},
                    code=SignInErrorCodeChoices.UNVERIFIED_EMAIL.value,
                )

            if not user.is_active:
                logger.error(
                    f"Disabled user's sign in attempt: Email{attrs.get("email") } IP Adress:{attrs.get("ip_address",None)} User Agent:{attrs.get("user_agent")}"
                )
                raise serializers.ValidationError(
                    {"email": "Unverified email"},
                    code=SignInErrorCodeChoices.ACCOUNT_DISABLED.value,
                )

            user.last_signed_in = timezone.now()
            user.save()

            refresh_token = RefreshToken.for_user(user)
            return {
                "user": UserModelSerializer(instance=user).data,
                "tokens": {
                    "access": refresh_token.access_token,
                    "refresh": str(refresh_token),
                },
            }

        except (User.DoesNotExist, ValueError):
            logger.error(
                f"Failed sign in attempt: Email{attrs.get("email") } IP Adress:{attrs.get("ip_address",None)} User Agent:{attrs.get("user_agent")}"
            )
            raise serializers.ValidationError(
                {"non_field_error": "Email or password  is incorrect"},
                code=SignInErrorCodeChoices.INCORRECT_EMAIL_PASSWORD.value,
            )


class AccountModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = "__all__"


class AccountWithUserModelSerializer(AccountModelSerializer):
    user = UserModelSerializer()

    class Meta(AccountModelSerializer.Meta):
        pass
