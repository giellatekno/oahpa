import os, sys

## sys.path = []
## # sys.path.append('/usr/lib/python2.6/site-packages/django')
sys.path.append('/home/mdf_oahpa/mdf_oahpa')
sys.path.append('/home/mdf_oahpa')

## import django ## ## 
## 
## fpath = open('/home/mdf_oahpa/mdf_oahpa/apache/pathtest', 'w')
## print >> fpath, [a + '\n' for a in sys.path]
## print >> fpath, django.VERSION
## print >> fpath, 'tmp'
## print >> fpath, 'tmp2'
## fpath.close()

os.environ['DJANGO_SETTINGS_MODULE'] = 'mdf_oahpa.settings'

from django.core.handlers import wsgi # import django.core.handlers.wsgi

application = wsgi.WSGIHandler()
