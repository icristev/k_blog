from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=200, verbose_name='Название поста', blank=True,  null=True,)
    text = models.TextField(blank=False)

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='posts',
        verbose_name='Автор поста'
    )

    image = models.ImageField(
        verbose_name='Изображение поста',
        upload_to='posts/',
        blank=True,
    )

    slug = models.SlugField(max_length=200,
                            unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    objects = models.Manager()      # менеджер, применяемый по умолчанию
    published = PublishedManager()  # менеджер для опубликованных постов

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Пост, к которому будет оставлен комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        null=True,
        verbose_name='Автор комментария',
    )
    text = models.TextField(
        max_length=300,
        verbose_name='Текст комментария',
        help_text='Текст комментария',
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания комментария')
    updated = models.DateTimeField(auto_now=True, verbose_name='Время обновления комментария')

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'

    def __str__(self):
        return f'Автор комментария: {self.author}, пост: {self.post}'
