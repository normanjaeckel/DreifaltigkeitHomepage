"""
Django settings for this project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

from <%= projectName %>.general_settings import *  # noqa: E225,E999
from <%= projectName %>.utils import EventType  # noqa: E225,E999


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<%= secretKey %>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

WSGI_APPLICATION = '<%= outputDirectoryBaseName %>.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'db.sqlite3'),
    }
}

# Install psycopg2 for PostgreSQL support.
#
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': '...',
#        'USER': '...',
#        'PASSWORD': '...',
#        'HOST': 'localhost',
#        'PORT': '5432'
#    }
# }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

if DEBUG:
    STATICFILES_DIRS = [os.path.join(os.path.dirname(__file__), 'static')]
else:
    STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')


# User uploaded files
# https://docs.djangoproject.com/en/1.9/topics/files/

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')


# Miscellaneous

EVENT_TYPES = [
    EventType(
        db_value='default',
        human_readable_value='Sonstige Veranstaltung',
        human_readable_value_plural='Sonstige Veranstaltungen',
        css_class_name_suffix='default',
    ),
]
