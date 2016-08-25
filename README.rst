Draft of a website the for Dreifaltigkeitskirchgemeinde Leipzig
===============================================================

This project is still under development.


Local development
-----------------

To setup a local development version run::

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


Credits
-------

The used template is `Starter template <http://getbootstrap.com/getting-started/#examples-framework>`_. The code of this template was released under the `Creative Commons Attribution 3.0 Unported (CC BY 3.0) <https://creativecommons.org/licenses/by/3.0/>`_ license by `@mdo <https://twitter.com/mdo>`_ and `@fat <https://twitter.com/fat>`_, Bootstrap (Twitter, Inc).
