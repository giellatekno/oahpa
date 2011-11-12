from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.conf import settings

import os, sys
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), x)
here_cross = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), *x)


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from settings import URL_PREFIX as prefix

if settings.DEV:
	admin_url = r'^admin/(.*)'
else:
	admin_url = r'^%s/admin/(.*)' % prefix

urlpatterns = patterns('',
	# Example:
	# (r'^smaoahpa/', include('smaoahpa.foo.urls')),
	url(r'^%s/$' % prefix, 'smaoahpa.smadrill.views.smaoahpa'),
	url(r'^%s/i18n/' % prefix, include('django.conf.urls.i18n')),
	url(r'^%s/media/(?P<path>.*)$' % prefix, 'django.views.static.serve',
		      	{'document_root': settings.MEDIA_ROOT}),
	url(r'^%s/courses/' % prefix, include('smaoahpa.courses.urls')),
	url(r'^%s/' % prefix, include('smaoahpa.smadrill.urls')),
	url(r'^%s/dialect/$' % prefix, 'smaoahpa.conf.views.dialect'),
	url(admin_url, admin.site.root),
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)



# urlpatterns += patterns(''
#	 (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': here('m')}),
# )

