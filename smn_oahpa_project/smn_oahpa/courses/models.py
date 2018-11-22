# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User, Group

from local_conf import LLL1

# TODO: need to create fixtures of groups and permissions
# TODO: hide delete course admin actions for Instructors group
# TODO: site-uit-no-default course added to fixtures

####
##
##		User data
##
####


class UserProfile(models.Model):
	""" This is more of a handy organizational object for now,
		and makes some things easier. Unfortunately, some other models
		here need to use the User model, and some need to use the
		UserProfile model. Would like to change this to make extending
		development easier, but it's not a huge priority to research
		what the problem is.
	"""
	user = models.ForeignKey(User)
	login_count = models.IntegerField(default=0)
	last_login = models.DateTimeField(null=True)
	site_cookie = models.IntegerField(null=True)

	def __unicode__(self):
		return self.user.username.encode('utf-8')

	@property
	def courses(self):
		return [a.course for a in self.user.courserelationship_set.all()]

	@property
	def instructorships(self):
		crs = self.user.courserelationship_set\
					.filter(relationship_type__name='Instructors')

		return [a.course for a in crs]

	@property
	def is_instructor(self):
		grs = self.user.groups.values_list('name', flat=True)
		if 'Instructors' in grs:
			return True
		else:
			return False

	@property
	def is_student(self):
		grs = self.user.courserelationship_set\
					   .values_list('relationship_type__name',
					   				flat=True)
		if 'Students' in grs:
			return True
		else:
			return False


	@property
	def open_id_link(self):
		return 'http://oahpa.uit.no/smn_oahpa/openid/%s' % self.user.username

	@property
	def grades(self):

		grades = self.usergradesummary_set.all()

		if grades.count() > 0:
			return grades
		else:
			return None



class UserLogin(models.Model):
	""" Tracking user logins. Model can be counted per user to check login counts,
		but also times are available.

	"""

	user = models.ForeignKey(UserProfile)
	timestamp = models.DateTimeField()

class UserGradeSummary(models.Model):
	""" Stores the summary for each game for grading purposes.
		Data here is aggregated by a post_save signal.
	"""
	user = models.ForeignKey(UserProfile)
	game = models.ForeignKey('Activity')
	average = models.FloatField(null=True)
	minimum = models.FloatField(null=True)
	maximum = models.FloatField(null=True)
	count = models.IntegerField(default=0)

	class Meta:
		verbose_name_plural = 'User grade summaries'
		ordering = ['average']

	@property
	def game_name(self):
		return self.game.name

	def __unicode__(self):
		return '%s grade totals for %s' % (self.user.user.username, self.game)

class UserGrade(models.Model):
	""" This model tracks individual user scores by game and date.
		For now we're not going to track any more than this data,
		but answers and input could be possible.
		TODO: admin isn't displaying date.
	"""

	user = models.ForeignKey(UserProfile)
	game = models.ForeignKey('Activity')
	datetime = models.DateTimeField(auto_now_add=True)
	score = models.IntegerField()
	total = models.IntegerField(default=5)

	def __unicode__(self):
		return u'Summary for %s from %s' % (self.user.user.username, self.game.name)

	class Meta:
		ordering = ['-datetime']
		permissions = (("can_change_score", "Can change grade"),)



class Activity(models.Model):
	""" Activity object for agregating course statistics.
	"""

	name = models.CharField(max_length=50)

	class Meta:
		verbose_name = 'activity'
		verbose_name_plural = 'activities'

	def __unicode__(self):
		return self.name

####
##
##		Course data
##
####

class Course(models.Model):
	""" Course object. Users listed as instructors here are granted access
		to the admin interface, via a post_save signal. In order for
		instructors to see anything, they must also be in the
		Instructors user group.

	"""
	name = models.CharField(max_length=50, default=u"Fluent in Southern Sámi in 10 days")
	identifier = models.CharField(max_length=12, default="SAM-1234")
	# instructors = models.ManyToManyField(User, related_name='instructorships')
	# students = models.ManyToManyField(User, related_name='studentships')
	site_link = models.URLField(max_length=200, blank=True, null=True)
	end_date = models.DateTimeField(null=True, default=None)

	@property
	def students(self):
		us = UserProfile.objects.filter(user__courserelationship__course=self)\
								.distinct()
		return us

class CourseRelationship(models.Model):
	""" This model contains information about the relationships of
		student-to-course and instructor-to-course, and provides expiration
		dates for the relationships.

		On expiration, relationships are not deleted, but rather dates are
		used as an access control. If no date is speficied, this is not an issue.

		On creation of the relationship, the date is copied from the course.
	"""
	DATE_HELP = ("Leave this blank to copy the course end date."
				 "If you wish to specify no end date, you will need to come back, "
				 "and remove it after adding the instructor.")

	relationship_type = models.ForeignKey(Group)
	user = models.ForeignKey(User)
	course = models.ForeignKey(Course)
	end_date = models.DateTimeField(null=True, blank=True, help_text=DATE_HELP)

	class Meta:
		unique_together = ("user",
							"course",
							"relationship_type",)


from django.db.models.signals import post_save, pre_save
from signals import create_profile, aggregate_grades, user_presave, course_relationship_postsave

post_save.connect(create_profile, sender=User,
	dispatch_uid=LLL1+"_oahpa.courses.models.post_save")

post_save.connect(aggregate_grades, sender=UserGrade,
	dispatch_uid=LLL1+"_oahpa.courses.models.post_save")

post_save.connect(course_relationship_postsave, sender=CourseRelationship,
	dispatch_uid=LLL1+"_oahpa.courses.models.post_save")

pre_save.connect(user_presave, sender=User,
	dispatch_uid=LLL1+"_oahpa.courses.models.pre_save")
