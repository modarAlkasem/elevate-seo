# REST Framework Imports
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

# Third-Party Imports
from rest_framework_simplejwt.authentication import JWTAuthentication
from sentry_sdk import set_tag
from drf_spectacular.utils import extend_schema_view

# Project Imports
from core.responses import Response

# App Imports
from .services import AuthService
from .openapi import AuthViewSetSchema

set_tag("feature", "authentication")


@extend_schema_view(
    sign_up=AuthViewSetSchema.sign_up(),
    sign_in=AuthViewSetSchema.sign_in(),
    sign_in_social=AuthViewSetSchema.sign_in_social(),
    sign_out=AuthViewSetSchema.sign_out(),
)
class AuthViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    @action(methods=["POST"], detail=False, url_name="signup", url_path="signup")
    def sign_up(self, request: Request) -> Response:
        return AuthService.sign_up(request)

    @action(methods=["POST"], detail=False, url_name="signin", url_path="signin")
    def sign_in(self, request: Request) -> Response:
        return AuthService.sign_in(request)

    @action(
        methods=["POST"],
        detail=False,
        url_name="signin-social",
        url_path="social/signin",
    )
    def sign_in_social(self, request: Request) -> Response:
        return AuthService.sign_in_social(request)

    @action(
        methods=["POST"],
        detail=False,
        url_name="signout",
        url_path="signout",
        authentication_classes=[JWTAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def sign_out(self, request: Request) -> Response:
        return AuthService.sign_out(request)
