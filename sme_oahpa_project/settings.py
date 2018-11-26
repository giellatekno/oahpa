# Django settings for univ_oahpa project.
# -*- encoding: utf-8 -*-
import os.path
import sys

os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# WSGI stuff
# import django.core.handlers.wsgi
# application = django.core.handlers.wsgi.WSGIHandler()

# Confirm this is in path.
#path = '/home/univ_oahpa/univ_oahpa/'
path = '/Users/car010/main/ped/univ_oahpa/'
if path not in sys.path:
    sys.path.append(path)

# This flag triggers now the URL patterns in url.py file.
# The production_setting.py is triggered now by os name.
DEV = False

# This flag triggers the settings on victorio for production in production_settings.py
# or development (feeding the db, syncdb, etc.)
# IMPORTANT: Do NOT svn ci the development settings file!

VDEV = True

# Cip's local config er different than Ryan's one

LCIP = False

# config flag for Heli
LHELI = False

# I prefer to use things like this because then settings don't need to depend on absolute paths all the time.
# Can just list the media or template dirs as here('templates') instead of '/home/me/.../smaoahpa/templates/

here = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), x)
here_cross = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), *x)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',
)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# just testing svn
ADMINS = (
#   ('Ciprian Gerstenberger', 'ciprian.gerstenberger@uit.no'),
#   ('Trond Trosterud', 'trond.trosterud@uit.no'),
#   ('Lene Antonsen', 'lene.antonsen@uit.no'),
        ('Ryan Johnson', 'rjo040@post.uit.no'),
        ('Heli Uibo', 'heli.uibo@ut.ee')
)

MANAGERS = ADMINS

# This is overridden below if the hostname is right.

# DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
# DATABASE_NAME = ''             # Or path to database file if using sqlite3.
# DATABASE_USER = ''             # Not used with sqlite3.
# DATABASE_PASSWORD = ''         # Not used with sqlite3.
# DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
# DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        #'NAME': 'test',                      # Or path to database file if using sqlite3.
        #'USER': 'test',                      # Not used with sqlite3.
        #'PASSWORD': 'test',                  # Not used with sqlite3.
        #'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        #'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
     }
}

TRANSLATABLE_MODEL_MODULES = ["courses.models"]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.

TIME_ZONE = 'Europe/Oslo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'no'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# http://oahpa.uit.no/univ_oahpa/

# URL_PREFIX = 'smaoahpa'
URL_PREFIX = 'davvi'
# URL_PREFIX = 'åarjel'

# Absolute path to the directory that holds media.

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# ADMIN_MEDIA_PREFIX = '/%s/admin/media/' % URL_PREFIX

STATIC_ROOT = here('static')
MEDIA_ROOT = here("media")
MEDIA_URL = '/%s/media/' % URL_PREFIX
STATIC_URL = '/%s/static/' % URL_PREFIX

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+&dhg83#u^mg$vnp^7u2xd8wo15&=_c#yf0*no-mzrej!@zdw_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'courses.authentication.CookieAuthMiddleware',
    'courses.middleware.GradingMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/univ_oahpa/univ_oahpa/templates',
    '/home/univ_oahpa/univ_oahpa/univ_drill/templates',
    '/home/univ_oahpa/univ_oahpa/courses/templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.request",
                "django.core.context_processors.csrf",
                "courses.context_processors.request_user",
                "courses.context_processors.courses_user",
                "survey.context_processors.display_survey_notice",
                "conf.context_processors.dialect",
                "geo.resolver.session_country",
                "conf.context_processors.site_root",
                "conf.context_processors.redirect_to",

                "conf.context_processors.grammarlinks",
                'django_messages.context_processors.inbox',

)


INSTALLED_APPS = (
    # 'south',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'rest_framework',
    'openid_provider',
    'univ_drill',
    'diff',
    'conf',
    'courses',
    'survey',
    'errorapi',
    'univ_feedback',
    'management',
    # 'testing',
    'django_messages',
    'django_extensions',
    'django_forms_bootstrap',
    'modeltranslation',
)

USE_TZ = True

LANGUAGES = (
    ('sme', 'North Sami'),
    ('no', 'Norwegian'),
    ('nb', 'Norwegian'),
    ('sv', 'Swedish'),
    ('en', 'English'),
    ('fi', 'Finnish'),
    #('de', 'German'),
)

OLD_NEW_ISO_CODES = {
    "fi": "fin",
    "ru": "rus",
    "en": "eng",
    "no": "nob",
    "nb": "nob",
    "de": "deu",
    "sv": "swe",
    "sma": "sma",
    "sme": "sme"
}

