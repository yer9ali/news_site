from django.db.models import (
    CharField,
    TextField,
    ForeignKey,
    SET_NULL,
    SlugField,
)
from django.db.models import Index
from slugify import slugify

from news_site.core.models.base import AbstractDateTime
from news_site.users.models import User


class Category(AbstractDateTime):
    """Модель категории новостных материалов"""

    title = CharField(max_length=250, verbose_name="Заголовок")

    slug = SlugField(max_length=250, verbose_name="Слаг", unique=True, blank=True)
    seo_title = CharField(max_length=250, verbose_name="СЕО заголовок")
    description = TextField(verbose_name="Описание", blank=True)

    parent_category = ForeignKey(
        "self",
        verbose_name="Родительская категория",
        null=True,
        blank=True,
        on_delete=SET_NULL,
        related_name="subcategories",
    )

    created_by = ForeignKey(User, verbose_name="Автор", on_delete=SET_NULL, null=True)

    class Meta:
        db_table = "category"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        indexes = [
            Index(
                fields=[
                    "id",
                ]
            )
        ]

    def save(self, *args, **kwargs):
        """
        Переопределение метода save для автоматического создания слага из заголовка.
        """

        self.slug = slugify(self.title)
        return super(Category, self).save()

    def __str__(self):
        return self.title
