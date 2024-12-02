from settings import LLL1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@@eq#_ow*e_1-i_!hs#2130!$&*-=9r_ypv+0&_e6&tj$u9#@a'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': LLL1+'_oahpa',                # Or path to database file if using sqlite3.
        'USER': LLL1+'_oahpa',                # Not used with sqlite3.
        'PASSWORD': 'smsGOGOsms',             # Not used with sqlite3.
        'HOST': '',                           # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
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

LOCALE_PATHS = (
    '/home/oahpa/'+LLL1+'_oahpa_project/locale',
)

if os.uname()[1] == 'gtoahpa-01.uit.no' or os.uname()[1] == 'gtoahpa-02.uit.no':
    LOOKUP_TOOL = '/usr/local/bin/lookup'  # xfst
    HFST_LOOKUP = '/bin/hfst-lookup' # hfst
    #LOOKUP_TOOL = '/opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/lookup'
else:
    LOOKUP_TOOL = '/usr/local/bin/lookup'  # xfst
    HFST_LOOKUP = '/usr/local/bin/hfst-lookup'

FST_DIRECTORY = '/opt/smi/'+LLL1+'/bin'
LOG_FILE = path + '/drill/vastaF_log.txt'

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
