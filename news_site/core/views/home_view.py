from django.core.cache import cache
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from loguru import logger

from news_site.core.cache import CustomCacheMixin
from news_site.core.queries import get_pinned_news_with_category


class HomeView(TemplateView, CustomCacheMixin):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pinned_news = get_pinned_news_with_category()

        context.update(
            {
                "pinned_news": pinned_news,
            }
        )
        return context

    def get(self, request, *args, **kwargs):
        cached_response = self.get_cached_response()
        if cached_response:
            return cached_response

        return super().get(request, *args, **kwargs)

    def get_cached_response(self):
        cache_key = self.home_cache_key()
        cached_data = cache.get(cache_key)

        if not cached_data:
            context = self.get_context_data()
            response = self.render_to_response(context)
            self.set_cache_by_key(cache_key, response)
            logger.info("Set cache home view")
            return response

        return cached_data

    def update_home_cache(self):
        pinned_news = get_pinned_news_with_category()

        template = loader.get_template(self.template_name)
        cache_key = self.home_cache_key()

        content = template.render(
            {
                "pinned_news": pinned_news,
            }
        )

        response = HttpResponse(content, status=200)
        self.set_cache_by_key(cache_key, response)
        logger.info("Updated cache home view")
