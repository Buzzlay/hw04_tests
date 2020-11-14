from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, User, Group


class StaticURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='dimabuslaev',
            email='dimabuslaev@mail.ru'
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.unauthorized_client = Client()

    def test_homepage(self):
        url = reverse('index')
        response = self.unauthorized_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_new_post(self):
        group = Group.objects.create(
            title='testgroup',
            description='test description',
            slug='1')
        response = self.authorized_client.post(
            reverse('new_post'),
            data={'text': 'текст публикации', 'group': group.id},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        post = Post.objects.first()
        self.assertEqual(post.text, 'текст публикации')
        self.assertEqual(post.author.username, 'dimabuslaev')
        self.assertEqual(post.group.title, 'testgroup')

    def test_unauthorized_user_newpage(self):
        response = self.unauthorized_client.get(
            reverse('new_post'),
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
        response = self.authorized_client.get(
            reverse(
                'profile',
                kwargs={'username': self.user.username}
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_post_edit(self):
        target_post = Post.objects.create(
            author=self.user,
            text='Текст публикации'
        )
        group = Group.objects.create(
            title='testgroup',
            description='test description',
            slug=1
        )
        response = self.authorized_client.post(
            reverse(
                'post_edit',
                kwargs={
                    'username': self.user.username,
                    'post_id': target_post.id
                }
            ),
            {'text': 'Этот текст публикации изменён', 'group': group.id},
            follow=True)
        self.assertEqual(response.status_code, 200)
        target_post.refresh_from_db()
        self.assertEqual(target_post.text, 'Этот текст публикации изменён')
        self.assertEqual(group.title, 'testgroup')

    def test_post_existence(self):
        post = Post.objects.create(author=self.user,
                                   text='Текст публикации')
        response_index = self.authorized_client.get(reverse('index'))
        response_profile = self.authorized_client.get(
            reverse(
                'profile',
                kwargs={'username': self.user.username}
            )
        )
        response_post = self.authorized_client.get(
            reverse(
                'post',
                kwargs={
                    'username': self.user.username,
                    'post_id': post.id
                }
            )
        )
        self.assertContains(response_index, 'Текст публикации')
        self.assertContains(response_profile, 'Текст публикации')
        self.assertContains(response_post, 'Текст публикации')
