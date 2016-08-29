from django.conf import settings
from django.contrib.sitemaps import Sitemap

from .models import Page


class HomeSitemap(Sitemap):
    """
    Sitemap definition for the home page.
    """
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return ['home']

    def location(self, obj):
        return settings.BASE_URL


class PageSitemap(Sitemap):
    """
    Sitemap definition for all pages.
    """
    changefreq = 'weekly'

    def items(self):
        return Page.objects.all()

    def priority(self, obj):
        return obj.sitemap_priority
