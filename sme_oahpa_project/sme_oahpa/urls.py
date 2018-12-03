"""sme_oahpa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf.urls import i18n

from settings import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')
sdv = importlib.import_module(LLL1+'_oahpa.drill.views')
scv = importlib.import_module(LLL1+'_oahpa.conf.views')
sav = importlib.import_module(LLL1+'_oahpa.courses.auth_views')

from django.views.generic import RedirectView

prefix = oahpa_module.settings.URL_PREFIX
MEDIA_ROOT = oahpa_module.settings.MEDIA_ROOT

admin_url = r'^%s/admin/' % prefix

urlpatterns = [
    url(r'^davvi/$', sdv.index),
    url(r'^%s/i18n/' % prefix, include('django.conf.urls.i18n')),
    url(r'^davvi/', include(LLL1+'_oahpa.drill.urls')),
    url(r'^davvi/courses/', include(LLL1+'_oahpa.courses.urls')),
    url(r'^%s/survey/' % prefix, include(LLL1+'_oahpa.survey.urls')),
    url(r'^%s/errorapi/' % prefix, include(LLL1+'_oahpa.errorapi.urls')),
    #url(r'^%s/messages/' % prefix, include('django_messages.urls')),
    url(r'^%s/accounts/login/$' % prefix, sav.cookie_login),
    url(r'^%s/media/(?P<path>.*)$' % prefix, serve, {'document_root': MEDIA_ROOT}),
    url(r'^%s/dialect/$' % prefix, scv.dialect),
    #url(r'^%s/favicon\.ico$' % prefix,
    #    'django.views.generic.simple.redirect_to',
    #    {'url': '/%s/media/images/favicon_16x16.ico' % prefix}),
    url(r'^%s/favicon\.ico$' % prefix, RedirectView.as_view(url='/%s/media/images/favicon_16x16.ico')),
    url(r'^admin/', admin.site.urls),
]
