# from smaoahpa.courses.models import CourseMembership
from django.contrib.auth.models import User, Group
from models import UserProfile
from django.db.models import Avg, Max, Min, Count

# TODO: export fixtures with group and base permissions.

# This causes an error on sync with a fresh db. 
try: 
	instructor_group = Group.objects.get(name='Instructors')
except:
	pass

# Problems when using loaddata, which we may want to use more often.
try:
	from functools import wraps
except ImportError:
	from django.utils.functional import wraps

import inspect

def disable_for_loaddata(signal_handler):
	""" Disable a function when Django is called via loaddata.
	"""
	@wraps(signal_handler)
	def wrapper(*args, **kwargs):
		for fr in inspect.stack():
			if inspect.getmodulename(fr[1]) == 'loaddata':
				return
		signal_handler(*args, **kwargs)
	return wrapper

@disable_for_loaddata
def aggregate_grades(sender, **kwargs):
	""" This aggregates all of the users grades into a UserGradeSummary
		which will then be displayed to instructors.
	""" 

	grade_object = kwargs['instance']
	prof = grade_object.user
	activity = grade_object.game

	gradesummary, _ = prof.usergradesummary_set.get_or_create(game=activity)
	grades = prof.usergrade_set.filter(game=activity)
	game_count = grades.count()

	if game_count > 0:
		stats = grades.aggregate(grade_max=Max('score'),
								grade_min=Min('score'),
								grade_avg=Avg('score'))

		gradesummary.average = stats['grade_avg']
		gradesummary.maximum = stats['grade_max']
		gradesummary.minimum = stats['grade_min']
		gradesummary.count = game_count
		gradesummary.save()

@disable_for_loaddata
def create_profile(sender, **kwargs):
	""" This signal creates UserProfile objects when the Django
		user models are saved.
	"""
	user_obj = kwargs['instance']
	profile, created = UserProfile.objects.get_or_create(user=user_obj)
	if created:
		profile.save()
	return True

@disable_for_loaddata
def grant_admin(sender, **kwargs):
	""" Course instructors gain access via is_staff. If extra permissions
		need to be assigned, this should be done here.
	"""

	course = kwargs['instance']
	instructors = course.instructors.all()
	instructors.update(is_staff=True)
	for i in instructors:
		i.groups.add(instructor_group)
	

	return True

@disable_for_loaddata
def user_presave(sender, instance, **kwargs):
	""" Increments uesr login count.
	"""
	user = instance
	try:
		userprofile = instance.get_profile()
	except UserProfile.DoesNotExist:
		userprofile = UserProfile.objects.create(user=user)
	try:
		if instance.last_login:
			old = instance.__class__.objects.get(pk=instance.pk)
			if instance.last_login != old.last_login:
				userprofile.userlogin_set.create(timestamp=instance.last_login)
	
		userprofile.login_count = userprofile.userlogin_set.all().count()
		userprofile.last_login = user.last_login
		userprofile.save()
	except User.DoesNotExist:
		pass
	
	return True

