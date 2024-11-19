from settings import LLL1

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '158+5%s4*4a@zkr$)-5m2ef%f1)b!(wb8iehwx-hv#r7!7@0u3'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': LLL1+'_oahpa',                      # Or path to database file if using sqlite3.
        'USER': LLL1+'_oahpa',                      # Not used with sqlite3.
        'PASSWORD': 'smaGOGOsma',                  # Not used with sqlite3.
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

if os.uname()[1] == 'gtoahpa-01.uit.no' or os.uname()[1] == 'gtoahpa-02.uit.no':
    LOOKUP_TOOL = '/usr/local/bin/lookup'  # xfst
    HFST_LOOKUP = '/bin/hfst-lookup' # hfst
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


#COOKIE_NAME = "wordpress_logged_in_"
#SESSION_COOKIE_DOMAIN = 'oahpa.no'
#SESSION_COOKIE_DOMAIN = 'gtoahpa-01.no'
#COOKIEAUTH_ADMIN_PREFIX = '/aarjel/admin'
#SESSION_ENGINE = "django.contrib.sessions.backends.file"
#SESSION_FILE_PATH = "/tmp/"+LLL1+"_oahpa/"

# Geo
GEOIP_PATH = '/home/oahpa/'+LLL1+'_oahpa_project/'+LLL1+'_oahpa/geo/data/'
GEOIP_COUNTRY = 'GeoLite2-Country.mmdb'
GEOIP_CITY = 'GeoLite2-City.mmdb'
