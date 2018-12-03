from django.conf.urls import *

from rest_framework import routers

from views import SurveyView, AnswerView
from views import answer, dismiss

from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')
ssv = importlib.import_module(LLL1+'_oahpa.survey.views')

router = routers.DefaultRouter()
router.register(r'surveys', SurveyView, base_name='surveys')
router.register(r'answer', AnswerView, base_name='answer')

urlpatterns = [
    url(r'^dismiss/$', ssv.dismiss),
    url(r'^answer/$', ssv.answer, name="answer_survey"),
    url(r'^api/', include(router.urls)),
]
