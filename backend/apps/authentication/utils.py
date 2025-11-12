# Python Imports
from typing import Optional
from datetime import datetime
import logging

# Django Imports
from django.utils import timezone
from django.conf import settings

# Third-Party Imports
from jose import jwt
from jose.exceptions import JWTError
import requests


# App Imports
from .constants import AccountProviderChoices, AccountTypeChoices


logger = logging.Logger(__name__)


def validate_google_tokens(id_token: str, access_token: str) -> Optional[dict]:
    GOOGLE_JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"

    try:
        jwks = requests.get(GOOGLE_JWKS_URL).json()
        claims = jwt.decode(
            token=id_token,
            access_token=access_token,
            key=jwks,
            algorithms=["RS256"],
            audience=settings.OAUTH_PROVIDERS["google"]["client_id"],
        )
        return {
            "user": {
                "name": (
                    claims.get("name")
                    if claims.get("name")
                    else f'{claims.get("given_name")} {claims.get("family_name")}'
                ),
                "email": claims.get("email"),
                "email_verified": claims.get("email_verified"),
                "avatar": claims.get("picture"),
                "last_signed_in": timezone.now(),
            },
            "provider_account_id": claims.get("sub"),
            "provider": AccountProviderChoices.GOOGLE.value,
            "id_token": id_token,
            "type": AccountTypeChoices.OAUTH.value,
            "expires_at": datetime.utcfromtimestamp(claims.get("exp")),
        }

    except JWTError as e:
        logger.error(str(e))
        return None
