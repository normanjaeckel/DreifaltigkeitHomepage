import csv
import datetime
import os

from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.utils import timezone
from django.views import generic
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import Event, Page
from .serializers import EventSerializer, PageSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    Viewset for events. See .models.Event.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class PageViewSet(viewsets.ModelViewSet):
    """
    Viewset for pages. See .models.Page.
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class LosungenViewSet(viewsets.ViewSet):
    """
    View for the Losungen (Evangelische Brüder-Unität Herrnhuter
    Brüdergemeine) of the current day.
    """
    permission_classes = (permissions.AllowAny,)

    def list(self, request, format=None):
        """
        Returns a dictionary with the Losungen and some metadata.
        """
        now = timezone.localtime(timezone.now())
        losungen_file = os.path.join(
            settings.MEDIA_ROOT,
            'Losungen Free {} Konvertiert.csv'.format(now.year)
        )
        try:
            with open(losungen_file) as csvfile:
                reader = csv.DictReader(csvfile)
                for item in reader:
                    day = datetime.datetime.strptime(item['Datum'], '%d.%m.%Y')
                    if day.date() == now.date():
                        break
                else:
                    item = None
        except FileNotFoundError as e:
            response = Response(
                {'details': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        else:
            if item:
                response = Response(item)
            else:
                response = Response(
                    {'details': 'No entry found in {}'.format(losungen_file)},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
        return response


class IndexView(generic.View):
    """
    Main entry point for this project.
    """
    def get(self, *args, **kwargs):
        with open(finders.find('index.html')) as f:
            content = f.read()
            return HttpResponse(content)
