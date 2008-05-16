from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^oahpa/', include('oahpa.foo.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
#    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/saara/ped'}),
#    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^mgame/$', 'ped.drill.views.index'),
    (r'^quizz/$', 'ped.drill.views.quizz'),
    (r'^num/$', 'ped.drill.views.numgame'),
    (r'^qa/$', 'ped.drill.views.qagame'),
    (r'^bare/$', 'ped.drill.views.bare'),
    (r'^context/$', 'ped.drill.views.context'),                       

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
