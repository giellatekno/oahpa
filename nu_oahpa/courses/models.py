# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

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
	
	def __unicode__(self):
		return self.user.username
	


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


ROLES = (
	(_('Student'), 'Student'),
	(_('Instructor'), 'Instructor'),
)

from django.db.models.signals import post_save, pre_save
from signals import create_profile, aggregate_grades, grant_admin, user_presave

post_save.connect(create_profile, sender=User, 
	dispatch_uid="oahpa.courses.models.post_save")

post_save.connect(aggregate_grades, sender=UserGrade,
	dispatch_uid="oahpa.courses.models.post_save")

post_save.connect(grant_admin, sender=Course,
	dispatch_uid="oahpa.courses.models.post_save")

pre_save.connect(user_presave, sender=User,
	dispatch_uid="oahpa.courses.models.pre_save")
