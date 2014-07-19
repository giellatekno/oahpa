from django.conf.urls.defaults import *

from rest_framework import routers

from views import SurveyView

router = routers.DefaultRouter()
router.register(r'surveys', SurveyView)

urlpatterns = patterns('surveys.views',
    url(r'^test_page/$', 'test_page'),
    url(r'^$', include(router.urls)),
)
