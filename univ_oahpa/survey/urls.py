from django.conf.urls.defaults import *

from rest_framework import routers

from views import SurveyView, AnswerView
from views import answer

router = routers.DefaultRouter()
router.register(r'surveys', SurveyView, base_name='surveys')
router.register(r'answer', AnswerView, base_name='answer')

urlpatterns = patterns('survey.views',
    url(r'^answer/$', 'answer'),
    url(r'^api/', include(router.urls)),
)
