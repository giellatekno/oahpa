# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User, Group

from operator import itemgetter

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

class CourseGoal(models.Model):
    """ This is a grouping of goals connected to a course.

    TODO: course goal evaluation for sub goals for user.
    TODO: fixtures with default set that can be copied to another
    course.

    """

    course = models.ForeignKey(Course, null=True, blank=True)
    created_by = models.ForeignKey(User)
    short_name = models.CharField(max_length=42)
    description = models.TextField(help_text=GOAL_HELP_TEXT)

    # TODO: maybe progression should be defined in related model
    # instead of many2many, so goals can be shared with different
    # orderings

    # goals = models.ManyToManyField('Goal', related_name='goals')

    def __unicode__(self):
        return u"%s - %s" % (self.course, self.short_name)

    def progress_for(self, user):
        ugis = sum( [list(g.goal.usergoalinstance_set.filter(user=user)) for g in self.goals.all()]
                  , []
                  )
        progresses = [float(ugi.progress) for ugi in ugis]
        if len(progresses) > 0:
            progress = sum(progresses)/float(len(progresses)) * 100
            progress_str = "%.0f" % progress
            return progress_str + '%'
        else:
            return "0%"


class CourseGoalGoal(models.Model):
    coursegoal = models.ForeignKey('CourseGoal', related_name="goals")
    goal = models.ForeignKey('Goal')

class Goal(models.Model):
    """ This is a course goal object, which is connected to criteria.
    """
    course = models.ForeignKey(Course, null=True, blank=True)
    created_by = models.ForeignKey(User)
    short_name = models.CharField(max_length=42)
    description = models.TextField(help_text=GOAL_HELP_TEXT)

    url_base = models.CharField(max_length=24)

    main_type = models.CharField(max_length=24)
    sub_type = models.CharField(max_length=24)

    # TODO: this should be a method that returns a URL based on the
    # activity definition, for now just making a shortcut. Can
    # eventually just use whatever code that the deeplink thing uses to
    # get the user to the right page.

    threshold = models.FloatField(default=80.0, help_text="Percentage user must get correct. E.g. 80.0")
    minimum_sets_attempted = models.IntegerField(default=5, help_text="Amount of sets user must try to be finished.")
    correct_first_try = models.BooleanField(default=False, help_text="Only count answers correct on the first try")

    @property
    def begin_url(self):
        """ Confusing, I know. 
        This constructs the URL that hte user is redirected to for
        permission checks.
        """
        from django.core.urlresolvers import reverse

        return reverse('begin_course_goal', kwargs={'goal_id': self.id})

    def start_url(self):
        """ This is the exercise start page that the user will see when
        they begin working on their goal. It is constructed from the
        parameters defined in the goal.
        """
        from django.conf import settings
        from urllib import urlencode

        URL_PREFIX = settings.URL_PREFIX
        params = dict([
            (p.parameter, p.value) for p in self.params.all()
        ])
        return "/%s%s?%s" % (URL_PREFIX, self.url_base, urlencode(params))

    def __unicode__(self):
        if self.course:
            return "%s - %s" % (unicode(self.course), self.short_name)
        else:
            return "User-defined <%s> - %s" % (unicode(self.created_by.username), self.short_name)

    def user_completed(self, user):
        goal_instance = self.usergoalinstance_set.filter(user=user)
        if len(goal_instance) > 0:
            return self.is_complete(goal_instance[0])
        else:
            return False

    def save(self, *args, **kwargs):
        self.last_attempt = datetime.datetime.now()
        super(UserGoalInstance, self).save(*args, **kwargs)

    def is_complete(self, user_goal_instance):
        import datetime

        # If this is completed, set the completed_date on the description
        if self.correct_first_try:
            up = user_goal_instance.correct_first_try
        else:
            up = user_goal_instance.correct

        if float(up) == 0.0:
            return False

        calc_progress = (float(up) / float(user_goal_instance.total_answered)) * 100

        if self.minimum_sets_attempted:
            completed_min_rounds = user_goal_instance.rounds >= self.minimum_sets_attempted
        else:
            completed_min_rouds = True

        passed_percent_correct = calc_progress >= self.threshold

        if passed_percent_correct and completed_min_rounds:
            user_goal_instance.grade = user_goal_instance.progress
            user_goal_instance.is_complete = True
            user_goal_instance.save()
            return True

        return False

    def student_set_count(self, user, logs):
        """ For a given goal, count the amount of question sets a user
        answered.
        """

        def exists(l):
            return l is not None

        values = logs.values_list('question_set')

        sets = filter(exists, map(itemgetter(0), values))

        return sorted(list(set(sets)))

    def evaluate_for_student(self, user, last_only=True, iteration=False):
        logs = UserActivityLog.objects.filter(user=user, usergoalinstance__goal=self)
        if iteration:
            logs = logs.filter(usergoalinstance__attempt_count=iteration)
        elif last_only:
            _max = max(logs.values_list('usergoalinstance__attempt_count', flat=True))
            logs = logs.filter(usergoalinstance__attempt_count=_max)

        if logs.count() == 0:
            print " -- nothing yet -- "
            return None

        question_sets = self.student_set_count(user, logs)

        # Amount of questions that the user answered correctly on the
        # first try.

        def get_correct_on_first_try(ls):
            first_round = ls.filter(question_tries=1, is_correct=True)
            return first_round

        def get_correct(ls):
            return ls.filter(is_correct=True)

        def get_total_answered_for_round(ls):
            # Answers generated at all, correct and incorrect.
            answered = 0
            _tries = list(set(map(itemgetter(0),
                                  ls.values_list('question_tries'))))
            for t in _tries:
                answered += ls.filter(question_tries=t).count()
            return answered

        correct_on_first_try = []
        all_correct = []
        amount_answered = 0

        for q in question_sets:
            set_logs = logs.filter(question_set=q)
            first_try = get_correct_on_first_try(set_logs)
            eventually = get_correct(set_logs)
            answered = get_total_answered_for_round(set_logs)

            print "round: " + repr(q)
            print "correct on first:   %d" % first_try.count()
            print "correct eventually: %d" % eventually.count()
            print "attempted:          %d" % answered
            print '--'

            correct_on_first_try.extend(get_correct_on_first_try(set_logs))
            all_correct.extend(eventually)
            amount_answered += answered

        print
        print '---'
        print "rounds:           %d" % max(question_sets)
        print "answered:         %d" % amount_answered
        print "correct on first: %d" % len(correct_on_first_try)
        print "correct at all:   %d" % len(all_correct)
        print '---'
        print

        result_args = {
            'rounds': max(question_sets),
            'total_answered': amount_answered,
            'correct_first_try': len(correct_on_first_try),
            'correct': len(all_correct),
            'progress': float(len(all_correct)) / float(amount_answered)
        }

        return result_args

