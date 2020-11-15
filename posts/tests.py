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
        self.assertEqual(post.author.username, self.user.username)
        self.assertEqual(post.group.title, group.title)

    def test_unauthorized_user_newpage(self):
        response = self.unauthorized_client.get(
            reverse('new_post'),
            follow=False
        )
        self.assertRedirects(
            response,
            f'{reverse("login")}?next={reverse("new_post")}',
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
            slug='1'
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
        self.assertEqual(target_post.group.title, group.title)

    def test_post_existence(self):
        group = Group.objects.create(
            title='testgroup',
            description='test description',
            slug='1'
        )
        post = Post.objects.create(author=self.user,
                                   text='Текст публикации',
                                   group=group)
        urls = [
            reverse('index'),
            reverse('profile', args=[self.user.username]),
            reverse(
                'post',
                args=[self.user.username, post.id]
            ),
            reverse('group_posts', args=[group.id])
        ]
        for url in urls:
            with self.subTest():
                response = self.authorized_client.get(url)
                if f'{self.user.username}' in url:
                    post_test = response.context['post']
                else:
                    post_test = response.context['page'][0]
                self.assertEqual(post_test.text, 'Текст публикации')
