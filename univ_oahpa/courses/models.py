# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User, Group

# TODO: need to create fixtures of groups and permissions
# TODO: hide delete course admin actions for Instructors group
# TODO: site-uit-no-default course added to fixtures

####
##
##      User data
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
    def studentships(self):
        crs = self.user.courserelationship_set\
                    .filter(relationship_type__name='Students')

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
        return 'http://oahpa.uit.no/univ_oahpa/openid/%s' % self.user.username
    
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
    user = models.ForeignKey('UserProfile')
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
##      Course data
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
    site_link = models.URLField(verify_exists=False, max_length=200, blank=True, null=True)
    end_date = models.DateTimeField(null=True, default=None, blank=True)

    @property
    def students(self):
        us = UserProfile.objects.filter(user__courserelationship__course=self)\
                                .distinct()
        return us

    def __unicode__(self):
        if self.identifier:
            return u"%s: %s" % (self.identifier, self.name)
        else:
            return u"%s" % self.name

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

##
## Course goals
##

GOAL_HELP_TEXT = _("""This is a plain-text description shown to students
describing their goal.""")

class Goal(models.Model):
    """ This is a course goal object, which is connected to criteria.
    """
    course = models.ForeignKey(Course)
    created_by = models.ForeignKey(User)
    short_name = models.CharField(max_length=42)
    description = models.TextField(help_text=GOAL_HELP_TEXT)

    # TODO: this should be a method that returns a URL based on the
    # activity definition, for now just making a shortcut. Can
    # eventually just use whatever code that the deeplink thing uses to
    # get the user to the right page.

    start_url = models.TextField()

    def __unicode__(self):
        return "%s - %s" % (unicode(self.course), self.short_name)

class GoalCriterion(models.Model):
    # TODO: just for now using a text field so that I can start testing,
    # eventually we'll have some conditions on how user activity logs
    # must be evaluated.
    # TODO: allow a user to reuse criteria from other goals?
    # TODO: criterion for setting the minimum amount of question sets a
    # user must go through
    goal = models.ForeignKey(Goal)
    description = models.TextField()

    # TODO: some ideas of criteria
    #    percent                 correct type                         log activity match 
    #    - 80%               |   correct of all answers            |  Leksa semantic set
    #    - 60%               |   correct on first try per question |  Morfa-C category & subcategory
    #    - 15 sets completed |   ----                              |  Morfa-S category & subcategory & subcategory

    # Said otherwise:
    #   - set of user log answers pertaining to goal, filtered by match
    #     category
    #   - sorted by date time
    #   - TODO: need a unique value for the answer set that the user is
    #     working on, which increments each time the user finishes the
    #     set

class UserGoalProgress(models.Model):
    # TODO: do not cascade and delete to this model if instructor
    # deletes a goal?
    goal = models.ForeignKey(Goal)
    user = models.ForeignKey(User)
    completed_date = models.DateTimeField()
    grade = models.IntegerField()

    # TODO: see how many sets a user completed this in?

class UserActivityLog(models.Model):
    """ Tracking user activity, question/answer completion, and feedback
    use.
    """
    user = models.ForeignKey(User)
    goal = models.ForeignKey(Goal)
    goal_repetition = models.IntegerField(default=1)
    is_correct = models.BooleanField()
    correct_answer = models.TextField()
    user_input = models.TextField()

    question_set = models.IntegerField(default=1)
    question_tries = models.IntegerField(default=1)

    # Now the rest of the attributes should just be meta where each
    # activity was generated, i.e., morfa-s, morfa-c, etc. This will be
    # indirectly contained in the Goal instance, so it may be that
    # anything else isn't needed.
    in_game = models.TextField()

def create_activity_log_from_drill_logs(request, user, drill_logs, current_user_goal=False):
    # TODO: do it all in one commit.

    drill_log_attrs = [
        # ('game', 'in_game'),
        # ('date', 'date'),
        # user's input
        ('userinput', 'user_input'),
        # correct or no?
        ('iscorrect', 'is_correct'),
        # the actual correct value
        ('correct', 'correct_answer'),
        # ('qid', 'qid'),
        # ?
        # ('example', 'example'),
        # ?
        # ('feedback', 'feedback'),
        # ?
        # ('comment', 'comment'),
        # ('messageid', 'messageid'),
        # ('lang', 'lang'),
        # TODO: is this all the lemmas or just some? maybe this is just for
        # sahka and cealkka
        # 'tasklemmas', 
    ]

    question_tries = request.session['question_try_count']

    for drill_log in drill_logs:
        activity_log_attrs = {}
        for drill_attr, log_attr in drill_log_attrs:
            activity_log_attrs[log_attr] = getattr(drill_log, drill_attr)
        activity_log_attrs['user'] = user
        activity_log_attrs['goal_id'] = current_user_goal
        activity_log_attrs['question_set'] = request.session['question_set_count']
        activity_log_attrs['question_tries'] = question_tries.get(drill_log.correct)

        # Check if there are existing logs for this question that we
        # need to update
        existing_kwargs = activity_log_attrs.copy()
        existing_kwargs.pop('user_input')
        existing_kwargs.pop('question_tries')
        existing = UserActivityLog.objects.filter(**activity_log_attrs)

        # If so, update, otherwise create.
        if existing:
            existing.update(question_tries=question_tries.get(drill_log.correct))
        else:
            UserActivityLog.objects.create(**activity_log_attrs)
    return

from django.db.models.signals import post_save, pre_save, post_delete
from .signals import *

post_save.connect(create_profile, sender=User,
    dispatch_uid="univ_oahpa.courses.models.post_save")

post_save.connect(aggregate_grades, sender=UserGrade,
    dispatch_uid="univ_oahpa.courses.models.post_save")

post_save.connect(course_relationship_postsave, sender=CourseRelationship,
    dispatch_uid="univ_oahpa.courses.models.post_save")

post_delete.connect(course_relationship_postdelete, sender=CourseRelationship,
    dispatch_uid="univ_oahpa.courses.models.pre_save")

pre_save.connect(user_presave, sender=User,
    dispatch_uid="univ_oahpa.courses.models.pre_save")

# vim: set ts=4 sw=4 tw=72 syntax=python :
