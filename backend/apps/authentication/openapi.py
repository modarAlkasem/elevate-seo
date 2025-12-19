# Python Imports
from typing import Callable

# Third Party Imports
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status

# App Imports
from authentication.serializers import (
    SignInSerializer,
    SignInSocialModelSerializer,
    SignOutSerializer,
    SignUpModelSerializer,
    UserModelSerializer,
)


class AuthViewSetSchema:

    @staticmethod
    def sign_up() -> Callable:
        return extend_schema(
            tags=["Authentication"],
            description="Sign user up with credentials",
            request=SignUpModelSerializer,
            responses={201: UserModelSerializer},
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
                            "updated_at": "2025-11-08T16:25:43.123456Z",
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
            responses={200: SignInSerializer},
            examples=[
                OpenApiExample(
                    name="Sign In Request Example",
                    value={
                        "email": "test@test.com",
                        "password": "#test12345",
                        "ip_address": "192.168.1.25",
                        "user_agent": "Chrome/120.0.0.0 Safari/537.36",
                    },
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
                                "last_signed_in": "2025-11-08T16:25:43.123456Z",
                                "is_active": True,
                                "avatar": None,
                                "created_at": "2025-11-08T16:25:43.123456Z",
                                "updated_at": "2025-11-08T16:25:43.123456Z",
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
            responses={200: SignInSocialModelSerializer},
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
                                "last_signed_in": "2025-11-08T16:25:43.123456Z",
                                "is_active": True,
                                "avatar": None,
                                "created_at": "2025-11-08T16:25:43.123456Z",
                                "updated_at": "2025-11-08T16:25:43.123456Z",
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
            examples=[
                OpenApiExample(
                    name="Sign Out Request Example",
                    value={"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ..."},
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
