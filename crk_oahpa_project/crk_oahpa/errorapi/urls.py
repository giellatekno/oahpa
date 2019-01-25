from django.conf.urls import *

urlpatterns = [
    url(r'^lookup/$', 'views.error_feedback_view'),
    url(r'^test_page/$', 'views.test_page'),
]

# vim: set ts=4 sw=4 tw=72 syntax=python :
