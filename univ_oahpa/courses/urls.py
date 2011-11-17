from django.conf.urls.defaults import *

# import os, sys
# here = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), x)
# here_cross = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), *x)
# @login_required decorator

from django.contrib.auth.views import login, logout
urlpatterns = patterns('django.contrib.auth.views',
	(r'^login/$', login, {'template_name': 'auth/login.html'}),
	(r'^logout/$', logout, {'template_name': 'auth/logout.html'}),
)

from courses.views import courses_main

urlpatterns += patterns('univ_oahpa.courses.views',
	(r'^$', courses_main),
)

