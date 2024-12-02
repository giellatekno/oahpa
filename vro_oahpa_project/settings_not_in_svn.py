from settings import LLL1

import os
import os.path
import sys

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.gtoahpa-01.uit.no','.gtoahpa-02.uit.no','127.0.0.1','localhost']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '36^i%$$ss0f&jp6djm7co&5)wt6gvlo-p0azsg1rjib%0vf+tl'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': LLL1+'_oahpa',
        'USER': LLL1+'_oahpa',
        'PASSWORD': 'katsikveleq22',
        'HOST': '',
        'PORT': '',
        #'HOST': 'localhost',
        #'PORT': '3043',
        #'OPTIONS': {
        # 'read_default_file': '/etc/my.cnf',
         # 'charset': 'utf8',
        # 'init_command': 'SET storage_engine=INNODB', #  ; SET table_type=INNODB',
        # }
    }
}

hostname = "oahpa.no"

LOCALE_PATHS = ('/home/oahpa/'+LLL1+'_oahpa_project/locale',)

FILE_CHARSET = 'utf8'
DEFAULT_CHARSET = 'utf8'
DATABASE_CHARSET =  'utf8'


# Absolute path to the directory that holds media.
MEDIA_ROOT = '/home/oahpa/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
STATIC_URL = '/home/oahpa/admin_media/'


#if os.uname()[1] == 'victorio.uit.no':
    #LOOKUP_TOOL = '/usr/local/bin/lookup'
 #   LOOKUP_TOOL = '/opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/lookup'

if os.uname()[1] == 'gtoahpa-01.uit.no' or os.uname()[1] == 'gtoahpa-02.uit.no':
    FST_DIRECTORY = '/opt/smi/'+LLL1+'/bin/'
    #LOOKUP_TOOL = '/usr/local/bin/lookup' # xfst
    LOOKUP_TOOL = '/usr/bin/hfst-lookup' # We are using hfst now for the generation of the word forms.
    #HFST_LOOKUP_TOOL = '/usr/bin/hfst-lookup' # hfst transducers are used in Numra.
    TTS_DIR = '/home/oahpa/synthts_vr/synthts_vr'
    MEDIA_DIR = '/home/oahpa/media/'
else:
    FST_DIRECTORY = '/Users/car010/main/langs/'+LLL1+'/gtoahpa_fst'
    LOOKUP_TOOL = '/usr/local/bin/lookup'
    TTS_DIR = '/Users/car010/vrotts/synthts_vr/synthts_vr'

#APERTIUM_DIRECTORY = '/Users/mslm/apertium/incubator/apertium-rus'

#if os.uname()[1] == 'gtoahpa-01.uit.no':
#	try:
#		if VDEV:
#			from production_settings import *
#	except:
#		print "Could not load production_settings.py"
#		sys.exit()
#else:
#	INSTALLED_APPS = INSTALLED_APPS + ('django_extensions',)

# #
#
# USER PROFILES
#
# #

AUTH_PROFILE_MODULE = 'courses.UserProfile'
LOGIN_REDIRECT_URL = '/'+LLL1+'_oahpa/courses/'
LOGIN_URL = '/'+LLL1+'_oahpa/courses/login/'

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
		'LOCATION': '/var/tmp/'+LLL1+'_oahpa_cache'
	},
}
