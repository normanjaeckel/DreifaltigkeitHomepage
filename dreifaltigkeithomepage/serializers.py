from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Serialiter for events. See .models.Event.
    """
    class Meta:
        model = Event
        fields = (
            'id',
            'type',
            'get_type_display',
            'title',
            'content',
            'begin',
            'duration',
            'on_home_before_begin',
            'not_on_event_type_page',
            'not_on_public_calendar',
        )
