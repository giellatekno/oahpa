from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    (r'^nu_oahpa/i18n/', include('django.conf.urls.i18n')),
    (r'^nu_oahpa/media/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': '/home/nu_oahpa/nu_oahpa/media'}),
    (r'^nu_oahpa/dialect/$', 'nu_oahpa.conf.views.dialect'),
    (r'^nu_oahpa/$', 'nu_oahpa.nu_drill.views.oahpa'),
    (r'^nu_oahpa/visl/$', 'nu_oahpa.nu_drill.views.visl'),
    (r'^nu_oahpa/morfa/$', 'nu_oahpa.nu_drill.views.mgame_n'),
    (r'^nu_oahpa/morfa_s/$', 'nu_oahpa.nu_drill.views.mgame_n'),
    (r'^nu_oahpa/morfa_v/$', 'nu_oahpa.nu_drill.views.mgame_v'),
    (r'^nu_oahpa/morfa_a/$', 'nu_oahpa.nu_drill.views.mgame_a'),
    (r'^nu_oahpa/morfa_l/$', 'nu_oahpa.nu_drill.views.mgame_l'),
    (r'^nu_oahpa/cmorfa/$', 'nu_oahpa.nu_drill.views.cmgame_n'),
    (r'^nu_oahpa/morfac/$', 'nu_oahpa.nu_drill.views.cmgame_n'),
    (r'^nu_oahpa/morfac_s/$', 'nu_oahpa.nu_drill.views.cmgame_n'),
    (r'^nu_oahpa/morfac_v/$', 'nu_oahpa.nu_drill.views.cmgame_v'),
    (r'^nu_oahpa/morfac_a/$', 'nu_oahpa.nu_drill.views.cmgame_a'),
    (r'^nu_oahpa/morfac_l/$', 'nu_oahpa.nu_drill.views.cmgame_l'),                       
    (r'^nu_oahpa/leksa/$', 'nu_oahpa.nu_drill.views.quizz'),
    (r'^nu_oahpa/leksa_n/$', 'nu_oahpa.nu_drill.views.quizz_n'),
    (r'^nu_oahpa/numra/$', 'nu_oahpa.nu_drill.views.num'),
    (r'^nu_oahpa/numra_ord/$', 'nu_oahpa.nu_drill.views.num_ord'),
    (r'^nu_oahpa/vasta/$', 'nu_oahpa.nu_drill.views.vasta'),
    (r'^nu_oahpa/sahka/$', 'nu_oahpa.nu_drill.views.sahka'),
    (r'^nu_oahpa/nu_feedback/$', 'nu_oahpa.nu_feedback.views.feedback'), 
        
    # Uncomment this for admin:
    (r'^nu_oahpa/admin/(.*)', admin.site.root),
    (r'^nu_oahpa/nu_courses/', include('nu_oahpa.nu_courses.urls')),
)
