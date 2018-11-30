from django.conf.urls import url, include, handler404, handler500
import views

# from django.conf import settings

urlpatterns = [
	# (r'^morfa/substantiv/$', 'smaoahpa.smadrill.views.morfa_game', {'pos': 'N'}),
	url(r'^morfas/der/$', views.morfa_game, {'pos': 'Der'}, name="morfa_s.der"),
	url(r'^morfas/v/$', views.morfa_game, {'pos': 'V'}, name="morfa_s.verb"),
	url(r'^morfas/s/$', views.morfa_game, {'pos': 'N'}),
	url(r'^morfas/s/px/$', views.morfa_game, {'pos': 'Px'}, name="morfa_s.px"),
	url(r'^morfas/a/$', views.morfa_game, {'pos': 'A'}, name="morfa_s.adj"),
	url(r'^morfas/p/$', views.morfa_game, {'pos': 'Pron'}, name="morfa_s.pron"),
	url(r'^morfas/l/$', views.morfa_game, {'pos': 'Num'}, name="morfa_s.num"),
	url(r'^morfas/$', views.morfa_game, {'pos': 'N'}, name="morfa_s.noun"),

	url(r'^leksa/$', views.leksa_game, name="leksa"),
	url(r'^leksa/names/$', views.leksa_game, {'place': True}, name="leksa.sted"),

	url(r'^numra/$', views.num, name="numra"),
	url(r'^numra/ord/$', views.num_ord, name="numra.ord"),
	url(r'^numra/klokka/$', views.num_clock, name="numra.klokka"),
	url(r'^numra/dato/$', views.dato, name="numra.dato"),
	# url(r'^numra_clock/medium/$', 'num_clock', {'clocktype': 'kl2'}),
	# url(r'^numra_clock/hard/$', 'num_clock', {'clocktype': 'kl3'}),

	# Contextual morfas
	url(r'^morfac/s/px/$', views.cmgame, {'pos': 'Px'}, name="morfa_c.px"),
	url(r'^morfac/der/$', views.cmgame, {'pos': 'Der'}, name="morfa_c.der"),
	url(r'^morfac/s/$', views.cmgame, {'pos': 'n'}),
	url(r'^morfac/v/$', views.cmgame, {'pos': 'v'}, name="morfa_c.verb"),
	url(r'^morfac/a/$', views.cmgame, {'pos': 'a'}, name="morfa_c.adj"),
	url(r'^morfac/p/$', views.cmgame, {'pos': 'Pron'}, name="morfa_c.pron"),
	url(r'^morfac/l/$', views.cmgame, {'pos': 'Num'}, name="morfa_c.num"),
	url(r'^morfac/$', views.cmgame, {'pos': 'n'}, name="morfa_c.noun"),
	url(r'^vastaf/$', views.vasta, name="vasta_f"),
	url(r'^vastas/$', views.cealkka, name="vasta_s"),
	url(r'^sahka/$', views.sahka, name="sahka"),
]

# # These are for me testing things, otherwise ignore.
# urlpatterns += patterns('smaoahpa.smadrill.new_views',
# 	# (r'^new_morfa/(?P<pos>V)/$', 'smaoahpa.smadrill.new_views.Morfa'),
# 	# (r'^new_morfa/(?P<pos>N|S)/$', 'smaoahpa.smadrill.new_views.Morfa'),
# 	# (r'^new_morfa/V/$', 'Game', {'gametype': 'MORFAV'}),
# 	# (r'^new_morfa/S/$', 'Game', {'gametype': 'MORFAS'}),
# 	# (r'^new_leksa/$', 'Game', {'gametype': 'LEKSA'}),
# )
