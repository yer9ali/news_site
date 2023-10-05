from django.http import HttpResponse
from django.template import loader
from django.views.generic import DetailView
from loguru import logger

from news_site.core.cache import CustomCacheMixin
from news_site.core.models import Category
from news_site.core.queries import get_category_by_slug, get_subcategory_by_id, get_news_category_by_id, \
    get_news_category_count_by_id


class CategoryView(DetailView, CustomCacheMixin):
    model = Category
    template_name = "pages/category.html"

    def get(self, request, *args, **kwargs):
        category_slug = kwargs["slug"]

        cache_key = self.get_category_cache_key(category_slug)
        cached_data = self.get_cache_by_key(cache_key)

        if cached_data:
            return cached_data

        category = get_category_by_slug(category_slug)
        sub_categories = get_subcategory_by_id(category.id)
        news_by_category = get_news_category_by_id(category.id)

        news_count_by_category = get_news_category_count_by_id(category.id)

        response = self.render_to_response(
            {
                "category": category,
                "all_news": news_by_category,
                "sub_categories": sub_categories,
                "total_obj": news_count_by_category,
            }
        )
        response.render()

        self.set_cache_by_key(cache_key, response)
        logger.info(f"Set cache category by slug {category_slug}")

        return response

    def update_category_cache(self, category_slug):
        cache_key = self.get_category_cache_key(category_slug)

        category = get_category_by_slug(category_slug)
        sub_categories = get_subcategory_by_id(category.id)
        news_by_category = get_news_category_by_id(category.id)
        news_count_by_category = get_news_category_count_by_id(category.id)

        template = loader.get_template(self.template_name)

        content = template.render(
            {
                "category": category,
                "all_news": news_by_category,
                "sub_categories": sub_categories,
                "total_obj": news_count_by_category,
            }
        )

        response = HttpResponse(content, status=200)
        self.set_cache_by_key(cache_key, response)

        logger.info(f"Updated cache category by slug {category_slug}")
