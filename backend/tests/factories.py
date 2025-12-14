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


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    id = factory.LazyFunction(uuid.uuid4)
    user = factory.SubFactory(UserFactory)
    type = factory.LazyAttribute(lambda _: AccountTypeChoices.CREDENTIALS.value)
    provider = factory.LazyAttribute(lambda _: AccountProviderChoices.CREDENTIALS.value)
    provider_account_id = factory.Faker("uuid4")
    token_type = None
    scope = None
    id_token = None
    expires_at = factory.LazyAttribute(lambda _: timezone.now() + timedelta(days=30))
