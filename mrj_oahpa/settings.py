# Django settings for mrj_oahpa project.
# -*- encoding: utf-8 -*-
import os.path
import sys

os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['DJANGO_SETTINGS_MODULE'] = 'mrj_oahpa.settings'

# WSGI stuff
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# Confirm this is in path.
path = '/Users/mslm/main/ped/mrj_oahpa'
if path not in sys.path:
    sys.path.append(path)


# This flag triggers now the URL patterns in url.py file.
# The production_setting.py is triggered now by os name.
DEV = True

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

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',
)

# just testing svn
ADMINS = (
#	('Ciprian Gerstenberger', 'ciprian.gerstenberger@uit.no'),
#	('Trond Trosterud', 'trond.trosterud@uit.no'),
#	('Lene Antonsen', 'lene.antonsen@uit.no'),
        ('Heli Uibo', 'heli1401@gmail.com')
)

MANAGERS = ADMINS

# This is overridden below if the hostname is right.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mrjoahpa',
        'USER': 'root',
        'PASSWORD': 'miisu1',
        'HOSTNAME': 'localhost'
    }
}


# DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
# DATABASE_NAME = here('mrjoahpa.db.sql')             # Or path to database file if using sqlite3.
# DATABASE_USER = ''             # Not used with sqlite3.
# DATABASE_PASSWORD = ''         # Not used with sqlite3.
# DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
# DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

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

# http://testing.oahpa.no/voro/

# URL_PREFIX = 'smaoahpa'
URL_PREFIX = 'voro'
# URL_PREFIX = '책arjel'

# Absolute path to the directory that holds media.
#MEDIA_ROOT = "/home/mrj_oahpa/mrj_oahpa/media/"
MEDIA_ROOT = here('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

MEDIA_URL = '/%s/media/' % URL_PREFIX

# MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/%s/admin/media/' % URL_PREFIX

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+&dhg83#u^mg$vnp^7u2xd8wo15&=_c#yf0*no-mzrej!@zdw_'

# List of callables that know how to import templates from various sources.
# Changed for Django 1.4
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.doc.XViewMiddleware',
	# 'smaoahpa.courses.middleware.GradingMiddleware',
 	# 'smaoahpa.management.middlewares.SQLLogToConsoleMiddleware',
)

ROOT_URLCONF = 'mrj_oahpa.urls'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
	os.path.join(os.path.dirname(__file__), 'mrj_drill/templates').replace('\\','/'),
)

TEMPLATE_CONTEXT_PROCESSORS = ( "django.contrib.auth.context_processors.auth",
				"django.core.context_processors.debug",
				"django.core.context_processors.i18n",
				"django.core.context_processors.media",
				"django.core.context_processors.request",
				"mrj_oahpa.courses.context_processors.request_user",
				"mrj_oahpa.conf.context_processors.dialect",
				"mrj_oahpa.conf.context_processors.site_root",
				"mrj_oahpa.conf.context_processors.grammarlinks",
)
#				"management.context_processors.admin_media_prefix")


INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.admin',
        #'openid_provider',  # commented out for local testing
        # 'mrj_oahpa',
	'mrj_oahpa.mrj_drill',
        'mrj_oahpa.conf',
	# 'mrj_oahpa.courses',
        #'mrj_oahpa.mrj_feedback',
        'mrj_oahpa.management',
        'gunicorn',
)


LANGUAGES = (
        #('sjd', 'Kildin Sami'),
        ('ru', 'Russian'),
        ('sme', 'North Sami'),
    ('mrj', 'Võro'),
	('no', 'Norwegian'),
	#('sv', 'Swedish'),
	('en', 'English'),
	('fi', 'Finnish'),
    ('et', 'Estonian'),
    ('lv', 'Latvian'),
	#('de', 'German'),
)

OLD_NEW_ISO_CODES = {
	"fi": "fin",
	"ru": "rus",
	"en": "eng",
	"et": "est",
	"no": "nob",
    "da": "dan",
	"de": "deu",
	"sv": "swe",
	"sma": "sma",
    "sme": "sme",
    "sjd": "sjd",
    "mrj": "mrj",
    "lv": "lat",
}

# Regular expression and language code. Regexp must apply 'inf' group to
# matched string.

# If infinitive is None, then we assume there is no similar infinitive
# presentation marking, or that it comes from tags for languages which
# have word forms in the system.


INFINITIVE_SUBTRACT = {
	'nob': ur'^(?P<inf>책 )?(?P<lemma>.*)$',
	'swe': ur'^(?P<inf>att )?(?P<lemma>.*)$',
	'eng': ur'^(?P<inf>to )?(?P<lemma>.*)$',
	'deu': ur'^(?P<inf>zu )?(?P<lemma>.*)$',
	'dan': ur'^(?P<inf>at )?(?P<lemma>.*)$',
}

INFINITIVE_ADD = {
	'nob': ur'책 \g<lemma>',
	'swe': ur'att \g<lemma>',
	'eng': ur'to \g<lemma>',
	'deu': ur'zu \g<lemma>',
	'dan': ur'at \g<lemma>',
}

DIALECTS = {
	'main': ('', 'Unrestricted'),
	#'GG': ('isme-GG.restr.fst', 'Western'),
	#'KJ': ('isme-KJ.restr.fst', 'Eastern'),
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

MAIN_LANGUAGE = ('mrj', 'Võro')
L1 = MAIN_LANGUAGE[0]

#if os.uname()[1] == 'victorio.uit.no':
    #LOOKUP_TOOL = '/usr/local/bin/lookup'
 #   LOOKUP_TOOL = '/opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/lookup'
if os.uname()[1] == 'gtlab.uit.no':
    FST_DIRECTORY = '/opt/smi/mrj/bin'
    LOOKUP_TOOL = '/usr/local/bin/lookup'
else:
    FST_DIRECTORY = '/Users/mslm/main/langs/mrj/src'
    LOOKUP_TOOL = '/Users/mslm/bin/lookup'

APERTIUM_DIRECTORY = '/Users/mslm/apertium/incubator/apertium-rus'


# #
#
# LOGGING
#
# #

# TODO: logging!
# http://docs.djangoproject.com/en/dev/topics/logging/

if os.uname()[1] == 'victorio.uit.no':
	try:
		if VDEV:
			from x_settings import *
		else:
			from production_settings import *
	except:
		print "Could not load production_settings.py"
		sys.exit()
else:
	INSTALLED_APPS = INSTALLED_APPS + ('django_extensions',)


if LCIP:
	try:
		from cip_settings import *
	except:
		print "Could not load cip_settings.py"
		sys.exit()

if LHELI:
        try:
                from heli_settings import *
        except:
                print "Could not load heli_settings.py"
                sys.exit()

# #
#
# USER PROFILES
#
# #

AUTH_PROFILE_MODULE = 'courses.UserProfile'
LOGIN_REDIRECT_URL = '/mrj_oahpa/courses/'
LOGIN_URL = '/mrj_oahpa/courses/login/'

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
		'LOCATION': '/var/tmp/mrjoahpa_cache'
	},
}
