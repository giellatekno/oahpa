# Functions for global configuration in oahpa-project.
# At the moment, only dialect settings.
from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')

from django import http
from django.core.cache import cache

settings = oahpa_module.settings
URL_PREFIX = settings.URL_PREFIX

from django.shortcuts import redirect

# Set the dialect for the user
def dialect(request):
    next = request.GET.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    print 'next=', next
    response = http.HttpResponseRedirect(next)
    if request.method == 'POST':
        dialect = request.POST.get('dialect', None)
        if dialect:
            if hasattr(request, 'session'):
                request.session['dialect'] = dialect
            else:
                response.set_cookie(settings.DIALECT_COOKIE_NAME, dialect)
    return response

def set_mobile(request):
	next = request.META.get('HTTP_REFERER', None)
	if not next:
		next = '/' + URL_PREFIX + '/'
	request.session['is_mobile'] = True
	return redirect(next)

def leave_mobile(request):
	next = request.META.get('HTTP_REFERER', None)
	if not next:
		next = '/' + URL_PREFIX + '/'
	try:
		request.session.pop('is_mobile')
	except KeyError:
		pass
	return redirect(next)
