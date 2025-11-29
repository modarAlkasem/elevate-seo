"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# Python Imports
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.append(os.path.join(BASE_DIR, "apps"))

# Django Imports
from django.core.asgi import get_asgi_application

# Third Party Imports
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()

# Project Imports
from scraping_jobs.routing import websocket_patterns
from core.middlewares import WebsocketJWTAuthentication

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            WebsocketJWTAuthentication(URLRouter(websocket_patterns))
        ),
    }
)
