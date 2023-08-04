from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, Post


class PostAPITestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(name='User1', 
                                         email='user1@example.com')
        self.user2 = User.objects.create(name='User2', 
                                         email='user2@example.com')
        self.post1 = Post.objects.create(user=self.user1, title='Post 1', body='Body 1')
        self.post2 = Post.objects.create(user=self.user2, title='Post 2', body='Body 2')
        self.client = APIClient()

    def test_get_all_users(self):
        url = reverse('get_all_users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_user_posts(self):
        url = reverse('get_user_posts', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user1.id)

    def test_add_post_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('add_post')
        data = {'user': self.user1.id, 'title': 'New Post', 'body': 'New Body'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)

    def test_add_post_unauthenticated(self):
        url = reverse('add_post')
        data = {'user': self.user1.id, 'title': 'New Post', 'body': 'New Body'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 2)

    def test_delete_post_own(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('delete_post', args=[self.post1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)

    def test_delete_post_not_own(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('delete_post', args=[self.post2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 2)
