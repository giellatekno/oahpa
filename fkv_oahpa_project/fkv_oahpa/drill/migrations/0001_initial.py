# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comment'
        db.create_table('rus_drill_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('rus_drill', ['Comment'])

        # Adding model 'Log'
        db.create_table('rus_drill_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('userinput', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('iscorrect', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('correct', self.gf('django.db.models.fields.TextField')()),
            ('example', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('feedback', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('messageid', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('rus_drill', ['Log'])

        # Adding model 'Semtype'
        db.create_table('rus_drill_semtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('semtype', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('rus_drill', ['Semtype'])

        # Adding model 'Source'
        db.create_table('rus_drill_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('rus_drill', ['Source'])

        # Adding model 'Dialect'
        db.create_table('rus_drill_dialect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dialect', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('rus_drill', ['Dialect'])

        # Adding model 'MorphPhonTag'
        db.create_table('rus_drill_morphphontag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stem', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('animate', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('inflection_class', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('stress_class', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('reflexive', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal('rus_drill', ['MorphPhonTag'])

        # Adding unique constraint on 'MorphPhonTag', fields ['stem', 'gender', 'animate', 'inflection_class', 'stress_class', 'reflexive']
        db.create_unique('rus_drill_morphphontag', ['stem', 'gender', 'animate', 'inflection_class', 'stress_class', 'reflexive'])

        # Adding model 'Word'
        db.create_table('rus_drill_word', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wordid', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='ru', max_length=5, db_index=True)),
            ('lemma', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('presentationform', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('pos', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('stem', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('animate', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('inflection_class', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('stress_class', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('reflexive', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('hid', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True)),
            ('compare', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('geography', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('tcomm', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('morphophon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.MorphPhonTag'], null=True)),
        ))
        db.send_create_signal('rus_drill', ['Word'])

        # Adding M2M table for field semtype on 'Word'
        db.create_table('rus_drill_word_semtype', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('word', models.ForeignKey(orm['rus_drill.word'], null=False)),
            ('semtype', models.ForeignKey(orm['rus_drill.semtype'], null=False))
        ))
        db.create_unique('rus_drill_word_semtype', ['word_id', 'semtype_id'])

        # Adding M2M table for field source on 'Word'
        db.create_table('rus_drill_word_source', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('word', models.ForeignKey(orm['rus_drill.word'], null=False)),
            ('source', models.ForeignKey(orm['rus_drill.source'], null=False))
        ))
        db.create_unique('rus_drill_word_source', ['word_id', 'source_id'])

        # Adding M2M table for field dialects on 'Word'
        db.create_table('rus_drill_word_dialects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('word', models.ForeignKey(orm['rus_drill.word'], null=False)),
            ('dialect', models.ForeignKey(orm['rus_drill.dialect'], null=False))
        ))
        db.create_unique('rus_drill_word_dialects', ['word_id', 'dialect_id'])

        # Adding model 'WordTranslation'
        db.create_table('rus_drill_wordtranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.Word'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('wordid', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('lemma', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('phrase', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('explanation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pos', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('geography', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('tcomm', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tcomm_pref', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('rus_drill', ['WordTranslation'])

        # Adding M2M table for field semtype on 'WordTranslation'
        db.create_table('rus_drill_wordtranslation_semtype', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wordtranslation', models.ForeignKey(orm['rus_drill.wordtranslation'], null=False)),
            ('semtype', models.ForeignKey(orm['rus_drill.semtype'], null=False))
        ))
        db.create_unique('rus_drill_wordtranslation_semtype', ['wordtranslation_id', 'semtype_id'])

        # Adding M2M table for field source on 'WordTranslation'
        db.create_table('rus_drill_wordtranslation_source', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('wordtranslation', models.ForeignKey(orm['rus_drill.wordtranslation'], null=False)),
            ('source', models.ForeignKey(orm['rus_drill.source'], null=False))
        ))
        db.create_unique('rus_drill_wordtranslation_source', ['wordtranslation_id', 'source_id'])

        # Adding model 'Tagset'
        db.create_table('rus_drill_tagset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tagset', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('rus_drill', ['Tagset'])

        # Adding model 'Tagname'
        db.create_table('rus_drill_tagname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tagname', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('tagset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.Tagset'])),
        ))
        db.send_create_signal('rus_drill', ['Tagname'])

        # Adding model 'Tag'
        db.create_table('rus_drill_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('string', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('attributive', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('case', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('mood', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('personnumber', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('pos', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('tense', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('rus_drill', ['Tag'])

        # Adding model 'Form'
        db.create_table('rus_drill_form', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.Word'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.Tag'])),
            ('fullform', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('rus_drill', ['Form'])

        # Adding M2M table for field dialects on 'Form'
        db.create_table('rus_drill_form_dialects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('form', models.ForeignKey(orm['rus_drill.form'], null=False)),
            ('dialect', models.ForeignKey(orm['rus_drill.dialect'], null=False))
        ))
        db.create_unique('rus_drill_form_dialects', ['form_id', 'dialect_id'])

        # Adding M2M table for field feedback on 'Form'
        db.create_table('rus_drill_form_feedback', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('form', models.ForeignKey(orm['rus_drill.form'], null=False)),
            ('feedbackmsg', models.ForeignKey(orm['rus_drill.feedbackmsg'], null=False))
        ))
        db.create_unique('rus_drill_form_feedback', ['form_id', 'feedbackmsg_id'])

        # Adding model 'Feedbackmsg'
        db.create_table('rus_drill_feedbackmsg', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('msgid', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('rus_drill', ['Feedbackmsg'])

        # Adding model 'Feedbacktext'
        db.create_table('rus_drill_feedbacktext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('feedbackmsg', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.Feedbackmsg'])),
            ('order', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
        ))
        db.send_create_signal('rus_drill', ['Feedbacktext'])

        # Adding model 'Question'
        db.create_table('rus_drill_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('qid', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('level', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('task', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('string', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('qtype', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('qatype', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='answer_set', null=True, to=orm['rus_drill.Question'])),
            ('gametype', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('lemmacount', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
        ))
        db.send_create_signal('rus_drill', ['Question'])

        # Adding M2M table for field source on 'Question'
        db.create_table('rus_drill_question_source', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm['rus_drill.question'], null=False)),
            ('source', models.ForeignKey(orm['rus_drill.source'], null=False))
        ))
        db.create_unique('rus_drill_question_source', ['question_id', 'source_id'])

        # Adding model 'QElement'
        db.create_table('rus_drill_qelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.Question'], null=True)),
            ('syntax', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('task', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('gametype', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('agreement', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='agreement_set', null=True, to=orm['rus_drill.QElement'])),
            ('semtype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.Semtype'], null=True)),
            ('game', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('copy', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='copy_set', null=True, to=orm['rus_drill.QElement'])),
        ))
        db.send_create_signal('rus_drill', ['QElement'])

        # Adding M2M table for field tags on 'QElement'
        db.create_table('rus_drill_qelement_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('qelement', models.ForeignKey(orm['rus_drill.qelement'], null=False)),
            ('tag', models.ForeignKey(orm['rus_drill.tag'], null=False))
        ))
        db.create_unique('rus_drill_qelement_tags', ['qelement_id', 'tag_id'])

        # Adding model 'WordQElement'
        db.create_table('rus_drill_wordqelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.Word'], null=True)),
            ('qelement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.QElement'], null=True)),
        ))
        db.send_create_signal('rus_drill', ['WordQElement'])

        # Adding model 'Dialogue'
        db.create_table('rus_drill_dialogue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('rus_drill', ['Dialogue'])

        # Adding model 'Utterance'
        db.create_table('rus_drill_utterance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('utterance', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('utttype', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.Topic'])),
        ))
        db.send_create_signal('rus_drill', ['Utterance'])

        # Adding M2M table for field links on 'Utterance'
        db.create_table('rus_drill_utterance_links', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('utterance', models.ForeignKey(orm['rus_drill.utterance'], null=False)),
            ('linkutterance', models.ForeignKey(orm['rus_drill.linkutterance'], null=False))
        ))
        db.create_unique('rus_drill_utterance_links', ['utterance_id', 'linkutterance_id'])

        # Adding M2M table for field formlist on 'Utterance'
        db.create_table('rus_drill_utterance_formlist', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('utterance', models.ForeignKey(orm['rus_drill.utterance'], null=False)),
            ('form', models.ForeignKey(orm['rus_drill.form'], null=False))
        ))
        db.create_unique('rus_drill_utterance_formlist', ['utterance_id', 'form_id'])

        # Adding model 'UElement'
        db.create_table('rus_drill_uelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('utterance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.Utterance'], null=True)),
            ('syntax', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.Tag'], null=True, blank=True)),
        ))
        db.send_create_signal('rus_drill', ['UElement'])

        # Adding model 'LinkUtterance'
        db.create_table('rus_drill_linkutterance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.Utterance'], null=True, blank=True)),
            ('target', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('variable', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('constant', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('rus_drill', ['LinkUtterance'])

        # Adding model 'Topic'
        db.create_table('rus_drill_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topicname', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('dialogue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rus_drill.Dialogue'])),
            ('number', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True)),
            ('image', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('rus_drill', ['Topic'])

        # Adding M2M table for field formlist on 'Topic'
        db.create_table('rus_drill_topic_formlist', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('topic', models.ForeignKey(orm['rus_drill.topic'], null=False)),
            ('form', models.ForeignKey(orm['rus_drill.form'], null=False))
        ))
        db.create_unique('rus_drill_topic_formlist', ['topic_id', 'form_id'])

        # Adding model 'Grammarlinks'
        db.create_table('rus_drill_grammarlinks', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=800, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
        ))
        db.send_create_signal('rus_drill', ['Grammarlinks'])


    def backwards(self, orm):
        # Removing unique constraint on 'MorphPhonTag', fields ['stem', 'gender', 'animate', 'inflection_class', 'stress_class', 'reflexive']
        db.delete_unique('rus_drill_morphphontag', ['stem', 'gender', 'animate', 'inflection_class', 'stress_class', 'reflexive'])

        # Deleting model 'Comment'
        db.delete_table('rus_drill_comment')

        # Deleting model 'Log'
        db.delete_table('rus_drill_log')

        # Deleting model 'Semtype'
        db.delete_table('rus_drill_semtype')

        # Deleting model 'Source'
        db.delete_table('rus_drill_source')

        # Deleting model 'Dialect'
        db.delete_table('rus_drill_dialect')

        # Deleting model 'MorphPhonTag'
        db.delete_table('rus_drill_morphphontag')

        # Deleting model 'Word'
        db.delete_table('rus_drill_word')

        # Removing M2M table for field semtype on 'Word'
        db.delete_table('rus_drill_word_semtype')

        # Removing M2M table for field source on 'Word'
        db.delete_table('rus_drill_word_source')

        # Removing M2M table for field dialects on 'Word'
        db.delete_table('rus_drill_word_dialects')

        # Deleting model 'WordTranslation'
        db.delete_table('rus_drill_wordtranslation')

        # Removing M2M table for field semtype on 'WordTranslation'
        db.delete_table('rus_drill_wordtranslation_semtype')

        # Removing M2M table for field source on 'WordTranslation'
        db.delete_table('rus_drill_wordtranslation_source')

        # Deleting model 'Tagset'
        db.delete_table('rus_drill_tagset')

        # Deleting model 'Tagname'
        db.delete_table('rus_drill_tagname')

        # Deleting model 'Tag'
        db.delete_table('rus_drill_tag')

        # Deleting model 'Form'
        db.delete_table('rus_drill_form')

        # Removing M2M table for field dialects on 'Form'
        db.delete_table('rus_drill_form_dialects')

        # Removing M2M table for field feedback on 'Form'
        db.delete_table('rus_drill_form_feedback')

        # Deleting model 'Feedbackmsg'
        db.delete_table('rus_drill_feedbackmsg')

        # Deleting model 'Feedbacktext'
        db.delete_table('rus_drill_feedbacktext')

        # Deleting model 'Question'
        db.delete_table('rus_drill_question')

        # Removing M2M table for field source on 'Question'
        db.delete_table('rus_drill_question_source')

        # Deleting model 'QElement'
        db.delete_table('rus_drill_qelement')

        # Removing M2M table for field tags on 'QElement'
        db.delete_table('rus_drill_qelement_tags')

        # Deleting model 'WordQElement'
        db.delete_table('rus_drill_wordqelement')

        # Deleting model 'Dialogue'
        db.delete_table('rus_drill_dialogue')

        # Deleting model 'Utterance'
        db.delete_table('rus_drill_utterance')

        # Removing M2M table for field links on 'Utterance'
        db.delete_table('rus_drill_utterance_links')

        # Removing M2M table for field formlist on 'Utterance'
        db.delete_table('rus_drill_utterance_formlist')

        # Deleting model 'UElement'
        db.delete_table('rus_drill_uelement')

        # Deleting model 'LinkUtterance'
        db.delete_table('rus_drill_linkutterance')

        # Deleting model 'Topic'
        db.delete_table('rus_drill_topic')

        # Removing M2M table for field formlist on 'Topic'
        db.delete_table('rus_drill_topic_formlist')

        # Deleting model 'Grammarlinks'
        db.delete_table('rus_drill_grammarlinks')


    models = {
        'rus_drill.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'rus_drill.dialect': {
            'Meta': {'object_name': 'Dialect'},
            'dialect': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rus_drill.dialogue': {
            'Meta': {'object_name': 'Dialogue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'rus_drill.feedbackmsg': {
            'Meta': {'object_name': 'Feedbackmsg'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msgid': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rus_drill.feedbacktext': {
            'Meta': {'object_name': 'Feedbacktext'},
            'feedbackmsg': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.Feedbackmsg']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'})
        },
        'rus_drill.form': {
            'Meta': {'object_name': 'Form'},
            'dialects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rus_drill.Dialect']", 'null': 'True', 'symmetrical': 'False'}),
            'feedback': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rus_drill.Feedbackmsg']", 'null': 'True', 'symmetrical': 'False'}),
            'fullform': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.Tag']"}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.Word']"})
        },
        'rus_drill.grammarlinks': {
            'Meta': {'object_name': 'Grammarlinks'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '800', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'rus_drill.linkutterance': {
            'Meta': {'object_name': 'LinkUtterance'},
            'constant': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.Utterance']", 'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'variable': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'rus_drill.log': {
            'Meta': {'object_name': 'Log'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'correct': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'example': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'feedback': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'game': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iscorrect': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'messageid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'userinput': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'rus_drill.morphphontag': {
            'Meta': {'unique_together': "(('stem', 'gender', 'animate', 'inflection_class', 'stress_class', 'reflexive'),)", 'object_name': 'MorphPhonTag'},
            'animate': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inflection_class': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'reflexive': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'stem': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stress_class': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'rus_drill.qelement': {
            'Meta': {'object_name': 'QElement'},
            'agreement': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'agreement_set'", 'null': 'True', 'to': "orm['rus_drill.QElement']"}),
            'copy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'copy_set'", 'null': 'True', 'to': "orm['rus_drill.QElement']"}),
            'game': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'gametype': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.Question']", 'null': 'True'}),
            'semtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.Semtype']", 'null': 'True'}),
            'syntax': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rus_drill.Tag']", 'symmetrical': 'False'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'rus_drill.question': {
            'Meta': {'object_name': 'Question'},
            'gametype': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lemmacount': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'level': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'qatype': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'qid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'qtype': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'answer_set'", 'null': 'True', 'to': "orm['rus_drill.Question']"}),
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rus_drill.Source']", 'symmetrical': 'False'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'rus_drill.semtype': {
            'Meta': {'object_name': 'Semtype'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semtype': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'rus_drill.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'rus_drill.tag': {
            'Meta': {'object_name': 'Tag'},
            'attributive': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'case': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mood': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'personnumber': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'pos': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'string': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'tense': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'rus_drill.tagname': {
            'Meta': {'object_name': 'Tagname'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tagname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'tagset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.Tagset']"})
        },
        'rus_drill.tagset': {
            'Meta': {'object_name': 'Tagset'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tagset': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'rus_drill.topic': {
            'Meta': {'object_name': 'Topic'},
            'dialogue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.Dialogue']"}),
            'formlist': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rus_drill.Form']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True'}),
            'topicname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'rus_drill.uelement': {
            'Meta': {'object_name': 'UElement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'syntax': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.Tag']", 'null': 'True', 'blank': 'True'}),
            'utterance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.Utterance']", 'null': 'True'})
        },
        'rus_drill.utterance': {
            'Meta': {'object_name': 'Utterance'},
            'formlist': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rus_drill.Form']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rus_drill.LinkUtterance']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.Topic']"}),
            'utterance': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'utttype': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'rus_drill.word': {
            'Meta': {'object_name': 'Word'},
            'animate': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'compare': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'dialects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rus_drill.Dialect']", 'null': 'True', 'symmetrical': 'False'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'geography': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'hid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inflection_class': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5', 'db_index': 'True'}),
            'lemma': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'morphophon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.MorphPhonTag']", 'null': 'True'}),
            'pos': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'presentationform': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'reflexive': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'semtype': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rus_drill.Semtype']", 'symmetrical': 'False'}),
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rus_drill.Source']", 'symmetrical': 'False'}),
            'stem': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stress_class': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tcomm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wordid': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'})
        },
        'rus_drill.wordqelement': {
            'Meta': {'object_name': 'WordQElement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qelement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.QElement']", 'null': 'True'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.Word']", 'null': 'True'})
        },
        'rus_drill.wordtranslation': {
            'Meta': {'object_name': 'WordTranslation'},
            'explanation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'geography': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'lemma': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'phrase': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pos': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'semtype': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rus_drill.Semtype']", 'symmetrical': 'False'}),
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rus_drill.Source']", 'symmetrical': 'False'}),
            'tcomm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tcomm_pref': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rus_drill.Word']"}),
            'wordid': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'})
        }
    }

    complete_apps = ['rus_drill']