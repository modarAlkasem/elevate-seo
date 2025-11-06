# Django Imports
from django.urls import path

# Third Party Imports
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="auth-token-refresh")
]
