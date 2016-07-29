import os, sys

from django.conf.urls import patterns, url, include, handler404, handler500
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings

here = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), x)
here_cross = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), *x)

admin.autodiscover()
admin.site.login = login_required(admin.site.login)

from settings import URL_PREFIX as prefix

admin_url = r'^%s/admin/' % prefix

urlpatterns = patterns('',
    # Example:
    # (r'^davvi_oahpa/', include('davvi_oahpa.foo.urls')),
    url(r'^%s/$' % prefix, 'davvi_drill.views.index'),
    url(r'^%s/i18n/' % prefix, include('django.conf.urls.i18n')),
    url(r'^%s/media/(?P<path>.*)$' % prefix, 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
    url(r'^%s/courses/' % prefix, include('courses.urls')),
    url(r'^%s/survey/' % prefix, include('survey.urls')),
    url(r'^%s/errorapi/' % prefix, include('errorapi.urls')),
    url(r'^%s/' % prefix, include('davvi_drill.urls')),
    url(r'^%s/dialect/$' % prefix, 'conf.views.dialect'),
    url(admin_url, include(admin.site.urls)),
    url(r'^%s/messages/' % prefix, include('django_messages.urls')),
    url(r'^%s/accounts/login/$' % prefix, 'courses.auth_views.cookie_login'),
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # url(r'^%s/openid/' % prefix, include('openid_provider.urls')),
    #url(r'^%s/favicon\.ico$' % prefix, 
    #        'django.views.generic.simple.redirect_to', 
    #        {'url': '/%s/media/images/favicon_16x16.ico' % prefix})
)

"""
urlpatterns = patterns('',
    # Example:
    # (r'^davvi_oahpa/', include('davvi_oahpa.foo.urls')),
    url(r'^%s/$' % prefix, 'davvi_oahpa.davvi_drill.views.index'),
    url(r'^%s/i18n/' % prefix, include('django.conf.urls.i18n')),
    url(r'^%s/media/(?P<path>.*)$' % prefix, 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
    url(r'^%s/courses/' % prefix, include('davvi_oahpa.courses.urls')),
    url(r'^%s/survey/' % prefix, include('davvi_oahpa.survey.urls')),
    url(r'^%s/errorapi/' % prefix, include('davvi_oahpa.errorapi.urls')),
    url(r'^%s/' % prefix, include('davvi_oahpa.davvi_drill.urls')),
    url(r'^%s/dialect/$' % prefix, 'davvi_oahpa.conf.views.dialect'),
    url(admin_url, include(admin.site.urls)),
    url(r'^%s/messages/' % prefix, include('django_messages.urls')),
    url(r'^%s/accounts/login/$' % prefix, 'courses.auth_views.cookie_login'),
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # url(r'^%s/openid/' % prefix, include('openid_provider.urls')),
    url(r'^%s/favicon\.ico$' % prefix, 
            'django.views.generic.simple.redirect_to', 
            {'url': '/%s/media/images/favicon_16x16.ico' % prefix})
)
"""

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^%s/static/(?P<path>.*)$' % prefix, 'serve'),
    )

