
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

from .authentication import CookieAuthMiddleware

from django.conf import settings

class CookieAuthentication(authentication.BaseAuthentication):

    def get_session_cookie_user(self, request):
        from django.contrib.sessions.backends.db import SessionStore
        from django.contrib.sessions.models import Session

        sess_id = request.COOKIES.get('sessionid', False)

        if not sess_id:
            return None

        s = Session.objects.get(pk=sess_id)
        u_id = s.get_decoded().get('_auth_user_id', None)

        return User.objects.get(pk=u_id)

    def get_cookie_user(self, request):

        matching_cookies = [(c, v) for c, v in request.COOKIES.iteritems()
                                    if c.startswith(settings.COOKIE_NAME_STARTSWITH)]

        try:
            cookie_name, wp_cookie = matching_cookies[0]
            wp_username, session, session_hex = wp_cookie.split('%7C')
            cookie_uid = wp_username
        except:
            cookie_uid = False

        if cookie_uid:
            return User.objects.get(username=cookie_uid)

        return cookie_uid

    def authenticate(self, request):

        u = self.get_cookie_user(request)

        if not u:
            u = self.get_session_cookie_user(request)

        if not u:
            return None

        return (u, None)

