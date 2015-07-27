# -*- coding: utf-8 -*-

### NB: this file is for testing an fst-based correct/incorrect
### validation.

from django import forms
from django.db.models import Q
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
import sms_oahpa.settings as settings

from sms_oahpa.conf.tools import switch_language_code

from sms_drill.models import *

import datetime
import socket
import sys, os
import itertools
from random import choice

try:
        LOG_FILE = sms_oahpa.settings.LOG_FILE
except:
        LOG_FILE = False

# TODO: have to be really restrictive here.
__all__ = [
    'MorfaQuestion',
]

# These settings should only be changed in sms_drills for now

from sms_drill.forms import (
    ADJCASE_CHOICES,
    ADJECTIVE_FILTER_DEFINITION,
    ADJECTIVE_QUESTION_ANSWER,
    ADJEX_CHOICES,
    ADJ_CONTEXT_CHOICES,
    BOOK_CHOICES,
    CASE_CHOICES,
    CASE_CHOICES_PRONOUN,
    CASE_CONTEXT_CHOICES,
    DEMONSTRATIVE_PRESENTATION,
    DERIVATION_CHOICES,
    DERIVATION_CHOICES_CONTEXT,
    DERIVATION_FILTER_DEFINITION,
    DERIVATION_QUESTION_ANSWER,
    DIALOGUE_CHOICES,
    FREQUENCY_CHOICES,
    GEOGRAPHY_CHOICES,
    GRADE_CHOICES,
    KLOKKA_CHOICES,
    LEVEL_CHOICES,
    NEGATIVE_VERB_PRES,
    NOUN_FILTER_DEFINITION,
    NOUN_QUESTION_ANSWER,
    NUMERAL_FILTER_DEFINITION,
    NUMERAL_QUESTION_ANSWER,
    NUMGAME_CHOICES,
    NUMGAME_CHOICES_PL,
    NUMLANGUAGE_CHOICES,
    NUM_BARE_CHOICES,
    NUM_CHOICES,
    NUM_CONTEXT_CHOICES,
    NUM_LEVEL_CHOICES,
    NUM_TYPE_CHOICES,
    PASSIVE_PRONOUNS_LIST,
    POS_CHOICES,
    PRONOUNS_LIST,
    PRONOUN_FILTER_DEFINITION,
    PRONOUN_QUESTION_ANSWER,
    PRONOUN_SUBCLASSES,
    PRON_CONTEXT_CHOICES,
    RECIPROCATIVE_PRESENTATION,
    RECIP_REFL_CHOICES,
    SEMTYPE_CHOICES,
    SYLLABLE_VALUES,
    TENSE_PRESENTATION,
    TRANS_CHOICES,
    VASTAS_NR_OF_TASKWORDS,
    VASTA_LEVELS,
    VERB_CLASSES,
    VERB_FILTER_DEFINITION,
    VERB_QUESTION_ANSWER,
    VTYPE_CHOICES,
    VTYPE_CONTEXT_CHOICES,
    WORDFORM_TYPE_CHOICES,

    GAME_TYPE_DEFINITIONS,
    GAME_FILTER_DEFINITIONS,

    # functions
    relax,
)

ALL_CHOICES = [
	ADJCASE_CHOICES, 
	ADJEX_CHOICES, 
	ADJ_CONTEXT_CHOICES,
	BOOK_CHOICES, 
	CASE_CHOICES, 
	CASE_CHOICES_PRONOUN, 
	CASE_CONTEXT_CHOICES,
	DIALOGUE_CHOICES, 
	FREQUENCY_CHOICES, 
	GEOGRAPHY_CHOICES, 
	GRADE_CHOICES,
	KLOKKA_CHOICES, 
	LEVEL_CHOICES, 
	NUMGAME_CHOICES, 
	NUMGAME_CHOICES_PL,
	NUMLANGUAGE_CHOICES, 
	NUM_BARE_CHOICES, 
	NUM_CHOICES, 
	NUM_CONTEXT_CHOICES,
	NUM_LEVEL_CHOICES,
	NUM_TYPE_CHOICES, 
	POS_CHOICES, 
	PRONOUN_SUBCLASSES, 
	PRON_CONTEXT_CHOICES,
	RECIP_REFL_CHOICES, 
	SEMTYPE_CHOICES, 
	SYLLABLE_VALUES,
	TRANS_CHOICES, 
	VASTA_LEVELS,
	VASTAS_NR_OF_TASKWORDS, 
	VERB_CLASSES,
	VTYPE_CHOICES, 
	VTYPE_CONTEXT_CHOICES
]

