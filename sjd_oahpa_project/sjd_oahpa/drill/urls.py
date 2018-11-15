from django.conf.urls import url, include, handler404, handler500
import views

urlpatterns = [
	url(r'^leksa/$', views.leksa_game, name="leksa"),
	url(r'^leksa/names/$', views.leksa_game, {'place': True}, name="leksa.sted"),
	url(r'^numra/$', views.num, name="numra"),
	url(r'^numra/ord/$', views.num_ord, name="numra.ord"),
	url(r'^numra/klokka/$', views.num_clock, name="numra.klokka"),
	url(r'^numra/dato/$', views.dato, name="numra.dato"),
]
