from rest_framework import viewsets

from .models import Event
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    Viewset for events. See .models.Event.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
