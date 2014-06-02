from django.conf.urls.defaults import *

# import os, sys
# here = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), x)
# here_cross = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), *x)
# @login_required decorator

from django.contrib.auth.views import login, logout
from courses.auth_views import cookie_login, cookie_logout, split_login

# Have to rename login/ to standard_login/ so that the cookie login falls back
# to standard login without unlimited redirects.  users who go to login/ and do
# not have the cookie, will be redirected here, users with the cookie will end
# up being logged in.

urlpatterns = patterns('django.contrib.auth.views',
    url(r'^standard_login/$', login, {'template_name': 'auth/login.html'}, name="standard_login"),
    url(r'^logout/$', logout, {'template_name': 'auth/logout.html'}, name="courses_logout"),
    url(r'^login/$', split_login, name="courses_login"),
    url(r'^cookie_login/$', cookie_login, name="cookie_login"),
    url(r'^cookie_logout/$', cookie_logout),
)

from views import ( courses_main
                  , instructor_student_detail
                  , begin_course_task
                  , courses_goal_construction
                  , course_invite
                  , courses_stats
                  , goal_history
                  , courses_coursegoal_construction
                  , courses_coursegoal_sub_goal_add
                  , course_enroll
                  , recipient_search
                  , personal_goals
                  )

from rest_framework import routers

from .data_api import ( UserStatsViewSet
                      , GoalParametersView
                      , FeedbackLogView
                      , CourseGoalView
                      , NotificationsView
                      )

router = routers.DefaultRouter()
router.register(r'stats', UserStatsViewSet)
router.register(r'goals', GoalParametersView, base_name='params')
router.register(r'coursegoals', CourseGoalView, base_name='coursegoals')
router.register(r'notifications', NotificationsView, base_name='notifications')
router.register(r'feedback', FeedbackLogView)

urlpatterns += patterns('univ_oahpa.courses.views',
    url(r'^goal/history/(?P<goal_id>\d+)/(?P<user_id>\d+)/$', goal_history,
        name="goal_history"),
    url(r'^goal/history/(?P<goal_id>\d+)/$', goal_history,
        name="goal_history"),
    url(r'^goal/begin/(?P<task_id>\d+)/$', begin_course_task,
        name="begin_course_task"),
    url(r'^create/coursegoal/add/goal/$', courses_coursegoal_sub_goal_add,
        name="courses_coursegoal_sub_goal_add"),
    url(r'^create/coursegoal/$', courses_coursegoal_construction,
        name="courses_coursegoal_construction"),
    url(r'^create/goal/$', courses_goal_construction,
        name="courses_goal_construction"),

    url(r'^personal_goals/$', personal_goals, name="personal_goals"),

    url(r'^invite/$', course_invite, name="course_invite"),
    url(r'^enroll/$', course_enroll, name="course_enroll"),
    url(r'^stats/$', courses_stats, name="courses_stats"),

    url(r'^api/', include(router.urls)),

    url(r'^(?P<cid>\d+)/(?P<uid>\d+)/$', instructor_student_detail),
    url(r'^$', courses_main, name="courses_index"),

    url(r"^recipient-search/$", recipient_search, name="recipient_search"),
)

# vim: set ts=4 sw=4 tw=72 syntax=python :
