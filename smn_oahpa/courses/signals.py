# from smn_oahpa.courses.models import CourseMembership
from django.contrib.auth.models import User, Group
from models import UserProfile
from django.db.models import Avg, Max, Min, Count

# TODO: instructors do not need admin access anymore, should disable those bits

# This causes an error on sync with a fresh db, so catch the error because this
# group does not need to be created if the script is called from the
# commandline.
from django.db.utils import DatabaseError

try: 
	instructor_group = Group.objects.get(name='Instructors')
except Group.DoesNotExist:
	instructor_group = Group.objects.create(name='Instructors')
	root = User.objects.get(pk=1)
	instructor_group.user_set.add(root)
	instructor_group.save()
except DatabaseError:
	pass
else:
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
			if inspect.getmodulename(fr[1]) in ['loaddata', 'manage']:
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


DEFAULT_ROOTS = [
	'http://129.242.218.43/wordpress/',
	'http://site.uit.no/',
	'http://site.uit.no/oahpa/',
]





@disable_for_loaddata
def create_profile(sender, **kwargs):
	""" This signal creates UserProfile objects when the Django
		user models are saved.
	"""
	from openid_provider.models import OpenID, TrustedRoot

	user_obj = kwargs['instance']
	profile, created = UserProfile.objects.get_or_create(user=user_obj)
	if created:
		profile.save()

	new_oid, created = OpenID.objects.get_or_create(user=user_obj,
													openid=user_obj.username,
													default=True)
	for root in DEFAULT_ROOTS:
		n, _ = new_oid.trustedroot_set.get_or_create(trust_root=root)
		n.save()
	

	return True


@disable_for_loaddata
def course_relationship_postsave(sender, **kwargs):
	""" Course instructors are added to the group Instructors, but not given
	permissions to log into the admin site anymore.

	Also, copy the date from the user's course, if it exists. If the date
	existent on the object is not the same as the course, we assume that a user
	has modified it and will not copy the date over.
	
	The model is only saved if a change has been made, that way there is no
	endless loop."""

	created = kwargs['created']
	courserelationship = kwargs['instance']
	course = courserelationship.course

	# Grant admin access to instructor
	instructors = course.courserelationship_set\
						.filter(relationship_type__name='Instructors')
	instructors = [i.user for i in instructors]

	for i in instructors:
		# i.is_staff = True
		i.groups.add(instructor_group)
		i.save()
	
	# Copy the course end_date
	user = courserelationship.user
	previous = courserelationship.end_date

	if course.end_date:
		if created:
			courserelationship.end_date = course.end_date
	
	if previous != courserelationship.end_date:
		courserelationship.save()

	
	return True

	
@disable_for_loaddata
def user_presave(sender, instance, **kwargs):
	""" Increments user login count.
	"""
	user = instance
	
	try:
		userprofile = instance.get_profile()
	except UserProfile.DoesNotExist:
		return False
	
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

