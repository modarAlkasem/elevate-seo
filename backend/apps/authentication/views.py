# REST Framework Imports
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# Third-Party Imports
from rest_framework_simplejwt.authentication import JWTAuthentication

# Project Imports
from core.responses import Response

# App Imports
from .services import AuthService


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