# #
#
# Form validation
#
# #


import re

from sms_oahpa.settings import INFINITIVE_SUBTRACT as infinitives_sub
from sms_oahpa.settings import INFINITIVE_ADD as infinitives_add

def is_correct(self, game, example=None):
	"""
	Determines if the given answer is correct (for a bound form).
	"""
	self.game = game
	self.example = example

	if not self.is_valid():
		return False
		
	self.userans = self.cleaned_data['answer']
	
	self.answer = self.userans.strip()
	
	if not game == "numra":
		self.answer = self.answer.rstrip('.!?,')
	
	self.error = "error"
	self.iscorrect = False
	
	if self.answer in set(self.correct_anslist) or \
			self.answer.lower() in set(self.correct_anslist) or \
			self.answer.upper() in set(self.correct_anslist):
		self.error = "correct"
		self.iscorrect = True
	
	# Log information about user answers.
	
	correctlist = u",".join([a for a in self.correct_anslist])
	self.correctlist = correctlist
	self.log_response()

def set_correct(self):
	"""
	Adds correct wordforms to the question form.
	"""
	if self.correct_ans:
		self.correct_answers = self.correct_ans[:]
		if type(self.correct_answers) == list:
			self.correct_answers = ', '.join(self.correct_answers)
	

def set_settings(self):
	# self.levels = { 
	# 		'l1':  ['l1'],
	# 		'l2':  ['l2', 'l1'], 
	# 		'l3':  ['l3', 'l2', 'l1'], 
	# 		'all': ['l3', 'l2', 'l1', 'all'], 
	# 	}
	
	# Construct arrays for level choices.
	
	# Commenting this out because I don't see yet why this needs to be constructed this way.
	# If it's done automatically so that more levels can be added, the code here will still need
	# to be altered... So it seems easiest to just hard-code this for now.
	
	# self.levels = {}
	# self.levels['all'] = [] 
	# for b in LEVEL_CHOICES:
	# 	if b[0] != 'all':
	# 		self.levels[b[0]] = [] 
	# 		self.levels['all'].append(b[0])
	# 		
	# 	self.levels[b[0]].append(b[0])
	# 
	# self.levels['l2'].append('l1')
	# for b in ['l1', 'l2']:
	# 	self.levels['l3'].append(b)
	
	
	# Turning these into dictionary type means there's no need to iterate to 
	# get the first tuple item. Also makes it easier to read. And, there are 
	# no many-to-many relationships in these tuples of tuples
	
	self.allsem = dict(SEMTYPE_CHOICES).keys()
	self.allcase = dict(CASE_CHOICES).keys()
	self.allcase_context = dict(CASE_CONTEXT_CHOICES).keys()
	self.proncase_context = dict(PRON_CONTEXT_CHOICES).keys()
	self.allvtype_context = dict(VTYPE_CONTEXT_CHOICES).keys()
	self.alladjcase = dict(ADJCASE_CHOICES).keys()  # added by Heli
	self.allgrade = dict(GRADE_CHOICES).keys() # added by Heli
	self.alladj_context = dict(ADJ_CONTEXT_CHOICES).keys()
	self.allnum_context = dict(NUM_CONTEXT_CHOICES).keys()
	self.allnum_bare = dict(NUM_BARE_CHOICES).keys()
	self.allnum_type = dict(NUM_TYPE_CHOICES).keys() # added by Heli
	self.sources = dict(BOOK_CHOICES).keys()
	self.geography = dict(GEOGRAPHY_CHOICES).keys()
	self.frequency = dict(FREQUENCY_CHOICES).keys() # added by Heli


