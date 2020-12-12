from django.test import TestCase, Client
from posts.models import Comment, Group, Post
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import SimpleUploadedFile


class PostBaseTestCase (TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = Group.objects.create(
            title='testtitle',
            slug='testslug',
            description='testdescription'
        )

        cls.posts_list = cls.group.posts.all()
        cls.paginator = Paginator(cls.posts_list, 10)

    def setUp(self):
        self.guest_client = Client()
        self.user = get_user_model().objects.create_user(username='testuser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        small_gif = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
                b'\x01\x00\x80\x00\x00\x00\x00\x00'
                b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                b'\x0A\x00\x3B'
        )
        self.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        self.post = Post.objects.create(
            text="testtext",
            author=self.user,
            pub_date="01.01.2020",
            group=self.group,
            image = self.uploaded,
        )
        self.post = Post.objects.get()

        self.comment = Comment.objects.create(
            text = 'testcomment',
            post = self.post,
            author = self.user,
            created = "01.01.2020"
        )
        self.comment = Comment.objects.get()
        
        site = Site.objects.get(pk=4)
        self.flat_about = FlatPage.objects.create(
            url='/about-author/',
            title='about me',
            content='<b>content</b>'
        )
        self.flat_tech = FlatPage.objects.create(
            url='/about-spec/',
            title='about my tech',
            content='<b>content</b>'
        )
        self.flat_about.sites.add(site)
        self.flat_tech.sites.add(site)
        self.static_pages = ('/about-author/', '/about-spec/')
