"""Replacement authentication decorators that work around redirection loops"""

try:
	from functools import wraps
except ImportError:
	from django.utils.functional import wraps

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.utils.http import urlquote

__all__ = ['login_required', 'permission_required', 'user_passes_test']

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

class trackGrade(object):
	""" This decorator expects that an HttpResponse has a context attribute,
	which it uses to retrieve the context. This is passed on to trackGrade.

	In order to use this, views_to_names must be defined on the decorator, as a
	dictionary with the decorated function name as the key, and the fancy log
	name as the value.

	It is probably easiest to define this in the view file that trackGrade is
	imported into:

		from courses.views import render_to_response
		from courses.views import trackGrade

		trackGrade.views_to_names = {
			# view function name: fancy log name
			'leksa_game': 'Leksa',

			'morfa_game': 'Morfa',

			'num': 'Numra cardinal',
		}

	This decorator also relies on a special render_to_response method, imported
	from courses.views. This method simply returns the response as normal, but
	includes a context attribute that is needed to track the grade.



	"""

	views_to_names = {
		'num': 'Numra',
		'num_ord': 'Numra ordinal',
		# etc...

	}

	def __init__(self, function):
		self.view_func = function
	
	def __call__(self, *args, **kwargs):
		""" This must return the HttpResponse from the original function
		"""

		from univ_oahpa.courses.views import trackGrade

		# grab the request, and execute the view function as normal
		request = args[0]
		response = self.view_func(*args, **kwargs)

		# It may be that the view somehow doesn't have a context argument,
		# in this case we don't want to track or return anything
		try:
			context = response.context
		except:
			context = False

		if context:
			log_entry_name = self.views_to_names.get(
								self.view_func.__name__, False)

			if log_entry_name:
				trackGrade(log_entry_name, request, context)

		return response


