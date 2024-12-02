import os, sys
import os.path
from settings import LLL1

from settings import URL_PREFIX


path = '/home/oahpa/'+LLL1+'_oahpa_project/'+LLL1+'_oahpa'

MEDIA_ROOT = '/home/oahpa/media'

LOCALE_PATHS = ('/home/oahpa/'+LLL1+'_oahpa_project/locale',)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k32t9e#$@%*s)7zij+8k0qzhpve^8t-i#zamww^ii-)-j8c-q-'

DEBUG = True

ALLOWED_HOSTS = ['.gtoahpa-01.uit.no','.gtoahpa-02.uit.no','127.0.0.1','localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': LLL1+'_oahpa',
        'USER': LLL1+'_oahpa',
        'PASSWORD': LLL1+'GOGO'+LLL1,
        #'HOST': 'localhost',
        #'PORT': '3040',
        #'OPTIONS': {
        # 'read_default_file': '/etc/my.cnf',
         # 'charset': 'utf8',
        # 'init_command': 'SET storage_engine=INNODB', #  ; SET table_type=INNODB',
        # }
    }
}

FILE_CHARSET = 'utf8'
DEFAULT_CHARSET = 'utf8'
DATABASE_CHARSET =  'utf8'


if os.uname()[1] == 'gtoahpa-01.uit.no' or os.uname()[1] == 'gtoahpa-02.uit.no':
    LOOKUP_TOOL = '/usr/local/bin/lookup'
    FST_DIRECTORY = '/opt/smi/'+LLL1+'/bin'
else:
    FST_DIRECTORY = '/Users/car010/main/langs/'+LLL1+'/gtoahpa_fst'
    LOOKUP_TOOL = '/usr/local/bin/lookup'

LOG_FILE = path + LLL1+'_oahpa/drill/vastaF_log.txt'


AUTH_PROFILE_MODULE = 'courses.UserProfile'
LOGIN_REDIRECT_URL = '/%s/courses/' % URL_PREFIX
LOGIN_URL = '/%s/courses/login/' % URL_PREFIX

CACHES = {
        'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': '/var/tmp/'+LLL1+'_oahpa_cache'
        },
}
