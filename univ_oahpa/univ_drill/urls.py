from django.conf.urls.defaults import patterns, url, include, handler404, handler500
# from django.conf import settings

urlpatterns = patterns('univ_oahpa.univ_drill.views',
	# (r'^morfa/substantiv/$', 'smaoahpa.smadrill.views.morfa_game', {'pos': 'N'}),
	url(r'^morfa/baakoe/v/$', 'morfa_game', {'pos': 'V'}, name="morfa_s.verb"),
	url(r'^morfa/baakoe/s/$', 'morfa_game', {'pos': 'N'}),
	url(r'^morfa/baakoe/a/$', 'morfa_game', {'pos': 'A'}, name="morfa_s.adj"),
	url(r'^morfa/baakoe/p/$', 'morfa_game', {'pos': 'Pron'}, name="morfa_s.pron"),
	url(r'^morfa/baakoe/$', 'morfa_game', {'pos': 'N'}, name="morfa_s.noun"),
	
	url(r'^leksa/$', 'leksa_game', name="leksa"),
	url(r'^leksa/sted/$', 'leksa_game', {'place': True}, name="leksa.sted"),

	url(r'^numra/$', 'num', name="numra"),
	url(r'^numra/ord/$', 'num_ord', name="numra.ord"),
	url(r'^numra/klokka/$', 'num_clock', name="numra.klokka"), 
	url(r'^numra/dato/$', 'dato', name="numra.dato"), 
	# url(r'^numra_clock/medium/$', 'num_clock', {'clocktype': 'kl2'}), 
	# url(r'^numra_clock/hard/$', 'num_clock', {'clocktype': 'kl3'}), 

	# Contextual morfas
	url(r'^morfa/raajese/s/$', 'cmgame', {'pos': 'n'}),
	url(r'^morfa/raajese/v/$', 'cmgame', {'pos': 'v'}, name="morfa_c.verb"),
	url(r'^morfa/raajese/a/$', 'cmgame', {'pos': 'a'}, name="morfa_c.adj"),
	url(r'^morfa/raajese/p/$', 'cmgame', {'pos': 'Pron'}, name="morfa_c.pron"),                       
	url(r'^morfa/raajese/$', 'cmgame', {'pos': 'n'}, name="morfa_c.noun"),
)

# # These are for me testing things, otherwise ignore.
# urlpatterns += patterns('smaoahpa.smadrill.new_views',
# 	# (r'^new_morfa/(?P<pos>V)/$', 'smaoahpa.smadrill.new_views.Morfa'),
# 	# (r'^new_morfa/(?P<pos>N|S)/$', 'smaoahpa.smadrill.new_views.Morfa'),
# 	# (r'^new_morfa/V/$', 'Game', {'gametype': 'MORFAV'}),
# 	# (r'^new_morfa/S/$', 'Game', {'gametype': 'MORFAS'}),
# 	# (r'^new_leksa/$', 'Game', {'gametype': 'LEKSA'}),
# )


