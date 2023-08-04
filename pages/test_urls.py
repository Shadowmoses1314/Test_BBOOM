from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class SimpleTests(TestCase):
    def setUp(self):
        # Create a test user and post for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(title='Test Post', body='This is a test post.', user=self.user)

    def test_user_list_view(self):
        # Test if the user list view returns a status code of 200
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)
        
        # Test if the user list view contains the user's username
        self.assertContains(response, self.user.username)

    def test_user_posts_view(self):
        # Test if the user posts view returns a status code of 200
        response = self.client.get(reverse('user-posts', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        
        # Test if the user posts view contains the post title and body
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.body)

    def test_create_post_view(self):
        # Test if the create post view redirects to login if not logged in
        response = self.client.get(reverse('create-post'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/login/?next=/create_post/')  # Assuming the login URL is /admin/login/

        # Test if the create post view returns a status code of 200 when logged in
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create-post'))
        self.assertEqual(response.status_code, 200)

        # Test if a new post is created when form is submitted
        response = self.client.post(reverse('create-post'), {'title': 'New Test Post', 'body': 'This is a new test post.'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 2)  # Assuming there was only 1 post before creating the new post

    def test_delete_post_view(self):
        # Test if the delete post view redirects to login if not logged in
        response = self.client.post(reverse('delete-post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/login/?next=/delete_post/{}/'.format(self.post.id))  # Assuming the login URL is /admin/login/

        # Test if a post is deleted when the form is submitted by the post owner
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete-post', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)

        # Test if a post is not deleted when the form is submitted by a non-owner user
        another_user = User.objects.create_user(username='anotheruser', password='anotherpassword')
        another_post = Post.objects.create(title='Another Post', body='This is another post.', user=another_user)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('delete-post', args=[another_post.id]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Post.objects.count(), 1)  # The post should not have been deleted
