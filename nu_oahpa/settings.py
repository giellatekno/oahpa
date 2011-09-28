# Django settings for oahpa project.
# Do not add this file to public svn, for security reasons!
import os.path
import sys

os.environ['PYTHON_EGG_CACHE'] = '/tmp'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Heli Uibo', 'heli'),
     ('Trond Trosterud', 'trond'),
     ('Lene Antonsen', 'lene'),
     ('Ciprian Gerstenberger', 'ciprian'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'oahpa.db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

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

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/nu_oahpa/ped/nu_oahpa/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://victorio.uit.no/nu_oahpa/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/nu_oahpa/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@wun)vvu8w(66r9$0vh0y$7rkfr_1+4y(_h5awb%7ow0bgkudj'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',		
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'nu_oahpa.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
	os.path.join(os.path.dirname(__file__), 'nu_drill/templates').replace('\\','/'),
	os.path.join(os.path.dirname(__file__), 'nu_feedback/templates').replace('\\','/'),
)

TEMPLATE_CONTEXT_PROCESSORS =("django.core.context_processors.auth",
                              "django.core.context_processors.debug",
                              "django.core.context_processors.i18n",
                              "django.core.context_processors.media",
                              "django.core.context_processors.request",
                              "nu_oahpa.nu_conf.context_processors.dialect",
                              "nu_oahpa.nu_courses.context_processors.request_user",)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'nu_oahpa.nu_drill',
    'nu_oahpa.nu_feedback',
    'nu_oahpa.nu_courses',
)


LANGUAGES = (
    ('en', 'English'),
    ('fi', 'Finnish'),
    ('no', 'Norwegian'),
    ('sme', 'North Sami'),
    ('sv', 'Swedish'),
    )

# #
#
# USER PROFILES
#
# #

AUTH_PROFILE_MODULE = 'nu_courses.UserProfile'
LOGIN_REDIRECT_URL = '/nu_oahpa/nu_courses/'
LOGIN_URL = '/nu_oahpa/nu_courses/login/'
SESSION_COOKIE_AGE = 45 * 60   # in seconds, timeout 45 minutes.

