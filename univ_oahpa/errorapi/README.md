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

4. Navigate to the test page (TODO: include url) and click words to see if
   everything runs. 

## So far...

This isn't able to be installed as a module, but: track requirements for the
package in requirements.txt, and make sure that as much as possible can be done
through this module or settings in `settings.py`. 

## Developing

If you need to build this as a package for installation on other projects: 

    python setup.py sdist

    pip install --user errorapi/dist/errorapi-0.1.tar.gz

    pip uninstall django-polls


