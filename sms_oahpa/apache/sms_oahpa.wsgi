import os, sys

## sys.path = []
## # sys.path.append('/usr/lib/python2.6/site-packages/django')
sys.path.append('/home/sms_oahpa/sms_oahpa')
sys.path.append('/home/sms_oahpa')

## import django ## ## 
## 
## fpath = open('/home/sms_oahpa/sms_oahpa/apache/pathtest', 'w')
## print >> fpath, [a + '\n' for a in sys.path]
## print >> fpath, django.VERSION
## print >> fpath, 'tmp'
## print >> fpath, 'tmp2'
## fpath.close()

os.environ['DJANGO_SETTINGS_MODULE'] = 'sms_oahpa.settings'

from django.core.handlers import wsgi # import django.core.handlers.wsgi

application = wsgi.WSGIHandler()
