# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 22:22
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


def add_base_pages(apps, schema_editor):
    """
    Adds the three basic pages for the project.
    """
    # We get the model from the versioned app registry.
    # If we directly import it, it'll be the wrong version.
    Page = apps.get_model('dreifaltigkeithomepage', 'Page')
    db_alias = schema_editor.connection.alias
    Page.objects.using(db_alias).bulk_create([
        Page(
            slug='gemeinde',
            title='Gemeinde',
            weight=1000
        ),
        Page(
            slug='kindergarten',
            title='Kindergarten',
            weight=2000
        ),
        Page(
            slug='dresdner59',
            title='Stadtteilprojekt Dresdner59',
            weight=3000
        ),
    ])


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('default', 'Sonstige Veranstaltung')], default='default', max_length=255, verbose_name='Veranstaltungstyp')),
                ('title', models.CharField(max_length=255, verbose_name='Titel')),
                ('content', models.TextField(blank=True, verbose_name='Inhalt')),
                ('begin', models.DateTimeField(help_text="Beispiel: '2013-07-20 14:00'.", verbose_name='Beginn')),
                ('duration', models.PositiveIntegerField(blank=True, help_text='Wenn nichts angegeben ist, wird keine Zeit für das Ende der Veranstaltung angezeigt.', null=True, verbose_name='Dauer in Minuten')),
                ('on_home_before_begin', models.PositiveIntegerField(default=30, help_text='Die Veranstaltung erscheint so viele Tage vor Beginn auf der Startseite. Wählen Sie 0, wenn die Veranstaltung niemals auf der Startseite erscheinen soll.', verbose_name='Auf der Startseite (in Tagen)')),
                ('not_on_event_type_page', models.BooleanField(help_text='Die Veranstaltung wird auf der Seite, auf der sonst die Veranstaltungen dieses Typs angezeigt werden, ausgeblendet.', verbose_name='Auf Veranstaltungstypenseite ausblenden')),
                ('not_on_public_calendar', models.BooleanField(help_text='Die Veranstaltung wird im öffentlichen Kalender ausgeblendet. Angemeldete Benutzer mit Berechtigtigung können sie aber sehen.', verbose_name='Im öffentlichen Kalender ausblenden')),
            ],
            options={
                'verbose_name_plural': 'Veranstaltungen',
                'permissions': (('can_see_hidden_events', 'Darf ausgeblendete Veranstaltungen sehen'),),
                'verbose_name': 'Veranstaltung',
                'ordering': ('begin',),
            },
        ),
        migrations.CreateModel(
            name='MediaFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mediafile', models.FileField(max_length=255, upload_to='', verbose_name='Datei')),
                ('uploaded_on', models.DateTimeField(auto_now_add=True, verbose_name='Hochgeladen am')),
            ],
            options={
                'verbose_name_plural': 'Dateien',
                'verbose_name': 'Datei',
                'ordering': ('-uploaded_on',),
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('flat', 'Statische Seite'), ('event', 'Veranstaltungsseite'), ('calendar', 'Kalender')], default='flat', max_length=255, verbose_name='Seitetyp')),
                ('slug', models.SlugField(help_text="Beispiel: 'impressum'. Jede Seite muss einen individuellen Eintrag haben.", unique=True, verbose_name='Slug/URL')),
                ('title', models.CharField(help_text="Beispiel: 'Impressum'. Der Titel wird als Link in den Menüs angezeigt.", max_length=100, verbose_name='Titel')),
                ('content', models.TextField(blank=True, verbose_name='Inhalt')),
                ('weight', models.IntegerField(default=100, help_text='Eine höhere Zahl bedeutet, dass der Eintrag im Menü weiter unten steht.', verbose_name='Platzierung')),
                ('sitemap_priority', models.DecimalField(decimal_places=1, default=0.5, help_text='Die Zahl gibt die Priorität in der Sitemap an. Sie wird von Suchmaschinen ausgewertet. Siehe <a href="http://www.sitemaps.org/de/protocol.html#prioritydef">Definition im Sitemapprotokoll</a>.', max_digits=2, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='Priorität in der Sitemap')),
                ('parent', models.ForeignKey(help_text='Es ist die übergeordnete Seite auszuwählen. Unterseiten erscheinen im Menü nur bis zur dritten Ebene.', null=True, on_delete=django.db.models.deletion.CASCADE, to='dreifaltigkeithomepage.Page', verbose_name='Elternelement')),
                ('required_permission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Permission', verbose_name='Erforderliche Berechtigung')),
            ],
            options={
                'verbose_name_plural': 'Seiten',
                'verbose_name': 'Seite',
                'ordering': ('weight', 'slug'),
            },
        ),
        migrations.RunPython(
            add_base_pages
        ),
    ]
