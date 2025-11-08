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
