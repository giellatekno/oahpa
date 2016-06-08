# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('place', models.CharField(max_length=100, blank=True)),
                ('game', models.CharField(max_length=10, blank=True)),
                ('language', models.CharField(max_length=10, blank=True)),
                ('email', models.CharField(max_length=50, blank=True)),
                ('message', models.CharField(max_length=500, blank=True)),
                ('confirmation', models.BooleanField()),
                ('confirmed_by', models.CharField(max_length=20, blank=True)),
                ('comments', models.CharField(max_length=100, blank=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('confirmation_date', models.DateField(null=True, blank=True)),
            ],
        ),
    ]
