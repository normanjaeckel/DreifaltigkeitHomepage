Draft of a website the for Dreifaltigkeitskirchgemeinde Leipzig
===============================================================

Development environment with Ubuntu 14.04.

::

    $ python3 -m venv .virtualenv
    $ source .virtualenv/bin/activate
    $ pip install --upgrade pip
    $ pip install --requirement requirements.txt
    $ npm install
    $ node_modules/.bin/bower install
    $ node_modules/.bin/gulp django
    $ node_modules/.bin/gulp
    $ python manage.py migrate
    $ python manage.py createsuperuser
    $ python manage.py runserver

