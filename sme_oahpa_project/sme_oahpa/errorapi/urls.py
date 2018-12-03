from django.conf.urls import *

from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')
sev = importlib.import_module(LLL1+'_oahpa.errorapi.views')

urlpatterns = [
    url(r'^lookup/$', sev.error_feedback_view),
    url(r'^test_page/$', sev.test_page),
]

# vim: set ts=4 sw=4 tw=72 syntax=python :
