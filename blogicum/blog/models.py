from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

# Импортируем абстрактную модель:
from core.models import BaseModel
from .constants import MAX_LEN


# User - модель для описания пользователя(встроенная).
User = get_user_model()


class PostManager(models.Manager):
    def published(self):
        """Возвращает опубликованные посты."""
        return self.filter(
            is_published=True,
            pub_date__lte=timezone.now()
        )

    def is_category_published(self):
        """
        Возвращает опубликованные посты
        с опубликованными категориями.
        """
        return self.published().filter(
            category__is_published=True
        )

    def get_post_detail(self, post_id):
        """Возвращает отдельный пост для детального отображения."""
        return (
            self.is_category_published()
            .select_related('location', 'category')
            .filter(id=post_id)
            .first()
        )

    def get_by_category(self, category):
        """Получает список постов по заданной категории"""
        return self.published().filter(category=category)


class Location(BaseModel):
    """Модель для описания локации."""

    name = models.CharField('Название места', max_length=MAX_LEN)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name', 'created_at',)

    def __str__(self) -> str:
        return self.name


class Category(BaseModel):
    """Модель для описания различных категорий постов."""

    title = models.CharField('Заголовок', max_length=MAX_LEN)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; '
                  + 'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('created_at', 'title',)

    def __str__(self) -> str:
        return self.title


class Post(BaseModel):
    """Модель для публикаций(постов)."""

    title = models.CharField('Заголовок', max_length=MAX_LEN)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  + 'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    objects = PostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
        default_related_name = 'post'

    def __str__(self) -> str:
        return self.title
