from django.conf.urls import url, include, handler404, handler500
import views

urlpatterns = [
	url(r'^morfa/baakoe/v/$', views.morfa_game, {'pos': 'V'}, name="morfa_s.verb"),
	url(r'^morfa/baakoe/s/$', views.morfa_game, {'pos': 'N'}),
	url(r'^morfa/baakoe/a/$', views.morfa_game, {'pos': 'A'}, name="morfa_s.adj"),
	url(r'^morfa/baakoe/p/$', views.morfa_game, {'pos': 'Pron'}, name="morfa_s.pron"),
	url(r'^morfa/baakoe/$', views.morfa_game, {'pos': 'N'}, name="morfa_s.noun"),
	url(r'^leksa/$', views.leksa_game, name="leksa"),
	url(r'^leksa/sted/$', views.leksa_game, {'place': True}, name="leksa.sted"),
	url(r'^numra/$', views.num, name="numra"),
	url(r'^numra/ord/$', views.num_ord, name="numra.ord"),
	url(r'^numra/klokka/$', views.num_clock, name="numra.klokka"),
	url(r'^numra/dato/$', views.dato, name="numra.dato"),
	# Contextual morfas
	url(r'^morfa/raajese/s/$', views.cmgame, {'pos': 'n'}),
	url(r'^morfa/raajese/v/$', views.cmgame, {'pos': 'v'}, name="morfa_c.verb"),
	url(r'^morfa/raajese/a/$', views.cmgame, {'pos': 'a'}, name="morfa_c.adj"),
	url(r'^morfa/raajese/p/$', views.cmgame, {'pos': 'Pron'}, name="morfa_c.pron"),
	url(r'^morfa/raajese/$', views.cmgame, {'pos': 'n'}, name="morfa_c.noun"),
]
