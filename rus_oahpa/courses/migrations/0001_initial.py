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
                'managed': True,
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
                ('end_date', models.DateTimeField(default=None, null=True)),
            ],
            options={
                'managed': True,
            },
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
            options={
                'managed': True,
            },
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
                'managed': True,
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
                'managed': True,
                'verbose_name_plural': 'User grade summaries',
            },
        ),
        migrations.CreateModel(
            name='UserLogin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
            ],
            options={
                'managed': True,
            },
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
            options={
                'managed': True,
            },
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
        migrations.AlterUniqueTogether(
            name='courserelationship',
            unique_together=set([('user', 'course', 'relationship_type')]),
        ),
    ]
