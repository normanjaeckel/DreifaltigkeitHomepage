from django.contrib import admin
from django.utils.translation import ugettext_lazy

from .models import Event, MediaFile, Page


class EventAdmin(admin.ModelAdmin):
    pass


class PageAdmin(admin.ModelAdmin):
    pass


class MediaFileAdmin(admin.ModelAdmin):
    pass


site_instance = admin.site
site_instance.site_title = ugettext_lazy(
    'Dreifaltigkeitskirchgemeinde Administration')
site_instance.site_header = ugettext_lazy(
    'Dreifaltigkeitskirchgemeinde Administration')

site_instance.register(Event, EventAdmin)
site_instance.register(Page, PageAdmin)
site_instance.register(MediaFile, MediaFileAdmin)
