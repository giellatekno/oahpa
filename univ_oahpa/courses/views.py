from django.template import RequestContext
from django.shortcuts import render_to_response
# from django.utils.translation import ugettext as _

from django.contrib.auth.decorators import login_required

from models import UserProfile, Course, UserGrade

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
			if gamename == 'Morfa':
				if 'case' in SETTINGS:
					game_type = SETTINGS['case']
				elif 'vtype' in SETTINGS:
					game_type = SETTINGS['vtype']
				elif 'adjcase' in SETTINGS and 'adj_context' in SETTINGS:
					game_type = SETTINGS['adjcase'] + ' ' + SETTINGS['adj_context']
				else:
					game_type = ''
				
				# The type of these variables can be several things,
				# apparently; so I'm watching out for that with this.
				true_values = [1, '1', True, 'True']
				all_values = ['all', 'All', 'ALL'] 

				if 'bisyllabic' in SETTINGS:
					if SETTINGS['bisyllabic'] in true_values: 
						game_type += ' - bisyllabic'
				elif 'trisyllabic' in SETTINGS:
					if SETTINGS['trisyllabic'] == true_values:
						game_type += ' - trisyllabic'
				elif 'contracted' in SETTINGS:
					if SETTINGS['contracted'] == true_values:
						game_type += ' - contracted'
			elif gamename in ['Leksa', 'Leksa-N']:
				try:			semtype = SETTINGS['semtype'].lower()
				except:			semtype = False
				
				try:			book = SETTINGS['source'].lower()
				except:			book = False
				
				try:			source = SETTINGS['book'].lower()
				except:			source = False
				
				if semtype:
					if semtype != 'all':
						game_type = 'set: %s' % semtype
				if source:
					if source != 'all':
						game_type = 'book: %s' % source
				if book:
					if book != 'all':
						game_type = 'book: %s' % book
			elif gamename == 'Numra':
				game_type = 'TODO:'
			
			
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
		'courses': request.user.studentships.all()
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

