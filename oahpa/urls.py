from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^oahpa/', include('oahpa.foo.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
#    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/saara/ped'}),
#    (r'^oahpa/admin/', include('django.contrib.admin.urls')),
    (r'^oahpa/mgame/$', 'oahpa.drill.views.mgame'),
    (r'^oahpa/quizz/$', 'oahpa.drill.views.quizz'),
    (r'^oahpa/num/$', 'oahpa.drill.views.numgame'),
    (r'^oahpa/qa/$', 'oahpa.drill.views.qagame'),
    (r'^oahpa/bare/$', 'oahpa.drill.views.bare'),
    (r'^oahpa/context/$', 'oahpa.drill.views.context'),                       

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
