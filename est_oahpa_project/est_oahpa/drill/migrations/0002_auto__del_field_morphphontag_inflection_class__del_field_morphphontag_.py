# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'MorphPhonTag', fields ['reflexive', 'gender', 'stress_class', 'stem', 'inflection_class', 'animate']
        db.delete_unique('drill_morphphontag', ['reflexive', 'gender', 'stress_class', 'stem', 'inflection_class', 'animate'])

        # Deleting field 'MorphPhonTag.inflection_class'
        db.delete_column('drill_morphphontag', 'inflection_class')

        # Deleting field 'MorphPhonTag.stress_class'
        db.delete_column('drill_morphphontag', 'stress_class')

        # Adding field 'MorphPhonTag.declension'
        db.add_column('drill_morphphontag', 'declension',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)

        # Adding unique constraint on 'MorphPhonTag', fields ['gender', 'animate', 'declension', 'reflexive', 'stem']
        db.create_unique('drill_morphphontag', ['gender', 'animate', 'declension', 'reflexive', 'stem'])

        # Deleting field 'Word.inflection_class'
        db.delete_column('drill_word', 'inflection_class')

        # Deleting field 'Word.stress_class'
        db.delete_column('drill_word', 'stress_class')

        # Adding field 'Word.declension'
        db.add_column('drill_word', 'declension',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'MorphPhonTag', fields ['gender', 'animate', 'declension', 'reflexive', 'stem']
        db.delete_unique('drill_morphphontag', ['gender', 'animate', 'declension', 'reflexive', 'stem'])

        # Adding field 'MorphPhonTag.inflection_class'
        db.add_column('drill_morphphontag', 'inflection_class',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)

        # Adding field 'MorphPhonTag.stress_class'
        db.add_column('drill_morphphontag', 'stress_class',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)

        # Deleting field 'MorphPhonTag.declension'
        db.delete_column('drill_morphphontag', 'declension')

        # Adding unique constraint on 'MorphPhonTag', fields ['reflexive', 'gender', 'stress_class', 'stem', 'inflection_class', 'animate']
        db.create_unique('drill_morphphontag', ['reflexive', 'gender', 'stress_class', 'stem', 'inflection_class', 'animate'])

        # Adding field 'Word.inflection_class'
        db.add_column('drill_word', 'inflection_class',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)

        # Adding field 'Word.stress_class'
        db.add_column('drill_word', 'stress_class',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)

        # Deleting field 'Word.declension'
        db.delete_column('drill_word', 'declension')


    models = {
        'drill.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'drill.dialect': {
            'Meta': {'object_name': 'Dialect'},
            'dialect': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'drill.dialogue': {
            'Meta': {'object_name': 'Dialogue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'drill.feedbackmsg': {
            'Meta': {'object_name': 'Feedbackmsg'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'msgid': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'drill.feedbacktext': {
            'Meta': {'object_name': 'Feedbacktext'},
            'feedbackmsg': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.Feedbackmsg']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'order': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'})
        },
        'drill.form': {
            'Meta': {'object_name': 'Form'},
            'dialects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['drill.Dialect']", 'null': 'True', 'symmetrical': 'False'}),
            'feedback': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['drill.Feedbackmsg']", 'null': 'True', 'symmetrical': 'False'}),
            'fullform': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.Tag']"}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.Word']"})
        },
        'drill.grammarlinks': {
            'Meta': {'object_name': 'Grammarlinks'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '800', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'drill.linkutterance': {
            'Meta': {'object_name': 'LinkUtterance'},
            'constant': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.Utterance']", 'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'variable': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'drill.log': {
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
        'drill.morphphontag': {
            'Meta': {'unique_together': "(('stem', 'gender', 'animate', 'declension', 'reflexive'),)", 'object_name': 'MorphPhonTag'},
            'animate': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'declension': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reflexive': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'stem': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'drill.qelement': {
            'Meta': {'object_name': 'QElement'},
            'agreement': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'agreement_set'", 'null': 'True', 'to': "orm['drill.QElement']"}),
            'copy': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'copy_set'", 'null': 'True', 'to': "orm['drill.QElement']"}),
            'game': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'gametype': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.Question']", 'null': 'True'}),
            'semtype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.Semtype']", 'null': 'True'}),
            'syntax': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['drill.Tag']", 'symmetrical': 'False'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'drill.question': {
            'Meta': {'object_name': 'Question'},
            'gametype': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lemmacount': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'level': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'qatype': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'qid': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'qtype': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'answer_set'", 'null': 'True', 'to': "orm['drill.Question']"}),
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['drill.Source']", 'symmetrical': 'False'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'drill.semtype': {
            'Meta': {'object_name': 'Semtype'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semtype': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'drill.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'drill.tag': {
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
        'drill.tagname': {
            'Meta': {'object_name': 'Tagname'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tagname': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'tagset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.Tagset']"})
        },
        'drill.tagset': {
            'Meta': {'object_name': 'Tagset'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tagset': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'drill.topic': {
            'Meta': {'object_name': 'Topic'},
            'dialogue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.Dialogue']"}),
            'formlist': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['drill.Form']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True'}),
            'topicname': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'drill.uelement': {
            'Meta': {'object_name': 'UElement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'syntax': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.Tag']", 'null': 'True', 'blank': 'True'}),
            'utterance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.Utterance']", 'null': 'True'})
        },
        'drill.utterance': {
            'Meta': {'object_name': 'Utterance'},
            'formlist': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['drill.Form']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'links': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['drill.LinkUtterance']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.Topic']"}),
            'utterance': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'utttype': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'drill.word': {
            'Meta': {'object_name': 'Word'},
            'animate': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'compare': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'declension': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'dialects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['drill.Dialect']", 'null': 'True', 'symmetrical': 'False'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'geography': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'hid': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '5', 'db_index': 'True'}),
            'lemma': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'morphophon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.MorphPhonTag']", 'null': 'True'}),
            'pos': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'presentationform': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'reflexive': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'semtype': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['drill.Semtype']", 'symmetrical': 'False'}),
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['drill.Source']", 'symmetrical': 'False'}),
            'stem': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tcomm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wordid': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'})
        },
        'drill.wordqelement': {
            'Meta': {'object_name': 'WordQElement'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'qelement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.QElement']", 'null': 'True'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.Word']", 'null': 'True'})
        },
        'drill.wordtranslation': {
            'Meta': {'object_name': 'WordTranslation'},
            'explanation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'geography': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'lemma': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'phrase': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pos': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'semtype': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['drill.Semtype']", 'symmetrical': 'False'}),
            'source': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['drill.Source']", 'symmetrical': 'False'}),
            'tcomm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tcomm_pref': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['drill.Word']"}),
            'wordid': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'})
        }
    }

    complete_apps = ['drill']