# comment
# DEBUG = open('/dev/ttys001', 'w')
# DEBUG = open('/dev/null', 'w')


def get_feedback(self, wordform, language):

	language = switch_language_code(language)
	
	feedbacks = wordform.feedback.filter(feedbacktext__language=language)\
					.order_by('feedbacktext__order')
	
	feedback_messages = []
	for feedback in feedbacks:
		texts = feedback.feedbacktext_set.filter(language=language).order_by('order')
		feedback_messages.extend([a.message for a in texts])

	message_list = []
	if feedback_messages:
		for text in feedback_messages:
			text = text.replace('WORDFORM', '"%s"' % wordform.word.lemma)
			message_list.append(text)
	
	self.feedback = ' \n '.join(list(message_list))

	### print wordform.fullform
	### print wordform.tag.string

	### print 'stem:' + wordform.word.stem
	### print 'gradation:' + wordform.word.gradation
	### print 'diphthong:' + wordform.word.diphthong
	### print 'rime:' + wordform.word.rime
	### print 'soggi:' + wordform.word.soggi
	### print 'attrsuffix:' + wordform.word.attrsuffix
	### print 'compsuffix:' + wordform.word.compsuffix


	### print self.feedback
	### print '--'
	### # NOTE: debug
	### # print wordform.id
	### # print wordform.feedback.all()
	### # print feedbacks
	### # print self.feedback
	### # print '\n'

def select_words(self, qwords, awords):
	"""
		Fetch words and tags from the database.
	"""
	from random import choice
	selected_awords = {}
	
	for syntax in awords.keys():
		word = None
		tag = None
		selected_awords[syntax] = {}

		# Select answer words and fullforms for interface
		if awords.has_key(syntax) and len(awords[syntax]) > 0:
			aword = choice(awords[syntax])
			if aword.has_key('tag'):
				selected_awords[syntax]['tag'] = aword['tag']
			if aword.has_key('task'): 
				selected_awords[syntax]['task'] = aword['task']
			if aword.has_key('taskword'):
				selected_awords[syntax]['taskword'] = aword['taskword']
			if aword.has_key('qelement'):
				qelem = aword['qelement']
				if type(qelem) is not long:  # to exclude MorfaC 
				    if qelem.task:  # words in VastaS answer frame where task="yes".
				        selected_awords[syntax]['taskword'] = qelem.task   
			if aword.has_key('word') and aword['word']:
				selected_awords[syntax]['word'] = aword['word']
			else:
				if aword.has_key('qelement') and selected_awords[syntax].has_key('tag'):
					# get form_list for a given qelement

					wqelems = WordQElement.objects.filter(qelement__id=aword['qelement'])

					# Some WordQElements are associated with words that have no
					# Forms, as such we have to randomly select one until we
					# find an element with forms. This is faster than filtering
					# by annotating and Count() 

					if wqelems.count() > 0:

						form_list = None
						i, max = 0, 50

						while not form_list and i < max:
							i += 1

							wqel = wqelems.order_by('?')[0]

							selected_awords[syntax]['word'] = wqel.word.id

							form_list = wqel.word.form_set.filter(
								tag__id = selected_awords[syntax]['tag']
							)

					if form_list:
						fullf = [f.fullform for f in form_list]
						selected_awords[syntax]['fullform'] = fullf[:]

				if not selected_awords[syntax].has_key('fullform'):
					if aword.has_key('fullform') and len(aword['fullform']) > 0:
						selected_awords[syntax]['fullform'] = aword['fullform'][:]

		if not selected_awords[syntax].has_key('fullform'):

			if selected_awords[syntax].has_key('word')\
				and selected_awords[syntax].has_key('tag'):

				form_list = Form.objects.filter(
								word__id=selected_awords[syntax]['word'],
								tag__id=selected_awords[syntax]['tag'],
							)
				
				excl = form_list.exclude(dialects__dialect='NG')

				if excl.count() > 0:
					form_list = excl

				form_list_dialects = form_list.filter(dialects__dialect=self.dialect)

				if form_list_dialects.count() > 0:
					form_list = form_list_dialects

				if form_list.count() > 0:
					fullf = []
					for f in form_list:
						fullf.append(f.fullform)
					selected_awords[syntax]['fullform'] = fullf[:]

		# make sure that there is something to print
		if not selected_awords[syntax].has_key('fullform'):
			selected_awords[syntax]['fullform'] = []
			selected_awords[syntax]['fullform'].append(syntax)
        print "selected awords: "
        print selected_awords
	return selected_awords



