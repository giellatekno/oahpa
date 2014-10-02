# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SurveyQuestion.question_text_sme'
        db.add_column('survey_surveyquestion', 'question_text_sme',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SurveyQuestion.question_text_no'
        db.add_column('survey_surveyquestion', 'question_text_no',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SurveyQuestion.question_text_sv'
        db.add_column('survey_surveyquestion', 'question_text_sv',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SurveyQuestion.question_text_en'
        db.add_column('survey_surveyquestion', 'question_text_en',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SurveyQuestion.question_text_fi'
        db.add_column('survey_surveyquestion', 'question_text_fi',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SurveyQuestionAnswerValue.answer_text_sme'
        db.add_column('survey_surveyquestionanswervalue', 'answer_text_sme',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SurveyQuestionAnswerValue.answer_text_no'
        db.add_column('survey_surveyquestionanswervalue', 'answer_text_no',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SurveyQuestionAnswerValue.answer_text_sv'
        db.add_column('survey_surveyquestionanswervalue', 'answer_text_sv',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SurveyQuestionAnswerValue.answer_text_en'
        db.add_column('survey_surveyquestionanswervalue', 'answer_text_en',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'SurveyQuestionAnswerValue.answer_text_fi'
        db.add_column('survey_surveyquestionanswervalue', 'answer_text_fi',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Survey.title_sme'
        db.add_column('survey_survey', 'title_sme',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Survey.title_no'
        db.add_column('survey_survey', 'title_no',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Survey.title_sv'
        db.add_column('survey_survey', 'title_sv',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Survey.title_en'
        db.add_column('survey_survey', 'title_en',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Survey.title_fi'
        db.add_column('survey_survey', 'title_fi',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Survey.description_sme'
        db.add_column('survey_survey', 'description_sme',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Survey.description_no'
        db.add_column('survey_survey', 'description_no',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Survey.description_sv'
        db.add_column('survey_survey', 'description_sv',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Survey.description_en'
        db.add_column('survey_survey', 'description_en',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Survey.description_fi'
        db.add_column('survey_survey', 'description_fi',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SurveyQuestion.question_text_sme'
        db.delete_column('survey_surveyquestion', 'question_text_sme')

        # Deleting field 'SurveyQuestion.question_text_no'
        db.delete_column('survey_surveyquestion', 'question_text_no')

        # Deleting field 'SurveyQuestion.question_text_sv'
        db.delete_column('survey_surveyquestion', 'question_text_sv')

        # Deleting field 'SurveyQuestion.question_text_en'
        db.delete_column('survey_surveyquestion', 'question_text_en')

        # Deleting field 'SurveyQuestion.question_text_fi'
        db.delete_column('survey_surveyquestion', 'question_text_fi')

        # Deleting field 'SurveyQuestionAnswerValue.answer_text_sme'
        db.delete_column('survey_surveyquestionanswervalue', 'answer_text_sme')

        # Deleting field 'SurveyQuestionAnswerValue.answer_text_no'
        db.delete_column('survey_surveyquestionanswervalue', 'answer_text_no')

        # Deleting field 'SurveyQuestionAnswerValue.answer_text_sv'
        db.delete_column('survey_surveyquestionanswervalue', 'answer_text_sv')

        # Deleting field 'SurveyQuestionAnswerValue.answer_text_en'
        db.delete_column('survey_surveyquestionanswervalue', 'answer_text_en')

        # Deleting field 'SurveyQuestionAnswerValue.answer_text_fi'
        db.delete_column('survey_surveyquestionanswervalue', 'answer_text_fi')

        # Deleting field 'Survey.title_sme'
        db.delete_column('survey_survey', 'title_sme')

        # Deleting field 'Survey.title_no'
        db.delete_column('survey_survey', 'title_no')

        # Deleting field 'Survey.title_sv'
        db.delete_column('survey_survey', 'title_sv')

        # Deleting field 'Survey.title_en'
        db.delete_column('survey_survey', 'title_en')

        # Deleting field 'Survey.title_fi'
        db.delete_column('survey_survey', 'title_fi')

        # Deleting field 'Survey.description_sme'
        db.delete_column('survey_survey', 'description_sme')

        # Deleting field 'Survey.description_no'
        db.delete_column('survey_survey', 'description_no')

        # Deleting field 'Survey.description_sv'
        db.delete_column('survey_survey', 'description_sv')

        # Deleting field 'Survey.description_en'
        db.delete_column('survey_survey', 'description_en')

        # Deleting field 'Survey.description_fi'
        db.delete_column('survey_survey', 'description_fi')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'courses.course': {
            'Meta': {'object_name': 'Course'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'default': "'SAM-1234'", 'max_length': '12'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u'Fluent in Southern S\\xe1mi in 10 days'", 'max_length': '50'}),
            'site_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'survey.survey': {
            'Meta': {'object_name': 'Survey'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fi': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_no': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sme': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target_course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Course']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title_fi': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title_sme': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title_sv': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'survey.surveyquestion': {
            'Meta': {'object_name': 'SurveyQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_text': ('django.db.models.fields.TextField', [], {}),
            'question_text_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'question_text_fi': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'question_text_no': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'question_text_sme': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'question_text_sv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': "orm['survey.Survey']"})
        },
        'survey.surveyquestionanswervalue': {
            'Meta': {'object_name': 'SurveyQuestionAnswerValue'},
            'answer_text': ('django.db.models.fields.TextField', [], {}),
            'answer_text_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'answer_text_fi': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'answer_text_no': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'answer_text_sme': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'answer_text_sv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answer_values'", 'to': "orm['survey.SurveyQuestion']"})
        },
        'survey.usersurvey': {
            'Meta': {'unique_together': "(('user', 'survey'),)", 'object_name': 'UserSurvey'},
            'completed': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responses'", 'to': "orm['survey.Survey']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'survey.usersurveyquestionanswer': {
            'Meta': {'object_name': 'UserSurveyQuestionAnswer'},
            'answer_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['survey.SurveyQuestion']"}),
            'user_survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_answers'", 'to': "orm['survey.UserSurvey']"})
        }
    }

    complete_apps = ['survey']