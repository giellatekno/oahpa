from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')

""" Replacement authentication decorators that work around redirection loops,
as well as the trackGrade decorator. """

try:
	from functools import wraps
except ImportError:
	from django.utils.functional import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.utils.http import urlquote

__all__ = ['login_required', 'permission_required', 'user_passes_test', 'trackGrade']

###
### Authentication decorators
###

def user_passes_test(test_func, login_url=None,
					 redirect_field_name=REDIRECT_FIELD_NAME):
	"""Replacement for django.contrib.auth.decorators.user_passes_test that
	returns 403 Forbidden if the user is already logged in.
	"""

	if not login_url:
		from django.conf import settings
		login_url = settings.LOGIN_URL

	def decorator(view_func):
		@wraps(view_func)
		def wrapper(request, *args, **kwargs):
			if test_func(request.user):
				return view_func(request, *args, **kwargs)
			elif request.user.is_authenticated():
				return HttpResponseForbidden('<h1>Permission denied</h1>')
			else:
				path = '%s?%s=%s' % (login_url, redirect_field_name,
									 urlquote(request.get_full_path()))
				return HttpResponseRedirect(path)
		return wrapper
	return decorator


def permission_required(perm, login_url=None):
	"""Replacement for django.contrib.auth.decorators.permission_required that
	returns 403 Forbidden if the user is already logged in.
	"""

	return user_passes_test(lambda u: u.has_perm(perm), login_url=login_url)


###
### Grade tracking
###


class trackGrade(object):
	""" This decorator expects that an HttpResponse has a context attribute,
	which it uses to retrieve the context. This is passed on to trackGrade.

	In order to use this import the following things

		from courses.views import render_to_response
		from courses.decorators import trackGrade

	And then decorate a view function, passing a log entry heading to the
	decorator.

		@trackGrade("Leksa")
		def leksa_game(request, place=False):
			...

	Currently the more detailed behavior of log subheadings is defined in
	courses.views.trackGrade.

	"""

	def __init__(self, log_name):
		self.log_name = log_name

	def __call__(self, view_function):
		""" This must return the HttpResponse from the original function
		"""

		def decorated_function(*args, **kwargs):
			trackGrade =  oahpa_module.courses.views.trackGrade

			# grab the request, and execute the view function as normal
			request = args[0]
			response = view_function(*args, **kwargs)

			# It may be that the view somehow doesn't have a context argument,
			# in this case we don't want to track or return anything
			try:
				context = response.context
			except:
				context = False

			if context:
				if self.log_name:
					trackGrade(self.log_name, request, context)

			return response

		return decorated_function
