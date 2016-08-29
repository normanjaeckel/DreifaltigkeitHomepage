from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from . import sitemaps, views
from .rest_api import router


sitemaps_dict = {
    'home': sitemaps.HomeSitemap,
    'pages': sitemaps.PageSitemap}


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps_dict}),
    url(r'^(|.+/)$', views.IndexView.as_view()),
]
