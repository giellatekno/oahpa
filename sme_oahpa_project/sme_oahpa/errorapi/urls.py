from django.conf.urls.defaults import *

urlpatterns = patterns('errorapi.views',
    url(r'^lookup/$', 'error_feedback_view'),
    url(r'^test_page/$', 'test_page'),
)

# vim: set ts=4 sw=4 tw=72 syntax=python :
