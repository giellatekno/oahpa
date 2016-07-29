from django.conf.urls import *

urlpatterns = patterns(
    '',
    ('^$', 'djopenid.views.index'),
    ('^consumer/', include('djopenid.consumer.urls')),
    ('^server/', include('djopenid.server.urls')),
)