class UserGoalInstance(models.Model):
    user = models.ForeignKey(User)
    goal = models.ForeignKey('Goal')

    # only one may be 'opened' at a time
    opened = models.BooleanField(default=True)
    attempt_count = models.IntegerField(default=1)

    progress = models.DecimalField(decimal_places=2, max_digits=4, default=0.0)

    is_complete = models.BooleanField(default=False)
    rounds = models.IntegerField(default=1)
    total_answered = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
    correct_first_try = models.IntegerField(default=0)

    last_attempt = models.DateTimeField(auto_now_add=True)
    grade = models.IntegerField(blank=True, null=True)

    class Meta(object):
        unique_together = (("user", "goal", "attempt_count"),)

    def __unicode__(self):
        return "%s: %.2f" % (self.goal.short_name, self.progress)

    @property
    def evaluation(self):
        return self.evaluate_instance()

    def evaluate_instance(self):
        evaluated = self.goal.evaluate_for_student(self.user, iteration=self.attempt_count)
        if (self.progress is not None) and (self.progress != evaluated.get('progress', False)):
            self.progress = evaluated.get('progress')
            self.save()
        if evaluated.get('progress', False):
            evaluated['progress'] = evaluated['progress'] * 100
        return evaluated

    def save(self, *args, **kwargs):
        vals = UserGoalInstance.objects.filter(user=self.user, goal=self.goal).values_list('attempt_count', flat=True)
        if len(vals) > 0:
            highest = max(
                UserGoalInstance.objects.filter(user=self.user, goal=self.goal).values_list('attempt_count', flat=True)
            )
            self.attempt_count = highest + 1
        super(UserGoalInstance, self).save(*args, **kwargs)

class GoalParameter(models.Model):
    goal = models.ForeignKey(Goal, related_name='params')
    parameter = models.CharField(max_length=64)
    value = models.CharField(max_length=64)

from univ_drill.models import Feedbackmsg, Feedbacktext

class UserFeedbackLog(models.Model):
    user = models.ForeignKey(User)
    goal = models.ForeignKey(Goal, null=True, blank=True)

    user_input = models.TextField()
    correct_answer = models.TextField()

    datetime = models.DateTimeField(auto_now_add=True)

    feedback_texts = models.TextField(Feedbacktext)

    # TODO: how much detailed info do we want on when the user clicked?
    # TODO: methods for determining whether user has reached a given
    # threshold for feedback levels

    def get_user_feedback_level(self, user):
        return '1'

class UserActivityLog(models.Model):
    """ Tracking user activity, question/answer completion, and feedback
    use.
    """
    user = models.ForeignKey(User)
    usergoalinstance = models.ForeignKey(UserGoalInstance)
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

    # TODO: datetime?

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

        # Copy
        for drill_attr, log_attr in drill_log_attrs:
            activity_log_attrs[log_attr] = getattr(drill_log, drill_attr)

        # Add some things not present in the original log entry
        activity_log_attrs['user'] = user
        activity_log_attrs['usergoalinstance_id'] = current_user_goal
        activity_log_attrs['question_set'] = request.session['question_set_count']
        activity_log_attrs['question_tries'] = question_tries.get(drill_log.correct)

        # Check if there are existing logs for this question that we
        # need to update
        existing_kwargs = activity_log_attrs.copy()
        existing_kwargs.pop('user_input')
        existing_kwargs.pop('question_tries')
        existing_kwargs.pop('is_correct')

        # We only want to replace previously incorrect logs.
        existing = UserActivityLog.objects.filter(**activity_log_attrs)

        # If so, update, otherwise create.
        if existing:
            if activity_log_attrs['is_correct'] == True:
                existing.update(question_tries=question_tries.get(drill_log.correct)+1,
                                user_input=activity_log_attrs['user_input'],
                                is_correct=activity_log_attrs['is_correct'])
            else:
                existing.update(question_tries=question_tries.get(drill_log.correct),
                                user_input=activity_log_attrs['user_input'],
                                is_correct=activity_log_attrs['is_correct'])
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
