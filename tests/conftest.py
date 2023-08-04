import pytest
from django.test import Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@pytest.fixture
def password():
    """Fixture that provides a password for testing."""
    return '1234567'

@pytest.fixture
def user(CustomUser, password):
    """Fixture that creates and returns a user for testing."""
    from accounts.models import CustomUser
    return CustomUser.objects.create_user(username='TestUser', email='test@ya.ru', password=password)

@pytest.fixture
def another_user(CustomUser, password):
    """Fixture that creates and returns another user for testing."""
    from accounts.models import CustomUser
    return CustomUser.objects.create_user(
        username='TestUser2',
        password=password,
        email='test2@ya.ru',
    )

@pytest.fixture
def token(user):
    """Fixture that provides a token for testing."""
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=user)
    return token.key
@pytest.fixture
def api_client():
    return Client()
@pytest.fixture
def user_client(token):
    """Fixture that provides an authenticated APIClient for testing."""
    from rest_framework.test import APIClient
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client
