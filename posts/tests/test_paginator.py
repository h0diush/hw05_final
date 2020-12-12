from posts.models import Post
from django.urls import reverse
from .base import PostBaseTestCase
from django.core.cache import cache



class PostPagesTest(PostBaseTestCase):

    def test_paginator(self):
        cache.clear()
        for i in range(15):
            Post.objects.create(
                text="testtext",
                author=self.user,
                pub_date="01.01.2020",
                group=self.group,
            )
        response = self.authorized_client.get(reverse('index'))
        self.assertEqual(len(response.context['page']), 10)
