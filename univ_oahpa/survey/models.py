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
    title = models.CharField()
    description = models.TextField()

    questions = models.ManyToManyField(SurveyQuestion, related_name='questions')

class SurveyQuestion(models.Model):
	""" Contains the survey question, and question type. Connects to any
	possible answer objects.
	"""
	question_text = models.TextField()
	question_type = models.CharField(choices=question_types)

	question_answer = models.ManyToManyField(SurveyQuestionAnswerValue, related_name='answers')


class SurveyQuestionAnswerValue(models.Model):
	""" A model for defining answer values for question types that allow
	for a choice. UserSurveyQuestionAnswer will only be auto-populated
	from this, not related by foreignkey
	"""
	question = models.ForeignKey(SurveyQuestion)
	answer_text = models.TextField()

## User survey results

class UserSurvey(models.Model):
	""" This is the user survey instance, to connect individual user
	answers together.
	"""
    survey = models.ForeignKey(Survey)
    user = models.ForeignKey(User)

    completed = models.DateTimeField(auto_now_add=True)

    answers = models.ManyToManyField(UserSurveyQuestionAnswer, related_name='user_answers')

class UserSurveyQuestionAnswer(models.Model):
	""" This object will store user answers, regardless of whether it
	comes from a database-specified choice, or user-entered free text.
	"""

    user_survey = models.ForeignKey(UserSurvey)
    question = models.ForeignKey(SurveyQuestion)
    answer_text = models.TextField()


