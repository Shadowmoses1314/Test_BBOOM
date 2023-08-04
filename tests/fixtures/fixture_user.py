

import pytest

@pytest.fixture
def password():
    return '1234567'

@pytest.fixture

def user(CustomUser, password):
    from accounts.models import CustomUser
    return CustomUser.objects.create_user(username='TestUser', email='test@ya.ru', password=password)

@pytest.fixture
def another_user(CustomUser, password):
    from accounts.models import CustomUser
    return CustomUser.objects.create_user(username='TestUser2', password=password, email='test2@ya.ru')

@pytest.fixture
def token(user):
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=user)
    return token.key

@pytest.fixture
def user_client(token):
    from rest_framework.test import APIClient
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return client