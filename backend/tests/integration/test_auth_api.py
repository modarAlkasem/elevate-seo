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

        url = reverse("authentication:auth-signup")

        data = {
            "name": "Test User",
            "email": "newuser@test.com",
            "password": "SecurePassword!",
        }

        response = api_client.post(url, data, format="json")

        assert status.HTTP_201_CREATED == response.status_code
        assert "email" in response.data
        assert response.data.get("email") == data.get("email")

    def test_signup_duplicate_email(self, api_client: APIClient, test_user):
        """Test signup falis with duplicate email"""

        url = reverse("authentication:auth-signup")

        data = {
            "name": "Test User",
            "email": test_user.email,
            "password": "SecurePassword!",
        }

        response = api_client.post(url, data, format="json")

        assert status.HTTP_400_BAD_REQUEST == response.status_code

    def test_signup_invalid_email(self, api_client: APIClient):
        """Test signup with invalid email format"""

        url = reverse("authentication:auth-signup")

        data = {
            "name": "Test User",
            "email": "invalid_email",
            "password": "SecurePassword!",
        }

        response = api_client.post(url, data, format="json")

        assert status.HTTP_400_BAD_REQUEST == response.status_code

    def test_signin_success(self, test_user, api_client: APIClient):
        """Test successful user signin"""

        url = reverse("authentication:auth-signin")

        data = {"email": test_user.email, "password": "SecurePass123!"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "tokens" in response.data
        assert "access" and "refresh" in response.data.get("tokens")

    def test_signin_wrong_password(self, test_user, api_client: APIClient):
        """Test signin with incorrect password"""

        url = reverse("authentication:auth-signin")

        data = {"email": test_user.email, "password": "SecurePass321!"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_signin_unexistent_user(self, test_user, api_client: APIClient):
        """Test signin with non-registered email"""

        url = reverse("authentication:auth-signin")

        data = {"email": "nonexistent@test.com", "password": "somepassword"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
