from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from posts.models import Post, User, Group


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='dimabuslaev', email='dimabuslaev@mail.ru')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.unauthorized_client = Client()

    def test_homepage(self):
        url = reverse_lazy('index')
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_post(self):
        group = Group.objects.create(title='testgroup', description='test description', slug=1)
        response = self.authorized_client.post(
            '/new/',
            data={'text': 'текст публикации', 'group': group.slug},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        post = get_object_or_404(Post, text='текст публикации')
        self.assertEqual(post.text, 'текст публикации')

    def test_unauthorized_user_newpage(self):
        response = self.unauthorized_client.get(
            '/new/',
            follow=False
        )
        self.assertRedirects(
            response,
            '/auth/login/?next=/new/',
            status_code=302,
            target_status_code=200
        )

    def test_profile_existence(self):
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.get(f'/{self.user.username}/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit(self):
        target_post = Post.objects.create(author=self.user, text='Текст публикации')
        group = Group.objects.create(title='testgroup', description='test description', slug=1)
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.post(
            f'/{self.user}/{target_post.id}/edit/',
            {'text': 'Этот текст публикации изменён', 'group': group.id},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        post = get_object_or_404(Post, author=self.user)
        self.assertEqual(post.text, 'Этот текст публикации изменён')
        self.assertEqual(post.group.title, 'testgroup')
