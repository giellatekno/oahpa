# -*- coding: utf-8 -*-

# TODO: models
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

from operator import itemgetter

import datetime

## 
## Survey
##

question_types = [
    ('freeform text', 'text'),
    ('single choice', 'choice'),
    ('multiple choice', 'multichoice'),
    ('yes/no', 'boolean'),
]

class Survey(models.Model):
    title = models.CharField()
    description = models.TextField()

    questions = models.ManyToManyField(SurveyQuestion, related_name='questions')

class SurveyQuestion(models.Model):
	question_text = models.TextField()
	question_answer = models.ManyToManyField(SurveyQuestionAnswerValue, related_name='answers')

	question_type = models.CharField(choices=question_types)

class SurveyQuestionAnswerValue(models.Model):
	question = models.ForeignKey(SurveyQuestion)
	answer_text = models.TextField()

class UserSurvey(models.Model):
    survey = models.ForeignKey(Survey)
    user = models.ForeignKey(User)

    completed = models.DateTimeField(auto_now_add=True)

    answers = manytomany UserSurveyQuestionAnswer

class UserSurveyQuestionAnswer(models.Model):
	""" This object will store user answers, regardless of whether it
	comes from a database-specified choice, or user-entered free text.
	"""

    

