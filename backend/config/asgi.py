"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

# Python Imports
import os

# Django Imports
from django.core.asgi import get_asgi_application

# Third Party Imports
from channels.routing import ProtocolTypeRouter


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({"http": django_asgi_app})
