from django.conf.urls.defaults import *

from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'lookup', LookupView)

urlpatterns += patterns('errorapi.views',
    url(r'^test/$', test_page),
    url(r'^$', include(router.urls)),
)

# vim: set ts=4 sw=4 tw=72 syntax=python :
