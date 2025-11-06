# Django Imports
from django.urls import path

# REST Framework Imports
from rest_framework.routers import DefaultRouter

# Third Party Imports
from rest_framework_simplejwt.views import TokenRefreshView

# App Imports
from .views import AuthViewSet

router = DefaultRouter()
router.register("", AuthViewSet, basename="auth")

urlpatterns = router.urls + [
    path("token/refresh/", TokenRefreshView.as_view(), name="auth-token-refresh")
]
