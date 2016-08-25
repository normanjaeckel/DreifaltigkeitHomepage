from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.views import generic
from rest_framework import viewsets

from .models import Event
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    Viewset for events. See .models.Event.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class IndexView(generic.View):
    """
    Main entry point for this project.
    """
    def get(self, *args, **kwargs):
        with open(finders.find('index.html')) as f:
            content = f.read()
            return HttpResponse(content)
