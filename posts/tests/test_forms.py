from django.urls import reverse
from posts.models import Group, Post
from .base import PostBaseTestCase


class PostsCreateFormTests(PostBaseTestCase):

    def test_create_post(self):
        """Валидная форма создает post."""

        group = Group.objects.create(
            title='test',
            slug='test-slug',
            description='test'
        )
        post_count = Post.objects.count()
        form_data = {
            'text': self.post.text,
            'group': group.id,
        }
        response = self.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True
        )

        post = response.context['page'][0]

        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, form_data['group'])

    def test_edit_post(self):
        """Валидная форма редактирует запись в Post."""

        form_data = {
            'text': 'self.post.text',
            'group': self.group.id,
        }
        posts_count = Post.objects.count()
        response = self.authorized_client.post(
            reverse('post_edit',
                    kwargs={'username': self.user.username,
                            'post_id': self.post.id}),
            data=form_data,
            follow=True)
        post = response.context.get('post')
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, form_data['group'])
        self.assertRedirects(response,
                             reverse('post',
                                     kwargs={'username': self.user.username,
                                             'post_id': self.post.id}))
