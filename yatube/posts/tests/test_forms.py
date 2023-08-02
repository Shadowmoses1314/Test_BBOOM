from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_group = Group.objects.create(
            title='Заголовок',
            description='Описание',
            slug='slug',
        )

    def setUp(self):
        self.user = User.objects.create(username='Old_name')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create_form(self):
        """Posts.Forms. Создание нового Post."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост',
            'group': PostFormTests.test_group.id
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': self.user.username}),
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
