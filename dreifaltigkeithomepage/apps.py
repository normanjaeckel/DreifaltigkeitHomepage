from django.apps import AppConfig
from django.utils.translation import ugettext_lazy


class ProjectAppConfig(AppConfig):
    """
    Django application configuration for this project.
    """
    name = 'dreifaltigkeithomepage'
    verbose_name = ugettext_lazy(
        'Homepage der Dreifaltigkeitskirchgemeinde Leipzig')

    def ready(self):
        from .rest_api import router
        from .views import (
            EventTypeViewSet,
            EventViewSet,
            LosungenViewSet,
            PageViewSet,
        )

        router.register(r'event', EventViewSet)
        router.register(r'page', PageViewSet)
        router.register(r'eventtype', EventTypeViewSet, 'eventtype')
        router.register(r'losungen', LosungenViewSet, 'losungen')
