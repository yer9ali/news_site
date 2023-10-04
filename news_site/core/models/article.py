import uuid

from django.db.models import (
    CharField,
    IntegerField,
    UUIDField,
    TextField,
    DateTimeField,
    ForeignKey,
    SET_NULL,
    ManyToManyField,
    SlugField,
)
from django.db.models import Index
from django.db.models.fields.files import ImageField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from news_site.core.models.base import AbstractDateTime
from news_site.core.models.category import Category
from news_site.core.models.tag import Tag
from news_site.users.models import User


class Article(AbstractDateTime):
    """
    Модель Article представляет собой основную структуру для новостных статей.
    Каждая статья содержит уникальный идентификатор, заголовок, описание, контент и метаданные.
    Статьи также могут быть связаны с тегами и категориями и иметь автора.
    """

    uid = UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    title = CharField(max_length=250, verbose_name=_("Заголовок"))
    description = TextField(verbose_name="Описание")

    content = HTMLField()
    slug = SlugField(max_length=250, verbose_name="Слаг", unique=True)
    image = ImageField(upload_to="content/", verbose_name="Изображение", max_length=1000)

    published_date = DateTimeField(verbose_name="Дата публикации", default=timezone.now)
    view_count = IntegerField(default=0, verbose_name="Количество просмотров")

    tags = ManyToManyField(Tag, related_name="tag_article", verbose_name="Теги", blank=True)

    categories = ManyToManyField(
        Category,
        related_name="category_article",
        verbose_name="Категории",
        blank=True,
    )

    created_by = ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=SET_NULL,
        null=True,
        related_name="created_articles",
    )

    class Meta:
        db_table = "article"
        ordering = ("-datetime_created", "-published_date")
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        indexes = [Index(fields=["view_count", "published_date", "datetime_created"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})


class PinnedArticle(AbstractDateTime):
    """
    Модель PinnedArticle предназначена для выделения определенных новостных статей, которые должны быть "закреплены"
    на главной странице. Каждая закрепленная статья связана с основной статьей и имеет порядковый номер для
    определения ее позиции.
    """

    article = ForeignKey(Article, verbose_name="Новость", on_delete=SET_NULL, blank=True, null=True)
    order = IntegerField(
        verbose_name="Позиция",
    )

    class Meta:
        ordering = ("order",)
        verbose_name = "Фиксированная новость"
        verbose_name_plural = "Фиксированные новости"
        indexes = [
            Index(
                fields=[
                    "order",
                ]
            )
        ]

    def __str__(self):
        return str(self.article)
