from django.template import RequestContext
# from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404


def render_to_response(*args, **kwargs):
	""" Append an attribute onto the response so that we can grab the context
	from it in the track decorator. It has to be an attribute so that it
	doesn't depend on the function returning the response to be decorated by
	@trackGrade to get proper output. """

	from django.shortcuts import render_to_response

	response = render_to_response(*args, **kwargs)
	# response.response_args = args
	response.context = args[1]

	return response

from django.contrib.auth.decorators import login_required

from models import UserProfile, Course, UserGrade, Activity

def cookie_login(request, next_page=None, required=False, **kwargs):
	""" Check for existing site.uit.no cookie
	"""

	if not next_page:
		next_page = '/myv_oahpa/courses/' # TODO: change next url for deep links
	if request.user.is_authenticated():
		message = "You are logged in as %s." % request.user.username
		request.user.message_set.create(message=message)
		return HttpResponseRedirect(next_page)

	# TODO: get cookie uid, for now just using a get variable.
	cookie_uid = request.GET.get('some_cookie')

	if cookie_uid:
		cookie_uid = int(cookie_uid)
		from django.contrib import auth
		user = auth.authenticate(cookie_uid=cookie_uid)
		if user is not None:
			auth.login(request, user)
			name = user.first_name or user.username
			message = "Login succeeded. Welcome, %s." % name
			user.message_set.create(message=message)
			return HttpResponseRedirect(next_page)
		# elif settings.CAS_RETRY_LOGIN or required:
			# return HttpResponseRedirect(_login_url(service))
		else:
			error = "<h1>Forbidden</h1><p>Login failed.</p>"
			return HttpResponseForbidden(error)
	else:
		return HttpResponseRedirect('/myv_oahpa/courses/standard_login/') # TODO: check


def cookie_logout(request, next_page=None, **kwargs):
	"""
	"""

	from django.contrib.auth import logout

	logout(request)

	# This can't redirect to cookie_logout, or else there are unlimited
	# redirects.

	if not next_page:
		next_page = '/myv_oahpa/courses/logout/'
	
	return HttpResponseRedirect(next_page)


def trackGrade(gamename, request, c):
	""" Takes a name of the game, request, and the context, and produces
		a course grade entry for the student.

		In the corresponding oahpa.drills.views, first import this function

			ex.)	from courses.views import trackGrade

		Then, insert the following into each view before the return render_to_response

			ex.)	trackGrade('Morfa', request, c)
					return render_to_response( etc ... )

		The first value is the name of the game, but this function handles
		the rest of choosing specifics, so course grade entries will display:

				Morfa - N-ILL - Bisyllabic
				Morfa - PRS - Trisyllabic
	"""
	SETTINGS = c['settingsform'].data
	
	if c['show_correct'] == 1 or c['all_correct'] == 1:
		if request.user.is_authenticated() and not request.user.is_anonymous():
			game_type = ''
			if 'gamename_key' in c['settings']:
				game_type = c['settings']['gamename_key']
					
			gamename = gamename + ' - ' + game_type

			points, _, total = c['score'].partition('/')
			activity, _ = Activity.objects.get_or_create(name=gamename)
			new_grade = UserGrade.objects.create(user=request.user.get_profile(),
												game=activity,
												score=points,
												total=total)


@login_required
def courses_main(request):
	""" This is the main view presented to users after login.
		Instructors will be shown a link to view grades and student progress,
		students will be shown their current progress in all of the games
		that they have records in.
	"""
	template = 'courses/courses_main.html'
	
	c = {}
	new_profile = None
	is_student = None

	try:
		profile = request.user.get_profile()
	except UserProfile.DoesNotExist:
		profile = UserProfile.objects.create(user=request.user)
		new_profile = True
	
	summary = False
	
	if profile.is_student:
		summary = profile.usergradesummary_set.all()
		if summary.count() == 0:
			new_profile = True
		is_student = True
	
	if profile.is_student:
		template = 'courses/courses_main.html'
	elif profile.is_instructor:
		template = 'courses/courses_main_instructor.html'
	
	c = {
		'user':  request.user,
		'profile':  profile,
		'new_profile':  new_profile,
		'is_student':  is_student,
		'summaries':  summary,
		'courses': Course.objects.filter(
									courserelationship__user=request.user)\
								 .distinct(),
	}

	return render_to_response(template, 
							  c, 
							  context_instance=RequestContext(request))

from django.contrib.auth.decorators import user_passes_test

def instructor_group(user):
	if user.get_profile().is_instructor:
		return True
	else:
		return False
	
@user_passes_test(instructor_group)
def instructor_student_detail(request, uid):
	student = UserProfile.objects.get(user__id=uid)
	instructor = request.user.get_profile()

	instructor_courses = list([a.id for a in instructor.instructorships])
	student_courses = list([a.id for a in student.courses])

	intersection = list(set(instructor_courses) & set(student_courses))

	if len(intersection) == 0:
		error = 'Student not found.'
		return HttpResponseForbidden(error)
	
	template = 'courses/instructor_student_detail.html'
	c = {}
	c['student'] = UserProfile.objects.get(user__id=uid)
	return render_to_response(template,
							  c,
							  context_instance=RequestContext(request))


