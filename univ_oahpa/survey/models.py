# -*- coding: utf-8 -*-

# TODO: middleware for watching for displaying the survey
# 
#       - must consider option that multiple surveys could be present at
#         any time
# 
#       - must consider that existing users who haven't been surveyed
#         need to be surveyed on some login

from django.db import models

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group

## 
## Survey
##

question_types = [
    ('freeform text', 'text'),
    ('single choice', 'choice'),
    ('multiple choice', 'multichoice'),
    ('yes/no', 'boolean'),
]

## Survey definition

class Survey(models.Model):
    """ Main survey object
    """
    title = models.CharField(max_length=50)
    description = models.TextField()

class SurveyQuestion(models.Model):
    """ Contains the survey question, and question type. Connects to any
    possible answer objects.
    """
    # TODO: Internationalization language
    survey = models.ForeignKey('Survey', related_name='questions')

    question_text = models.TextField()
    question_type = models.CharField(max_length=18, choices=question_types)

    def __unicode__(self):
        return self.question_text

    def __repr__(self):
        if len(self.question_text) > 15:
            return self.question_text[0:15]
        else:
            return self.question_text

# TODO: translation

#   https://github.com/deschler/django-modeltranslation
#   https://github.com/Yaco-Sistemas/django-transmeta/
#   https://pythonhosted.org/django-translatable/

# class SurveyQuestionTranslations(models.Model):
#     question = models.ForeignKey('SurveyQuestion')
# 
#     language = models.CharField(max_length=5)
#     text = models.TextField()

class SurveyQuestionAnswerValue(models.Model):
    """ A model for defining answer values for question types that allow
    for a choice. UserSurveyQuestionAnswer will only be auto-populated
    from this, not related by foreignkey
    """
    question = models.ForeignKey(SurveyQuestion, related_name='answer_values')
    answer_text = models.TextField()

    def __unicode__(self):
        return self.answer_text

    def __repr__(self):
        if len(self.answer_text) > 15:
            return self.answer_text[0:15]
        else:
            return self.answer_text

## User survey results

class UserSurvey(models.Model):
    """ This is the user survey instance, to connect individual user
    answers together.
    """
    survey = models.ForeignKey(Survey)
    user = models.ForeignKey(User)

    completed = models.DateTimeField(auto_now_add=True)

class UserSurveyQuestionAnswer(models.Model):
    """ This object will store user answers, regardless of whether it
    comes from a database-specified choice, or user-entered free text.
    """

    user_survey = models.ForeignKey(UserSurvey)
    question = models.ForeignKey(SurveyQuestion)
    answer_text = models.TextField()

