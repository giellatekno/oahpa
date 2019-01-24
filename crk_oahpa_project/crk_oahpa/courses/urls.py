from django.conf.urls.defaults import *

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


urlpatterns = [
	url(r'^standard_login/$', TemplateView.as_view(template_name="auth/login.html")),
	url(r'^logout/$', TemplateView.as_view(template_name="auth/logout.html")),
    url(r'^login/$', cookie_login),
	url(r'^cookie_logout/$', cookie_logout),
]

from views import courses_main, instructor_student_detail

urlpatterns += [
    url(r'^(?P<cid>\d+)/(?P<uid>\d+)/$', instructor_student_detail),
    url(r'^$', courses_main, name="courses_index"),
]
