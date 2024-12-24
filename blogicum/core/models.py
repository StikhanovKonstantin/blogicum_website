from django.db import models


class BaseModel(models.Model):
    """
    Абстрактная модель.
    Добавляет к другим моделям дату и время создания,
    а также флажок 'Опубликовано'.
    """

    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True
    )

    class Meta:
        abstract = True
