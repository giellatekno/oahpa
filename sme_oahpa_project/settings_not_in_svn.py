from settings import LLL1

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
path = '/home/oahpa/'+LLL1+'_oahpa_project/'+LLL1+'_oahpa'
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
LOOKUP2CG = '/opt/smi/sme/bin/lookup2cg'
CG3 = '/bin/cg3'
PREPROCESS = '/opt/smi/sme/bin/preprocess'
LOOKUPSERV_PORT = 80
LOG_FILE = path + '/drill/vastaF_log.txt'
LOG_FILE_VS = path + '/drill/vastaF_and_Sahka_CGanalysis_log.txt'
LOG_FILE_V = path + '/drill/vastas_log.txt'

_join_path = lambda x: os.path.join(os.getcwd(), x)

ERROR_FST_SETTINGS = {
    'lookup_tool': 'lookup -flags mbTT',
    'fst_path': '/opt/smi/sme/bin/ped-sme.fst', #server
    'error_log_path': _join_path('error_fst_log.txt'),
    'error_message_files': {
        #'nob': _join_path('../sme/meta/morfaerrorfstmessages.xml'), #server
        'nob': _join_path('sme_data/meta_data/morfaerrorfstmessages.xml'),
    }
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


#These are in original settings
'''
COOKIE_NAME = "wordpress_logged_in_"
SESSION_COOKIE_DOMAIN = 'oahpa.no'
COOKIEAUTH_ADMIN_PREFIX = '/aarjel/admin'
SESSION_ENGINE = "django.contrib.sessions.backends.file"
SESSION_FILE_PATH = "/tmp/smaoahpa/"
'''

# Geo
GEOIP_PATH = '/home/oahpa/'+LLL1+'_oahpa_project/'+LLL1+'_oahpa/geo/data/'
GEOIP_COUNTRY = 'GeoLite2-Country_20181204/GeoLite2-Country.mmdb'
GEOIP_CITY = 'GeoLite2-City_20181204/GeoLite2-City.mmdb'
