from daterangefilter.filters import DateRangeFilter
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from news_site.core.models import Category, Tag, Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Создать категорию",
            {
                "fields": [
                    "title",
                    "slug",
                    "seo_title",
                    "description",
                    "parent_category",
                    "created_by",
                ]
            },
        ),
    ]

    list_display = ["title", "created_by"]

    prepopulated_fields = {"slug": ("title",)}

    list_filter = [
        "created_by",
    ]

    search_fields = ["title"]

    autocomplete_fields = ("parent_category",)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            "Создать тег",
            {
                "fields": [
                    "title",
                    "slug",
                    "description",
                    "seo_description",
                    "created_by",
                ]
            },
        ),
    ]

    search_fields = ["title"]

    list_display = ["title", "created_by"]

    prepopulated_fields = {"slug": ("title",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            _("Создать новость"),
            {
                "fields": [
                    "title",
                    "slug",
                    "description",
                    "content",
                    "image",
                    "published_date",
                    "view_count",
                    "tags",
                    "categories",
                    "created_by",
                ]
            },
        ),
    ]
    list_display = (
        "title",
        "created_by",
    )

    search_fields = ["page_title"]

    autocomplete_fields = [
        "tags",
        "categories",
    ]

    list_filter = (("published_date", DateRangeFilter),)

    prepopulated_fields = {"slug": ("title",)}
