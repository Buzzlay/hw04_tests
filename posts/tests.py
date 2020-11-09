from django.test import TestCase, Client

from posts.models import Post, User


class StaticURLTests(TestCase):
    # Метод класса должен быть декорирован

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='dimabuslaev')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.unauthorized_client = Client()

    def test_homepage(self):
        response = StaticURLTests.unauthorized_client.get('index')
        self.assertEqual(response.status_code, 200)

    def test_new_post(self):
        response = StaticURLTests.authorized_client.post(
            '/new/',
            {'text': 'Это текст публикации', 'group': 'tolstoyleo'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user_newpage(self):
        response = StaticURLTests.unauthorized_client.get(
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
        StaticURLTests.authorized_client.force_login(self.user)
        response = StaticURLTests.authorized_client.get(f'/{self.user.username}/')
        self.assertEqual(response.status_code, 200)

    def test_post_edit(self):
        target_post = Post.objects.create(author=self.user, text='Текст публикации 2')
        StaticURLTests.authorized_client.post(
            f'/{self.user.username}/{target_post.id}/edit/',
            {'text': 'Этот текст публикации изменён', 'group': 'buzzlay'},
            follow=True
        )
        self.assertEqual(target_post.text, 'Текст публикации')
        #self.assertEqual(post.group, 'buzzlay')