# #
#
# Oahpa form meta-classes
#
# #



class OahpaSettings(forms.Form):
	"""
		The metaform for game settings. Various games subclass from this form.
	"""
	set_settings = set_settings
	
	def clean(self):
		x = self.cleaned_data['bisyllabic']
		print 'clean: ', x
		return self.cleaned_data
	
	def set_default_data(self):
		self.default_data = {
					'language' : 'sms',  # sme in univ_oahpa
					'syll' : ['2syll'],
					'bisyllabic': 'on',
					'trisyllabic': False,
					'contracted': False,
					'level' : 'all',
					'lemmacount' : '2',
					'case': 'N-ILL',
					'pos' : 'N',
					'vtype' : 'PRS',
					'adjcase' : 'ATTR',
					'number' : '',
					'pron_type': 'Pers',
					'proncase' : 'N-ILL',
					'grade' : '',  # was: '' 'Pos' is not a good idea beacuse it is implicit in the database.
					'case_context' : 'N-SG-ACC',
					'vtype_context' : 'V-PRS',
					'pron_context' : 'P-PERS',
					'num_context' : 'NUM-ATTR',
					'num_level' : '1',
					'num_type' : 'CARD',  # added by Heli
					'derivation_type' : 'V-DER-PASS',
					'derivation_type_context' : 'DER-PASSV', # was V-DER
					'geography': 'world',
					'frequency' : [],
					'num_bare' : 'N-ILL',
					'adj_context' : 'ATTRPOS',
					'source' : 'all'}

