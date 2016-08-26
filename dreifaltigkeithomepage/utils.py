from django.conf import settings


class EventType:
    """
    Helper class to define types of events. See .model.Event.type.
    """
    def __init__(self, db_value, human_readable_value,
                 human_readable_value_plural=None,
                 css_class_name_suffix='primary'):
        self.db_value = db_value
        self.human_readable_value = human_readable_value
        self.human_readable_value_plural = (
            human_readable_value_plural or human_readable_value + 's')
        self.css_class_name = 'event-{}'.format(css_class_name_suffix)

    @property
    def choices(self):
        """
        Returns a tuple that can be used for Django model field choices
        entries.
        """
        return self.db_value, self.human_readable_value

    @classmethod
    def get_all_choices(cls):
        """
        Returns an iterable of all event types that are configured in the
        settings (EVENT_TYPES). The result can be used for Django model
        field choices.
        """
        return (event_type.choices for event_type in settings.EVENT_TYPES)
