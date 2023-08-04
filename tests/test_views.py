# pages/test_urls.py
import pytest
from django.urls import reverse
from pages.models import CustomUser
from pages.models import Post

@pytest.fixture
def user():
    return CustomUser.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def post(user):
    return Post.objects.create(title='Test Post', body='This is a test post.', user=user)

@pytest.fixture
def authenticated_client(client, user):
    client.login(username='testuser', password='testpassword')
    return client

@pytest.mark.django_db
def test_about_page(client):
    url = reverse('about')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_list(authenticated_client, user):
    url = reverse('user-list')
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert user.username.encode() in response.content

@pytest.mark.django_db
def test_user_posts(authenticated_client, user, post):
    url = reverse('user-posts', args=[user.id])
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert post.title.encode() in response.content

@pytest.mark.django_db
def test_create_post(authenticated_client, user):
    url = reverse('create-post')
    data = {'title': 'New Post', 'body': 'This is a new post.'}
    response = authenticated_client.post(url, data)
    assert response.status_code == 302
    assert Post.objects.filter(title='New Post').exists()

@pytest.mark.django_db
def test_delete_post(authenticated_client, user, post):
    url = reverse('delete-post', args=[post.id])
    response = authenticated_client.post(url)
    assert response.status_code == 302
    assert not Post.objects.filter(title='Test Post').exists()  # Изменили проверку на удаление поста
