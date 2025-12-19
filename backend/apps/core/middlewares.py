# Python Imports
from urllib.parse import parse_qs

# Third-Party Imports
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    TokenError,
    AuthenticationFailed,
    ExpiredTokenError,
)

# Project Imports
from authentication.models import User


class WebsocketJWTAuthentication(BaseMiddleware):

    def _get_raw_token(self, scope) -> str:
        raw_qs = scope.get("query_string", b"").decode("utf-8")
        parsed_qs: dict = parse_qs(raw_qs)

        token: list = parsed_qs.get("token")
        if token:
            return token[0]

        raise AuthenticationFailed("No access token is provided")

    def _get_validated_token(self, raw_token: str) -> AccessToken:

        try:
            return AccessToken(raw_token)
        except (TokenError, ExpiredTokenError) as e:
            raise InvalidToken(e.args[0])

    async def _get_user(self, validated_token: AccessToken) -> User:

        try:
            return await User.objects.aget(id=validated_token.payload.get("user_id"))
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")

    async def __call__(self, scope, receive, send):

        try:
            raw_token = self._get_raw_token(scope)

            validated_token = self._get_validated_token(raw_token)

            user = await self._get_user(validated_token)

            scope["user"] = user

            return await super().__call__(scope, receive, send)

        except Exception as e:
            await send({"type": "websocket.close", "code": 4001, "reason": str(e)})
