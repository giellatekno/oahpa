# Functions for global configuration in oahpa-project.
# At the moment, only dialect settings.
from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')

settings = oahpa_module.settings

from django import http
from django.core.cache import cache

# Set the dialect for the user
def dialect(request):
    next = request.REQUEST.get('next', None)
    print next
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = http.HttpResponseRedirect(next)
    if request.method == 'POST':
        dialect = request.POST.get('dialect', None)
        if dialect:
            if hasattr(request, 'session'):
                request.session['dialect'] = dialect
            else:
                response.set_cookie(settings.DIALECT_COOKIE_NAME, dialect)
    return response
