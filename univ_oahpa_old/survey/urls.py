from django.conf.urls.defaults import *

from rest_framework import routers

from views import SurveyView, AnswerView
from views import answer, dismiss

router = routers.DefaultRouter()
router.register(r'surveys', SurveyView, base_name='surveys')
router.register(r'answer', AnswerView, base_name='answer')

urlpatterns = patterns('survey.views',
    url(r'^dismiss/$', 'dismiss'),
    url(r'^answer/$', 'answer', name="answer_survey"),
    url(r'^api/', include(router.urls)),
)