class OahpaQuestion(forms.Form):
	"""
		Meta form for question/answer section.
	"""
	is_correct = is_correct
	set_correct = set_correct
	get_feedback = get_feedback
	
	# Set answer widget. Can this JS actually be moved to templates? 
	KEYDOWN = 'javascript:return process(this, event, document.gameform);'
	answer_attrs = {'size': 45} # , 'onkeydown': KEYDOWN}
	answer = forms.CharField(max_length=45, widget=forms.TextInput(attrs=answer_attrs))
	
	def log_response(self):
		import datetime

		today = datetime.date.today()
		# print ','.join(self.correct_anslist)

		log, c = Log.objects.get_or_create(userinput=self.answer,
											correct=','.join(self.correct_anslist),
											iscorrect=self.iscorrect,
											example=self.example,
											game=self.game,
											date=today)
	
	def __init__(self, *args, **kwargs):
		correct_val = False
		if 'correct_val' in kwargs:
			correct_val = kwargs.get('correct_val')
			kwargs.pop('correct_val')
		
		super(OahpaQuestion, self).__init__(*args, **kwargs)
		
		# set correct and error values
		if correct_val == "correct":
			self.error = "correct"
			
	def init_variables(self, possible, userans_val, accepted_answers, preferred=False):
		# Get lemma and feedback
		self.feedback = ""
		self.messages = []
		if preferred:
			self.correct_ans = preferred
		else:
			self.correct_ans = accepted_answers
		self.correct_answers = ""
		self.case = ""
		self.userans = userans_val
		self.correct_anslist = []
		self.error = "empty"
		self.problems = "error"
		self.pron = ""
		self.pron_imp = ""
		self.PronPNBase = PRONOUNS_LIST
		self.is_relaxed = ""
		self.is_tcomm = ""
		forms = []
		relaxings = []
		if hasattr(self, 'translang'):
			if self.translang == 'sms':   # was: sme
 				# Relax spellings.
				accepted_answers = [force_unicode(item) for item in accepted_answers]
				forms = sum([relax(force_unicode(item)) for item in accepted_answers], [])
				# need to subtract legal answers and make an only relaxed list.
				relaxings = [item for item in forms if force_unicode(item) not in accepted_answers]
			#else:
		if (hasattr(self, 'gametype') and self.gametype == 'leksa'): # this applies only to Leksa
				# add infinitives as possible answers
			if self.word.pos == 'V':
				if self.translang in infinitives_sub and infinitives_add:
					infin_s = infinitives_sub[self.translang]
					infin_a = infinitives_add[self.translang]

					lemma = re.compile(infin_s)
					infins = [lemma.sub(infin_a, force_unicode(ax)) for ax in accepted_answers]
					accepted_answers = infins + accepted_answers

				forms = accepted_answers
		
		self.correct_anslist = [force_unicode(item) for item in accepted_answers] + \
							   [force_unicode(f) for f in forms]
		self.relaxings = relaxings



# #
#
# Morfa Forms 
#
# #

class MorfaSettings(OahpaSettings):
	"""
		A form for the settings part of the game form, e.g., the form used to
		set case, stem and source books for quiz questions.
		
		This is a separate form from the one which validates questions and
		answers.
	"""
	case = forms.ChoiceField(initial='N-ILL', choices=CASE_CHOICES, widget=forms.Select)
	pron_type = forms.ChoiceField(initial='PERS', choices=PRONOUN_SUBCLASSES, widget=forms.Select)
	proncase = forms.ChoiceField(initial='N-ILL', choices=CASE_CHOICES_PRONOUN, widget=forms.Select)
	adjcase = forms.ChoiceField(initial='ATTR', choices=ADJCASE_CHOICES, widget=forms.Select)  # was ADJEX_CHOICES
	vtype = forms.ChoiceField(initial='PRS', choices=VTYPE_CHOICES, widget=forms.Select)
	num_bare = forms.ChoiceField(initial='N-ILL', choices=NUM_BARE_CHOICES, widget=forms.Select)
	num_level = forms.ChoiceField(initial='1', choices=NUM_LEVEL_CHOICES, widget=forms.Select)
	num_type = forms.ChoiceField(initial='CARD',choices=NUM_TYPE_CHOICES, widget=forms.Select)
	derivation_type = forms.ChoiceField(initial='V-DER-PASS', choices=DERIVATION_CHOICES, widget=forms.Select)
	derivation_type_context = forms.ChoiceField(initial='DER-PASSV', choices=DERIVATION_CHOICES_CONTEXT, widget=forms.Select)
	num_context = forms.ChoiceField(initial='NUM-ATTR', choices=NUM_CONTEXT_CHOICES, widget=forms.Select)
	case_context = forms.ChoiceField(initial='N-SG-ACC', choices=CASE_CONTEXT_CHOICES, widget=forms.Select)
	adj_context = forms.ChoiceField(initial='ATTR', choices=ADJ_CONTEXT_CHOICES, widget=forms.Select)
	vtype_context = forms.ChoiceField(initial='V-PRS', choices=VTYPE_CONTEXT_CHOICES, widget=forms.Select)
	pron_context = forms.ChoiceField(initial='P-PERS', choices=PRON_CONTEXT_CHOICES, widget=forms.Select)
	wordform_type = forms.ChoiceField(initial='', choices=WORDFORM_TYPE_CHOICES, widget=forms.Select)
	book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select) 
	bisyllabic = forms.BooleanField(required=False, initial=True)
	trisyllabic = forms.BooleanField(required=False, initial=False)
	contracted = forms.BooleanField(required=False, initial=False)
	grade = forms.ChoiceField(initial='POS', choices=GRADE_CHOICES, widget=forms.Select) 
	
	def __init__(self, *args, **kwargs):
		self.set_settings()
		self.set_default_data()
		super(MorfaSettings, self).__init__(*args, **kwargs)

		# If this is set, then the form has been posted by the user otherwise
		# it hasn't
		try:
			post_data = args[0]
		except:
			post_data = False

		if post_data:
			# Use a restricted choice set for pronoun case for Refl and Recipr
			if 'pron_type' in post_data:
				if post_data['pron_type'].lower() in ['refl', 'recipr']:
					self.fields['proncase'].choices = RECIP_REFL_CHOICES




