from django.conf.urls.defaults import *

from django.contrib.auth.views import login, logout
urlpatterns = patterns('django.contrib.auth.views',
	(r'^login/$', login, {'template_name': 'auth/login.html'}),
	(r'^logout/$', logout, {'template_name': 'auth/logout.html'}),
)

urlpatterns += patterns('oahpa.courses.views',
	(r'^$', 'courses_main'),
)

