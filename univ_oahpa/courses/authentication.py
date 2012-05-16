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

from courses.views import cookie_login, cookie_logout
from courses.models import Course

__all__ = ['CookieAuthMiddleware', 'CookieAuth']

class CookieAuthMiddleware(object):
	""" Middleware that allows cookie authentication """

	def process_view(self, request, view_func, view_args, view_kwargs):
		"""Forwards unauthenticated requests to the admin page to the cookie
		login URL, as well as calls to django.contrib.auth.views.login and
		logout.
		"""
		if view_func == cookie_login:
			return cookie_login(request, *view_args, **view_kwargs)
		elif view_func == cookie_logout:
			return cookie_logout(request, *view_args, **view_kwargs)

		# TODO: this is now different
		print settings.COOKIE_NAME
		print request.path
		if settings.COOKIE_NAME:
			if not request.path.startswith(settings.COOKIE_NAME):
				return None
		elif not view_func.__module__.startswith('django.contrib.admin.'):
			return None

		if request.user.is_authenticated():
			if request.user.is_staff:
				return None
			else:
				error = ('<h1>Forbidden</h1><p>You do not have staff '
						 'privileges.</p>')
				return HttpResponseForbidden(error)

		params = urlencode({REDIRECT_FIELD_NAME: request.get_full_path()})
		return HttpResponseRedirect(reverse(cookie_login) + '?' + params)


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
		# TODO: rename
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


