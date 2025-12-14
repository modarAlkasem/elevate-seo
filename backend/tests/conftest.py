"""Shared Fixtures"""

# DRF Imports
from rest_framework.test import APIClient

# Third Party Imports
import pytest

# Project Imports
from .factories import AccountFactory


@pytest.fixture
def api_client():
    """Unauthenticated API Client"""
    return APIClient()


@pytest.fixture
def authenticated_client(db):
    """Authenticated API Client with test user"""
    account = AccountFactory()
    user = account.user
    client = APIClient.force_authenticate(user=user)
    return client, user


@pytest.fixture
def test_user(db):
    """Create test user"""
    account = AccountFactory()
    user = account.user
    return user
