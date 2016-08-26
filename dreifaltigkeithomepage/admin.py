from django.apps import apps
from django.contrib import admin
from django.utils.translation import ugettext_lazy

from .models import Event, MediaFile, Page


class EventAdmin(admin.ModelAdmin):
    pass


class PageAdmin(admin.ModelAdmin):
    pass


class MediaFileAdmin(admin.ModelAdmin):
    pass


description = ugettext_lazy('{app_name} Administration').format(
    app_name=apps.get_app_config('dreifaltigkeithomepage').verbose_name)

site_instance = admin.site
site_instance.site_title = description
site_instance.site_header = description

site_instance.register(Event, EventAdmin)
site_instance.register(Page, PageAdmin)
site_instance.register(MediaFile, MediaFileAdmin)
