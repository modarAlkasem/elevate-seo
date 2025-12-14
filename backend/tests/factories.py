# Python Imports
import uuid
from datetime import timedelta

# Django Imports
from django.contrib.auth.hashers import make_password
from django.utils import timezone

# Third Party Imports
import factory
from factory.django import DjangoModelFactory

# Project Imports
from apps.authentication.models import User, Account
from apps.authentication.constants import AccountTypeChoices, AccountProviderChoices


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    name = factory.Faker("name")
    email = factory.Sequence(lambda n: f"user{n}@test.com")
    password = "defaultpassword"
    email_verified = True
    last_signed_in = None
    is_active = True
    avatar = factory.Faker("image_url")

    @factory.post_generation
    def hash_password(obj, create, extracted, **kwargs):
        obj.password = make_password(obj.password)

        if create:
            obj.save()
