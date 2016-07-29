# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'activity',
                'verbose_name_plural': 'activities',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default='Fluent in Southern S\xe1mi in 10 days', max_length=50)),
                ('identifier', models.CharField(default=b'SAM-1234', max_length=12)),
                ('site_link', models.URLField(null=True, blank=True)),
                ('end_date', models.DateTimeField(default=None, null=True, blank=True)),
                ('token', models.CharField(help_text=b'Token generated for share links. Only generate these, do not enter manually.', max_length=128, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseGoal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=42)),
                ('short_name_sme', models.CharField(max_length=42, null=True)),
                ('short_name_no', models.CharField(max_length=42, null=True)),
                ('short_name_sv', models.CharField(max_length=42, null=True)),
                ('short_name_en', models.CharField(max_length=42, null=True)),
                ('short_name_fi', models.CharField(max_length=42, null=True)),
                ('description', models.TextField(help_text='This is a plain-text description shown to students\ndescribing their goal.')),
                ('description_sme', models.TextField(help_text='This is a plain-text description shown to students\ndescribing their goal.', null=True)),
                ('description_no', models.TextField(help_text='This is a plain-text description shown to students\ndescribing their goal.', null=True)),
                ('description_sv', models.TextField(help_text='This is a plain-text description shown to students\ndescribing their goal.', null=True)),
                ('description_en', models.TextField(help_text='This is a plain-text description shown to students\ndescribing their goal.', null=True)),
                ('description_fi', models.TextField(help_text='This is a plain-text description shown to students\ndescribing their goal.', null=True)),
                ('threshold', models.FloatField(help_text=b'Complete goals must average this amount.', null=True, blank=True)),
                ('percent_goals_completed', models.FloatField(default=80.0, help_text=b'This percentage of associated goals must be completed', null=True, blank=True)),
                ('course', models.ForeignKey(blank=True, to='courses.Course', null=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseGoalGoal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coursegoal', models.ForeignKey(related_name='goals', to='courses.CourseGoal')),
            ],
        ),
        migrations.CreateModel(
            name='CourseRelationship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('end_date', models.DateTimeField(help_text=b'Leave this blank to copy the course end date.If you wish to specify no end date, you will need to come back, and remove it after adding the instructor.', null=True, blank=True)),
                ('course', models.ForeignKey(to='courses.Course')),
                ('relationship_type', models.ForeignKey(to='auth.Group')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=128)),
                ('short_name_sme', models.CharField(max_length=128, null=True)),
                ('short_name_no', models.CharField(max_length=128, null=True)),
                ('short_name_sv', models.CharField(max_length=128, null=True)),
                ('short_name_en', models.CharField(max_length=128, null=True)),
                ('short_name_fi', models.CharField(max_length=128, null=True)),
                ('remote_task', models.BooleanField(default=False)),
                ('remote_page', models.TextField()),
                ('url_base', models.CharField(max_length=24)),
                ('main_type', models.CharField(max_length=24)),
                ('sub_type', models.CharField(max_length=24)),
                ('threshold', models.FloatField(default=80.0, help_text=b'Percentage user must get correct. E.g. 80.0')),
                ('minimum_sets_attempted', models.IntegerField(default=5, help_text=b'Amount of sets user must try to be finished.')),
                ('correct_first_try', models.BooleanField(default=False, help_text=b'Only count answers correct on the first try')),
                ('course', models.ForeignKey(blank=True, to='courses.Course', null=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GoalParameter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parameter', models.CharField(max_length=64)),
                ('value', models.CharField(max_length=64)),
                ('goal', models.ForeignKey(related_name='params', to='courses.Goal')),
            ],
        ),
        migrations.CreateModel(
            name='UserActivityLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_correct', models.BooleanField()),
                ('correct_answer', models.TextField()),
                ('user_input', models.TextField()),
                ('question', models.TextField()),
                ('question_set', models.IntegerField(default=1)),
                ('question_tries', models.IntegerField(default=1)),
                ('in_game', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFeedbackLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_input', models.TextField()),
                ('correct_answer', models.TextField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('feedback_texts', models.TextField()),
                ('goal', models.ForeignKey(blank=True, to='courses.Goal', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGoalInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('opened', models.BooleanField(default=True)),
                ('attempt_count', models.IntegerField(default=1)),
                ('progress', models.DecimalField(default=0.0, max_digits=11, decimal_places=4)),
                ('is_complete', models.BooleanField(default=False)),
                ('rounds', models.IntegerField(default=1)),
                ('total_answered', models.IntegerField(default=0)),
                ('correct', models.IntegerField(default=0)),
                ('correct_first_try', models.IntegerField(default=0)),
                ('last_attempt', models.DateTimeField(auto_now_add=True)),
                ('grade', models.IntegerField(null=True, blank=True)),
                ('goal', models.ForeignKey(to='courses.Goal')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('score', models.IntegerField()),
                ('total', models.IntegerField(default=5)),
                ('game', models.ForeignKey(to='courses.Activity')),
            ],
            options={
                'ordering': ['-datetime'],
                'permissions': (('can_change_score', 'Can change grade'),),
            },
        ),
        migrations.CreateModel(
            name='UserGradeSummary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('average', models.FloatField(null=True)),
                ('minimum', models.FloatField(null=True)),
                ('maximum', models.FloatField(null=True)),
                ('count', models.IntegerField(default=0)),
                ('game', models.ForeignKey(to='courses.Activity')),
            ],
            options={
                'ordering': ['average'],
                'verbose_name_plural': 'User grade summaries',
            },
        ),
        migrations.CreateModel(
            name='UserLogin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login_count', models.IntegerField(default=0)),
                ('last_login', models.DateTimeField(null=True)),
                ('site_cookie', models.IntegerField(null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='userlogin',
            name='user',
            field=models.ForeignKey(to='courses.UserProfile'),
        ),
        migrations.AddField(
            model_name='usergradesummary',
            name='user',
            field=models.ForeignKey(to='courses.UserProfile'),
        ),
        migrations.AddField(
            model_name='usergrade',
            name='user',
            field=models.ForeignKey(to='courses.UserProfile'),
        ),
        migrations.AddField(
            model_name='useractivitylog',
            name='usergoalinstance',
            field=models.ForeignKey(to='courses.UserGoalInstance'),
        ),
        migrations.AddField(
            model_name='coursegoalgoal',
            name='goal',
            field=models.ForeignKey(related_name='courses', to='courses.Goal'),
        ),
        migrations.AlterUniqueTogether(
            name='usergoalinstance',
            unique_together=set([('user', 'goal', 'attempt_count')]),
        ),
        migrations.AlterUniqueTogether(
            name='courserelationship',
            unique_together=set([('user', 'course', 'relationship_type')]),
        ),
    ]
