from django.db.models import (
    CharField,
    TextField,
    SlugField,
    ForeignKey,
    SET_NULL,
)

from news_site.core.models.base import AbstractDateTime
from news_site.users.models import User


class Tag(AbstractDateTime):
    """Модель тега новостных материалов"""

    title = CharField(max_length=250, verbose_name="Заголовок")
    slug = SlugField(max_length=250, unique=True, verbose_name="Слаг")
    description = TextField(verbose_name="Описание")

    seo_description = CharField(max_length=100, verbose_name="Описание для СЕО", blank=True)
    created_by = ForeignKey(User, verbose_name="Автор", on_delete=SET_NULL, null=True)

    class Meta:
        db_table = "tag"
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.title
