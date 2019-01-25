"""
WSGI config for LLL1_OAHPA project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from settings import LLL1

os.environ.setdefault("DJANGO_SETTINGS_MODULE", LLL1+"_oahpa.settings")

application = get_wsgi_application()
