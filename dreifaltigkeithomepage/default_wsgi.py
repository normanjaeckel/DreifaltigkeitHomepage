"""
WSGI config for this project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

# Use the following lines for deployment:
#
# import site
#
# BASE_DIR = os.path.dirname('<%= outputDirectory %>')
# site.addsitedir(BASE_DIR)
# site.addsitedir(os.path.join(
#     BASE_DIR, '.virtualenv', 'lib', 'python3.4', 'site-packages'))

from django.core.wsgi import get_wsgi_application  # isort:skip

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    '<%= outputDirectoryBaseName %>.settings')

application = get_wsgi_application()
