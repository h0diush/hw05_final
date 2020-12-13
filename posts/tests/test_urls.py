from django.test import Client
from django.contrib.auth import get_user_model
from .base import PostBaseTestCase
from django.core.cache import cache
from django.urls import reverse


class PostUrlTest(PostBaseTestCase):

    # доступна любому пользователю
    def test_posts_index_exists_at_desired_location_anonymous(self):
        """Возможно подключиться к главной странице"""
        response = self.guest_client.get(reverse('index'))
        self.assertEquals(
            response.status_code,
            200,
            'Невозможно подключиться к главной странице')

    def test_posts_profile_exists_at_desired_location_anonymous(self):
        """Страница пользователя с постами"""
        response = self.guest_client.get(reverse('profile', kwargs={'username': 'testuser'}))
        self.assertEquals(
            response.status_code,
            200,
            'Невозможно подключиться к странице профиля пользователя')

    def test_posts_post_exists_at_desired_location_anonymous(self):
        """Страница пользователя с постами"""
        response = self.guest_client.get(reverse('post', kwargs={'username': 'testuser', 'post_id': '1'}))
        self.assertEquals(
            response.status_code,
            200,
            'Невозможно подключиться к странице с постом')

    # неавторизованный пользователь
    def test_posts_group_slug_exists_at_desired_location_anonymous(self):
        """Страница group/test_slug доступна неавторизованному пользователю"""
        response = self.guest_client.get(reverse('slug', kwargs={'slug': 'testslug'}))
        self.assertEquals(
            response.status_code,
            200,
            'Страница group/test_slug должна быть доступна неавторизованному пользователю')

    def test_posts_new_exists_at_desired_location_anonymous(self):
        """Данная страница не доступна неавторизованному пользователю"""
        response = self.guest_client.get(reverse('new_post'))
        self.assertEquals(
            response.status_code,
            302,
            'Данная страница не должна быть доступна неавторизованному пользователю')

    def test_posts_edit_exists_at_desired_location_anonymous(self):
        """Данная страница не доступна неавторизованному пользователю"""
        response = self.guest_client.get(reverse('post_edit', kwargs={'username': 'testuser', 'post_id': '1'}))
        self.assertEquals(
            response.status_code,
            302,
            'Данная страница не должна быть доступна неавторизованному пользователю')

    def test_comment_posts_anonymous(self):
        """Данная страница не доступна неавторизованному пользователю"""
        response = self.guest_client.get(
            reverse(
                'add_comment',
                kwargs={
                    'username': 'testuser',
                    'post_id': '1'}))
        self.assertEquals(
            response.status_code,
            302,
            'Только авторизованный пользователь может оставлять комментарии')

    # авторизованный пользователь

    def test_posts_new_exists_authorized_client(self):
        """Данная страница доступна авторизованному пользователю"""
        response = self.authorized_client.get(reverse('new_post'))
        self.assertEquals(
            response.status_code,
            200,
            'Данная страница должна быть доступна авторизованному пользователю')

    def test_posts_group_slug_authorized_client(self):
        """Страница group/test_slug доступна авторизованному пользователю"""
        response = self.authorized_client.get(reverse('slug', kwargs={'slug': 'testslug'}))
        self.assertEquals(
            response.status_code,
            200,
            'Страница group/test_slug должна быть доступна авторизованному пользователю')

    def test_posts_edit_authorized_client_and_author_post(self):
        """Данная страница не доступна неавторизованному пользователю и не автору поста"""

        response = self.authorized_client.get(reverse('post_edit', kwargs={'username': 'testuser', 'post_id': '1'}))
        self.assertEquals(
            response.status_code,
            200,
            'Данная страница не должна быть доступна неавторизованному пользователю и не атору поста')

    def test_posts_edit_authorized_client_and_author_not_post(self):
        """Данная страница не доступна авторизованному пользователю и не автору поста"""
        author_not_post = Client()
        author = get_user_model().objects.create_user(username='alex')
        author_not_post.force_login(author)
        response = author_not_post.get(reverse('post_edit', kwargs={'username': 'testuser', 'post_id': '1'}))
        self.assertEquals(
            response.status_code,
            302,
            'Данная страница не должна быть доступна авторизованному пользователю и не атору поста')

    def test_comment_posts_authorized_client(self):
        """Данная страница не доступна авторизованному пользователю"""
        response = self.authorized_client.get(
            reverse(
                'add_comment',
                kwargs={
                    'username': 'testuser',
                    'post_id': '1'}))
        self.assertEquals(
            response.status_code,
            200,
            'Только авторизованный пользователь может оставлять комментарии')

    def test_404(self):
        response = self.guest_client.get('/wdwdad/wdaw/22')
        self.assertEqual(response.status_code, 404)

    # проверка соответствия шаблонов
    def test_urls_uses_correct_template(self):
        """URL-адрес соответствует шаблону"""
        cache.clear()
        templates_url_names = {
            'index.html': '/',
            'group.html': '/group/testslug/',
            'new_post.html': '/new/',
            'profile.html': '/testuser/',
            'post.html': '/testuser/1/',
            'post_edit.html': '/testuser/1/edit/',
            'follow.html': '/follow/'
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(
                    reverse_name)
                self.assertTemplateUsed(response, template)
