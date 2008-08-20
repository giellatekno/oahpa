from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^oahpa/', include('oahpa.foo.urls')),
    (r'^oahpa/i18n/', include('django.conf.urls.i18n')),
#    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/saara/ped'}),
#    (r'^oahpa/admin/', include('django.contrib.admin.urls')),
    (r'^oahpa/morfa/$', 'oahpa.drill.views.mgame_n'),
    (r'^oahpa/morfa_s/$', 'oahpa.drill.views.mgame_n'),
    (r'^oahpa/morfa_v/$', 'oahpa.drill.views.mgame_v'),
    (r'^oahpa/morfa_a/$', 'oahpa.drill.views.mgame_a'),
    (r'^oahpa/morfa_l/$', 'oahpa.drill.views.mgame_l'),
    (r'^oahpa/leksa/$', 'oahpa.drill.views.quizz'),
    (r'^oahpa/leksa_n/$', 'oahpa.drill.views.quizz_n'),
    (r'^oahpa/logut/$', 'oahpa.drill.views.numgame'),
    (r'^oahpa/numra/$', 'oahpa.drill.views.numgame'),
    (r'^oahpa/vasta/$', 'oahpa.drill.views.vasta_n'),
    (r'^oahpa/vasta_s/$', 'oahpa.drill.views.vasta_n'),
    (r'^oahpa/vasta_v/$', 'oahpa.drill.views.vasta_v'),
    (r'^oahpa/vasta_a/$', 'oahpa.drill.views.vasta_a'),
    (r'^oahpa/qa/$', 'oahpa.drill.views.qagame'), 
        

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
