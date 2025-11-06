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
