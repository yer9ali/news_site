from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader
from django.views.generic import DetailView
from loguru import logger

from news_site.core.cache import CustomCache
from news_site.core.models import Tag
from news_site.core.queries import get_news_tag_by_id, get_news_tag_count_by_id


class TagsDetailView(DetailView, CustomCache):
    model = Tag
    template_name = "pages/tag.html"

    def get(self, request, *args, **kwargs):
        tag_slug = kwargs["slug"]

        tag_cache_key = self.get_tag_cache_key(tag_slug)
        cached_data = self.get_cache_by_key(tag_cache_key)

        if cached_data:
            return cached_data

        tag = get_object_or_404(Tag, tag_slug=tag_slug)
        all_tag_news = get_news_tag_by_id(tag.id)
        news_tag_count = get_news_tag_count_by_id(tag.id)

        response = self.render_to_response(
            {
                "tags": tag,
                "all_news": all_tag_news,
                "total_obj": news_tag_count,
            }
        )
        response.render()

        self.set_cache_by_key(tag_cache_key, response)
        logger.info(f"Set cache tag by slug {tag_slug}")

        return response

    def update_tag_detail_cache(self, tag_slug):
        cache_key = self.get_tag_cache_key(tag_slug)

        tag = get_object_or_404(Tag, tag_slug=tag_slug)
        all_tag_news = get_news_tag_by_id(tag.id)
        news_tag_count = get_news_tag_count_by_id(tag.id)


        template = loader.get_template(self.template_name)

        content = template.render(
            {
                "tags": tag,
                "all_news": all_tag_news,
                "total_obj": news_tag_count,
            }
        )

        response = HttpResponse(content, status=200)
        self.set_cache_by_key(cache_key, response)

        logger.info(f"Updated cache tag by slug {tag_slug}")
