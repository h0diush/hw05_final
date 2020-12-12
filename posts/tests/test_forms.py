from django.urls import reverse
from posts.models import Group, Post
from .base import PostBaseTestCase
from django.core.files.uploadedfile import SimpleUploadedFile


class PostsCreateFormTests(PostBaseTestCase):

    def test_create_post(self):
        """Валидная форма создает post."""

        group = Group.objects.create(
            title='test',
            slug='test-slug',
            description='test'
        )
        small_gif = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
                b'\x01\x00\x80\x00\x00\x00\x00\x00'
                b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        post_count = Post.objects.count()
        form_data = {
            'text': self.post.text,
            'group': group.id,
            'image': uploaded
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
        self.small_gif = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
                b'\x01\x00\x80\x00\x00\x00\x00\x00'
                b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                b'\x0A\x00\x3B'
        )
        self.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=self.small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'self.post.text',
            'group': self.group.id,
            'image': self.uploaded
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
