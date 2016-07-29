# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('title_sme', models.CharField(max_length=50, null=True)),
                ('title_no', models.CharField(max_length=50, null=True)),
                ('title_sv', models.CharField(max_length=50, null=True)),
                ('title_en', models.CharField(max_length=50, null=True)),
                ('title_fi', models.CharField(max_length=50, null=True)),
                ('description', models.TextField()),
                ('description_sme', models.TextField(null=True)),
                ('description_no', models.TextField(null=True)),
                ('description_sv', models.TextField(null=True)),
                ('description_en', models.TextField(null=True)),
                ('description_fi', models.TextField(null=True)),
                ('target_course', models.ForeignKey(blank=True, to='courses.Course', help_text=b'If you wish to make this visble only to users in a certain course, select it here.', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.TextField()),
                ('question_text_sme', models.TextField(null=True)),
                ('question_text_no', models.TextField(null=True)),
                ('question_text_sv', models.TextField(null=True)),
                ('question_text_en', models.TextField(null=True)),
                ('question_text_fi', models.TextField(null=True)),
                ('question_type', models.CharField(help_text=b'<strong>NB</strong>: For single and multiple choice\nanswers, you must specify answer options. Yes/no and Freeform need no\nchoices.', max_length=18, choices=[(b'text', b'freeform text'), (b'choice', b'single choice'), (b'multichoice', b'multiple choice'), (b'boolean', b'yes/no')])),
                ('survey', models.ForeignKey(related_name='questions', to='survey.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestionAnswerValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_text', models.TextField()),
                ('answer_text_sme', models.TextField(null=True)),
                ('answer_text_no', models.TextField(null=True)),
                ('answer_text_sv', models.TextField(null=True)),
                ('answer_text_en', models.TextField(null=True)),
                ('answer_text_fi', models.TextField(null=True)),
                ('question', models.ForeignKey(related_name='answer_values', to='survey.SurveyQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='UserSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.DateTimeField(auto_now_add=True)),
                ('survey', models.ForeignKey(related_name='responses', to='survey.Survey')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Response',
                'verbose_name_plural': 'Responses',
            },
        ),
        migrations.CreateModel(
            name='UserSurveyQuestionAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_text', models.TextField()),
                ('question', models.ForeignKey(to='survey.SurveyQuestion')),
                ('user_survey', models.ForeignKey(related_name='user_answers', to='survey.UserSurvey')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='usersurvey',
            unique_together=set([('user', 'survey')]),
        ),
    ]
