# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lang', models.CharField(max_length=5)),
                ('comment', models.CharField(max_length=100)),
                ('level', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Dialect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dialect', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Dialogue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Feedbackmsg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msgid', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Feedbacktext',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.CharField(max_length=200)),
                ('language', models.CharField(max_length=6)),
                ('order', models.CharField(max_length=3, blank=True)),
                ('feedbackmsg', models.ForeignKey(to='rus_drill.Feedbackmsg')),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fullform', models.CharField(max_length=200)),
                ('dialects', models.ManyToManyField(to='rus_drill.Dialect', null=True)),
                ('feedback', models.ManyToManyField(to='rus_drill.Feedbackmsg', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grammarlinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('address', models.CharField(max_length=800, null=True, blank=True)),
                ('language', models.CharField(max_length=5, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LinkUtterance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target', models.CharField(max_length=20, null=True, blank=True)),
                ('variable', models.CharField(max_length=20, null=True, blank=True)),
                ('constant', models.CharField(max_length=20, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game', models.CharField(max_length=30)),
                ('date', models.DateField(null=True, blank=True)),
                ('userinput', models.CharField(max_length=200)),
                ('iscorrect', models.BooleanField()),
                ('correct', models.TextField()),
                ('example', models.CharField(max_length=200, null=True)),
                ('feedback', models.CharField(max_length=200, null=True)),
                ('comment', models.CharField(max_length=200)),
                ('messageid', models.CharField(max_length=100, null=True)),
                ('lang', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='MorphPhonTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stem', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=20)),
                ('animate', models.CharField(max_length=20)),
                ('inflection_class', models.CharField(max_length=20)),
                ('declension', models.CharField(max_length=20)),
                ('reflexive', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='QElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('syntax', models.CharField(max_length=50)),
                ('identifier', models.CharField(max_length=20)),
                ('task', models.CharField(max_length=20)),
                ('gametype', models.CharField(max_length=7)),
                ('gender', models.CharField(max_length=5)),
                ('animate', models.CharField(max_length=5)),
                ('game', models.CharField(max_length=20)),
                ('agreement', models.ForeignKey(related_name='agreement_set', blank=True, to='rus_drill.QElement', null=True)),
                ('copy', models.ForeignKey(related_name='copy_set', blank=True, to='rus_drill.QElement', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qid', models.CharField(max_length=200)),
                ('level', models.IntegerField(max_length=3)),
                ('task', models.CharField(max_length=20)),
                ('string', models.CharField(max_length=200)),
                ('qtype', models.CharField(max_length=20)),
                ('qatype', models.CharField(max_length=20)),
                ('gametype', models.CharField(max_length=7)),
                ('lemmacount', models.IntegerField(max_length=3)),
                ('question', models.ForeignKey(related_name='answer_set', blank=True, to='rus_drill.Question', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Semtype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('semtype', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string', models.CharField(unique=True, max_length=40)),
                ('attributive', models.CharField(max_length=5)),
                ('case', models.CharField(max_length=5)),
                ('grade', models.CharField(max_length=10)),
                ('infinite', models.CharField(max_length=10)),
                ('mood', models.CharField(max_length=5)),
                ('number', models.CharField(max_length=5)),
                ('personnumber', models.CharField(max_length=8)),
                ('gender', models.CharField(max_length=5)),
                ('animate', models.CharField(max_length=5)),
                ('pos', models.CharField(max_length=12)),
                ('subclass', models.CharField(max_length=10)),
                ('tense', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Tagname',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tagname', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Tagset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tagset', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topicname', models.CharField(max_length=50, null=True, blank=True)),
                ('number', models.IntegerField(max_length=3, null=True)),
                ('image', models.CharField(max_length=50, null=True, blank=True)),
                ('dialogue', models.ForeignKey(to='rus_drill.Dialogue')),
                ('formlist', models.ManyToManyField(to='rus_drill.Form')),
            ],
        ),
        migrations.CreateModel(
            name='UElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('syntax', models.CharField(max_length=50)),
                ('tag', models.ForeignKey(blank=True, to='rus_drill.Tag', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Utterance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('utterance', models.CharField(max_length=500, null=True, blank=True)),
                ('utttype', models.CharField(max_length=20, null=True, blank=True)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('formlist', models.ManyToManyField(to='rus_drill.Form')),
                ('links', models.ManyToManyField(to='rus_drill.LinkUtterance')),
                ('topic', models.ForeignKey(to='rus_drill.Topic')),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wordid', models.CharField(max_length=200, db_index=True)),
                ('language', models.CharField(default=b'rus', max_length=5, db_index=True)),
                ('lemma', models.CharField(max_length=200, db_index=True)),
                ('lemma_stressed', models.CharField(max_length=200, db_index=True)),
                ('presentationform', models.CharField(max_length=5)),
                ('pos', models.CharField(max_length=12)),
                ('stem', models.CharField(max_length=20)),
                ('animate', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=20)),
                ('declension', models.CharField(max_length=20)),
                ('loc2', models.BooleanField(default=False)),
                ('gen2', models.BooleanField(default=False)),
                ('reflexive', models.NullBooleanField()),
                ('inflection_class', models.CharField(max_length=20)),
                ('zaliznjak', models.CharField(max_length=20)),
                ('hid', models.IntegerField(default=None, max_length=3, null=True)),
                ('chapter', models.CharField(max_length=10)),
                ('compare', models.CharField(max_length=5)),
                ('frequency', models.CharField(max_length=10)),
                ('geography', models.CharField(max_length=10)),
                ('tcomm', models.BooleanField(default=False)),
                ('aspect', models.CharField(max_length=20)),
                ('motion', models.CharField(max_length=20)),
                ('dialects', models.ManyToManyField(to='rus_drill.Dialect', null=True)),
                ('morphophon', models.ForeignKey(to='rus_drill.MorphPhonTag', null=True)),
                ('semtype', models.ManyToManyField(to='rus_drill.Semtype')),
                ('source', models.ManyToManyField(to='rus_drill.Source')),
            ],
        ),
        migrations.CreateModel(
            name='WordQElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qelement', models.ForeignKey(to='rus_drill.QElement', null=True)),
                ('word', models.ForeignKey(to='rus_drill.Word', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WordTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=5, db_index=True)),
                ('wordid', models.CharField(max_length=200, db_index=True)),
                ('lemma', models.CharField(max_length=200, blank=True)),
                ('phrase', models.TextField(blank=True)),
                ('explanation', models.TextField(blank=True)),
                ('pos', models.CharField(max_length=12)),
                ('frequency', models.CharField(max_length=10)),
                ('geography', models.CharField(max_length=10)),
                ('tcomm', models.BooleanField(default=False)),
                ('tcomm_pref', models.BooleanField(default=False)),
                ('semtype', models.ManyToManyField(to='rus_drill.Semtype')),
                ('source', models.ManyToManyField(to='rus_drill.Source')),
                ('word', models.ForeignKey(to='rus_drill.Word')),
            ],
        ),
        migrations.AddField(
            model_name='uelement',
            name='utterance',
            field=models.ForeignKey(to='rus_drill.Utterance', null=True),
        ),
        migrations.AddField(
            model_name='tagname',
            name='tagset',
            field=models.ForeignKey(to='rus_drill.Tagset'),
        ),
        migrations.AddField(
            model_name='question',
            name='source',
            field=models.ManyToManyField(to='rus_drill.Source'),
        ),
        migrations.AddField(
            model_name='qelement',
            name='question',
            field=models.ForeignKey(to='rus_drill.Question', null=True),
        ),
        migrations.AddField(
            model_name='qelement',
            name='semtype',
            field=models.ForeignKey(to='rus_drill.Semtype', null=True),
        ),
        migrations.AddField(
            model_name='qelement',
            name='tags',
            field=models.ManyToManyField(to='rus_drill.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='morphphontag',
            unique_together=set([('stem', 'gender', 'animate', 'declension', 'inflection_class', 'reflexive')]),
        ),
        migrations.AddField(
            model_name='linkutterance',
            name='link',
            field=models.ForeignKey(blank=True, to='rus_drill.Utterance', null=True),
        ),
        migrations.AddField(
            model_name='form',
            name='tag',
            field=models.ForeignKey(to='rus_drill.Tag'),
        ),
        migrations.AddField(
            model_name='form',
            name='word',
            field=models.ForeignKey(to='rus_drill.Word'),
        ),
    ]
