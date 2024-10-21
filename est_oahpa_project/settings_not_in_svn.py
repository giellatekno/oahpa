from settings import LLL1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['.gtoahpa-01.uit.no','127.0.0.1','localhost']

# Development mode
#DEBUG = True
#ALLOWED_HOSTS = []

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+&dhg83#u^mg$vnp^7u2xd8wo15&=_c#yf0*no-mzrej!@zdw_'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': LLL1+'_oahpa',                      # Or path to database file if using sqlite3.
        'USER': LLL1+'_oahpa',                      # Not used with sqlite3.
        'PASSWORD': 'Varbola1343',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
     }
}

hostname = "oahpa.no"

### PATHS ###
import os
import os.path
import sys
# Confirm this is in path.
path = '/home/oahpa/'+LLL1+'_oahpa_project'
if path not in sys.path:
    sys.path.append(path)

LOCALE_PATHS = ('/home/oahpa/'+LLL1+'_oahpa_project/locale',)

if os.uname()[1] == 'gtoahpa-01.uit.no':
    LOOKUP_TOOL = '/usr/local/bin/lookup'  # xfst
    HFST_LOOKUP = '/usr/bin/hfst-lookup' # hfst
else:
    LOOKUP_TOOL = '/usr/local/bin/lookup'  # xfst
    HFST_LOOKUP = '/usr/local/bin/hfst-lookup'

FST_DIRECTORY = '/opt/smi/'+LLL1+'/bin'
LOG_FILE = path + '/drill/vastaF_log.txt'

TOOLS_DIRECTORY = '/home/oahpa/gtsvn/giella-core/scripts'
DEV_DIRECTORY = '/home/oahpa/gtsvn/langs_'+LLL1+'_devtools'

# Absolute path to the directory that holds media.
MEDIA_ROOT = '/home/oahpa/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
STATIC_URL = '/home/oahpa/admin_media/'

CACHES = {
        'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': '/var/tmp/'+LLL1+'_oahpa_cache'
        },
}
