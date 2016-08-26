from django.conf.urls import include, url
from django.contrib import admin

from . import views
from .rest_api import router


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^(|.+/)$', views.IndexView.as_view()),
]
