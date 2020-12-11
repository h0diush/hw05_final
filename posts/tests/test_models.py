from .base import PostBaseTestCase


class GroupTaseClass(PostBaseTestCase):

    def test_group_title(self):
        group = GroupTaseClass.group
        expected_object_name = group.title
        self.assertEquals(
            expected_object_name,
            str(group),
            'объект Group не эдентичен полю title')

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        group = GroupTaseClass.group
        field_verboses = {
            'title': 'Заголовок',
            'slug': 'Слаг',
            'description': 'Описание',
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)


class PostTaseClass(PostBaseTestCase):

    def test_verbose_name(self):
        post = self.post
        field_verboses = {
            'text': 'Текст',
            'pub_date': 'Дата публикации',
            'author': "Автор",
            'group': 'Группа'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_post_str(self):
        post = self.post
        expected_object_name = post.text[:15]
        self.assertEquals(expected_object_name, str(post),
                          'объект Group не соответствует полю Text '
                          'или больше 15 символов')
