# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('courses_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('login_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('site_cookie', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('courses', ['UserProfile'])

        # Adding model 'UserLogin'
        db.create_table('courses_userlogin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.UserProfile'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('courses', ['UserLogin'])

        # Adding model 'UserGradeSummary'
        db.create_table('courses_usergradesummary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.UserProfile'])),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Activity'])),
            ('average', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('minimum', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('maximum', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('courses', ['UserGradeSummary'])

        # Adding model 'UserGrade'
        db.create_table('courses_usergrade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.UserProfile'])),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Activity'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('total', self.gf('django.db.models.fields.IntegerField')(default=5)),
        ))
        db.send_create_signal('courses', ['UserGrade'])

        # Adding model 'Activity'
        db.create_table('courses_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('courses', ['Activity'])

        # Adding model 'Course'
        db.create_table('courses_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=u'Fluent in Southern S\xe1mi in 10 days', max_length=50)),
            ('identifier', self.gf('django.db.models.fields.CharField')(default='SAM-1234', max_length=12)),
            ('site_link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('courses', ['Course'])

        # Adding model 'CourseRelationship'
        db.create_table('courses_courserelationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('relationship_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Course'])),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('courses', ['CourseRelationship'])

        # Adding unique constraint on 'CourseRelationship', fields ['user', 'course', 'relationship_type']
        db.create_unique('courses_courserelationship', ['user_id', 'course_id', 'relationship_type_id'])

        # Adding model 'CourseGoal'
        db.create_table('courses_coursegoal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Course'], null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=42)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('threshold', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('percent_goals_completed', self.gf('django.db.models.fields.FloatField')(default=80.0, null=True, blank=True)),
        ))
        db.send_create_signal('courses', ['CourseGoal'])

        # Adding model 'CourseGoalGoal'
        db.create_table('courses_coursegoalgoal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('coursegoal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='goals', to=orm['courses.CourseGoal'])),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='courses', to=orm['courses.Goal'])),
        ))
        db.send_create_signal('courses', ['CourseGoalGoal'])

        # Adding model 'Goal'
        db.create_table('courses_goal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Course'], null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('url_base', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('main_type', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('sub_type', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('threshold', self.gf('django.db.models.fields.FloatField')(default=80.0)),
            ('minimum_sets_attempted', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('correct_first_try', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('courses', ['Goal'])

        # Adding model 'UserGoalInstance'
        db.create_table('courses_usergoalinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Goal'])),
            ('opened', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('attempt_count', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('progress', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=11, decimal_places=4)),
            ('is_complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rounds', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('total_answered', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('correct', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('correct_first_try', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_attempt', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('grade', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('courses', ['UserGoalInstance'])

        # Adding unique constraint on 'UserGoalInstance', fields ['user', 'goal', 'attempt_count']
        db.create_unique('courses_usergoalinstance', ['user_id', 'goal_id', 'attempt_count'])

        # Adding model 'GoalParameter'
        db.create_table('courses_goalparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='params', to=orm['courses.Goal'])),
            ('parameter', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('courses', ['GoalParameter'])

        # Adding model 'UserFeedbackLog'
        db.create_table('courses_userfeedbacklog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Goal'], null=True, blank=True)),
            ('user_input', self.gf('django.db.models.fields.TextField')()),
            ('correct_answer', self.gf('django.db.models.fields.TextField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('feedback_texts', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('courses', ['UserFeedbackLog'])

        # Adding model 'UserActivityLog'
        db.create_table('courses_useractivitylog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('usergoalinstance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.UserGoalInstance'])),
            ('is_correct', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('correct_answer', self.gf('django.db.models.fields.TextField')()),
            ('user_input', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('question_set', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('question_tries', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('in_game', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('courses', ['UserActivityLog'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserGoalInstance', fields ['user', 'goal', 'attempt_count']
        db.delete_unique('courses_usergoalinstance', ['user_id', 'goal_id', 'attempt_count'])

        # Removing unique constraint on 'CourseRelationship', fields ['user', 'course', 'relationship_type']
        db.delete_unique('courses_courserelationship', ['user_id', 'course_id', 'relationship_type_id'])

        # Deleting model 'UserProfile'
        db.delete_table('courses_userprofile')

        # Deleting model 'UserLogin'
        db.delete_table('courses_userlogin')

        # Deleting model 'UserGradeSummary'
        db.delete_table('courses_usergradesummary')

        # Deleting model 'UserGrade'
        db.delete_table('courses_usergrade')

        # Deleting model 'Activity'
        db.delete_table('courses_activity')

        # Deleting model 'Course'
        db.delete_table('courses_course')

        # Deleting model 'CourseRelationship'
        db.delete_table('courses_courserelationship')

        # Deleting model 'CourseGoal'
        db.delete_table('courses_coursegoal')

        # Deleting model 'CourseGoalGoal'
        db.delete_table('courses_coursegoalgoal')

        # Deleting model 'Goal'
        db.delete_table('courses_goal')

        # Deleting model 'UserGoalInstance'
        db.delete_table('courses_usergoalinstance')

        # Deleting model 'GoalParameter'
        db.delete_table('courses_goalparameter')

        # Deleting model 'UserFeedbackLog'
        db.delete_table('courses_userfeedbacklog')

        # Deleting model 'UserActivityLog'
        db.delete_table('courses_useractivitylog')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percent_goals_completed': ('django.db.models.fields.FloatField', [], {'default': '80.0', 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
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