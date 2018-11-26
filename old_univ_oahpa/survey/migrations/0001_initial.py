# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Survey'
        db.create_table('survey_survey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('target_course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Course'], null=True, blank=True)),
        ))
        db.send_create_signal('survey', ['Survey'])

        # Adding model 'SurveyQuestion'
        db.create_table('survey_surveyquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', to=orm['survey.Survey'])),
            ('question_text', self.gf('django.db.models.fields.TextField')()),
            ('question_type', self.gf('django.db.models.fields.CharField')(max_length=18)),
        ))
        db.send_create_signal('survey', ['SurveyQuestion'])

        # Adding model 'SurveyQuestionAnswerValue'
        db.create_table('survey_surveyquestionanswervalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answer_values', to=orm['survey.SurveyQuestion'])),
            ('answer_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('survey', ['SurveyQuestionAnswerValue'])

        # Adding model 'UserSurvey'
        db.create_table('survey_usersurvey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='responses', to=orm['survey.Survey'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('completed', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('survey', ['UserSurvey'])

        # Adding unique constraint on 'UserSurvey', fields ['user', 'survey']
        db.create_unique('survey_usersurvey', ['user_id', 'survey_id'])

        # Adding model 'UserSurveyQuestionAnswer'
        db.create_table('survey_usersurveyquestionanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_survey', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_answers', to=orm['survey.UserSurvey'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.SurveyQuestion'])),
            ('answer_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('survey', ['UserSurveyQuestionAnswer'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserSurvey', fields ['user', 'survey']
        db.delete_unique('survey_usersurvey', ['user_id', 'survey_id'])

        # Deleting model 'Survey'
        db.delete_table('survey_survey')

        # Deleting model 'SurveyQuestion'
        db.delete_table('survey_surveyquestion')

        # Deleting model 'SurveyQuestionAnswerValue'
        db.delete_table('survey_surveyquestionanswervalue')

        # Deleting model 'UserSurvey'
        db.delete_table('survey_usersurvey')

        # Deleting model 'UserSurveyQuestionAnswer'
        db.delete_table('survey_usersurveyquestionanswer')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target_course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Course']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'survey.surveyquestion': {
            'Meta': {'object_name': 'SurveyQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_text': ('django.db.models.fields.TextField', [], {}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': "orm['survey.Survey']"})
        },
        'survey.surveyquestionanswervalue': {
            'Meta': {'object_name': 'SurveyQuestionAnswerValue'},
            'answer_text': ('django.db.models.fields.TextField', [], {}),
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