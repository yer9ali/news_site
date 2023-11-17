from django.db.models.signals import post_save
from django.dispatch import receiver

from news_site.core.models.article import PinnedArticle
from news_site.core.views.home_view import HomeView


@receiver(post_save, sender=PinnedArticle)
def pinned_article_save(sender, instance, **kwargs):
    """ Обновление кеша при сохранении PinnedArticle todo тут надо реализовать без HomeView"""
    home_view = HomeView()
    home_view.update_home_cache()
