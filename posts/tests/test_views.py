from posts.models import Follow, Post
from django.urls import reverse
from django import forms
from .base import PostBaseTestCase
from django.core.cache import cache


class PostPagesTest(PostBaseTestCase):

    # Проверяем используемые шаблоны
    def test_posts_uses_correct_template(self):
        """Соответствие URL-адресов HTML-шаблонам"""
        cache.clear()
        templates_pages_names = {
            'index.html': reverse('index'),
            'group.html': reverse('slug', kwargs={'slug': 'testslug'}),
            'new_post.html': reverse('new_post'),
            'profile.html': reverse('profile', kwargs={'username': 'testuser'}),
            'post.html': reverse('post', kwargs={'username': 'testuser', 'post_id': '1'}),
            'post_edit.html': reverse('post_edit', kwargs={'username': 'testuser', 'post_id': '1'}),
            'comments.html': reverse('add_comment', kwargs={'username': 'testuser', 'post_id': '1'}),
            'follow.html': reverse('follow_index'),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # проверяем context
    def test_homepage_shows_correct_context(self):
        """context главной страницы"""
        cache.clear()
        response = self.authorized_client.get(reverse('index'))
        post_text = response.context.get('page')[0].text
        post_author = response.context.get('page')[0].author
        post_group = response.context.get('page')[0].group
        post_image = response.context.get('page')[0].image
        self.assertEqual(post_text, 'testtext')
        self.assertEqual(post_author, self.user)
        self.assertEqual(post_group, PostPagesTest.group)
        self.assertEqual(post_image.size, self.uploaded.size)

    def test_group_page_show_correct_context(self):
        """context страницы с группами"""
        response = self.authorized_client.get(reverse("slug",
                                                      kwargs={"slug": "testslug"}))
        post_text = response.context.get("page")[0].text
        post_author = response.context.get("page")[0].author
        post_pub_date = response.context.get("page")[0].pub_date
        post_group = response.context.get("page")[0].group
        post_image = response.context.get("page")[0].image
        self.assertEqual(post_text, self.post.text)
        self.assertEqual(post_author, self.user)
        self.assertEqual(post_pub_date, self.post.pub_date)
        self.assertEqual(post_group, self.group)
        self.assertEqual(post_image.size, self.uploaded.size)

    def test_profile_page_show_correct_context(self):
        """context страницы пользователя"""
        response = self.authorized_client.get(
            reverse("profile", kwargs={'username': 'testuser'}))
        post_text = response.context.get("page")[0].text
        post_author = response.context.get("page")[0].author
        post_pub_date = response.context.get("page")[0].pub_date
        post_group = response.context.get("page")[0].group
        post_image = response.context.get("page")[0].image
        self.assertEqual(post_text, self.post.text)
        self.assertEqual(post_author, self.user)
        self.assertEqual(post_pub_date, self.post.pub_date)
        self.assertEqual(post_group, self.group)
        self.assertEqual(post_image.size, self.uploaded.size)

    def test_post_page_show_correct_context(self):
        """context страницы поста"""
        response = self.authorized_client.get(
            reverse(
                "post",
                kwargs={
                    'username': 'testuser',
                    'post_id': '1'}))
        post_text = response.context.get("post").text
        post_author = response.context.get("post").author
        post_pub_date = response.context.get("post").pub_date
        post_group = response.context.get("post").group
        post_image = response.context.get("post").image
        self.assertEqual(post_text, self.post.text)
        self.assertEqual(post_author, self.user)
        self.assertEqual(post_pub_date, self.post.pub_date)
        self.assertEqual(post_group, self.group)
        self.assertEqual(post_image.size, self.uploaded.size)

    def test_new_shows_correct_context(self):
        """context страницы добовления поста"""
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_post_context(self):
        """context страницы редактирования поста"""
        response = self.authorized_client.get(
            reverse(
                'post_edit',
                kwargs={
                    'username': 'testuser',
                    'post_id': '1'}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_authorized_client_follow_user(self):
        count = Follow.objects.count()
        self.authorized_client.get(reverse('profile_follow', kwargs={'username': 'testuser'}))
        follow = Follow.objects.create(
            user=self.user,
            author=self.user2
        )
        follow = Follow.objects.get()
        self.assertEqual(count+1, Follow.objects.count())
        self.assertEqual(follow.author, self.user2)

    def test_authorized_client_unfollow_user(self):
        count = Follow.objects.count()
        Follow.objects.create(user=self.user, author=self.user2)
        self.assertEqual(count+1, Follow.objects.count())        
        self.authorized_client.post(reverse('profile_unfollow', kwargs={'username': 'testuser2'}))
        self.assertFalse(Follow.objects.exists())


    