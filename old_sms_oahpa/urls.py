import os, sys

#from django.conf.urls import url, include
from django.conf.urls import url, include, handler404, handler500
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from sms_drill import views
from sms_drill.views import index

here = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), x)
here_cross = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), *x)

admin.autodiscover()
admin.site.login = login_required(admin.site.login)

from settings import URL_PREFIX as prefix

admin_url = r'^%s/admin/' % prefix

urlpatterns =  [
	# Example:
	# (r'^sms_oahpa/', include('sms_oahpa.foo.urls')),
	#url(r'^%s/$' % prefix, 'sms_oahpa.sms_drill.views.sms_oahpa'),
        #url(r'^s/$' % prefix, index, name='index'),
        url(r'^nuorti/$', views.index, name='index'),
        url(r'^%s/i18n/' % prefix, include('django.conf.urls.i18n')),
	#url(r'^%s/media/(?P<path>.*)$' % prefix, 'django.views.static.serve',
        #       		      	{'document_root': settings.MEDIA_ROOT}),
	#url(r'^%s/courses/' % prefix, include('courses.urls')),
	#url(r'^%s/' % prefix, include('sms_oahpa.sms_drill.urls')),
	#url(r'^%s/dialect/$' % prefix, 'sms_oahpa.conf.views.dialect'),
        #url(admin_url, include(admin.site.urls)),
	#url(admin_url, admin.site.root),
	#(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]



# urlpatterns += patterns(''
#	 (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': here('m')}),
# )

