from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title



class Post(models.Model):
    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name='Автор',)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True,
        verbose_name='Группа')
    image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name='Картинка',)

    def __str__(self):
        return self.text[:15]

class Comment(models.Model):
    class Meta:
        ordering = ['-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии' 

    post = models.ForeignKey(Post, 
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='Пост')
    author = models.ForeignKey(User, 
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    created = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)

    def __str__(self):
        return self.text

class Follow(models.Model):
    user = models.ForeignKey(User, 
    on_delete=models.CASCADE,
        related_name="follower",
        verbose_name='Подписчик')
    author = models.ForeignKey(User, 
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name='Автор')
