# -*- encoding: utf-8 -*-

""" Manage additional locales not supported in the base installation of
Django.

This is a way of ensuring that we do not need to constantly update
locales within the Django library path, and ensures that upgrades to new
versions of Django will not require migrating the locale files.

Inspiration: http://stackoverflow.com/questions/12946830/how-to-add-new-languages-into-django-my-language-uyghur-or-uighur-is-not-su

"""

from django.conf import global_settings

gettext_noop = lambda s: s

EXTRA_LANG_INFO = {
    'sme': {
        'bidi': False, # left-to-right, True = right-to-left
        'code': 'sme',
        'name': 'North Saami',
        'name_local': u'Davvisámegiella',
    },
}

# Add ISO codes here
RIGHT_TO_LEFT_LANGUAGES = []

import django.conf.locale

LANG_INFO = dict(django.conf.locale.LANG_INFO.items() + EXTRA_LANG_INFO.items())

django.conf.locale.LANG_INFO = LANG_INFO

# Languages using BiDi (right-to-left) layout
LANGUAGES_BIDI = global_settings.LANGUAGES_BIDI + RIGHT_TO_LEFT_LANGUAGES

#from django.conf import settings
#if settings.DEBUG:
	#print "Added custom locales."
