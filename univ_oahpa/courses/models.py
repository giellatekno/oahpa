# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

# TODO: Grades still need to be added when users submit forms and get
#		responses, but for now most of the basic stuff is there.

# TODO: need to create fixtures of groups and permissions

# TODO: hide delete course admin actions for Instructors group

# TODO: add login/logout links to other templates so users find it. 

# TODO: switch strings to gettext strings.

# TODO: display strings in Meta

# TODO: grades in course admin view somehow? or at least link to objs?

class UserProfile(models.Model):
	""" This is more of a handy organizational object for now, 
		and makes some things easier. Unfortunately, some other models
		here need to use the User model, and some need to use the
		UserProfile model. Would like to change this to make extending
		development easier, but it's not a huge priority to research
		what the problem is.
	"""
	user = models.ForeignKey(User)
	
	def __unicode__(self):
		userinfo = (self.user.username, self.user.first_name, 
					self.user.last_name, self.user.email)
		userstr = '%s: %s %s, %s' % userinfo
		return userstr

class UserGradeSummary(models.Model):
	""" Stores the summary for each game for grading purposes.
		Data here is aggregated by a post_save signal.
	"""
	user = models.ForeignKey(UserProfile)
	game = models.CharField(max_length='50')
	average = models.DecimalField(max_digits=15, decimal_places=3, null=True)
	minimum = models.DecimalField(max_digits=15, decimal_places=3, null=True)
	maximum = models.DecimalField(max_digits=15, decimal_places=3, null=True)
	count = models.IntegerField(default=0)

	def __unicode__(self):
		return '%s grade totals for %s' % (self.user.user.username, self.game)


class UserGrade(models.Model):
	""" This model tracks individual user scores by game and date.
		For now we're not going to track any more than this data, 
		but answers and input could be possible.
		TODO: admin isn't displaying date.
	"""

	user = models.ForeignKey(UserProfile)
	game = models.CharField(max_length='50')
	datetime = models.DateTimeField(auto_now_add=True)
	score = models.IntegerField()
	total = models.IntegerField(default=5)

	class Meta:
		ordering = ['-datetime']
		permissions = (("can_change_score", "Can change grade"),)

class Course(models.Model):
	""" Course object. Users listed as instructors here are granted access
		to the admin interface, via a post_save signal. In order for
		instructors to see anything, they must also be in the
		Instructors user group.

	"""
	name = models.CharField(max_length=50, default=u"Fluent in Southern Sámi in 10 days")
	identifier = models.CharField(max_length=12, default="SAM-1234")
	instructors = models.ManyToManyField(User, related_name='instructorships')
	students = models.ManyToManyField(User, related_name='studentships')

	def __unicode__(self):
		r = self.identifier + u': ' + self.name
		return r


ROLES = (
	(_('Student'), 'Student'),
	(_('Instructor'), 'Instructor'),
)

from django.db.models.signals import post_save
from signals import create_profile, aggregate_grades, grant_admin

post_save.connect(create_profile, sender=User, 
	dispatch_uid="univ_oahpa.courses.models.post_save")

post_save.connect(aggregate_grades, sender=UserGrade,
	dispatch_uid="univ_oahpa.courses.models.post_save")

post_save.connect(grant_admin, sender=Course,
	dispatch_uid="univ_oahpa.courses.models.post_save")


