from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404

from django.conf import settings
from .models import Goal, UserGoalInstance
from .views import render_to_response

from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')

URL_PREFIX = oahpa_module.settings.URL_PREFIX

def split_login(request):

    next_page = request.GET.get('next', False)

    if not next_page:
        # TODO: change next url for deep links
        next_page = '/%s/courses/' % URL_PREFIX

    c = {}
    c['next_page'] = next_page

    template = 'split_login.html'
    return render_to_response(template,
                              c,
                              context_instance=RequestContext(request))

def cookie_login(request, next_page=None, required=False, **kwargs):
    """ Check for existing site.uit.no cookie
    """
    from django.conf import settings
    from django.contrib import auth

    if not next_page:
        # TODO: change next url for deep links
        next_page = '/%s/courses/' % URL_PREFIX
    if request.user.is_authenticated():
        message = "You are logged in as %s." % request.user.username
        # request.user.message_set.create(message=message)
        return HttpResponseRedirect(next_page)

    matching_cookies = [(c, v) for c, v in request.COOKIES.iteritems()
                                if c.startswith(settings.COOKIE_NAME_STARTSWITH)]

    try:
        cookie_name, wp_cookie = matching_cookies[0]
        wp_username, session, session_hex = wp_cookie.split('%7C')
        cookie_uid = wp_username
    except:
        cookie_uid = False

    if cookie_uid:
        user = auth.authenticate(cookie_uid=cookie_uid)
        if user is not None:
            auth.login(request, user)
            name = user.username
            message = "Login succeeded. Welcome, %s." % name
            # user.message_set.create(message=message)
            return HttpResponseRedirect(next_page)
        # elif settings.CAS_RETRY_LOGIN or required:
            # return HttpResponseRedirect(_login_url(service))
        else:
            error = "<h1>Forbidden</h1><p>Login failed.</p>"
            return HttpResponseForbidden(error)
    else:
        return HttpResponseRedirect('/%s/courses/standard_login/' % URL_PREFIX)
        # TODO: check

def cookie_logout(request, next_page=None, **kwargs):
    """
    """

    from django.contrib.auth import logout

    try:
        del request.session['auth_source']
    except:
        pass

    logout(request)

    # TODO: redirect to kursa logout link

    # This can't redirect to cookie_logout, or else there are unlimited
    # redirects.

    if not next_page:
        next_page = '/%s/courses/logout/' % URL_PREFIX

    return HttpResponseRedirect(next_page)
