from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^oahpa/', include('oahpa.foo.urls')),
    (r'^oahpa/i18n/', include('django.conf.urls.i18n')),
#    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/saara/ped'}),
#    (r'^oahpa/admin/', include('django.contrib.admin.urls')),
    (r'^oahpa/morfa/$', 'oahpa.drill.views.mgame'),
    (r'^oahpa/leksa/$', 'oahpa.drill.views.quizz'),
    (r'^oahpa/logut/$', 'oahpa.drill.views.numgame'),
    (r'^oahpa/qa/$', 'oahpa.drill.views.qagame'), 
        

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
