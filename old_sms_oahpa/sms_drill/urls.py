from django.conf.urls.defaults import patterns, url, include, handler404, handler500
# from django.conf import settings

urlpatterns = patterns('sms_oahpa.sms_drill.views',
	# (r'^morfa/substantiv/$', 'sms_oahpa.sms_drill.views.morfa_game', {'pos': 'N'}),
	url(r'^morfas/der/$', 'morfa_game', {'pos': 'Der'}, name="morfa_s.der"),
	url(r'^morfas/derverb/$', 'morfa_game', {'pos': 'Derverb'}, name="morfa_s.derverb"),
	url(r'^morfas/v/$', 'morfa_game', {'pos': 'V'}, name="morfa_s.verb"),
	url(r'^morfas/s/$', 'morfa_game', {'pos': 'N'}),
	url(r'^morfas/s/px/$', 'morfa_game', {'pos': 'Px'}, name="morfa_s.px"),
	url(r'^morfas/a/$', 'morfa_game', {'pos': 'A'}, name="morfa_s.adj"),
	url(r'^morfas/p/$', 'morfa_game', {'pos': 'Pron'}, name="morfa_s.pron"),
	url(r'^morfas/l/$', 'morfa_game', {'pos': 'Num'}, name="morfa_s.num"),
	url(r'^morfas/$', 'morfa_game', {'pos': 'N'}, name="morfa_s.noun"),
	url(r'^morfas/s/px/$', 'morfa_game', {'pos': 'Px'}, name="morfa_s.px"),
	url(r'^leksa/$', 'leksa_game', name="leksa"),
	url(r'^leksa/names/$', 'leksa_game', {'place': True}, name="leksa.sted"),

	url(r'^numra/$', 'num', name="numra"),
	url(r'^numra/ord/$', 'num_ord', name="numra.ord"),
	url(r'^numra/klokka/$', 'num_clock', name="numra.klokka"), 
	url(r'^numra/dato/$', 'dato', name="numra.dato"), 
	# url(r'^numra_clock/medium/$', 'num_clock', {'clocktype': 'kl2'}), 
	# url(r'^numra_clock/hard/$', 'num_clock', {'clocktype': 'kl3'}), 

	# Contextual morfas
	url(r'^morfac/der/$', 'cmgame', {'pos': 'Der'}, name="morfa_c.der"),
	url(r'^morfac/s/$', 'cmgame', {'pos': 'n'}),
	url(r'^morfac/v/$', 'cmgame', {'pos': 'v'}, name="morfa_c.verb"),
	url(r'^morfac/a/$', 'cmgame', {'pos': 'a'}, name="morfa_c.adj"),
	url(r'^morfac/p/$', 'cmgame', {'pos': 'Pron'}, name="morfa_c.pron"),
	url(r'^morfac/l/$', 'cmgame', {'pos': 'Num'}, name="morfa_c.num"),                       
	url(r'^morfac/$', 'cmgame', {'pos': 'n'}, name="morfa_c.noun"),
	url(r'^vastaf/$', 'vasta', name="vasta_f"),
	url(r'^vastas/$', 'cealkka', name="vasta_s"),
	url(r'^sahka/$', 'sahka', name="sahka"),
	
)

# # These are for me testing things, otherwise ignore.
# urlpatterns += patterns('sms_oahpa.sms_drill.new_views',
# 	# (r'^new_morfa/(?P<pos>V)/$', 'sms_oahpa.sms_drill.new_views.Morfa'),
# 	# (r'^new_morfa/(?P<pos>N|S)/$', 'sms_oahpa.sms_drill.new_views.Morfa'),
# 	# (r'^new_morfa/V/$', 'Game', {'gametype': 'MORFAV'}),
# 	# (r'^new_morfa/S/$', 'Game', {'gametype': 'MORFAS'}),
# 	# (r'^new_leksa/$', 'Game', {'gametype': 'LEKSA'}),
# )


