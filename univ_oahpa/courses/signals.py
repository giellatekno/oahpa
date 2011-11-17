# from univ_oahpa.courses.models import CourseMembership
from django.contrib.auth.models import User, Group
from courses.models import UserProfile
from django.db.models import Avg, Max, Min, Count

# TODO: export fixtures with group and base permissions.

# This causes an error on sync with a fresh db. 
try: 
	instructor_group = Group.objects.get(name='Instructors')
except:
	pass



def aggregate_grades(sender, **kwargs):
	""" This aggregates all of the users grades into a UserGradeSummary
		which will then be displayed to instructors.
	""" 

	grade_object = kwargs['instance']
	prof = grade_object.user
	game_name = grade_object.game

	gradesummary, _ = prof.usergradesummary_set.get_or_create(game=game_name)
	grades = prof.usergrade_set.filter(game=game_name)
	game_count = grades.count()

	if game_count > 0:
		stats = grades.aggregate(grade_max=Max('score'),
								grade_min=Min('score'),
								grade_avg=Avg('score'))

		gradesummary.average = stats['grade_avg']
		gradesummary.maximum = stats['grade_max']
		gradesummary.minimum = stats['grade_min']
		gradesummary.count =game_count
		gradesummary.save()

def create_profile(sender, **kwargs):
	""" This signal creates UserProfile objects when the Django
		user models are saved.
	"""
	user_obj = kwargs['instance']
	profile, created = UserProfile.objects.get_or_create(user=user_obj)
	if created:
		profile.save()
	return True

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

