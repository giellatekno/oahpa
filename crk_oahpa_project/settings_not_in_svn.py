from settings import LLL1

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+&dhg83#u^mg$vnp^7u2xd8wo15&=_c#yf0*no-mzrej!@zdw_'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': LLL1+'_oahpa',                      # Or path to database file if using sqlite3.
        'USER': LLL1+'_oahpa',                      # Not used with sqlite3.
        'PASSWORD': LLL1+'GOGO'+LLL1,                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
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

LOOKUP_OPTS = ''

if os.uname()[1] == 'gtoahpa-01.uit.no' or os.uname()[1] == 'gtoahpa-02.uit.no':
    LOOKUP_TOOL = '/usr/local/bin/lookup'  # xfst
    HFST_LOOKUP = '/usr/bin/hfst-lookup' # hfst
    LOOKUP_OPTS = '-flags mbTT'

    # when installing ...
    #if 'install.py' in sys.argv:
    #    LOOKUP_TOOL = '/usr/bin/hfst-optimized-lookup'
    #    LOOKUP_OPTS = '-qx'
else:
    LOOKUP_TOOL = '/usr/local/bin/lookup'  # xfst
    HFST_LOOKUP = '/usr/bin/hfst-lookup'

ENG_FST_DIRECTORY = '../crk_data/englexc/'
ENG_DIALECTS = {
    'main': ('../crk_data/englexc/ieng.fst', 'Unrestricted'),
}

ENG_HLOOKUP_TOOL = '/usr/local/bin/lookup'
ENG_LOOKUP_TOOL = '/usr/local/bin/lookup -flags mbTT'

FST_DIRECTORY = '/opt/smi/'+LLL1+'/bin'
LOG_FILE = path + '/drill/vastaF_log.txt'

GAME_FSTS = {
    'dato': {
        'generate': FST_DIRECTORY + '/transcriptor-date-digit2text.filtered.lookup.hfstol',
        'answers': FST_DIRECTORY + '/transcriptor-date-text2digit.filtered.lookup.hfstol',
    },
    'numbers': {
        'generate': FST_DIRECTORY + '/transcriptor-numbers-digit2text.filtered.lookup.hfstol',
        'answers': FST_DIRECTORY + '/transcriptor-numbers-text2digit.filtered.lookup.hfstol',
    },
    'clock': {
        'generate': FST_DIRECTORY + '/transcriptor-clock-digit2text.filtered.lookup.hfstol',
        'answers': FST_DIRECTORY + '/transcriptor-clock-text2digit.filtered.lookup.hfstol',
    },
    'money': {
        'generate': FST_DIRECTORY + '/transcriptor-money-digit2text.filtered.lookup.hfstol',
        'answers': FST_DIRECTORY + '/transcriptor-money-text2digit.filtered.lookup.hfstol',
    },
}

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

_join_path = lambda x: os.path.join(os.getcwd(), x)

ERROR_FST_SETTINGS = {
    #'lookup_tool': 'hfst-optimised-lookup',
    'lookup_tool': 'hfst-lookup',
    #'fst_path': '/opt/smi/crk/bin/transcriptor-numbers-text2digit.filtered.lookup.hfstol',
    #'fst_path': FST_DIRECTORY +'/transcriptor-numbers-text2digit.filtered.lookup.hfstol',
    'fst_path': FST_DIRECTORY +'/transcriptor-numbers-text2digit.filtered.lookup.hfstol',
    'error_log_path': _join_path('error_fst_log.txt'),
    'error_message_files': {
        'eng': _join_path('crk_data/meta_data/errorfstmessages.xml'),
    }
}
