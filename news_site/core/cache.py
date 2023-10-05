from django.core.cache import cache

from news_site.core.const import CACHE_TTL


class CustomCacheMixin:

    def home_cache_key(self):
        return f"home_key"

    def get_all_news_cache_key(self):
        return "all_news_cache_key"

    def get_news_cache_key(self, news_alias):
        return f"news_cache_{news_alias}"

    def get_category_cache_key(self, category_slug):
        return f"category_cache_{category_slug}"

    def get_tag_cache_key(self, tag_slug):
        return f"tag_cache_{tag_slug}"

    def get_cache_by_key(self, cache_key):
        return cache.get(cache_key)

    def set_cache_by_key(self, cache_key, response):
        cache.set(cache_key, response, CACHE_TTL)

    def delete_cache_by_key(self, cache_key):
        cache.delete(cache_key)
