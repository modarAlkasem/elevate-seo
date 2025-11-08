# Python Imports
from typing import Callable

# REST Framework Imports
from rest_framework.request import Request
from rest_framework import status

# Third Party Imports
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from urllib3 import response

# App Imports
from authentication.serializers import (
    SignInSocialModelSerializer,
    SignUpModelSerializer,
    SignInSerializer,
    SignOutSerializer,
    UserModelSerializer,
)


class AuthViewSetSchema:

    @staticmethod
    def sign_up() -> Callable:
        return extend_schema(
            tags=["Authentication"],
            description="Sign user up with credentials",
            request=SignUpModelSerializer,
            responses=UserModelSerializer,
            examples=[
                OpenApiExample(
                    name="Sign Up New User Request Example",
                    value={"email": "test@test.com", "password": "#test12345"},
                    request_only=True,
                ),
                OpenApiExample(
                    name="Sign Up New User Response Example",
                    value={
                        "data": {
                            "id": 1,
                            "name": None,
                            "email": "test@test.com",
                            "email_verified": "True",
                            "last_signed_in": None,
                            "is_active": True,
                            "avatar": None,
                            "created_at": "2025-11-08T16:25:43.123456Z",
                            "updated_at": None,
                        },
                        "status_code": status.HTTP_201_CREATED,
                        "status_text": "CREATED",
                    },
                    response_only=True,
                ),
            ],
        )

    @staticmethod
    def sign_in() -> Callable:
        return extend_schema(
            tags=["Authentication"],
            description="Sign user in with credentials",
            request=SignInSerializer,
            responses=None,
            examples=[
                OpenApiExample(
                    name="Sign In Request Example",
                    value={"email": "test@test.com", "password": "#test12345"},
                    request_only=True,
                ),
                OpenApiExample(
                    name="Sign In Response Example",
                    value={
                        "data": {
                            "user": {
                                "id": 1,
                                "name": None,
                                "email": "test@test.com",
                                "email_verified": "True",
                                "last_signed_in": None,
                                "is_active": True,
                                "avatar": None,
                                "created_at": "2025-11-08T16:25:43.123456Z",
                                "updated_at": None,
                            },
                            "tokens": {
                                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ...",
                                "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ...",
                            },
                        },
                        "status_code": status.HTTP_200_OK,
                        "status_text": "SUCCESS",
                    },
                    response_only=True,
                ),
            ],
        )

    @staticmethod
    def sign_in_social() -> Callable:
        return extend_schema(
            tags=["Authentication"],
            description="Sign user in with social provider",
            request=SignInSocialModelSerializer,
            responses=None,
            examples=[
                OpenApiExample(
                    name="Social Sign In Request Example",
                    value={
                        "email": "test@test.com",
                        "provider": "GOOGLE",
                        "id_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ...",
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ...",
                    },
                    request_only=True,
                ),
                OpenApiExample(
                    name="Social Sign In Response Example",
                    value={
                        "data": {
                            "user": {
                                "id": 1,
                                "name": None,
                                "email": "test@test.com",
                                "email_verified": "True",
                                "last_signed_in": None,
                                "is_active": True,
                                "avatar": None,
                                "created_at": "2025-11-08T16:25:43.123456Z",
                                "updated_at": None,
                            },
                            "tokens": {
                                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ...",
                                "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ...",
                            },
                        },
                        "status_code": status.HTTP_200_OK,
                        "status_text": "SUCCESS",
                    },
                    response_only=True,
                ),
            ],
        )

    @staticmethod
    def sign_out() -> Callable:
        return extend_schema(
            tags=["Authentication"],
            description="Sign user out",
            request=SignOutSerializer,
            responses=None,
            examples=[
                OpenApiExample(
                    name="Sign Out Request Example",
                    value={
                        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ..."
                    },
                    request_only=True,
                ),
                OpenApiExample(
                    name="Sign Out Response Example",
                    value={
                        "data": None,
                        "status_code": status.HTTP_200_OK,
                        "status_text": "SUCCESS",
                    },
                    response_only=True,
                ),
            ],
        )
