import datetime

from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.formats import localize
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

from .utils import EventType


class Event(models.Model):
    """
    Model for events.

    Every event belongs to one event type. See .utils.EventType.
    """
    type = models.CharField(
        ugettext_lazy('Veranstaltungstyp'),
        max_length=255,
        choices=EventType.get_all_choices(),
        default='default',
    )

    title = models.CharField(
        ugettext_lazy('Titel'),
        max_length=255,
        # TODO: help_text=ugettext_lazy('...'),
    )

    content = models.TextField(
        ugettext_lazy('Inhalt'),
        blank=True,
        # TODO: help_text=ugettext_lazy('...'),
    )

    begin = models.DateTimeField(
        ugettext_lazy('Beginn'),
        help_text=ugettext_lazy("Beispiel: '2013-07-20 14:00'."))

    duration = models.PositiveIntegerField(
        ugettext_lazy('Dauer in Minuten'),
        null=True,
        blank=True,
        help_text=ugettext_lazy(
            'Wenn nichts angegeben ist, wird keine Zeit für das Ende der '
            'Veranstaltung angezeigt.'),
    )

    on_home_before_begin = models.PositiveIntegerField(
        ugettext_lazy('Auf der Startseite (in Tagen)'),
        default=30,
        help_text=ugettext_lazy(
            'Die Veranstaltung erscheint so viele Tage vor Beginn auf der '
            'Startseite. Wählen Sie 0, wenn die Veranstaltung niemals auf der '
            'Startseite erscheinen soll.'),
    )

    not_on_event_type_page = models.BooleanField(
        ugettext_lazy('Auf Veranstaltungstypenseite ausblenden'),
        blank=True,
        help_text=ugettext_lazy(
            'Die Veranstaltung wird auf der Seite, auf der sonst die '
            'Veranstaltungen dieses Typs angezeigt werden, ausgeblendet.'),
    )

    not_on_public_calendar = models.BooleanField(
        ugettext_lazy('Im öffentlichen Kalender ausblenden'),
        blank=True,
        help_text=ugettext_lazy(
            'Die Veranstaltung wird im öffentlichen Kalender ausgeblendet. '
            'Angemeldete Benutzer mit Berechtigtigung können sie aber sehen.'),
    )

    class Meta:
        ordering = ('begin',)
        verbose_name = ugettext_lazy('Veranstaltung')
        verbose_name_plural = ugettext_lazy('Veranstaltungen')
        permissions = (
            (
                'can_see_hidden_events',
                ugettext_lazy('Darf ausgeblendete Veranstaltungen sehen'),
            ),
        )

    def __str__(self):
        return ' – '.join((localize(self.begin), self.title))

    @property
    def end(self):
        duration = self.duration or 0
        return self.begin + datetime.timedelta(minutes=duration)


class Page(models.Model):
    """
    Model for flat pages, event pages and special pages.
    """
    PAGE_CHOICES = (
        ('flat', ugettext_lazy('Statische Seite')),
        ('event', ugettext_lazy('Veranstaltungsseite')),
        ('calendar', ugettext_lazy('Kalender')),
    )

    type = models.CharField(
        ugettext_lazy('Seitetyp'),
        max_length=255,
        choices=PAGE_CHOICES,
        default='flat',
    )

    slug = models.SlugField(
        ugettext_lazy('Slug/URL'),
        unique=True,
        help_text=ugettext_lazy(
            "Beispiel: 'impressum'. Jede Seite muss einen individuellen "
            "Eintrag haben."),
    )

    title = models.CharField(
        ugettext_lazy('Titel'),
        max_length=100,
        help_text=ugettext_lazy(
            "Beispiel: 'Impressum'. Der Titel wird als Link in den Menüs "
            "angezeigt."),
    )

    # TODO: is_in_navbar = models.BooleanField
    # TODO: is_in_main_menu = models.BooleanField

    content = models.TextField(
        ugettext_lazy('Inhalt'),
        blank=True,
        # TODO: help_text=ugettext_lazy('...'),
    )

    parent = models.ForeignKey(
        'self',
        verbose_name=ugettext_lazy('Elternelement'),
        null=True,
        help_text=ugettext_lazy(
            'Es ist die übergeordnete Seite auszuwählen. Unterseiten '
            'erscheinen im Menü nur bis zur dritten Ebene.'),
        )

    weight = models.IntegerField(
        ugettext_lazy('Platzierung'),
        default=100,
        help_text=ugettext_lazy(
            'Eine höhere Zahl bedeutet, dass der Eintrag im Menü weiter '
            'unten steht.'),
    )

    required_permission = models.ForeignKey(
        Permission,
        verbose_name=ugettext_lazy('Erforderliche Berechtigung'),
        null=True,
        blank=True,
        # TODO: help_text=ugettext_lazy('...'),
    )

    sitemap_priority = models.DecimalField(
        ugettext_lazy('Priorität in der Sitemap'),
        max_digits=2,
        decimal_places=1,
        default=0.5,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text=ugettext_lazy(
            'Die Zahl gibt die Priorität in der Sitemap an. Sie wird von '
            'Suchmaschinen ausgewertet. Siehe '
            '<a href="http://www.sitemaps.org/de/protocol.html#prioritydef">'
            'Definition im Sitemapprotokoll</a>.'),
    )

    class Meta:
        ordering = ('weight', 'slug',)
        verbose_name = ugettext_lazy('Seite')
        verbose_name_plural = ugettext_lazy('Seiten')

    def __str__(self):
        result = ''
        if self.parent is not None:
            result = str(self.parent) + ' – '
        return result + self.title

    def get_absolute_url(self):
        """
        Returns the URL to the page. Slugs of child and parent pages are
        combined.
        """
        url = reverse('page', args=[self.slug])
        if self.parent is not None:
            url = self.parent.get_absolute_url()[:-1] + url
        return url

    def clean(self):
        """
        Checks parent field to prevent hierarchical loops.
        """
        super().clean()
        ancestor = self.parent
        while ancestor is not None:
            if ancestor == self:
                raise ValidationError(_(
                    'Fehler: Es darf keine zirkuläre Hierarchie erstellt '
                    'werden. Wählen Sie ein anderes Elternelement.'))
            ancestor = ancestor.parent


class MediaFile(models.Model):
    """
    Model for uploaded files like images.
    """
    mediafile = models.FileField(
        ugettext_lazy('Datei'),
        max_length=255,
    )

    uploaded_on = models.DateTimeField(
        ugettext_lazy('Hochgeladen am'),
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-uploaded_on',)
        verbose_name = ugettext_lazy('Datei')
        verbose_name_plural = ugettext_lazy('Dateien')

    def __str__(self):
        return self.mediafile.url
