# Django Imports
from django.urls import reverse

# DRF Imports
from rest_framework import status
from rest_framework.test import APIClient

# Third-party Imports
import pytest

# Project Imports
from ..factories import AccountFactory, UserFactory


@pytest.mark.django_db
class TestAuthenticationAPI:
    """Test Authentication Endpoints"""

    def test_signup_success(self, api_client: APIClient):
        """Test successful user registeration using credentials method"""

        url = reverse("authentication:signup")

        data = {
            "name": "Test User",
            "email": "newuser@test.com",
            "password": "SecurePassword!",
        }

        response = api_client.post(url, data, format="json")

        assert status.HTTP_201_CREATED == response.status_code
        assert "email" in response.data
        assert response.data.get("email") == data.get("email")

    def test_signup_duplicate_email(self, api_client):
        """Test signup falis with duplicate email"""

        url = reverse("authentication:signup")

        data = {
            "name": "Test User",
            "email": "newuser@test.com",
            "password": "SecurePassword!",
        }

        response = api_client.post(url, data, format="json")

        assert status.HTTP_400_BAD_REQUEST == response.status_code
