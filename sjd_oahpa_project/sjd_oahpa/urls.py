"""LLL1_oahpa URL Configuration

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
from django.conf.urls import url
from django.contrib import admin

from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf.urls import i18n

from settings import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')
sdv = importlib.import_module(LLL1+'_oahpa.drill.views')
scv = importlib.import_module(LLL1+'_oahpa.conf.views')

prefix = oahpa_module.settings.URL_PREFIX
MEDIA_ROOT = oahpa_module.settings.MEDIA_ROOT

admin_url = r'^%s/admin/' % prefix

urlpatterns = [
    url(r'^%s/$' % prefix, sdv.index, name='index'),
    url(r'^%s/i18n/' % prefix, include('django.conf.urls.i18n')),
    url(r'^%s/' % prefix, include(LLL1+'_oahpa.drill.urls')),
    url(r'^%s/courses/' % prefix, include(LLL1+'_oahpa.courses.urls')),
    url(r'^%s/media/(?P<path>.*)$' % prefix, serve, {'document_root': MEDIA_ROOT}),
    url(r'^%s/dialect/$' % prefix, scv.dialect),
    url(admin_url, admin.site.urls),
]
