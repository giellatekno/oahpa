from django.conf.urls.defaults import patterns, url, include, handler404, handler500
from django.conf import settings

import os, sys
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), x)
here_cross = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), *x)


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from settings import URL_PREFIX as prefix

admin_url = r'^%s/admin/' % prefix

urlpatterns = patterns('',
	# Example:
	# (r'^univ_oahpa/', include('univ_oahpa.foo.urls')),
	url(r'^%s/$' % prefix, 'univ_oahpa.univ_drill.views.index'),
	url(r'^%s/i18n/' % prefix, include('django.conf.urls.i18n')),
	url(r'^%s/media/(?P<path>.*)$' % prefix, 'django.views.static.serve',
		      	{'document_root': settings.MEDIA_ROOT}),
	url(r'^%s/courses/' % prefix, include('univ_oahpa.courses.urls')),
	url(r'^%s/' % prefix, include('univ_oahpa.univ_drill.urls')),
	url(r'^%s/dialect/$' % prefix, 'univ_oahpa.conf.views.dialect'),
	url(admin_url, include(admin.site.urls)),
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

from django.http import HttpResponseRedirect

from django_openid.provider import Provider
from django.shortcuts import render_to_response as render

class AnonProvider(Provider):
    def user_is_logged_in(self, *args):
        return True
    
    def user_owns_openid(self, *args):
        return True
    
    def user_trusts_root(self, *args):
        return True

def openid_page(request, slug):
    return render('openid_page.html', {
        'slug': slug,
        'full_url': request.build_absolute_uri(),
        'server_url': request.build_absolute_uri('%s/u/' % prefix),
    })

urlpatterns += patterns('',
    (r'^%s/openid/$' % prefix, lambda r: HttpResponseRedirect('/openid/')),
    (r'^%s/u/(\w+)/$' % prefix, openid_page),
    (r'^%s/u/$' % prefix, AnonProvider()),
)



# urlpatterns += patterns(''
#	 (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': here('m')}),
# )

