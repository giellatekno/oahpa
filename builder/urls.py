from django.conf.urls.defaults import *

# import os, sys
# here = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), x)
# here_cross = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), *x)
# @login_required decorator

from django.contrib.auth.views import login, logout

from views import ( builder_main
                  )

from rest_framework import routers

from .api import ( WordView
                 , FormView
#                  , GoalParametersView
#                  , FeedbackLogView
#                  , CourseGoalView
#                  , NotificationsView
#                  , SubmissionView
                 )

router = routers.DefaultRouter()
router.register(r'words', WordView, base_name='words')
router.register(r'forms', FormView, base_name='forms')

urlpatterns = patterns('univ_oahpa.courses.views',
    url(r'^api/', include(router.urls)),

    url(r'^$', builder_main),
)

# vim: set ts=4 sw=4 tw=72 syntax=python :
