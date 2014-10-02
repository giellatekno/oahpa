# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Goal.short_name_sme'
        db.add_column('courses_goal', 'short_name_sme',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Goal.short_name_no'
        db.add_column('courses_goal', 'short_name_no',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Goal.short_name_sv'
        db.add_column('courses_goal', 'short_name_sv',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Goal.short_name_en'
        db.add_column('courses_goal', 'short_name_en',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Goal.short_name_fi'
        db.add_column('courses_goal', 'short_name_fi',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding field 'CourseGoal.short_name_sme'
        db.add_column('courses_coursegoal', 'short_name_sme',
                      self.gf('django.db.models.fields.CharField')(max_length=42, null=True, blank=True),
                      keep_default=False)

        # Adding field 'CourseGoal.short_name_no'
        db.add_column('courses_coursegoal', 'short_name_no',
                      self.gf('django.db.models.fields.CharField')(max_length=42, null=True, blank=True),
                      keep_default=False)

        # Adding field 'CourseGoal.short_name_sv'
        db.add_column('courses_coursegoal', 'short_name_sv',
                      self.gf('django.db.models.fields.CharField')(max_length=42, null=True, blank=True),
                      keep_default=False)

        # Adding field 'CourseGoal.short_name_en'
        db.add_column('courses_coursegoal', 'short_name_en',
                      self.gf('django.db.models.fields.CharField')(max_length=42, null=True, blank=True),
                      keep_default=False)

        # Adding field 'CourseGoal.short_name_fi'
        db.add_column('courses_coursegoal', 'short_name_fi',
                      self.gf('django.db.models.fields.CharField')(max_length=42, null=True, blank=True),
                      keep_default=False)

        # Adding field 'CourseGoal.description_sme'
        db.add_column('courses_coursegoal', 'description_sme',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CourseGoal.description_no'
        db.add_column('courses_coursegoal', 'description_no',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CourseGoal.description_sv'
        db.add_column('courses_coursegoal', 'description_sv',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CourseGoal.description_en'
        db.add_column('courses_coursegoal', 'description_en',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CourseGoal.description_fi'
        db.add_column('courses_coursegoal', 'description_fi',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Goal.short_name_sme'
        db.delete_column('courses_goal', 'short_name_sme')

        # Deleting field 'Goal.short_name_no'
        db.delete_column('courses_goal', 'short_name_no')

        # Deleting field 'Goal.short_name_sv'
        db.delete_column('courses_goal', 'short_name_sv')

        # Deleting field 'Goal.short_name_en'
        db.delete_column('courses_goal', 'short_name_en')

        # Deleting field 'Goal.short_name_fi'
        db.delete_column('courses_goal', 'short_name_fi')

        # Deleting field 'CourseGoal.short_name_sme'
        db.delete_column('courses_coursegoal', 'short_name_sme')

        # Deleting field 'CourseGoal.short_name_no'
        db.delete_column('courses_coursegoal', 'short_name_no')

        # Deleting field 'CourseGoal.short_name_sv'
        db.delete_column('courses_coursegoal', 'short_name_sv')

        # Deleting field 'CourseGoal.short_name_en'
        db.delete_column('courses_coursegoal', 'short_name_en')

        # Deleting field 'CourseGoal.short_name_fi'
        db.delete_column('courses_coursegoal', 'short_name_fi')

        # Deleting field 'CourseGoal.description_sme'
        db.delete_column('courses_coursegoal', 'description_sme')

        # Deleting field 'CourseGoal.description_no'
        db.delete_column('courses_coursegoal', 'description_no')

        # Deleting field 'CourseGoal.description_sv'
        db.delete_column('courses_coursegoal', 'description_sv')

        # Deleting field 'CourseGoal.description_en'
        db.delete_column('courses_coursegoal', 'description_en')

        # Deleting field 'CourseGoal.description_fi'
        db.delete_column('courses_coursegoal', 'description_fi')


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
        'courses.activity': {
            'Meta': {'object_name': 'Activity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
        'courses.coursegoal': {
            'Meta': {'object_name': 'CourseGoal'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Course']", 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fi': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_no': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sme': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent_goals_completed': ('django.db.models.fields.FloatField', [], {'default': '80.0', 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
            'short_name_fi': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
            'short_name_no': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
            'short_name_sme': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
            'short_name_sv': ('django.db.models.fields.CharField', [], {'max_length': '42', 'null': 'True', 'blank': 'True'}),
            'threshold': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'courses.coursegoalgoal': {
            'Meta': {'object_name': 'CourseGoalGoal'},
            'coursegoal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'goals'", 'to': "orm['courses.CourseGoal']"}),
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': "orm['courses.Goal']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'courses.courserelationship': {
            'Meta': {'unique_together': "(('user', 'course', 'relationship_type'),)", 'object_name': 'CourseRelationship'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Course']"}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relationship_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Group']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'courses.goal': {
            'Meta': {'object_name': 'Goal'},
            'correct_first_try': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Course']", 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_type': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'minimum_sets_attempted': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'short_name_fi': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'short_name_no': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'short_name_sme': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'short_name_sv': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'sub_type': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'threshold': ('django.db.models.fields.FloatField', [], {'default': '80.0'}),
            'url_base': ('django.db.models.fields.CharField', [], {'max_length': '24'})
        },
        'courses.goalparameter': {
            'Meta': {'object_name': 'GoalParameter'},
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'params'", 'to': "orm['courses.Goal']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'courses.useractivitylog': {
            'Meta': {'object_name': 'UserActivityLog'},
            'correct_answer': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_game': ('django.db.models.fields.TextField', [], {}),
            'is_correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'question_set': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'question_tries': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'user_input': ('django.db.models.fields.TextField', [], {}),
            'usergoalinstance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.UserGoalInstance']"})
        },
        'courses.userfeedbacklog': {
            'Meta': {'object_name': 'UserFeedbackLog'},
            'correct_answer': ('django.db.models.fields.TextField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feedback_texts': ('django.db.models.fields.TextField', [], {}),
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Goal']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'user_input': ('django.db.models.fields.TextField', [], {})
        },
        'courses.usergoalinstance': {
            'Meta': {'unique_together': "(('user', 'goal', 'attempt_count'),)", 'object_name': 'UserGoalInstance'},
            'attempt_count': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'correct': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'correct_first_try': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Goal']"}),
            'grade': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_attempt': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'opened': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'progress': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '11', 'decimal_places': '4'}),
            'rounds': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'total_answered': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'courses.usergrade': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'UserGrade'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.UserProfile']"})
        },
        'courses.usergradesummary': {
            'Meta': {'ordering': "['average']", 'object_name': 'UserGradeSummary'},
            'average': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'minimum': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.UserProfile']"})
        },
        'courses.userlogin': {
            'Meta': {'object_name': 'UserLogin'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.UserProfile']"})
        },
        'courses.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'login_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'site_cookie': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['courses']