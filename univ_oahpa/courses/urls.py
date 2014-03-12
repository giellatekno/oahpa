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

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^standard_login/$', login, {'template_name': 'auth/login.html'}),
    url(r'^logout/$', logout, {'template_name': 'auth/logout.html'}, name="courses_logout"),
    url(r'^login/$', cookie_login, name="courses_login"),
    url(r'^cookie_logout/$', cookie_logout),
)

from views import courses_main, instructor_student_detail, begin_course_goal

urlpatterns += patterns('univ_oahpa.courses.views',
    url(r'^(?P<uid>\d+)/$', instructor_student_detail),
    url(r'^$', courses_main, name="courses_index"),
    url(r'^goal/begin/(?P<goal_id>\d+)/$', begin_course_goal,
        name="begin_course_goal"),
)

from rest_framework import routers
from .views import UserStatsViewSet

router = routers.DefaultRouter()
router.register(r'stats', UserStatsViewSet)

urlpatterns += patterns('univ_oahpa.courses.views',
    url(r'^', include(router.urls)),
)

# vim: set ts=4 sw=4 tw=72 syntax=python :
