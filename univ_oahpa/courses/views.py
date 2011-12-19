from django.template import RequestContext
# from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect, HttpResponseForbidden


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
		next_page = '/univ_oahpa/courses/' # TODO: change next url for deep links
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
		return HttpResponseRedirect('/univ_oahpa/courses/standard_login/') # TODO: check


def cookie_logout(request, next_page=None, **kwargs):
	"""
	"""

	from django.contrib.auth import logout

	logout(request)

	# This can't redirect to cookie_logout, or else there are unlimited
	# redirects.

	if not next_page:
		next_page = '/univ_oahpa/courses/logout/'
	
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
			if gamename.startswith('Morfa'):
				if 'case' in SETTINGS:
					game_type = SETTINGS['case']
				elif 'vtype' in SETTINGS:
					game_type = SETTINGS['vtype']
				elif 'adjcase' in SETTINGS:
					game_type = SETTINGS['adjcase']
				else:
					game_type = ''
				
				# The type of these variables can be several things,
				# apparently; so I'm watching out for that with this.
				true_values = [1, '1', True, 'True', 'on']
				all_values = ['all', 'All', 'ALL']
				sylls = []

				if 'bisyllabic' in SETTINGS:
					if SETTINGS['bisyllabic'] in true_values: 
						sylls.append('bisyllabic')
				if 'trisyllabic' in SETTINGS:
					if SETTINGS['trisyllabic'] in true_values:
						sylls.append('trisyllabic')
				if 'contracted' in SETTINGS:
					if SETTINGS['contracted'] in true_values:
						sylls.append('contracted')
				game_type += ' - ' + '/'.join(sylls)
				
			elif gamename in ['Leksa', 'Leksa-N']:
				try:			semtype = SETTINGS['semtype'].lower()
				except:			semtype = False
				
				game_type = ''
				true_values = [1, '1', True, 'True', 'on']
				
				places = []
				try:			sapmi = SETTINGS['sapmi']; places.append(True)
				except:			sapmi = False
				
				try:			world = SETTINGS['world']; places.append(True)
				except:			world = False
				
				try:			suopma = SETTINGS['suopma']; places.append(True)
				except:			suopma = False
				
				try:			common = SETTINGS['common']; places.append(True)
				except:			common = False
				
				try:			rare = SETTINGS['rare']; places.append(True)
				except:			rare = False
				
				try:			book = SETTINGS['source'].lower()
				except:			book = False
				
				try:			source = SETTINGS['book'].lower()
				except:			source = False
				
				if semtype:
					if semtype != 'all':
						game_type += 'set: %s' % semtype
				if len(places) > 0:
					game_type = ''
					placetypes = []
					if sapmi in true_values:		placetypes.append('sapmi')
					if suopma in true_values:		placetypes.append('suopma')
					if world in true_values:		placetypes.append('world')
					if common in true_values:		placetypes.append('common')
					if rare in true_values:			placetypes.append('rare')
					game_type += ' - places: ' + '/'.join(placetypes)
				if source:
					if source != 'all':
						game_type += 'book: %s' % source
				if book:
					if book != 'all':
						game_type += 'book: %s' % book
						game_type = 'set: %s' % semtype
				if source:
					if source != 'all':
						game_type += 'book: %s' % source
				if book:
					if book != 'all':
						game_type += 'book: %s' % book
			elif gamename == 'Numra':
				game_type = SETTINGS['numgame']
			
			
			elif gamename.startswith('C-Morfa'):
				game_type = ''
				try:			case_context = SETTINGS['case_context']
				except:			case_context = ''
				
				try:			vtype_context = SETTINGS['vtype_context']
				except:			vtype_context = ''
				
				try:			adj_context = SETTINGS['adj_context']
				except:			adj_context = ''
				
				try:			num_context = SETTINGS['num_context']
				except:			num_context = ''
				
				try:			book = SETTINGS['book']
				except:			book = ''
				
				try:			source = SETTINGS['source']
				except:			source = ''
				
				game_type += case_context + vtype_context + adj_context + num_context
				game_type += ' '
				game_type += book + source
							
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
	
	if not request.user.is_staff:
		summary = profile.usergradesummary_set.all()
		if summary.count() == 0:
			new_profile = True
		is_student = True
	
	c = {
		'user':  request.user,
		'profile':  profile,
		'new_profile':  new_profile,
		'is_student':  is_student,
		'summaries':  summary,
		'courses': Course.objects.filter(courserelationship__user=request.user),
	}

	return render_to_response(template, c, context_instance=RequestContext(request))


# NOTES:
#	forms.LeksaSettings - user selects: semtype, transtype, source
#						  form has: gametype, language, frequency,
#						  geography, syll []

#	forms.MorfaSettings - user selects: case, adjcase, vtype, num_bare,
#						adj_context, vtype_context, book, bisyllabic,
#						trisyllabic, contracted, grade


#   smaoahpa and smeoahpa will differ on this a lot.

#	maybe shouldn't try to subclass forms, so much as make dicts/lists of
#	stuff that will be settings.

def course_link(request):
	""" This view creates a Morfa or Leksa game corresponding to instructors' preset 
		options. 

		Could be slightly tough, require creating request objects with post data.

		one Link model may be tricky, would like to include a cutoff for dates that
		new grades will no longer be stored. Link object should be passed to trackGrade

	"""
	
	pass

