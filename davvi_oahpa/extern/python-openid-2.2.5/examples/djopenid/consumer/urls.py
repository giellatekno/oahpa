
from django.conf.urls import *

urlpatterns = patterns(
    'djopenid.consumer.views',
    (r'^$', 'startOpenID'),
    (r'^finish/$', 'finishOpenID'),
    (r'^xrds/$', 'rpXRDS'),
)
