#!/usr/bin/env python
import os, sys
from django.core.wsgi import get_wsgi_application
    
sys.path.append(' /Users/tiina/main/ped/davvi_oahpa')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_wsgi_application()
