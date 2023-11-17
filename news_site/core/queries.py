from news_site.core.models import Category
from news_site.core.models.article import PinnedArticle, Article


def get_pinned_news_with_category():
    return PinnedArticle.objects.select_related("article").prefetch_related("article__categories")[:8]


def get_categories():
    return Category.objects.select_related("parent_category").values("id", "title", "slug")


def get_news_by_alias(alias):
    return Article.objects.select_related("author").prefetch_related("tags", "categories").get_detail_404(alias=alias)


def get_news_by_uid(uid):
    return Article.objects.select_related("author").prefetch_related("tags", "categories").get_detail_404(pk=uid)


def get_like_news(news_pk, news_category):
    return (
        Article.objects.exclude(pk=news_pk)
        .get_published()
        .prefetch_related("categories")
        .filter(categories__in=str(news_category))
        .get_published()[:6]
    )


def get_news_tag_by_id(tag_id):
    return Article.objects.prefetch_related("categories").get_published().filter(tags=tag_id)


def get_news_tag_count_by_id(tag_id):
    return Article.objects.get_published().filter(tags=tag_id).count()


def get_category_by_slug(category_slug):
    return Category.objects.get_detail_404(slug=category_slug)


def get_subcategory_by_id(category_id):
    return Category.objects.get_sub_category(category_id)


def get_news_category_by_id(category_id):
    return Article.objects.prefetch_related("categories").get_published().filter(categories__in=str(category_id))


def get_news_category_count_by_id(category_id):
    return Article.objects.get_published().filter(categories=str(category_id)).count()


def get_last_news():
    return Article.objects.prefetch_related("categories").only("alias", "title", "published_date").get_published()[:20]


def get_news_count_with_category():
    return Article.objects.prefetch_related("categories").get_published().count()
