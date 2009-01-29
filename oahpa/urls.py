from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^oahpa/i18n/', include('django.conf.urls.i18n')),
    (r'^oahpa/media/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': '/Users/saara/ped/oahpa/media'}),
    (r'^oahpa/dialect/$', 'oahpa.conf.views.dialect'),
    (r'^oahpa/$', 'oahpa.drill.views.oahpa'),
    (r'^visl/$', 'oahpa.drill.views.visl'),
    (r'^oahpa/morfa/$', 'oahpa.drill.views.mgame_n'),
    (r'^oahpa/morfa_s/$', 'oahpa.drill.views.mgame_n'),
    (r'^oahpa/morfa_v/$', 'oahpa.drill.views.mgame_v'),
    (r'^oahpa/morfa_a/$', 'oahpa.drill.views.mgame_a'),
    (r'^oahpa/morfa_l/$', 'oahpa.drill.views.mgame_l'),
    (r'^oahpa/cmorfa/$', 'oahpa.drill.views.cmgame_n'),
    (r'^oahpa/morfac/$', 'oahpa.drill.views.cmgame_n'),
    (r'^oahpa/morfac_s/$', 'oahpa.drill.views.cmgame_n'),
    (r'^oahpa/morfac_v/$', 'oahpa.drill.views.cmgame_v'),
    (r'^oahpa/morfac_a/$', 'oahpa.drill.views.cmgame_a'),
    (r'^oahpa/morfac_l/$', 'oahpa.drill.views.cmgame_l'),                       
    (r'^oahpa/leksa/$', 'oahpa.drill.views.quizz'),
    (r'^oahpa/leksa_n/$', 'oahpa.drill.views.quizz_n'),
    (r'^oahpa/numra/$', 'oahpa.drill.views.num'),
    (r'^oahpa/numra_ord/$', 'oahpa.drill.views.num_ord'),
    (r'^oahpa/vasta/$', 'oahpa.drill.views.vasta'),
    (r'^oahpa/sahka/$', 'oahpa.drill.views.sahka'),
    (r'^oahpa/feedback/$', 'oahpa.feedback.views.feedback'), 
        
    # Uncomment this for admin:
    (r'^oahpa/admin/(.*)', admin.site.root),
)