class MorfaQuestion(OahpaQuestion):
	"""
	Questions for morphology game. 
	"""

	def is_correct(self, game, example=None):
		"""
		Determines if the given answer is correct (for a bound form).
		"""
		self.game = game
		self.example = example

		# lookupserv

		from .lookup_client import lookup as t_lookup

		if not self.is_valid():
			return False
			
		self.userans = self.cleaned_data['answer']
		
		self.answer = self.userans.strip()
		
		if userans_val.strip():
			print 'zomg'
			success, l_data = t_lookup('sms-analyze-norm', userans_val.encode('utf-8'))
		
		# TODO: this should go in correct_anslist, which is probably a
		# list of FST-generated lemmas

		print self.correct_anslist

		self.error = "error"
		self.iscorrect = False
		
		if self.answer in set(self.correct_anslist) or \
				self.answer.lower() in set(self.correct_anslist) or \
				self.answer.upper() in set(self.correct_anslist):
			self.error = "correct"
			self.iscorrect = True
		
		# Log information about user answers.
		
		correctlist = u",".join([a for a in self.correct_anslist])
		self.correctlist = correctlist
		self.log_response()

	def set_correct(self):
		"""
		Adds correct wordforms to the question form.
		"""
		if self.correct_ans:
			self.correct_answers = self.correct_ans[:]
			if type(self.correct_answers) == list:
				self.correct_answers = ', '.join(self.correct_answers)
	
	
	def __init__(self, word, tag, baseform, correct, accepted_answers,
					answer_presentation, translations, question, dialect, language,
					userans_val, correct_val, conneg, *args, **kwargs):

		
		lemma_widget = forms.HiddenInput(attrs={'value': word.id})
		tag_widget = forms.HiddenInput(attrs={'value': tag.id})
		self.translang = 'sme'
		kwargs['correct_val'] = correct_val
		super(MorfaQuestion, self).__init__(*args, **kwargs)

		# initialize variables
		self.init_variables(possible=[], 
							userans_val=userans_val, 
							accepted_answers=accepted_answers)

		if tag.string.lower().find('conneg') > -1:
			if conneg:
				conneg_agr = conneg
			else:
				conneg_agr = choice(self.PronPNBase.keys())
		else:
			conneg_agr = False

		conneg_widget = forms.HiddenInput(attrs={'value': conneg_agr})

		self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
		self.fields['tag_id'] = forms.CharField(widget=tag_widget, required=False)
		self.fields['conneg'] = forms.CharField(widget=conneg_widget, required=False)

		try:
			self.lemma = baseform.fullform
		except AttributeError:
			self.lemma = baseform

		self.wordclass = word.wordclass
		if not self.pron:
			self.pron = False
		
		#print self.lemma, correct
		#print baseform.tag, correct.tag


		
		# Retrieve feedback information
		self.get_feedback(correct, language)
		
		# Take only the first translation for the tooltip
		if len(translations) > 0:
			self.translations = translations[0]
			
		if tag.pos == "N":
			self.case = tag.case

		if tag.pos == 'Pron':
			self.case = tag.case
					
		self.tag = tag.string
		
		if tag.pos == "V": 
			if not self.pron:
				if tag.string.find("ConNeg") > -1:
					# TODO: New choice for every refresh, fix!
					pers = conneg_agr
					pronoun = self.PronPNBase[pers]
					neg_verb = NEGATIVE_VERB_PRES[pers]

					self.pron = '%s %s' % (pronoun, neg_verb)
				elif tag.personnumber:
					pronbase = self.PronPNBase[tag.personnumber]
					pronoun = pronbase
					self.pron = pronoun
					
					if self.pron and tag.mood == "Imprt":
						self.pron_imp = "(" + self.pron + ")"
						self.pron = ""
					# TODO: conneg only in Prs
			
			# Odne 'today', ikte 'yesterday'
			if (tag.tense in ['Prs','Prt']) and (tag.mood == 'Ind'):
				time = TENSE_PRESENTATION.get(tag.tense, False)
				if (tag.personnumber == 'Sg4'):
				    self.pron = ' '.join([pronoun, time])  # Sg4: (4) Today ...
				else:
				    self.pron = ' '.join([time, pronoun])  # Sg1..Sg3, Pl1..Pl3: Today Pron ...

			if ("+Der/Pass" in tag.string) and ("+V" in tag.string):
				# Odne mun ___
				# Ikte mun ___
				# Ikte dat (okta) ___ 

				# Choose one if not set, if set then game is in progress, and
				# do not choose another
				pers = tag.personnumber
				if not pers:
					pers = conneg_agr
				time = TENSE_PRESENTATION.get(tag.tense, False) 
				pronoun = PASSIVE_PRONOUNS_LIST[pers]

				number = ''
				if pers in ['Sg3', 'Pl3']:
					number = '(%s)' % DEMONSTRATIVE_PRESENTATION.get(tag.personnumber, False)

				self.pron = ' '.join([time, pronoun, number])

			# All pres? 
			if tag.string.find("Der/AV") > -1:
				self.pron = TENSE_PRESENTATION.get(tag.tense, False) + " " + self.pron

		if tag.pos == "Pron":
			# Various display alternations for pronouns.
			
			# Reciprocative:
			# 	guhtet guoibmámet
			# 	goabbat guoibmámet

			if tag.subclass == 'Recipr':
				if tag.possessive.find('PxDu'):
					px_no = 'Du'
				elif tag.possessive.find('PxPl'):
					px_no = 'Pl'
				pronoun = RECIPROCATIVE_PRESENTATION.get(px_no, False)
				if pronoun:
					self.pron = pronoun

			# Demonstrative:
			# 	dát okta
			# 	dát máŋga

			if tag.subclass == 'Dem':
				noun_pres = DEMONSTRATIVE_PRESENTATION.get(tag.number, False)

				if noun_pres:
					self.lemma += ' (%s)' % force_unicode(noun_pres).encode('utf-8')
		
		log_name = "morfa_%s" % tag.pos
		try:
			self.is_correct(log_name, self.lemma + "+" + self.tag)
		except TypeError:
			self.is_correct(log_name, self.lemma.lemma + "+" + self.tag)
		
		# set correct and error values
		if correct_val:
			if correct_val == "correct":
				self.error="correct"
			# relax
			if userans_val in self.relaxings:
				self.is_relaxed = "relaxed"
				self.strict = 'Strict form'
			else:
				self.is_relaxed = ""
		
		self.correct_ans = answer_presentation
		

#  vim: set ts=4 sw=4 tw=72 syntax=python noexpandtab :