# Regular expression and language code. Regexp must apply 'inf' group to
# matched string.

# If infinitive is None, then we assume there is no similar infinitive
# presentation marking, or that it comes from tags for languages which
# have word forms in the system.


INFINITIVE_SUBTRACT = {
    'nob': ur'^(?P<inf>å )?(?P<lemma>.*)$',
    'swe': ur'^(?P<inf>att )?(?P<lemma>.*)$',
    'eng': ur'^(?P<inf>to )?(?P<lemma>.*)$',
    'deu': ur'^(?P<inf>zu )?(?P<lemma>.*)$',
}

INFINITIVE_ADD = {
    'nob': ur'å \g<lemma>',
    'swe': ur'att \g<lemma>',
    'eng': ur'to \g<lemma>',
    'deu': ur'zu \g<lemma>',
}

DIALECTS = {
    #'main': ('oahpa-isme-norm.fst', 'Unrestricted'),  # old infra
    #'GG': ('isme-GG.restr.fst', 'Western'),
    #'KJ': ('isme-KJ.restr.fst', 'Eastern'),
    'main': ('generator-oahpa-gt-norm.xfst', 'Unrestricted'),
    'GG': ('generator-oahpa-gt-norm-dial_GG.xfst', 'Western'),
    'KJ': ('generator-oahpa-gt-norm-dial_KJ.xfst', 'Eastern'),
    'NG': (None, 'Non-Presented forms'),
}

DEFAULT_DIALECT = 'GG'
NONGEN_DIALECT = 'NG'
# # #
#
# Some settings for the install.py scripts
#
# # #

# maybe some of these actually should be options in the install script...

MAIN_LANGUAGE = ('sme', 'North Sami')
L1 = MAIN_LANGUAGE[0]

LOOKUP_TOOL = '/usr/bin/lookup'
FST_DIRECTORY = '/opt/smi/sme/bin'
#LOOKUP2CG = '/usr/local/bin/lookup2cg'
LOOKUP2CG = '/home/heli/main/gt/script/lookup2cg'
CG3 = '/usr/bin/vislcg3'
#PREPROCESS = '/opt/sami/cg/bin/preprocess '
PREPROCESS = "/home/heli/main/gt/script/preprocess "


# FST_DIRECTORY = '/home/ryan/gtsvn/gt/sme/bin'

# #
#
# LOGGING
#
# #

import logging
from loggers import initialize_loggers

initialize_loggers()

#from production_settings import *

#logging.basicConfig(
#    level = logging.DEBUG,
#    format = '%(asctime)s %(levelname)s %(message)s',
#    filename = '/tmp/log',
#    filemode = 'w'
#)


# #
#
# USER PROFILES
#
# #

AUTH_PROFILE_MODULE = 'courses.UserProfile'
LOGIN_REDIRECT_URL = '/%s/courses/' % URL_PREFIX
LOGIN_URL = '/%s/courses/login/' % URL_PREFIX

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/univ_oahpa_cache'
    },
}

MODELTRANSLATION_TRANSLATION_FILES = (
    'translation',
)

##
## Root Cookie
##

# COOKIE_NAME = "http://oahpa.no/"
COOKIE_NAME_STARTSWITH = "wordpress_logged_in_"
SESSION_COOKIE_DOMAIN = 'oahpa.no'
COOKIEAUTH_ADMIN_PREFIX = '/davvi/admin'
SESSION_ENGINE = "django.contrib.sessions.backends.file"
SESSION_FILE_PATH = "/tmp/oahpa/"

AUTHENTICATION_BACKENDS = (
    'courses.authentication.CookieAuth',
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'PAGINATE_BY': 10
}

_join_path = lambda x: os.path.join(os.getcwd(), x)

ERROR_FST_SETTINGS = {
    'lookup_tool': 'lookup -flags mbTT',
    'fst_path': '/opt/smi/sme/bin/ped-errortag-sme.fst',
    'error_log_path': _join_path('error_fst_log.txt'),
    'error_message_files': {
        'nob': _join_path('../sme/meta/morfaerrorfstmessages.xml'),
    }
}



GEOIP_PATH = '/home/univ_oahpa/univ_oahpa/geo/data/'
GEOIP_LIBRARY_PATH = '/home/univ_oahpa/univ_oahpa/geo/geoip/lib/libGeoIP.so'
GEOIP_COUNTRY = 'GeoIP.dat'
GEOIP_CITY = 'GeoLiteCity.dat'

LOOKUPSERV_PORT = 9000
