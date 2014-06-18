# Error API

`errorapi` is a system for providing pedagogical feedback when users click on a
word.

Quick start
-----------

1. Add "errorapi" to your `INSTALLED_APPS` setting like this::

    INSTALLED_APPS = (
        ...
        'errorapi',
    )

2. Include the polls URLconf in your project urls.py like this::

    url(r'^errorapi/', include('errorapi.urls')),

3. Run `python manage.py migrate` to create the errorapi models.


## Developing

If you need to build this as a package for installation on other projects: 

    python setup.py sdist

    pip install --user errorapi/dist/errorapi-0.1.tar.gz

    pip uninstall django-polls


