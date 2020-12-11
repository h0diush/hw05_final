from .base import PostBaseTestCase


class StaticURLTests(PostBaseTestCase):

    def test_static_pages_response(self):
        for url in self.static_pages:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200, f'url: {url}')
