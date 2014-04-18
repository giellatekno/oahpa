""" Authentication and Middleware for site.uit.no cookie.

Changes required to settings (will elaborate on this more later):

 * add CookieAuthMiddleware
 * add CookieAuth auth backend
 * add Cookie path
 * add settings.py COOKIE_NAME (path to root that provided the cookie, http://kursa.oahpa.no/)

 * see also: views in courses views for cookie_login and cookie_logout
"""

from urllib import urlencode

from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse

from courses.auth_views import cookie_login, cookie_logout
from courses.models import Course

__all__ = ['CookieAuthMiddleware', 'CookieAuth']

class CookieAuthMiddleware(object):
    """ Middleware that allows cookie authentication """

    def get_cookie_user(self, request):
        matching_cookies = [(c, v) for c, v in request.COOKIES.iteritems()
                                    if c.startswith(settings.COOKIE_NAME)]

        try:
            cookie_name, wp_cookie = matching_cookies[0]
            wp_username, session, session_hex = wp_cookie.split('%7C')
            cookie_uid = wp_username
        except:
            cookie_uid = False

        return cookie_uid

    def process_view(self, request, view_func, view_args, view_kwargs):
        """ If the user's session contains a cookie from WordPress, and they
        are not logged in to Oahpa, then we log them in and continue them on
        their merry way to the page they entered at. If their cookie is no
        longer present, yet they are still logged in to Oahpa, they are logged
        out, and redirected to the logout page. Exceptions are made for certain
        view functions.
        """
        from django.contrib import auth

        if view_func == cookie_login:
            return cookie_login(request, *view_args, **view_kwargs)
        elif view_func == cookie_logout:
            return cookie_logout(request, *view_args, **view_kwargs)

        cookie_user = self.get_cookie_user(request)

        # For admin pages...
        if view_func.__module__.startswith('django.contrib.admin.'):
            # ... log out if the cookie is no longer present
            if cookie_user:
                if not request.user.is_authenticated():
                    user = auth.authenticate(cookie_uid=cookie_user)
                    if user is not None:
                        auth.login(request, user)
            else:
                if request.user.is_authenticated():
                    return HttpResponseRedirect(reverse(cookie_logout))

            # Otherwise do not care.
            return None

        if cookie_user and not request.user.is_authenticated():
            user = auth.authenticate(cookie_uid=cookie_user)
            if user is not None:
                auth.login(request, user)
                # In order to ensure that auth is not terminated
                # automatically for each session that results from
                # passworded auth, set a session variable here.
                request.session['auth_method'] = 'cookie'
                return None # request
        elif not cookie_user and request.user.is_authenticated():
            method = request.session.get('auth_method')
            if method:
                if request.session['auth_method'] == 'cookie':
                    return HttpResponseRedirect(reverse(cookie_logout))



from courses.models import UserProfile
from django.contrib.auth.models import User

class CookieAuth(object):
    """ A class for authenticating by the site.uit.no cookie.

        Add this to settings.AUTHENTICATION_BACKENDS 
        
        AUTHENTICATION_BACKENDS = (
            'courses.authentication.CookieAuth',
            'django.contrib.auth.backends.ModelBackend',
        )

        See: https://docs.djangoproject.com/en/dev/topics/auth/

        Code based on CAS auth

        Summary: Django tries all available auth methods, moving on
        to the next if one fails.
    """

    def get_user(self, user_id):
        try:
            UP = UserProfile.objects.get(user__id=user_id)
            return UP.user
        except UserProfile.DoesNotExist:
            return None

    def authenticate(self, cookie_uid):
        try:
            UP = UserProfile.objects.get(user__username=cookie_uid)
            return UP.user
        except UserProfile.DoesNotExist:
            return self.create_new_user(cookie_uid)

        return None

    def create_new_user(self, cookie_uid):
        import md5
        from django.contrib.auth.models import Group

        # TODO: random md5
        password = '!^293!' + str(cookie_uid) + '!293^!'
        password = md5.md5(password).hexdigest()

        U, created = User.objects.get_or_create(username=cookie_uid)
        if created:
            U.password = password
            U.save()

        try:
            UP = U.get_profile()
        except UserProfile.DoesNotExist:
            UP = UserProfile.objects.create(user=U)
        UP.save()

        # add to default site-uit-no course
        try:
            site = Course.objects.get(identifier='site-default')
        except Course.DoesNotExist:
            # Create default course, and add root user to it
            site = Course.objects.create(
                name='kursa.oahpa.no default course',
                identifier='site-default',)
            root = User.objects.get(pk=1)
            instructor_group = Group.objects.get(name="Instructors")
            site.courserelationship_set.create(user=root,
                    relationship_type=instructor_group)
            site.save()

        student_group = Group.objects.get(name="Students")

        site.courserelationship_set.create(user=U,
                    relationship_type=student_group)
        site.save()

        return U


# vim: set ts=4 sw=4 tw=72 syntax=python :
