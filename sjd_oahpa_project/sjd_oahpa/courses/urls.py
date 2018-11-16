from django.conf.urls import *

# import os, sys
# here = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), x)
# here_cross = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), *x)
# @login_required decorator

from django.contrib.auth.views import login, logout
from courses.views import cookie_login, cookie_logout

# Have to rename login/ to standard_login/ so that the cookie login falls back
# to standard login without unlimited redirects.  users who go to login/ and do
# not have the cookie, will be redirected here, users with the cookie will end
# up being logged in.

urlpatterns = patterns('django.contrib.auth.views',
	(r'^standard_login/$', login, {'template_name': 'auth/login.html'}),
	(r'^logout/$', logout, {'template_name': 'auth/logout.html'}),
	(r'^login/$', cookie_login),
	(r'^cookie_logout/$', cookie_logout),
)

from views import courses_main, instructor_student_detail

urlpatterns += patterns('sjd_oahpa.courses.views',
	(r'^(?P<uid>\d+)/$', instructor_student_detail),
	(r'^$', courses_main),
)
