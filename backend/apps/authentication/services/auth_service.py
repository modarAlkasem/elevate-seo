# REST Framework Imports
from rest_framework import status
from rest_framework.request import Request
from rest_framework.serializers import ValidationError

# Third Party Imports
from rest_framework_simplejwt.tokens import RefreshToken

# Project Imports
from core.responses import Response

# App Imports
from ..serializers import (
    SignInSerializer,
    SignInSocialModelSerializer,
    SignOutSerializer,
    SignUpModelSerializer,
    UserModelSerializer,
)
from ..constants import SignInErrorCodeChoices, SignUpErrorCodeChoices


class AuthService:

    @staticmethod
    def sign_up(request: Request) -> Response:
        data = request.data
        response = {}
        serializer = SignUpModelSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            response = {
                "data": UserModelSerializer(instance=user).data,
                "status_code": status.HTTP_201_CREATED,
                "status_text": "CREATED",
            }

        except ValidationError as e:
            response = {
                "data": e.detail,
                "status_code": status.HTTP_400_BAD_REQUEST,
            }

            if "email" in e.detail:
                for error in e.detail["email"]:
                    if error.code == SignUpErrorCodeChoices.EMAIL_ALREADY_EXISTS.value:
                        response["status_text"] = error.code

        return Response(**response)

    @staticmethod
    def sign_in(request: Request) -> Response:
        data = request.data
        response = {}
        serializer = SignInSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)

            response = {
                "data": serializer.validated_data,
                "status_code": status.HTTP_200_OK,
            }

        except ValidationError as e:
            response = {"data": e.detail, "status_code": status.HTTP_401_UNAUTHORIZED}

            [_, [error_detail]] = list(e.detail.items())[0]
            if error_detail.code in SignInErrorCodeChoices.values:
                response["status_text"] = error_detail.code

        return Response(**response)

    @staticmethod
    def sign_in_social(request: Request) -> Response:
        data = request.data
        serializer = SignInSocialModelSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.validated_data, status_code=status.HTTP_200_OK)

    @staticmethod
    def sign_out(request: Request) -> Response:

        data = request.data
        serializer = SignOutSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        refresh_token = RefreshToken(serializer.validated_data["refresh"].token)
        refresh_token.blacklist()

        return Response()
