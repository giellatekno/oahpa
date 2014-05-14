# -*- encoding: utf-8 -*-
from django import forms
from django.db.models import Q
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
import univ_oahpa.settings as settings

from univ_oahpa.conf.tools import switch_language_code

from models import *
#from game import * 
#from univ_oahpa.univ_drill.game import relax
import datetime
import socket
import sys, os, re
import itertools
from random import choice

# TODO: These should be accessible in the admin interface, not hardcoded.

PRONOUNS_LIST = {'Sg1':'mun', 'Sg2':'don', 'Sg3':'son',
		  'Pl1':'mii', 'Pl2':'dii', 'Pl3':'sii',
		  'Du1':'moai', 'Du2':'doai', 'Du3':'soai'}

# DEMONSTRATIVE_PRESENTATION plus Sg3/Pl3
PASSIVE_PRONOUNS_LIST = {'Sg1':'mun', 'Sg2':'don', 'Sg3':'dat',
		  'Pl1':'mii', 'Pl2':'dii', 'Pl3':'dat',
		  'Du1':'moai', 'Du2':'doai', 'Du3':'soai'}

POSSESSIVE_PRONOUNS_LIST = {'Sg1':'mu', 'Sg2':'du', 'Sg3':'su',
		  'Pl1':'min', 'Pl2':'din', 'Pl3':'sin',
		  'Du1':'munno', 'Du2':'dudno', 'Du3':'sudno'}

NEGATIVE_VERB_PRES = {'Sg1':'in', 'Sg2':'it', 'Sg3':'ii',
		  'Pl1':'eat', 'Pl2':'ehpet', 'Pl3':'eai',
		  'Du1':'ean', 'Du2':'eahppi', 'Du3':'eaba'}

TENSE_PRESENTATION = {
	'Prt': u'ikte',
	'Prs': u'odne',
	'PrfPrc': u'lea',
}

RECIPROCATIVE_PRESENTATION = {
	'Du': u'guhtet',
	'Pl': u'goabbat',
}

DEMONSTRATIVE_PRESENTATION = {
	'Sg': u'okta',
	'Sg3': u'okta',
	'Pl': u'máŋga',
	'Pl3': u'máŋga',
}

POS_CHOICES = (
	('N', _('noun')),
	('V', _('verb')),
	('A', _('adjective')),
	('Num', _('numeral')),
	('Pron', _('pronoun')),
)

CASE_CHOICES = (
	('NOMPL', _('plural')),
	('N-ACC', _('accusative')),
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
	('N-GEN', _('genitive')),
	('N-ESS', _('essive')),
)

# For now this is just a part of a test, used in game.Game.get_db_info_new
# I wanted a very general way to specify question/answers.

NOUN_QUESTION_ANSWER = {
	# gametype			question		answer
	'NOMPL': [('N+Sg+Nom', 'N+Pl+Nom')],
	'N-ACC': [('N+NumberN+Nom', 'N+NumberN+Acc')],
	'N-ILL': [('N+NumberN+Nom', 'N+NumberN+Ill')],
	'N-LOC': [('N+NumberN+Nom', 'N+NumberN+Loc')],
	'N-COM': [('N+NumberN+Nom', 'N+NumberN+Com')],
	'N-GEN': [('N+NumberN+Nom', 'N+NumberN+Gen')],
	'N-ESS': [('N+NumberN+Nom', 'N+Ess')],
}

NOUN_FILTER_DEFINITION = ['stem', 'source']

# Pers - akk, gen, ill, lok, kom
# Dem - akk, gen, ill, lok, kom
CASE_CHOICES_PRONOUN = (
	('N-ACC', _('accusative')),
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
	('N-GEN', _('genitive')),
	# ('N-ESS', _('essive')),
)

PRONOUN_QUESTION_ANSWER = {
	# gametype			question		answer
	'N-ACC': [('Pron+Subclass+NumberN+Nom', 'Pron+Subclass+NumberN+Acc')],
	'N-ILL': [('Pron+Subclass+NumberN+Nom', 'Pron+Subclass+NumberN+Ill')],
	'N-LOC': [('Pron+Subclass+NumberN+Nom', 'Pron+Subclass+NumberN+Loc')],
	'N-COM': [('Pron+Subclass+NumberN+Nom', 'Pron+Subclass+NumberN+Com')],
	'N-GEN': [('Pron+Subclass+NumberN+Nom', 'Pron+Subclass+NumberN+Gen')],
}

PRONOUN_FILTER_DEFINITION = ['pron_type',]

# Refl - ill, lok, kom
# Recipr - ill, lok, kom
RECIP_REFL_CHOICES = (
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
)

PRONOUN_SUBCLASSES = (
	('Pers', _('personal')),
	('Dem', _('demonstrative')),
	('Recipr', _('reciprocative')),
	('Refl', _('reflexive')),
	('Rel', _('relative')),
)

CASE_CONTEXT_CHOICES = (
	('N-NOM-PL', _('plural')),
	('N-ACC', _('accusative')),
	('N-GEN', _('genitive')),
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
	('N-ESS', _('essive')),
	('N-MIX', _('mix')),
)

# 
# No inessive or essive, and no choice between nom sg. and pl, but nom sg and pl come together.
# 
PRON_CONTEXT_CHOICES = (
	#('P-NOM', _('nominative')), Morfa C pronomen nominativ skal fjernes fra menyen dersom oppgavene har ingen hensikt.
	('P-PERS', _('personal')),
	('P-DEM', _('demonstrative')),
	('P-RECIPR', _('reciprocative')),
	('P-REFL', _('reflexive')),
	('P-REL', _('relative')),
)

WORDFORM_TYPE_CHOICES = (
	('goabbat', _('goabbat/guhtet')),
	('nubbi', _('nubbi/nuppit')),
)

ADJCASE_CHOICES = (
	('NOMPL', _('plural')),
	('ATTR', _('attributive')),
	('N-ACC', _('accusative')),
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
	('N-GEN', _('genitive')),
	('N-ESS', _('essive')),
)

ADJECTIVE_QUESTION_ANSWER = {
	# gametype			question		answer
	'NOMPL': [('A+Sg+Nom', 'A+Pl+Nom')],
	'ATTR': [('A+Sg+Nom', 'A+Attr')],
	'N-ACC': [('A+NumberA+Nom', 'A+NumberN+Acc')],
	'N-ILL': [('A+NumberA+Nom', 'A+NumberN+Ill')],
	'N-LOC': [('A+NumberA+Nom', 'A+NumberN+Loc')],
	'N-COM': [('A+NumberA+Nom', 'A+NumberN+Com')],
	'N-GEN': [('A+NumberA+Nom', 'A+NumberN+Gen')],
	'N-ESS': [('A+NumberA+Nom', 'A+Ess')],
}

ADJECTIVE_FILTER_DEFINITION = ['grade', 'stem', 'source']

ADJEX_CHOICES = (
	('A-ATTR', _('attributive')),	# A+Nom+Sg -> A+Attr
	('A-COMP', _('comparative')),		# A+Nom+Sg -> Comp	
	('A-SUPERL', _('superlative')),	# A+Nom+Sg -> Superl

)

ADJ_CONTEXT_CHOICES = (
	('ATTRPOS', _('attributive positive')),
	('ATTRCOMP', _('attributive comparative')),
	('ATTRSUP', _('attributive superlative')),
	('PREDPOS', _('predicative positive')),
	('PREDCOMP', _('predicative comparative')),
	('PREDSUP', _('predicative superlative')),
)

GRADE_CHOICES = (
	('POS', _('positive')),
	('COMP', _('comparative')),
	('SUPERL', _('superlative')),
)

NUM_CONTEXT_CHOICES = (
	('NUM-ATTR', _('attributive')),
	('NUM-NOM-PL', _('plural')),
	('NUM-ACC', _('accusative')),
	('NUM-ILL', _('illative')),
	('NUM-LOC', _('locative')),
	('NUM-COM', _('comitative')),
	('COLL-NUM', _('collective')),
	('ORD-NUM', _('ordinals')),
)

NUM_BARE_CHOICES = (
	('NOMPL', _('plural')),
	('N-ACC', _('accusative')),
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
)

NUMERAL_QUESTION_ANSWER = {
	# gametype			question		answer
	'N-ESS': [('Num+NumberN+Nom', 'Num+Ess')],
	'N-LOC': [('Num+NumberN+Nom', 'Num+NumberN+Loc')],
	'N-ILL': [('Num+NumberN+Nom', 'Num+NumberN+Ill')],
}

NUMERAL_FILTER_DEFINITION = ['stem', 'source']

NUM_LEVEL_CHOICES = (
	('1', _('First level')),
	('2', _('Second level')),
)

NUM_TYPE_CHOICES = (
	('CARD', _('cardinal')),
	('ORD', _('ordinal')),
	('COLL', _('collective')),
)

VTYPE_CHOICES = (
	('PRS', _('present')),
	('PRT', _('past')),
	('PRF', _('perfect')),
	('GER', _('gerund')),
	('COND', _('conditional')),
	('IMPRT', _('imperative')),
	('POT', _('potential')),
)

VERB_QUESTION_ANSWER = {
	'PRS': [('V+Inf', 'V+Ind+Prs+Person-Number')],
	'PRT': [('V+Inf', 'V+Ind+Prt+Person-Number')],
	'PRF': [('V+Inf', 'V+PrfPrc')],
	'GER': [('V+Inf', 'V+Ger')],
	'COND': [('V+Inf', 'V+Cond+Prs+Person-Number')],
	'IMPRT': [('V+Inf', 'V+Imprt+Person-Number')],
	'POT': [('V+Inf', 'V+Pot+Prs+Person-Number')],
}

VERB_FILTER_DEFINITION = ['stem', 'source']

VTYPE_CONTEXT_CHOICES = (
	('V-PRS', _('present')),
	('V-PRT', _('past')),
	('V-PRF', _('perfect')),
	('V-GER', _('gerund')),
	('V-COND', _('conditional')),
	('V-IMPRT', _('imperative')),
	('V-POT', _('potential')),
	('V-MIX', _('mix')),
	('TEST', _('test questions')),
 )

LEVEL_CHOICES = (
	('l1', _('Level 1')),
	('l2', _('Level 1-2')),
	('l3', _('Level 1-3')),
	('all', _('All')),
)


DERIVATION_CHOICES = (
	('V-DER-PASS', _('passive derivation')),
	('A-DER-V', _('adjective->verb derivation')),
)

POSSESSIVE_CHOICES = (
	('N-PX-GROUP1', _('Family')),
	('N-PX-GROUP2', _('Other')),
	('N-PX-GROUP3', _('All')),
)

POSSESSIVE_NUMBER_CHOICES = (
	('N-SG', _('Singular')),
	('N-DU', _('Dual')),
	('N-PL', _('Plural')),
)

POSSESSIVE_CHOICE_SEMTYPES = dict((
	('N-PX-GROUP1', ['FAMILY']),
	('N-PX-GROUP2', ['BODYPART', 'ANIMAL', 'PXPROPERTY',]),
	('N-PX-GROUP3', ['BODYPART', 'ANIMAL', 'PXPROPERTY', 'FAMILY',]),
))

POSSESSIVE_GROUP1_CASE = (
	('N-NOM', _('nominative')),
	('N-ACC', _('accusative')),
	('N-COM', _('comitative')),
	('N-GEN', _('genitive')),
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
)

POSSESSIVE_GROUP2_CASE = (
	('N-ACC', _('accusative')),
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
	('N-GEN', _('genitive')),
)

POSSESSIVE_GROUP3_CASE = (
    ('N-NOM', _('nominative')),
	('N-ACC', _('accusative')),
	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
	('N-COM', _('comitative')),
	('N-GEN', _('genitive')),
)

POSSESSIVE_CONTEXT_CHOICES = (
	('PX-ACC', _('accusative')),
	('PX-ILL', _('illative')),
	('PX-LOC', _('locative')),
	('PX-COM', _('comitative')),
	('PX-GEN', _('genitive')),
)


DERIVATION_QUESTION_ANSWER = {
	'A-DER-V': [('A+Sg+Nom', 'A+Der/AV+V+Ind+Prs+Person-Number')],
}

POSSESSIVE_QUESTION_ANSWER = {
	'N-PX-GROUP1': [('N+NumberN+Nom', 'N+NPxNumber+PxCase1+Possessive')],
	'N-PX-GROUP2': [('N+NumberN+Nom', 'N+NPxNumber+PxCase2+Possessive')],
	'N-PX-GROUP3': [('N+NumberN+Nom', 'N+NPxNumber+PxCase3+Possessive')],
}

POSSESSIVE_FILTER_DEFINITION = ['semtype']  # Heli

DERIVATION_FILTER_DEFINITION = False

DERIVATION_CHOICES_CONTEXT = (
	('A-DER-V', _('adjective->verb derivation')),
	('DER-PASSV', _('passive derivation')),
)

BOOK_CHOICES = (
	('d1', _('Davvin 1')),
	('d2', _('Davvin 1-2')),
	('d3', _('Davvin 1-3')),
	('d4', _('Davvin 1-4')),
	('AA', _('Aikio komp.')),
	('c1', _('Cealkke 1')),
	('c2', _('Cealkke 1-2')),
	('c3', _('Cealkke 1-3')),
	('c4', _('Cealkke 1-4')),
	('sam1031_1', _('SAM-1031-1')),
	('sam1031_2', _('SAM-1031-2')),
	('algu', _('algu')),
	('sara', _('sara')),
	('bures', _('Bures bures fas')),
	('oaidnalit', _('Oaidnalit')),
	('all', _('All')),
)

FREQUENCY_CHOICES = (
	('rare', _('rare')),
	('common', _('common')),
)

GEOGRAPHY_CHOICES = (
	('world', _('world')),
	('sapmi', _('sapmi')), # was: sápmi, maybe characters with diacritics not allowed in drop-down menus
	('suopma', _('suopma')),
)

VASTA_LEVELS = (
	('1', _('First level')),
	('2', _('Second level')),
	('3', _('Third level')),
)

VASTAS_LEVELS = (
	('1', _('Level 1')),
	('2', _('Level 2')),
	('3', _('Level 3')),
	('12', _('Level 1-2')),
	('13', _('Level 1-3')),
	#('all', _('All')),
)


VASTAS_NR_OF_TASKWORDS = (
	('2', _('2')),
	('3', _('3')),
	('4', _('4')),
)

TRANS_CHOICES = (
	('smenob', _('North Sami to Norwegian')),
	('nobsme', _('Norwegian to North Sami')),
#	('smeswe', _('North Sami to Swedish')),
#	('swesme', _('Swedish to North Sami')),
	('smefin', _('North Sami to Finnish')),
	('finsme', _('Finnish to North Sami')),
#	('smeeng', _('North Sami to English')),
#	('engsme', _('English to North Sami')),
#	('smedeu', _('North Sami to German')),
#	('deusme', _('German to North Sami')),
)

NUMLANGUAGE_CHOICES = (
	('sme', _('North Sami')),
#	('smj', _('Lule Sami')),
#	('sma', _('South Sami')),
#	('smn', _('Inari Sami')),
#	('sjd', _('Kildin Sami')),
#	('sms', _('Skolt Sami')),
#	('fin', _('Finnish')),
)

SEMTYPE_CHOICES = (
	('FAMILY', _('family')), 
	('HUMAN', _('human')),
	('HUMAN-LIKE', _('human-like')),
	('ANIMAL', _('animal')),
	('FOOD/DRINK', _('food/drink')),
	('TIME', _('time')),
	('CONCRETES', _('concretes')),
	('BODY', _('body')),
	('CLOTHES', _('clothes')),
	('BUILDINGS/ROOMS', _('buildings/rooms')),
	('CITY', _('city')), 
	('NATUREWORDS', _('naturewords')),
	('LEISURETIME/AT_HOME', _('leisuretime/at_home')),
	('CHRISTMAS', _('christmas')),
	('PLACES', _('places')),
	('LITERATURE', _('literature')),
	('SCHOOL/EDUCATION', _('school/education')),
	('ABSTRACTS', _('abstracts')),
	('WORK/ECONOMY/TOOLS', _('work/economy/tools')),
	('MULTIWORD', _('Multiword')),
	('all', _('all')),
)

NUM_CHOICES = (
	('10', _('0-10')),
	('20', _('0-20')),
	('100', _('0-100')),
	('1000', _('0-1000')),
#	('ALL', _('all')),
)

NUMGAME_CHOICES = (
	('string', _('String to numeral')),
	('numeral', _('Numeral to string')),
)

NUMGAME_CHOICES_PL = (
	('string', _('Strings to numerals')),
	('numeral', _('Numerals to strings')),
)

# These are not actually used in Forms, but used as a way to sneak these
# into the locale files so that the trans tag may be applied to
# form.wordclass without altering code here

VERB_CLASSES = (
	('I', _('I')),
	('II', _('II')),
	('III', _('III')),
	('IV', _('IV')),
	('V', _('V')),
	('VI', _('VI')),
	('Odd', _('Odd')),
)

KLOKKA_CHOICES = (
	('kl1', _('easy')),
	('kl2', _('medium')),
	('kl3', _('hard')),
)

DIALOGUE_CHOICES = (
	('firstmeeting', _('Firstmeeting')),
	('firstmeeting_boy', _('Firstmeeting boy')),
	('firstmeeting_girl', _('Firstmeeting girl')),
	('firstmeeting_man', _('Firstmeeting man')),
	('visit', _('Visit')),
	('grocery', _('Grocery')),
	('shopadj', _('Shopadj')),
)

# BOOK_CHOICES = tuple(
#	[(source.name, source.name) for source in Source.objects.all()] + \
#	[('all', _('ALL'))]
# )


# Syllables are manually coded in the templates, but it's useful to get the
# translation strings here, also for the courses module logging.

SYLLABLE_VALUES = (
	('2syll', _('bisyllabic')),
	('3syll', _('trisyllabic')),
	('Csyll', _('contracted')),
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
	POSSESSIVE_CONTEXT_CHOICES, 
	PRONOUN_SUBCLASSES, 
	PRON_CONTEXT_CHOICES,
	RECIP_REFL_CHOICES, 
	SEMTYPE_CHOICES, 
	SYLLABLE_VALUES,
	TRANS_CHOICES, 
	VASTA_LEVELS,
	VASTAS_LEVELS,
	VASTAS_NR_OF_TASKWORDS, 
	VERB_CLASSES,
	VTYPE_CHOICES, 
	VTYPE_CONTEXT_CHOICES]


GAME_TYPE_DEFINITIONS = {
	'A': ADJECTIVE_QUESTION_ANSWER,
	'Der': DERIVATION_QUESTION_ANSWER,
	'Px': POSSESSIVE_QUESTION_ANSWER,
	'N': NOUN_QUESTION_ANSWER,
	'Num': NUMERAL_QUESTION_ANSWER,
	'Pron': PRONOUN_QUESTION_ANSWER,
	'V': VERB_QUESTION_ANSWER,
}

GAME_FILTER_DEFINITIONS = {
	'A': ADJECTIVE_FILTER_DEFINITION,
	'Der': DERIVATION_FILTER_DEFINITION,
	'Px': POSSESSIVE_FILTER_DEFINITION,
	#'Px': POSSESSIVE_QUESTION_ANSWER,  # Is that correct?
	'N': NOUN_FILTER_DEFINITION,
	'Num': NUMERAL_FILTER_DEFINITION,
	'Pron': PRONOUN_FILTER_DEFINITION,
	'V': VERB_FILTER_DEFINITION,
}

# #
#
# Form validation
#
# #


import re

from univ_oahpa.settings import INFINITIVE_SUBTRACT as infinitives_sub
from univ_oahpa.settings import INFINITIVE_ADD as infinitives_add

def relax(strict):
	"""Returns a list of relaxed possibilities, making changes by relax_pairs.
		
		Many possibilities are generated in the event that users are
		inconsistent in terms of substituting one letter but not substituting 
		another, however, *all* possibilities are not generated.
		
		E.g., *ryøjnesjäjja is accepted for ryöjnesjæjja
				(user types ø instead of ö consistently)
				
				... but ...
			  
			  *töølledh is not accepted for töölledh
				(user mixes the two in one word)
		
		Similarly, directionality is included. <i> is accepted for <ï>, but
		not vice versa.
		
		E.g.:  *ååjmedïdh is not accepted for ååjmedidh, 
				... but ...
				*miele is accepted for mïele.
	"""
	from django.utils.encoding import force_unicode
	
	relaxed = strict
	sub_str = lambda _string, _target, _sub: _string.replace(_target, _sub)
	
	relax_pairs = {
		# key: value
		# key is accepted for value
		u'ø': u'ö',
		u'ä': u'æ',
		u'i': u'ï'
	}
	
	# Create an iterator. We want to generate as many possibilities as 
	# possible (very fast), so more relaxed options are available.
	searches = relax_pairs.items()
	permutations = itertools.chain(itertools.permutations(searches))
	perms_flat = sum([list(a) for a in permutations], [])
	
	# Individual possibilities
	relaxed_perms = [sub_str(relaxed, R, S) for S, R in perms_flat]
	
	# Possibilities applied one by one
	for S, R in perms_flat:
		relaxed = sub_str(relaxed, R, S)
		relaxed_perms.append(relaxed)
	
	# Return list of unique possibilities
	relaxed_perms = list(set(relaxed_perms))
	relaxed_perms = [force_unicode(item) for item in relaxed_perms]

	return relaxed_perms

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
	#		'l1':  ['l1'],
	#		'l2':  ['l2', 'l1'], 
	#		'l3':  ['l3', 'l2', 'l1'], 
	#		'all': ['l3', 'l2', 'l1', 'all'], 
	#	}
	
	# Construct arrays for level choices.
	
	# Commenting this out because I don't see yet why this needs to be constructed this way.
	# If it's done automatically so that more levels can be added, the code here will still need
	# to be altered... So it seems easiest to just hard-code this for now.
	
	# self.levels = {}
	# self.levels['all'] = [] 
	# for b in LEVEL_CHOICES:
	#	if b[0] != 'all':
	#		self.levels[b[0]] = [] 
	#		self.levels['all'].append(b[0])
	#		
	#	self.levels[b[0]].append(b[0])
	# 
	# self.levels['l2'].append('l1')
	# for b in ['l1', 'l2']:
	#	self.levels['l3'].append(b)
	
	
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
	self.syll = dict(SYLLABLE_VALUES).keys() # added by Heli


# comment
# DEBUG = open('/dev/ttys001', 'w')
# DEBUG = open('/dev/null', 'w')


def get_feedback(self, wordform, language):

	language = switch_language_code(language)
	
	# TODO: user_level depends on the wordform and the user's feedback
	# log entries.

	# TODO: need to also select the nearest level to the user's level,
	# so that if the user's level has no message, then we get the
	# highest level available.
	feedbacks = wordform.feedback.filter(feedbacktext__language=language)\
					.order_by('feedbacktext__order')\
					.order_by('feedbacktext__user_level')
	
	feedback_messages = []
	feedback_ids = []

	# TODO: default ordering of feedback by user_level, so that 1 always
	# comes up first.
	for feedback in feedbacks:
		texts = feedback.feedbacktext_set.filter(language=language)\
											.order_by('order')\
											.order_by('user_level')
		feedback_messages.extend([a.message for a in texts])
		feedback_ids.append(feedback.msgid)

	try:
		baseform = wordform.getBaseform()
	except:
		baseform = wordform
	
	message_list = []
	if feedback_messages:
		for text in feedback_messages:
			fenc = lambda x: force_unicode(x)
			text = text.replace('WORDFORM', '"%s"' % fenc(baseform.word.lemma))
			message_list.append(text)
	
	self.feedback = ' \n '.join(list(message_list))
	self.feedback_ids = ','.join(feedback_ids)

	### print 'stem:' + wordform.word.stem
	### print 'gradation:' + wordform.word.gradation
	### print 'diphthong:' + wordform.word.diphthong
	### print 'rime:' + wordform.word.rime
	### print 'soggi:' + wordform.word.soggi
	### print 'attrsuffix:' + wordform.word.attrsuffix
	### print 'compsuffix:' + wordform.word.compsuffix


	### print 'feedback:' + self.feedback
	### print '--'
	### # NOTE: debug
	### # print wordform.id
	### # print wordform.feedback.all()
	### # print feedbacks
	### # print self.feedback

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
				if isinstance(qelem, QElement):  # to exclude MorfaC 
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
				
				form_list = filter_set_by_dialect(form_list, self.dialect)
				if form_list.count() > 0:
					fullf = []
					for f in form_list:
						fullf.append(f.fullform)
					selected_awords[syntax]['fullform'] = fullf[:]

		# make sure that there is something to print
		if not selected_awords[syntax].has_key('fullform'):
			selected_awords[syntax]['fullform'] = []
			selected_awords[syntax]['fullform'].append(syntax)
		# print "selected awords: "
		# print selected_awords
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
		# x = self.cleaned_data.get('bisyllabic'
		# print 'clean: ', x
		return self.cleaned_data
	
	def set_default_data(self):
		self.default_data = {
					'language' : 'sme', # why rus ?
					'syll' : ['2syll','3syll','Csyll'],
					'bisyllabic': True,  # was 'on'
					'trisyllabic': True,
					'contracted': True,
					'level' : 'all',
					'lemmacount' : ['2','3','4'], # was: '2', but we have removed the lemmacount menu from the GUI
					'case': 'NOMPL',
					'pos' : 'N',
					'vtype' : 'PRS',
					'adjcase' : 'ATTR',
					'number' : '',
					'pron_type': 'Pers',
					'proncase' : 'N-ACC', # was 'NOMPL'
					'grade' : '',  # was: '' 'Pos' is not a good idea beacuse it is implicit in the database.
					'case_context' : 'N-NOM-PL',
					'vtype_context' : 'V-PRS',
					'pron_context' : 'P-PERS',
					'num_context' : 'NUM-ATTR',
					'num_level' : '1',
					'num_type' : 'CARD',  # added by Heli
					'derivation_type' : 'V-DER-PASS',
					'derivation_type_context' : 'DER-PASSV', # was V-DER

					'possessive_type': 'N-PX-GROUP1',
					'possessive_number': 'N-SG',

					'possessive_case': "N-ACC",
					'possessive_case_context': 'PX-ACC',  # MorfaC px
					'geography': 'world',
					'frequency' : ['common'],
					'num_bare' : 'NOMPL',
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

		log_kwargs = {
			'userinput': self.answer,
			'correct': ','.join(self.correct_anslist),
			'iscorrect': self.iscorrect,
			'example': self.example,
			'game': self.game,
			'date': today
		}
		if self.user:
			log_kwargs['username'] = self.user.username
		if self.user_country:
			log_kwargs['user_country'] = self.user_country

		log, c = Log.objects.get_or_create(**log_kwargs)
		self.last_log = log
	
	def __init__(self, *args, **kwargs):
		correct_val = False
		if 'correct_val' in kwargs:
			correct_val = kwargs.get('correct_val')
			kwargs.pop('correct_val')

		if 'user' in kwargs:
			self.user = kwargs.pop('user')
		else:
			self.user = False

		if 'user_country' in kwargs:
			self.user_country = kwargs.pop('user_country')
		else:
			self.user_country = False
		
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
			if self.translang == 'sme':
				# Relax spellings.
				accepted_answers = [force_unicode(item) for item in accepted_answers]
				forms = sum([relax(force_unicode(item)) for item in accepted_answers], [])
				# need to subtract legal answers and make an only relaxed list.
				relaxings = [item for item in forms if force_unicode(item) not in accepted_answers]
			else:

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

		#def generate_fields(self,answer_size, maxlength):
		#	self.fields['answer'] = forms.CharField(max_length = maxlength, \
		 #									   widget=forms.TextInput(\
		  #  attrs={'size': answer_size, 'onkeydown':'javascript:return process(this, event,document.gameform);',}))  # copied from old-oahpa

# #
#
# Leksa Forms
#
# #

class LeksaSettings(OahpaSettings):
	semtype = forms.ChoiceField(initial='HUMAN', choices=SEMTYPE_CHOICES)
	transtype = forms.ChoiceField(choices=TRANS_CHOICES, widget=forms.Select)
	# For placename quizz
	geography = forms.ChoiceField(initial='world', choices=GEOGRAPHY_CHOICES)
	#frequency = forms.MultipleChoiceField(required=False, widget=CheckboxSelectMultiple, choices=FREQUENCY_CHOICES)  # added
	common = forms.BooleanField(required=False, initial='1')
	rare = forms.BooleanField(required=False,initial=0)
	# sapmi = forms.BooleanField(required=False, initial='1')
	# world = forms.BooleanField(required=False,initial=0)
	# suopma = forms.BooleanField(required=False,initial=0)
	source = forms.ChoiceField(initial='all', choices=BOOK_CHOICES)
	# level = forms.ChoiceField(initial='all', choices=LEVEL_CHOICES, widget=forms.Select(attrs={'onchange':'javascript:return SetIndex(document.gameform.semtype,this.value);',}))
	
	default_data = {'gametype' : 'bare', 'language' : 'sme', 'dialogue' : 'GG', 
			'syll' : [], 
			'bisyllabic': False,
			'trisyllabic': False,
			'contracted': False,
			'source': 'all',
			'semtype' : 'HUMAN',
			'geography' : 'world',
			'frequency' : ['common'] # added
			}

	
	# set default language pair from session language setting.
	def __init__(self, *args, **kwargs):
		if 'initial_transtype' in kwargs:
			initial_transtype = kwargs.pop('initial_transtype')
		else:
			initial_transtype = False

		self.set_settings()
		super(LeksaSettings, self).__init__(*args, **kwargs)

		if initial_transtype:
			self.fields['transtype'].initial = initial_transtype
			self.default_data['transtype'] = initial_transtype
	

class LeksaQuestion(OahpaQuestion):
	"""
	Questions for word quizz
	"""
	
	def __init__(self, tcomms, stat_pref, preferred, possible, transtype, word, correct, translations, question, userans_val, correct_val, *args, **kwargs):
		lemma_widget = forms.HiddenInput(attrs={'value' : word.id})
		self.translang = transtype[-3::]
		self.word = word
		kwargs['correct_val'] = correct_val
		super(LeksaQuestion, self).__init__(*args, **kwargs)
				
		self.tcomm = None
		if tcomms:
			if userans_val in tcomms:
				self.tcomm = True
			else:
				self.tcomm = None

		
		self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
		
		if type(word) == Word:
			self.lemma = word.lemma
		else:
			self.lemma = word.definition
		
		if word.pos.upper() == 'V':
			if word.language in infinitives_sub and infinitives_add:
				infin_s = infinitives_sub[word.language]
				infin_a = infinitives_add[word.language]

				lemma = re.compile(infin_s)
				lemmax = lemma.sub(infin_a, force_unicode(self.lemma))
				self.lemma = force_unicode(lemmax)

		self.init_variables(possible=translations, 
							userans_val=userans_val, 
							accepted_answers=possible, 
							preferred=preferred)
		
		self.is_correct("leksa", self.lemma)
		# set correct and error values
		if correct_val:
			if correct_val == "correct":
				self.error = "correct"
			# relax
			if userans_val in self.relaxings:
				self.is_relaxed = "relaxed"
				self.strict = 'Strict form'
			else:
				self.is_relaxed = ""
		
		if stat_pref:
			self.correct_ans = stat_pref

		# Displayed answer also needs infinitive marking
		# Needs to happen last because of stat_pref
		if word.pos.upper() == 'V':
			if self.translang in infinitives_sub and infinitives_add:
				infin_s = infinitives_sub[self.translang]
				infin_a = infinitives_add[self.translang]
		
				lemma = re.compile(infin_s)
				
				self.correct_ans = [lemma.sub(infin_a, force_unicode(ax)) for ax in self.correct_ans]
				self.correct_ans = [force_unicode(ax) for ax in self.correct_ans]
		
	


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
	case = forms.ChoiceField(initial='NOMPL', choices=CASE_CHOICES, widget=forms.Select)
	pron_type = forms.ChoiceField(initial='PERS', choices=PRONOUN_SUBCLASSES, widget=forms.Select)
	proncase = forms.ChoiceField(initial='NOMPL', choices=CASE_CHOICES_PRONOUN, widget=forms.Select)
	adjcase = forms.ChoiceField(initial='ATTR', choices=ADJCASE_CHOICES, widget=forms.Select)  # was ADJEX_CHOICES
	vtype = forms.ChoiceField(initial='PRS', choices=VTYPE_CHOICES, widget=forms.Select)
	num_bare = forms.ChoiceField(initial='NOMPL', choices=NUM_BARE_CHOICES, widget=forms.Select)
	num_level = forms.ChoiceField(initial='1', choices=NUM_LEVEL_CHOICES, widget=forms.Select)
	num_type = forms.ChoiceField(initial='CARD',choices=NUM_TYPE_CHOICES, widget=forms.Select)
	derivation_type = forms.ChoiceField(initial='V-DER-PASS', choices=DERIVATION_CHOICES, widget=forms.Select)
	derivation_type_context = forms.ChoiceField(initial='DER-PASSV', choices=DERIVATION_CHOICES_CONTEXT, widget=forms.Select)
	# TODO: Px - N-ACC here, but problem is N-NOM isn't available in all
	# types. was: initial=None
	possessive_case = forms.ChoiceField(initial='N-ACC', choices=POSSESSIVE_GROUP1_CASE, widget=forms.Select, required=False)
	possessive_type = forms.ChoiceField(initial='N-PX-GROUP1', choices=POSSESSIVE_CHOICES, widget=forms.Select)
	possessive_number = forms.ChoiceField(initial='N-SG', choices=POSSESSIVE_NUMBER_CHOICES, widget=forms.Select)
	possessive_case_context = forms.ChoiceField(initial='PX-ACC',choices=POSSESSIVE_CONTEXT_CHOICES, widget=forms.Select, required=False)
	num_context = forms.ChoiceField(initial='NUM-ATTR', choices=NUM_CONTEXT_CHOICES, widget=forms.Select)
	case_context = forms.ChoiceField(initial='N-NOM-PL', choices=CASE_CONTEXT_CHOICES, widget=forms.Select)
	adj_context = forms.ChoiceField(initial='ATTR', choices=ADJ_CONTEXT_CHOICES, widget=forms.Select)
	vtype_context = forms.ChoiceField(initial='V-PRS', choices=VTYPE_CONTEXT_CHOICES, widget=forms.Select)
	pron_context = forms.ChoiceField(initial='P-PERS', choices=PRON_CONTEXT_CHOICES, widget=forms.Select)
	book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select) 
	bisyllabic = forms.BooleanField(required=False, initial=True)
	trisyllabic = forms.BooleanField(required=False, initial=True)
	contracted = forms.BooleanField(required=False, initial=True)
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

			_ptype = post_data.get('possessive_type', False)
			if _ptype:
				self.fields['possessive_case'].choices = {
					'N-PX-GROUP1': POSSESSIVE_GROUP1_CASE,
					'N-PX-GROUP2': POSSESSIVE_GROUP2_CASE,
					'N-PX-GROUP3': POSSESSIVE_GROUP3_CASE,
				}[post_data['possessive_type']]

			### # check the case against choices in new set and select
			### # default if not present
			### problem occurs because nominative is not among the possible cases for possessive type 'other' (not 'family')
			### _pcase = post_data.get('possessive_case', False)
			### if _pcase:
			###	if _pcase == 'N-NOM' and _ptype == 'N-PX-GROUP2':
			###		_new_default = 'N-ACC'
			###	else:
			###		_new_default = _pcase
			###	self.fields['possessive_case'].default = _new_default
			###	self.fields['possessive_case'].initial = _new_default
			###	self.default_data['possessive_case'] = _new_default

			### if _pcase:
			 ###	_possible_cases = [
			 ###		a[0] for a in self.fields['possessive_case'].choices
			 ###	]
			 ###	if not _pcase in _possible_cases:
			 ###		print "omg problems"
			 ###		_new_default = 'N-ACC' # self.fields['possessive_case'].choices[0][0]
			 ###		self.fields['possessive_case'].default = _new_default

			### print self.fields['possessive_case']
			### _new_default = 'N-ACC'
			### _new_default = self.fields['possessive_case'].choices[0][0]





class MorfaQuestion(OahpaQuestion):
	"""
	Questions for morphology game. 
	"""
	
	def __init__(self, word, tag, baseform, correct, accepted_answers,
					answer_presentation, translations, question, dialect, language,
					userans_val, correct_val, conneg, *args, **kwargs):
		
		lemma_widget = forms.HiddenInput(attrs={'value': word.id})
		tag_widget = forms.HiddenInput(attrs={'value': tag.id})
		self.translang = 'sme'
		self.dialect = dialect
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
			if tag.possessive:
				pers = tag.possessive.replace('Px', '')
				pronoun = POSSESSIVE_PRONOUNS_LIST[pers]
				num = DEMONSTRATIVE_PRESENTATION.get(tag.number, False)
				if num:
					num = ' ' + num
				else:
					num = ''
				self.pron = '(%s%s)' % (pronoun, num)

		if tag.pos == 'Pron':
			self.case = tag.case
					
		self.tag = tag.string
		
		if tag.pos == "V": 
			_pronoun_presentation = False
			_tense_presentation = False
			_neg_presentation = False
			_number_presentation = False
			if not self.pron:
				if tag.string.find("ConNeg") > -1:
					# TODO: New choice for every refresh, fix!
					pers = conneg_agr
					pronoun = self.PronPNBase[pers]
					neg_verb = NEGATIVE_VERB_PRES[pers]
					
					_pronoun_presentation = pronoun
					_neg_presentation = neg_verb
				elif tag.personnumber:
					pronbase = self.PronPNBase[tag.personnumber]
					pronoun = pronbase
					_pronoun_presentation = pronoun
					self.pron = pronoun
					
					if self.pron and tag.mood == "Imprt":
						self.pron_imp = "(" + self.pron + ")"
						self.pron = ""
						_pronoun_presentation = False
					# TODO: conneg only in Prs
			
			# Odne 'today', ikte 'yesterday'
			
			# All pres? 
			
			# son -> dat (okta), sii -> dat (máŋga)
			# because some verbs are not suitable to use with a human as object:

			if tag.subclass in ["Der/AV","Der/PassL"]:
				if pronoun == 'son':
					pronoun = "dat (okta)"
				elif pronoun == 'sii':
					pronoun = force_unicode("dat (máŋga)")

			if tag.string.find("Der/AV") > -1 or tag.tense in ['Prs','Prt'] and tag.mood == 'Ind':
				time = TENSE_PRESENTATION.get(tag.tense, False)
				_tense_presentation = time
			elif tag.string == "V+PrfPrc":
				time = TENSE_PRESENTATION.get(tag.infinite, False)
				_tense_presentation = time

			elif ("+Der/Pass" in tag.string) and ("+V" in tag.string):
				# Odne mun ___
				# Ikte mun ___
				# Ikte dat (okta) ___ 

				# Choose one if not set, if set then game is in progress, and
				# do not choose another
				pers = tag.personnumber
				if not pers:
					pers = conneg_agr
				time = TENSE_PRESENTATION.get(tag.tense, False) 
				_tense_presentation = time
				pronoun = PASSIVE_PRONOUNS_LIST[pers]
				_pronoun_presentation = pronoun

				number = ''
				if pers in ['Sg3', 'Pl3']:
					number = '(%s)' % DEMONSTRATIVE_PRESENTATION.get(tag.personnumber, False)
					_number_presentation = number

			self.pron = ' '.join([a for a in [_tense_presentation,
											  _pronoun_presentation,
											  _number_presentation,
											  _neg_presentation] if a])

			
		if tag.pos == "Pron":
			# Various display alternations for pronouns.
			
			# Reciprocative:
			#	guhtet guoibmámet
			#	goabbat guoibmámet

			if tag.subclass == 'Recipr':
				if tag.possessive.find('PxDu'):
					px_no = 'Du'
				elif tag.possessive.find('PxPl'):
					px_no = 'Pl'
				pronoun = RECIPROCATIVE_PRESENTATION.get(px_no, False)
				if pronoun:
					self.pron = pronoun

			# Demonstrative:
			#	dát okta
			#	dát máŋga

			if tag.subclass == 'Dem':
				noun_pres = DEMONSTRATIVE_PRESENTATION.get(tag.number, False)

				if noun_pres:
					# self.lemma is unicode, concatenating results in
					# encoding error
					self.lemma = u"%s %s" % (self.lemma, noun_pres)
					self.lemma = self.lemma.encode('utf-8')
					#self.lemma += u'( %s)' % noun_pres
					#self.lemma = force_unicode(self.lemma).encode('utf-8')

			# Personal pronouns:
			# mun, don, son, mii, dii, sii, moai, doai etc.
			# plus dat (okta), dat (máŋga)

			if tag.subclass == 'Pers':
				if self.lemma == 'dat':
					noun_pres = DEMONSTRATIVE_PRESENTATION.get(tag.personnumber, False)
					if noun_pres:
						self.lemma = u"%s (%s)" % (self.lemma, noun_pres)
						self.lemma = force_unicode(self.lemma).encode('utf-8')
						#self.lemma += u' (%s)' % noun_pres
						#self.lemma = force_unicode(self.lemma).encode('utf-8')
						
		
		log_name = "morfa_%s" % tag.pos
		self.tag = force_unicode(self.tag).encode('utf-8')
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
# #
#
# Numra Forms
#
# #


class NumSettings(OahpaSettings):
	maxnum = forms.ChoiceField(initial='10', choices=NUM_CHOICES, widget=forms.RadioSelect)
	numgame = forms.ChoiceField(initial='string', choices=NUMGAME_CHOICES, widget=forms.RadioSelect)
	numlanguage = forms.ChoiceField(initial='sme', choices=NUMLANGUAGE_CHOICES, widget=forms.RadioSelect)
	# TODO: remove mandatory need to set default data, should be done through 'initial' field setting.
	default_data = {'language' : 'nob', 'numlanguage' : 'sme', 'dialect' : 'GG', 'maxnum' : '10', 'numgame': 'string'}  # dialogue = 'GG' ???
					
	def __init__(self, *args, **kwargs):
		self.set_settings()
		super(NumSettings, self).__init__(*args, **kwargs)


class NumQuestion(OahpaQuestion):
	"""
	Questions for numeral quizz
	"""
	game_log_name = 'numra'

	def answer_relax(self, answer):
		""" Method for relaxing answers. Override if needed.
		"""

		return answer

	def is_correct(self, game, example=None):
		self.game = game
		self.example = example

		if not self.is_valid():
			return False

		self.userans = self.cleaned_data['answer']
		self.answer = self.userans.strip()

		self.error = "error"
		self.iscorrect = False

		correct_test = self.game_obj.check_answer(self.question_str, 
													self.userans, 
													self.correct_anslist)
		if correct_test:
			self.error = "correct"
			self.iscorrect = True

		self.correctlist = u",".join(list(set(self.correct_anslist)))
		
		self.log_response()

	
	def __init__(self, numeral, num_string, num_list, gametype, userans_val, correct_val, game, *args, **kwargs):
		numeral_widget = forms.HiddenInput(attrs={'value' : numeral})
		kwargs['correct_val'] = correct_val
		self.userans_val = self.userans = userans_val
		self.game_obj = game

		if 'no_eval_correct' in kwargs:
			no_eval_correct = kwargs.pop('no_eval_correct')
		else:
			no_eval_correct = False

		super(NumQuestion, self).__init__(*args, **kwargs)
		wforms = []
		self.relaxings = []
		
		# Initialize variables
		if gametype == "string":
			self.init_variables(force_unicode(numeral), userans_val, [ numeral ])
			example = num_string
			self.question_str = num_string
		else:
			self.init_variables(force_unicode(num_list[0]), userans_val, num_list)
			wforms = sum([relax(force_unicode(item)) for item in num_list], [])
			# need to subtract legal answers and make an only relaxed list.
			self.relaxings = [item for item in wforms if item not in num_list]
			example = numeral
			self.question_str = numeral
		
		self.correct_anslist = self.correct_anslist + [force_unicode(f) for f in wforms]
		
		self.fields['numeral_id'] = forms.CharField(widget=numeral_widget, required=False)
		
		if gametype == "string":
			self.numstring = num_string
		self.numeral = numeral
		
		# Correctness not evaluated here but in child class. Short fix 
		
		if not no_eval_correct:
			self.is_correct(self.game_log_name, example)
		
		if correct_val:
			if correct_val == "correct":
				self.error = "correct"
			# relax
			if userans_val in self.relaxings:
				self.is_relaxed = "relaxed"
				self.strict = 'Strict form'
			else:
				self.is_relaxed = ""
		
		
# #
#
# Klokka Forms
#
# #


class KlokkaSettings(NumSettings):
	numgame = forms.ChoiceField(initial='string', choices=NUMGAME_CHOICES_PL, widget=forms.RadioSelect)
	gametype = forms.ChoiceField(initial='kl1', choices=KLOKKA_CHOICES, widget=forms.RadioSelect)
	default_data = {'language' : 'nob', 'numlanguage' : 'sme', 'dialogue' : 'GG', 'gametype' : 'kl1', 'numgame': 'string'}
					
	def __init__(self, *args, **kwargs):
		self.set_settings()
		super(KlokkaSettings, self).__init__(*args, **kwargs)


class KlokkaQuestion(NumQuestion):
	"""
	Questions for numeral quizz
	"""
	game_log_name = "klokka"

	def relax_military(self, number):
		""" Change the presentation of numerals above 13 to their lower equivalents.

		"""
		military = [
			('13', '01'),
			('14', '02'),
			('15', '03'),
			('16', '04'),
			('17', '05'),
			('18', '06'),
			('19', '07'),
			('20', '08'),
			('21', '09'),
			('22', '10'),
			('23', '11'),
			('00', '12'),
		]
		military_dict = dict(military)

		options = [number]
		hh, _, mm = number.partition(':')
		
		try:
			switched = '%s:%s' % (military_dict[hh], mm)
			return switched
		except KeyError:
			return number

	def __init__(self, *args, **kwargs):
		present_list = kwargs.get('present_list')
		accept_list = kwargs.get('accept_list')
		kwargs.pop('present_list')
		kwargs.pop('accept_list')
		
		numeral = kwargs.get('numeral')
		num_string = kwargs.get('num_string')
		correct_val = kwargs.get('correct_val')
		userans_val = kwargs.get('userans_val')
		self.gametype = gametype = kwargs.get('gametype')
		prefix = kwargs.get('prefix')
		data = kwargs.get('data')


		numeral_widget = forms.HiddenInput(attrs={'value' : numeral})
		kwargs['correct_val'] = correct_val
		self.userans_val = self.userans = userans_val
		
		kwargs['num_list'] = present_list
		# Prevent double evaluation of correctness

		kwargs['no_eval_correct'] = True
		super(KlokkaQuestion, self).__init__(*args, **kwargs)

		wforms = []
		self.relaxings = []
		# Initialize variables
		if gametype == "string":
			self.init_variables(force_unicode(numeral), userans_val, [ numeral ])
			example = num_string
			
		else:
			self.init_variables(force_unicode(accept_list), userans_val, present_list)
			wforms = sum([relax(force_unicode(item)) for item in accept_list], [])
			# need to subtract legal answers and make an only relaxed list.
			self.relaxings = [item for item in wforms if item not in accept_list]
			example = numeral
		
		self.correct_anslist = self.correct_anslist + [force_unicode(f) for f in wforms]

		
		self.fields['numeral_id'] = forms.CharField(widget=numeral_widget, required=False)
		
		self.numstring = num_string

		# Need to change presentation of certain numerals to avoid 
		if gametype == "string":
			relaxed_presentation = [self.relax_military(a) for a in self.correct_anslist[:]]
			self.correct_ans = relaxed_presentation + self.correct_anslist
			self.correct_ans = self.correct_ans[0]
		else:
			# Clear numstring to switch presentation
			self.numstring = None

		
		self.numeral = numeral

		self.is_correct(self.game_log_name, example)
		
		if correct_val:
			if correct_val == "correct":
				self.error = "correct"
			# relax
			if userans_val in self.relaxings:
				self.is_relaxed = "relaxed"
				self.strict = 'Strict form'
			elif userans_val in accept_list and userans_val not in present_list:
				self.is_relaxed = "relaxed"
				self.strict = 'Strict form'
			else:
				self.is_relaxed = ""
	
	def is_correct(self, game, example=None):
		self.game = game
		self.example = example

		if not self.is_valid():
			return False

		self.userans = self.cleaned_data['answer']
		self.answer = self.userans.strip()

		self.error = "error"
		self.iscorrect = False

		correct_test = self.game_obj.check_answer(self.question_str, 
													self.userans, 
													self.correct_anslist)
		if correct_test:
			self.error = "correct"
			self.iscorrect = True

		self.correctlist = u",".join(list(set(self.correct_anslist)))
		
		self.log_response()


# #
#
# Dato Forms
#
# #

class DatoSettings(KlokkaSettings):
	gametype = None # Disable gametype (easy, medium, hard)

	default_data = {'language' : 'nob', 'numlanguage' : 'sme', 'numgame': 'string'}


class DatoQuestion(KlokkaQuestion):
	
	game_log_name = "dato"

	def answer_relax(self, answer):
		""" No need to relax.
		"""

		return answer




# #
#
# MorfaC Forms
#
# #


class ContextMorfaQuestion(OahpaQuestion):
	"""
	Questions for contextual morfa
	"""

	select_words = select_words
	qtype_verbs = set(['V-PRS', 'V-PRT', 'V-COND','V-IMPRT', 'TEST'])

	def generate_fields(self,answer_size, maxlength):
		self.fields['answer'] = forms.CharField(max_length = maxlength, \
												widget=forms.TextInput(\
			attrs={'size': answer_size,}))
			
			# 'onkeydown':'javascript:return process(this, event,document.gameform);'
	
	def __init__(self, question, qanswer, question_words, answer_words,
				dialect, language, userans_val, correct_val, *args, **kwargs):
		# TODO: userans_val and accept_list, something here.
		self.init_variables("", userans_val, [])
		self.lemma = ""
		self.dialect = dialect

		qtype=question.qtype
		if qtype in self.qtype_verbs:
			qtype = 'PRS'

		question_widget = forms.HiddenInput(attrs={'value' : question.id})
		answer_widget = forms.HiddenInput(attrs={'value' : qanswer.id})
		atext = qanswer.string
		task = qanswer.task
		if not task:
			error_msg = u"not task: %s %s (%s)" % (atext, question.qid, question.qatype)

			raise Http404(error_msg)
		super(ContextMorfaQuestion, self).__init__(*args, **kwargs)

		answer_size = 20
		maxlength = 30

		self.generate_fields(20,30)

		self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)
		self.fields['answer_id'] = forms.CharField(widget=answer_widget, required=False)

		# Select words for the the answer
		selected_awords = self.select_words(question_words, answer_words)
		answer_task = selected_awords.get(task)
		tag_id = answer_task.get('tag')
		wrd_id = answer_task.get('word')
		form_lemma = answer_task.get('fullform')
		possibilities = Form.objects.filter(tag__pk=tag_id, word__pk=wrd_id)

		relaxed = []
		form_list = []
		
		if not selected_awords.has_key(task):
			raise Http404(task + " " + atext + " " + str(qanswer.id))			
		if len(selected_awords[task]['fullform'])>0:
			for f in selected_awords[task]['fullform']:
				self.correct_anslist.append(force_unicode(f))
			
			accepted = sum([relax(force_unicode(item)) for item in self.correct_anslist], [])
			self.relaxings = [item for item in accepted if item not in self.correct_anslist]
			# add NG forms to relaxings
			self.correct_anslist += sum(
				[relax(force_unicode(f.fullform))
					for f in possibilities
					if force_unicode(f.fullform) not in self.correct_anslist],
				[])

			self.correct_anslist.extend(self.relaxings)
			log_w = Word.objects.get(id=selected_awords[task]['word'])
			w_str = force_unicode(log_w.lemma).encode('utf-8')
			w_pos = log_w.pos
			t_str = force_unicode(Tag.objects.get(id=selected_awords[task]['tag']).string).encode('utf-8')
			log_name = "contextual_morfa_" + w_pos
			log_value = '%s+%s' % (w_str, t_str)
			log_value = ""
			self.is_correct(log_name, log_value)
			self.correct_ans = self.correct_anslist[0]

		self.correct_anslist = [force_unicode(item) for item in accepted]

		# # Include all dialect forms/NG forms.
		# self.accepted_anslist = sum(
		# 	[relax(force_unicode(f.fullform))
		# 		for f in possibilities
		# 		if f.fullform not in self.correct_anslist],
		# 	[])

		self.qattrs = {}
		self.aattrs = {}
		for syntax in question_words.keys():
			qword = question_words[syntax]
			if qword.has_key('word'):
				self.qattrs['question_word_' + syntax] = qword['word']
			if qword.has_key('tag') and qword['tag']:
				self.qattrs['question_tag_' + syntax] = qword['tag']
			if qword.has_key('fullform') and qword['fullform']:
				self.qattrs['question_fullform_' + syntax] = qword['fullform'][0]

		for syntax in selected_awords.keys():
			if selected_awords[syntax].has_key('word'):
				self.aattrs['answer_word_' + syntax] = selected_awords[syntax]['word']
			if selected_awords[syntax].has_key('tag'):
				self.aattrs['answer_tag_' + syntax] = selected_awords[syntax]['tag']
			if selected_awords[syntax].has_key('fullform') and len(selected_awords[syntax]['fullform']) == 1:
				self.aattrs['answer_fullform_' + syntax] = selected_awords[syntax]['fullform'][0]
		
		# Forms question string and answer string out of grammatical elements and other strings.
		qstring = ""
		astring= ""

		# Format question string
		qtext = question.string
		for w in qtext.split():
			if not question_words.has_key(w):
				qstring = qstring + " " + force_unicode(w)
			else:
				if question_words[w].has_key('fullform'):
					qstring = qstring + " " + force_unicode(question_words[w]['fullform'][0])
				else:
					qstring = qstring + " " + force_unicode(w)
		qstring = qstring.replace(" -","-")
		qstring = qstring.replace(" .",".")
		
		
		try:
			answer_word = selected_awords[task]['word']
		except KeyError:
			answer_word = False
			# print 'fail: ', question.qid
			# print ' task: ', task
			self.error = 'error'
			self.lemma = 'error in answer words: ' + question.qid
			return
			# self.lemma = question.qid
		answer_tag = selected_awords[task]['tag']
		selected_awords[task]['fullform'][0] = 'Q'
		
		# Get lemma for contextual morfa
		# lemma is displayed as the 'task' word in parentheses after the question
		answer_word_el = Word.objects.get(id=answer_word)
		answer_tag_el = Tag.objects.get(id=answer_tag)
		self.lemma = answer_word_el.lemma
		self.tooltip_question_id = question.qid

		# Set tooltip translations
		transl = answer_word_el.translations2(language)
		# if len(transl) == 0:
			# transl = answer_word_el.translations2('nob') # Norwegian as default
		if len(transl) > 0:
			xl = transl[0]
			self.translations = xl.definition
		
		if answer_word_el.pos == 'V':
			self.wordclass = answer_word_el.wordclass
	
		# If the asked word is in Pl, generate nominal form

		if answer_tag_el.pos == "N":
			if qtype == "COLL-NUM":
				self.lemma = answer_word_el.lemma
			else:
				if answer_tag_el.number=="Sg" or answer_tag_el.case=="Ess" or answer_tag_el.case=="Nom":  #was: qtype="N-NOM-PL"
					self.lemma = answer_word_el.lemma
				else:
					nplforms = Form.objects.filter(word__pk=answer_word, tag__case='Nom', tag__number='Pl')
					if nplforms.count() > 0:
						self.lemma = nplforms[0].fullform
					else:
						self.lemma = answer_word_el.lemma + " (plural) fix this"
		
		if qtype == "ORD-NUM":
			self.lemma = answer_word_el.lemma

		if answer_tag_el.pos == "Pron":
			# Hide task word for Recipr and Refl
			if qtype in ["P-REFL", "P-RECIPR", "P-REL"]:
				self.lemma = False

		# Retrieve feedback information
		try:
			answer_word_forms = Form.objects.filter(word__pk=answer_word,
													tag=answer_tag_el)
													
			answer_word_forms = filter_set_by_dialect(answer_word_forms, self.dialect)
												
			answer_word_form = answer_word_forms[0] 
		except:
			answer_word_form = False 
		
		if answer_word_form:
			self.get_feedback(answer_word_form, language)

		# Format answer string
		for w in atext.split():
			if w.count("(") > 0:
			  continue
			
			if not selected_awords.has_key(w) or not selected_awords[w].has_key('fullform'):
				astring = astring + " " + force_unicode(w)
			else:
				astring = astring + " " + force_unicode(selected_awords[w]['fullform'][0])
					
		# Remove leading whitespace and capitalize.
		astring = astring.lstrip()
		qstring = qstring.lstrip()
		astring = astring[0].capitalize() + astring[1:]
		qstring = qstring[0].capitalize() + qstring[1:]

		qstring = qstring + "?"
		# Add dot if the last word is not the open question.
		if astring.count("!")==0 and not astring[-1]=="Q":
			astring = astring + "."
		self.question=qstring

		# Format answer strings for context
		q_count = astring.count('Q')
		if q_count > 0:
			astrings = astring.split('Q')
			if astrings[0]:
				self.answertext1 = astrings[0]
			if astrings[1]:
				self.answertext2 = astrings[1]

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

		if answer_word == False:
			self.lemma = '%s - error: %s' % (answer_word_el.lemma, question.qid)



def vasta_is_correct(self,question,qwords,language,utterance_name=None):
	"""
	Analyzes the answer and returns a message.
	"""
	from django.conf import settings

	# LOOKUP_TOOL = '/usr/bin/lookup'
	# FST_DIRECTORY = '/opt/smi/sme/bin'
	# LOOKUP2CG = '/usr/local/bin/lookup2cg'
	# CG3 = '/usr/local/bin/vislcg3'
	# PREPROCESS = '/opt/sami/cg/bin/preprocess'

	try:
		_ = settings.FST_DIRECTORY
		_ = settings.LOOKUP_TOOL
		_ = settings.LOOKUP2CG
		_ = settings.CG3
		_ = settings.PREPROCESS
	except:
		err =  "Check that settings.py contains the following settings:"
		err += "  FST_DIRECTORY, LOOKUP_TOOL, LOOKUP2CG, CG3, PREPROCESS"


	if not self.is_valid():
		return None, None, None

	noanalysis=False

	fstdir = settings.FST_DIRECTORY
	fst = fstdir + "/ped-sme.fst"
	print fst
	lo = settings.LOOKUP_TOOL
	lookup = " | " + lo + " -flags mbTT -utf8 -d " + fst
	print lookup
	#lookup2cg = " | /Users/pyry/gtsvn/gt/script/lookup2cg" # on Ryan's machine
	#lookup2cg = " | /usr/local/bin/lookup2cg " # on victorio
	lookup2cg = " | " + settings.LOOKUP2CG
	cg3 = settings.CG3
	preprocess = " | " + settings.PREPROCESS
	#preprocess = " | /Users/mslm/main/gt/script/preprocess "
	dis_bin = settings.FST_DIRECTORY + "/sme-ped.cg3"

	vislcg3 = " | " + cg3 + " --grammar " + dis_bin + " -C UTF-8"
	
	self.userans = self.cleaned_data['answer']
	answer = self.userans.rstrip()
	answer = answer.lstrip()
	answer = answer.rstrip('.!?,')

	self.error = "error"
				
	qtext = question
	qtext = qtext.rstrip('.!?,')

	#logfile = open('/home/univ_oahpa/univ_oahpa/univ_drill/vastaF_and_Sahka_CGanalysis_log.txt','w')
	
	host = 'localhost'
	port = 9000  # was: 9000, TODO - add to settings.py
	size = 1024

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((host,port)) # on victorio
		sys.stdout.write('%')

		analysis = ""
		question_lookup = "echo \"" + force_unicode(qtext).encode('utf-8') + "\"" + preprocess
		words = os.popen(question_lookup).readlines()
		for qword in words: # or qwords ?
			cohort=""
			w = qword.lstrip().rstrip()
			s.send(w)  # on victorio
			cohort = s.recv(size)
		  
			if not cohort or cohort == w:
				cohort = w + "\n"
			if cohort=="error":
				raise Http404
			analysis = analysis + force_unicode(cohort).encode('utf-8')

		if self.gametype=="sahka":
			analysis = analysis + "\"<^qdl_id>\"\n\t\"^sahka\" QDL " + force_unicode(utterance_name).encode('utf-8') +"\n"
		else:
			analysis = analysis + "\"<^qst>\"\n\t\"^qst\" QDL\n"

	   #logfile.write(analysis+"\n")
		data_lookup = "echo \"" + force_unicode(answer).encode('utf-8') + "\"" + preprocess
		words = os.popen(data_lookup).readlines()
		analyzed=""
		for w in words:
			w=w.strip()
			s.send(w)  # on vic
			analyzed = analyzed + force_unicode(s.recv(size)).encode('utf-8')
		s.send("q")  # on vic
		s.close()

	except socket.error:	# port 9000 not available => morph. analysis will be done by ped-sme.fst
		# analyse words in the question
		analysis = ""
		question_lookup = "echo \"" + force_unicode(qtext).encode('utf-8') + "\"" + preprocess
		words = os.popen(question_lookup).readlines()
		for qword in words: # or qwords ?
			cohort=""
			w = qword.lstrip().rstrip()
			word_lookup = "echo \"" + force_unicode(w).encode('utf-8') + "\"" + lookup + lookup2cg  # on Heli's machine
			morfanal = os.popen(word_lookup).readlines()
			for row in morfanal:
				#row = row.strip()
				cohort = cohort + force_unicode(row).encode('utf-8')
			if not cohort or cohort == w:
				cohort = w + "\n"
			if cohort=="error":
				raise Http404
			analysis = analysis + cohort

		if self.gametype=="sahka":
			analysis = analysis + "\"<^qdl_id>\"\n\t\"^sahka\" QDL " + force_unicode(utterance_name).encode('utf-8') +"\n"
		else:
			analysis = analysis + "\"<^qst>\"\n\t\"^qst\" QDL\n"

		#logfile.write(analysis+"\n")
		
		# analyse words in the answer
		
		data_lookup = "echo \"" + force_unicode(answer).encode('utf-8') + "\"" + preprocess
		words = os.popen(data_lookup).readlines()
		analyzed=""
		for w in words:
			w=w.strip()	
			word_lookup = "echo \"" + force_unicode(w).encode('utf-8') + "\"" + lookup + lookup2cg  # on Heli's machine
			morfanal = os.popen(word_lookup).readlines()
			ans_cohort=""
			for row in morfanal:
				ans_cohort = ans_cohort + row
			analyzed = analyzed + ans_cohort
   # except socket.timeout:
	#	raise Http404("Technical error, please try again later.")			

	#logfile.write(analyzed+"\n")
	print "morph. analysis:\n",analyzed
	analysis = analysis + analyzed
	analysis = analysis + "\"<.>\"\n\t\".\" CLB"
	analysis = analysis.rstrip()
	analysis = analysis.replace("\"","\\\"")

	ped_cg3 = "echo \"" + analysis + "\"" + vislcg3
	checked = os.popen(ped_cg3).readlines()
	print "syntactic analysis:\n",checked

	wordformObj=re.compile(r'^\"<(?P<msgString>.*)>\".*$', re.U)
	messageObj=re.compile(r'^.*(?P<msgString>&(grm|err|sem)[\w-]*)\s*$', re.U)
	targetObj=re.compile(r'^.*\"(?P<targetString>[\wáÁæÆåÅáÁšŠŧŦŋŊøØđĐžZčČ-]*)\".*dia-.*$', re.U)
	# Extract the lemma	
	constantObj=re.compile(r'^.*\"\<(?P<targetString>[\wáÁæÆåÅáÁšŠŧŦŋŊøØđĐžZčČ-]*)\>\".*$', re.U)
	diaObj=re.compile(r'^.*(?P<targetString>&dia-[\w]*)\s*$', re.U)

	# Each wordform may have a set of tags.
	spelling = False
	msgstrings = {}
	diastring = "jee"
	lemma=""
	for line in checked:
		line = line.strip()
		#logfile.write(line+"\n")

		#Find the lemma first
		matchObj=constantObj.search(line)
		if matchObj:
			lemma = matchObj.expand(r'\g<targetString>')

		#The wordform
		matchObj=wordformObj.search(line)
		if matchObj:
			wordform = matchObj.expand(r'\g<msgString>')
			msgstrings[wordform] = {}
			
		#grammatical/semantic/other error
		matchObj=messageObj.search(line)
		if matchObj:
			msgstring = matchObj.expand(r'\g<msgString>')
			if msgstring.count("nonword") > 0:  # was: spelling
				spelling = True
			msgstrings[wordform][msgstring] = 1

		#Store the baseform if tehre is dia-whatever
		matchObj=targetObj.search(line)
		if matchObj:
			msgstring = matchObj.expand(r'\g<targetString>')
			msgstrings[wordform]['dia-target'] = msgstring
			msgstrings[wordform]['dia-lemma'] = lemma

		# What is the dia-tag?
		matchObj=diaObj.search(line)
		if matchObj:
			msgstring = matchObj.expand(r'\g<targetString>')
			msgstrings[wordform][msgstring] = 1
			diastring=msgstring			
			

	msg=[]
	message_ids=[]
	dia_msg = []
	target = ""
	variable=""
	constant=""
	found=False
	#Interface language	
	if not language: language = "nob"
	language = switch_language_code(language)
	#if language == "no" : language = "nob"
	#if language == "fi" : language = "fin"
	#if language == "en" : language = "eng"
	if not language in ["nob","sme","fin","eng","swe"]: language="nob"
	for w in msgstrings.keys():
		if found: break
		for m in msgstrings[w].keys():
			if spelling and m.count("nonword") == 0: continue
			m = m.replace("&","") 
			if Feedbackmsg.objects.filter(msgid=m).count() > 0:
				msg_el = Feedbackmsg.objects.filter(msgid=m)[0]
				message = Feedbacktext.objects.filter(feedbackmsg=msg_el,language=language)[0].message
				msg_id = msg_el.msgid  # added
				print msg_id
				message_ids.append(msg_id)  # added
				#w = force_unicode(w).encode('utf-8')
				message = message.replace("WORDFORM","\"" + force_unicode(w) + "\"") 
				msg.append(message)
				if not spelling:
					found=True
					break				
			else:
				if m.count("dia-") == 0:
					msg.append(m)
					if not spelling:
						found=True
						break
			if m.count("dia-") > 0:
				dia_msg.append(m)
		if msgstrings[w].has_key('dia-target'):
			constant = msgstrings[w]['dia-lemma']
			variable = msgstrings[w]['dia-target']
		if msgstrings[w].has_key('dia-unknown'):
			constant = msgstrings[w]['dia-lemma']
			variable = msgstrings[w]['dia-unknown']

	#iscorrect is used only in logging
	iscorrect=False
	if not msg:
		self.error = "correct"
		iscorrect=True

	feedbackmsg=' '.join(msg)
	p = re.compile(r'<.*?>')
	feedbackmsg = p.sub('', feedbackmsg)
	if message_ids:
		feedbackmsg_id = message_ids[0]
	else:
		feedbackmsg_id = ""
	today=datetime.date.today()
	log_kwargs = {
		'userinput': self.userans,
		'feedback': feedbackmsg,
		'iscorrect': iscorrect,
		'qid': utterance_name,
		'example': question,
		'game': self.gametype,
		'date': today,
		'lang': language,
		'messageid': feedbackmsg_id
	}
	if self.user:
		log_kwargs['username'] = self.user.username
	if self.user_country:
		log_kwargs['user_country'] = self.user_country
	log = Log.objects.get_or_create(**log_kwargs)
	self.last_log = log
	#log.save()		   
	
	variables = []
	variables.append(variable)
	variables.append(constant)
	#logfile.write("variable in message:"+variables[0])
        #logfile.write("msg:"+msg[0])
	#logfile.write("dia_msg:"+dia_msg[0])
	return msg, dia_msg, variables


class VastaSettings(OahpaSettings):

	book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
	level = forms.ChoiceField(initial='1', choices=VASTA_LEVELS, widget=forms.Select)

	def __init__(self, *args, **kwargs):
		self.set_settings()
		self.set_default_data()
		self.default_data['gametype'] = 'qa'
		super(VastaSettings, self).__init__(*args, **kwargs)

class VastaQuestion(OahpaQuestion):
	"""
	Questions for vasta
	"""

	select_words = select_words
	vasta_is_correct = vasta_is_correct
		
	def __init__(self, question, qwords, language, userans_val, correct_val, *args, **kwargs):				 

		self.init_variables("", userans_val, [])
		
		question_widget = forms.HiddenInput(attrs={'value' : question.id})

		super(VastaQuestion, self).__init__(*args, **kwargs)

		maxlength=60
		answer_size=60
		self.fields['answer'] = forms.CharField(max_length = maxlength, \
												widget=forms.TextInput(\
			attrs={'size': answer_size, 'onkeydown':'javascript:return process(this, event, document.gameform);',}))

		self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)

		self.qattrs= {}
		for syntax in qwords.keys():
			qword = qwords[syntax]
			if qword.has_key('word'):
				self.qattrs['question_word_' + syntax] = qword['word']
			if qword.has_key('tag') and qword['tag']:
				self.qattrs['question_tag_' + syntax] = qword['tag']
			if qword.has_key('fullform') and qword['fullform']:
				self.qattrs['question_fullform_' + syntax] = qword['fullform'][0]

		# Forms question string and answer string out of grammatical elements and other strings.
		qstring = ""

		# Format question string
		qtext = question.string
		for w in qtext.split():
			if not qwords.has_key(w): qstring = qstring + " " + force_unicode(w)
			else:
				if qwords[w].has_key('fullform'):
					qstring = qstring + " " + force_unicode(qwords[w]['fullform'][0])
				else:
					qstring = qstring + " " + w
		# this is for -guovttos
		qstring=qstring.replace(" -","-");
		qstring=qstring.replace("- ","-");
					
		# Remove leading whitespace and capitalize.
		qstring = qstring.lstrip()
		qstring = qstring[0].capitalize() + qstring[1:]

		qstring = qstring + "?"
		self.question=qstring
		question_id = question.qid

		# In qagame, all words are considered as answers.
		self.gametype="vasta"
		self.messages, jee, joo  = self.vasta_is_correct(qstring.encode('utf-8'), qwords, language, question_id)
		
		# set correct and error values
		if correct_val == "correct":
			self.error="correct"


def sahka_is_correct(self,utterance,targets,language):
	"""
	Analyzes the answer and returns a message.
	"""
	if not self.is_valid():
		return False

	if not self.cleaned_data.has_key('answer'):
		return
	qwords = {}
	# Split the question to words for analaysis.

	self.messages, self.dia_messages, self.variables = self.vasta_is_correct(utterance.utterance, None, language, utterance.name)
	#self.variables = [ "Kárášjohka" ]
	#self.dia_messages = [ "dia-unknown" ]

	if not self.messages:
		self.error = "correct"

	for answer in self.dia_messages:
		answer = answer.lstrip("dia-")
		if answer == "target":
			self.target = answer

	
class SahkaSettings(OahpaSettings):

	#dialogue = forms.ChoiceField(initial='firstmeeting', choices=DIALOGUE_CHOICES, widget=forms.Select)
	
	def __init__(self, *args, **kwargs):
		self.set_settings()
		self.set_default_data()
		self.default_data['gametype'] = 'sahka'
		self.default_data['dialogue_id'] = '1'
		self.default_data['dialogue'] = 'firstmeeting'
		self.default_data['topicnumber'] = '0'
		self.default_data['image'] = 'sahka.png'
		self.default_data['wordlist'] = ''
		self.default_data['num_fields'] = '2'
		self.default_data['attempts'] = 0
		super(SahkaSettings, self).__init__(*args, **kwargs)

		# Link to grammatical explanation for each page
		self.grammarlinkssme = Grammarlinks.objects.filter(language="sme")
		self.grammarlinksno = Grammarlinks.objects.filter(language="no")

	def init_hidden(self, topicnumber, num_fields, dialogue, image, wordlist, attempts):
		
		# Store topicnumber as hidden input to keep track of topics.
		#print "topicnumber", topicnumber
		#print "num_fields", num_fields
		topicnumber = topicnumber
		num_fields = num_fields
		dialogue = dialogue
		image = image
		wordlist = wordlist
		attempts = attempts


class SahkaQuestion(OahpaQuestion):
	"""
	Sahka: Dialogue game
	"""

	select_words = select_words
	sahka_is_correct = sahka_is_correct
	vasta_is_correct = vasta_is_correct

	def __init__(self, utterance, qwords, targets, global_targets, language, userans_val, correct_val, *args, **kwargs):				 
		
		self.init_variables("", userans_val, [])

		utterance_widget = forms.HiddenInput(attrs={'value' : utterance.id})
		facit_widget = forms.HiddenInput(attrs={'value' : utterance.facit})		
		
		super(SahkaQuestion, self).__init__(*args, **kwargs)

		if utterance.utttype == "question":
			maxlength=50
			answer_size=50
			self.fields['answer'] = forms.CharField(max_length = maxlength, \
													widget=forms.TextInput(\
			attrs={'size': answer_size, 'onkeydown':'javascript:return process(this, event, document.gameform);',}))

		self.fields['utterance_id'] = forms.CharField(widget=utterance_widget, required=False)
		self.fields['facit'] = forms.CharField(widget=facit_widget, required=False)

		self.global_targets = global_targets
		#print self.global_targets
		self.utterance =""
		self.qattrs={}

		if utterance:
			self.utterance_id=utterance.id
			#self.utterance=utterance.utterance
						
			# Forms question string and answer string out of grammatical elements and other strings.
			qstring = ""
			
			# Format question string
			qtext = utterance.utterance
			for w in qtext.split():
				if not qwords.has_key(w):
					qstring = qstring + " " + force_unicode(w)
					self.qattrs['question_fullform_' + w] = force_unicode(w)
				else:
					if qwords[w].has_key('fullform'):
						qstring = qstring + " " + force_unicode(qwords[w]['fullform'][0])
						self.qattrs['question_fullform_' + w] = qwords[w]['fullform'][0]
					else:
						qstring = qstring + " " + w
						self.qattrs['question_fullform_' + w] = w

			# this is for -guovttos
			qstring=qstring.replace(" -","-");
			qstring=qstring.replace("- ","-");
					
			# Remove leading whitespace and capitalize.
			qstring=qstring.replace(" .",".");
			qstring=qstring.replace(" ?","?");
			qstring=qstring.replace(" !","!");

			qstring = qstring.lstrip()
			if len(qstring)>0:
				qstring = qstring[0].capitalize() + qstring[1:]

			self.utterance=qstring

		self.target=""
		self.constant=""
		self.dia_messages = ""		
		self.gametype="sahka"
		self.variables = []
		self.variables.append("")
		self.variables.append("")
		self.sahka_is_correct(utterance,targets,language)
		if self.target:
			variable=""
			constant=""
			if utterance.links.filter(target=self.target).count()>0:
				variable = utterance.links.filter(target=self.target)[0].variable
				if variable:
					self.qattrs['target_' + variable] = self.variables[0]
					self.global_targets[variable] = { 'target' : self.variables[0] }
				constant = utterance.links.filter(target=self.target)[0].constant
				if constant:
					self.qattrs['target_' + constant] = self.variables[1]
					self.global_targets[constant] = { 'target' : self.variables[1] }
		for t in self.global_targets.keys():
			if not self.qattrs.has_key(t):
				self.qattrs['target_' + t] = self.global_targets[t]['target']

		#self.error="correct"
		self.errormsg = ""
		self.correct_answers = utterance.facit
		self.utterance_type=utterance.utttype # Heli: This was needed to make utterance type accessible in templates.

		if correct_val == "correct":
			self.error="correct"
			

###########
## Vasta-S (Cealkka)
###########
def cealkka_is_correct(self,question,qwords,awords,language,question_id=None):  #was: question_id=None
	"""
	Analyzes the answer and returns a message.
	"""
	if not self.is_valid():
		return None, None, None

	noanalysis=False
	
	fstdir = settings.FST_DIRECTORY
	fst = fstdir + "/ped-sme.fst"
	print fst
	lo = settings.LOOKUP_TOOL
	lookup = " | " + lo + " -flags mbTT -utf8 -d " + fst
	print lookup
	#lookup2cg = " | /Users/pyry/gtsvn/gt/script/lookup2cg" # on Ryan's machine   
	#lookup2cg = " | /usr/local/bin/lookup2cg " # on victorio
	lookup2cg = " | " + settings.LOOKUP2CG
	cg3 = settings.CG3
	preprocess = " | " + settings.PREPROCESS
	dis_bin = settings.FST_DIRECTORY + "/sme-ped.cg3"

	vislcg3 = " | " + cg3 + " --grammar " + dis_bin + " -C UTF-8"
	
	self.userans = self.cleaned_data['answer']
	answer = self.userans.rstrip()
	answer = answer.lstrip()
	answer = answer.rstrip('.!?,')
	#print answer

	self.error = "error"
				
	qtext = question
	qtext = qtext.rstrip('.!?,')

	#logfile = open('/home/univ_oahpa/univ_oahpa/univ_drill/CGanalysis_log.txt', 'w')
	host = 'localhost'
	port = 9000  # was: 9000, TODO - add to settings.py
	size = 1024

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((host,port)) # on vic
		sys.stdout.write('%')

		analysis = ""
		question_lookup = "echo \"" + qtext + "\"" + preprocess
		words = os.popen(question_lookup).readlines()
		#print question_id
		#print words
		#print qwords
		for word in words:
			w=""
			cohort=""
			#print word
			# All the words will go through morph.analyser, even if they have a tag-attribute already. We do it to avoid problems with compound words.
			w = force_unicode(word).encode('utf-8')
			w=w.lstrip().rstrip()
			s.send(w) # sends a word to lookupserv
			cohort = s.recv(size)
			if not cohort or cohort == w:
				cohort = w + "\n"
			if cohort=="error":
				raise Http404
			#logfile.write(cohort+"\n")
			analysis = analysis + force_unicode(cohort).encode('utf-8')
		#logfile.write(analysis+"\n")
			#print analysis
		### Lemmas and POS tags of task words are gathered into the variables 
		### tasklemmas and taskpos respectively. Tasklemmas and taskpos will be 
		### sent to CG together with the morph. analysed question and answer.
		tasklemmas = ""
		logtasklemmas = ""
		malemma_without_hash = ""
		taskpos = ""
		morfanal = ""
		for aword in awords:
			#print aword
			#logfile.write(aword)
			if aword.has_key('taskword') and aword['taskword']:
				tlemma = aword['fullform']
				tlemma = force_unicode(tlemma).encode('utf-8')
				tlemma = tlemma.strip()
				#print tlemma
				#logfile.write(tlemma+" ")
				tasktag = Tag.objects.filter(id=aword['tag'])
				tasktagstring = tasktag[0].string
				taskpos = tasktag[0].pos
				ttag = tasktagstring.replace("+"," ")
				ttag = force_unicode(ttag).encode('utf-8')
				#print ttag
				#logfile.write(ttag+"\n")
				s.send(tlemma)  # on vic
				word_lookup = force_unicode(s.recv(size)).encode('utf-8')  # on vic
				#logfile.write(word_lookup)
				ans_cohort=""
				#print rows
				rows = word_lookup.split("\n")  # on vic
				morfanal = ""
				for row in rows:
					row = force_unicode(row).encode('utf-8')
					ans_cohort = ans_cohort + row
					#logfile.write(row + "\n")
					malemmas = row.split("\"")
					if row:
						 malemma = force_unicode(malemmas[1]).encode('utf-8')
					malemma_without_hash = malemma.replace('#','')
					taglist = ttag.split()
					tag_match = 1
					for entag in taglist:
						if entag not in row:
							tag_match = 0
					if tag_match and tlemma == malemma_without_hash:  # 'Sg Nom' or 'V Inf' is not enough - exact tag sequence needed, and also need to compare the primary form to the analysed word, to resolve ambiguities
						#print malemmas
						 #logfile.write(malemma+"\n")
						#print malemma
						#print malemma_without_hash
						tasklemmas = force_unicode(tasklemmas).encode('utf-8') + "\n\t\"" + force_unicode(malemma).encode('utf-8') + "\" "+ force_unicode(taskpos).encode('utf-8')
				logtasklemmas = logtasklemmas + " " + force_unicode(malemma_without_hash).encode('utf-8') + " " + force_unicode(taskpos).encode('utf-8')
				morfanal = morfanal + force_unicode(ans_cohort).encode('utf-8')  # END
					
		analysis = force_unicode(analysis).encode('utf-8') + "\"<^vastas>\"\n\t\"^vastas\" QDL " + force_unicode(question_id).encode('utf-8') + " " + force_unicode(tasklemmas).encode('utf-8') + "\n"
		#####
		#print analysis
		#logfile.write(analysis)
		data_lookup = "echo \"" + force_unicode(answer).encode('utf-8') + "\"" + preprocess
		word = os.popen(data_lookup).readlines()
		#print word
		analyzed=""
		for c in word:		
			c=c.strip()
			print c
			s.send(c) # on vic
			analyzed = analyzed + s.recv(size)
			
		s.send("q")  # on vic
		s.close()  # on vic

	except socket.timeout:
		raise Http404("Technical error, please try again later.")
	"""
	except socket.error:
		analysis = ""
		data_lookup = "echo \"" + qtext + "\"" + preprocess
		words = os.popen(data_lookup).readlines()
		print question_id
		#print words
		#print qwords
		for word in words:
			w=""
			cohort=""
			#print word
			# All the words will go through morph.analyser, even if they have a tag-attribute already. We do it to avoid problems with compound words.
			w = force_unicode(word).encode('utf-8')
			w=w.lstrip().rstrip()
			word_lookup = "echo \"" + force_unicode(w).encode('utf-8') + "\"" + lookup + lookup2cg  # on Heli's machine
			morfanal = os.popen(word_lookup).readlines()
			for row in morfanal:
				cohort = cohort + row
				#print cohort
			analysis = analysis + cohort
		tasklemmas = ""
		logtasklemmas = ""
		for aword in awords:
			#print aword
			#logfile.write(aword)
			if aword.has_key('taskword') and aword['taskword']:
				tlemma = aword['fullform']
				tlemma = force_unicode(tlemma).encode('utf-8')
				tlemma = tlemma.strip()
				#print tlemma
				#logfile.write(tlemma+" ")
				tasktag = Tag.objects.filter(id=aword['tag'])
				tasktagstring = tasktag[0].string
				taskpos = tasktag[0].pos
				ttag = tasktagstring.replace("+"," ")
				#print ttag
				#logfile.write(ttag+"\n")
				ans_cohort = ""
				word_lookup = "echo \"" + force_unicode(tlemma).encode('utf-8') + "\"" + lookup + lookup2cg  # on Heli's machine
				rows = os.popen(word_lookup).readlines()
				morfanal = ""
				for row in rows:
					ans_cohort = ans_cohort + row
					#logfile.write(row + "\n")
					malemmas = row.split("\"")
					if row:
						 malemma = malemmas[1]
					malemma_without_hash = malemma.replace('#','')
					taglist = ttag.split()
					tag_match = 1
					for entag in taglist:
						if entag not in row:
							tag_match = 0
					if tag_match and tlemma == malemma_without_hash:  # 'Sg Nom' or 'V Inf' is not enough - exact tag sequence needed, and also need to compare the primary form to the analysed word, to resolve ambiguities
						#print malemmas
						 #logfile.write(malemma+"\n")
						#print malemma
						#print malemma_without_hash
						tasklemmas = tasklemmas + "\n\t\"" + force_unicode(malemma).encode('utf-8') + "\" "+taskpos
						logtasklemmas = logtasklemmas + " " + malemma_without_hash + " " + taskpos
					morfanal = morfanal + ans_cohort  # END
					
		analysis = analysis + "\"<^vastas>\"\n\t\"^vastas\" QDL " + question_id + " " + force_unicode(tasklemmas).encode('utf-8') + "\n"
		# analyse the user's answer
		data_lookup = "echo \"" + force_unicode(answer).encode('utf-8') + "\"" + preprocess
		word = os.popen(data_lookup).readlines()
		#print word
		analyzed=""
		for c in word:		
			c=c.strip()	
			word_lookup = "echo \"" + force_unicode(c).encode('utf-8') + "\"" + lookup + lookup2cg  # on Heli's machine
			morfanal = os.popen(word_lookup).readlines()
			ans_cohort=""
			for row in morfanal:
				ans_cohort = ans_cohort + row
			analyzed = analyzed + ans_cohort
	#except Exception, e:
		#print Exception
		#print e
	"""
	

	
	analysis = analysis + analyzed
	analysis = analysis + "\"<.>\"\n\t\".\" CLB"
	analysis = analysis.rstrip()
	analysis = analysis.replace("\"","\\\"")
	#print "Morph. analysis: \n", analysis
	#logfile.write(analysis)
	ped_cg3 = "echo \"" + analysis + "\"" + vislcg3
	checked = os.popen(ped_cg3).readlines()
	#print "Syntax analysis: \n", checked

	wordformObj=re.compile(r'^\"<(?P<msgString>.*)>\".*$', re.U)
	messageObj=re.compile(r'^.*(?P<msgString>&(grm|err|sem)[\w-]*)\s*$', re.U)
	targetObj=re.compile(r'^.*\"(?P<targetString>[\wáÁæÆåÅáÁšŠŧŦŋŊøØđĐžZčČ-]*)\".*dia-.*$', re.U)
	# Extract the lemma	
	constantObj=re.compile(r'^.*\"\<(?P<targetString>[\wáÁæÆåÅáÁšŠŧŦŋŊøØđĐžZčČ-]*)\>\".*$', re.U)
	diaObj=re.compile(r'^.*(?P<targetString>&dia-[\w]*)\s*$', re.U)

	# Each wordform may have a set of tags.
	spelling = False
	msgstrings = {}
	diastring = "jee"
	lemma=""
	for line in checked:
		line = line.strip()

		#Find the lemma first
		matchObj=constantObj.search(line)
		if matchObj:
			lemma = matchObj.expand(r'\g<targetString>')

		#The wordform
		matchObj=wordformObj.search(line)
		if matchObj:
			wordform = matchObj.expand(r'\g<msgString>')
			msgstrings[wordform] = {}
			
		#grammatical/semantic/other error
		matchObj=messageObj.search(line)
		if matchObj:
			msgstring = matchObj.expand(r'\g<msgString>')
			if msgstring.count("nonword") > 0:   # was: spellingerror
				spelling = True
			msgstrings[wordform][msgstring] = 1

		#Store the baseform if there is dia-whatever
		matchObj=targetObj.search(line)
		if matchObj:
			msgstring = matchObj.expand(r'\g<targetString>')
			msgstrings[wordform]['dia-target'] = msgstring
			msgstrings[wordform]['dia-lemma'] = lemma

		# What is the dia-tag?
		matchObj=diaObj.search(line)
		if matchObj:
			msgstring = matchObj.expand(r'\g<targetString>')
			msgstrings[wordform][msgstring] = 1
			diastring=msgstring			
			

	msg=[]
	dia_msg = []
	message_ids = []
	target = ""
	variable=""
	constant=""
	found=False
	#Interface language	
	if not language: language = "nob"
	language = switch_language_code(language)
	#if language == "no" : language = "nob"
	#if language == "fi" : language = "fin"
	#if language == "en" : language = "eng"
	if not language in ["nob","sme","fin","eng","swe"]: language="nob"

	#print msgstrings
	for w in msgstrings.keys():
		if found: break
		for m in msgstrings[w].keys():
			if spelling and m.count("nonword") == 0: continue  # was: spelling
			m = m.replace("&","") 
			if Feedbackmsg.objects.filter(msgid=m).count() > 0:
				msg_el = Feedbackmsg.objects.filter(msgid=m)[0]
				#print msg_el
				message = Feedbacktext.objects.filter(feedbackmsg=msg_el, language=language)[0].message
				#print message
				msg_id = msg_el.msgid  # added
				#print msg_id
				message = message.replace("WORDFORM","\"" + force_unicode(w) + "\"") 
				msg.append(message)
				message_ids.append(msg_id)  # added
				if not spelling:
					found=True
					break				
			else:
				if m.count("dia-") == 0:
					msg.append(m)
					if not spelling:
						found=True
						break
			if m.count("dia-") > 0:
				dia_msg.append(m)
		if msgstrings[w].has_key('dia-target'):
			constant = msgstrings[w]['dia-lemma']
			variable = msgstrings[w]['dia-target']
		if msgstrings[w].has_key('dia-unknown'):
			constant = msgstrings[w]['dia-lemma']
			variable = msgstrings[w]['dia-unknown']

	#iscorrect is used only in logging
	iscorrect=False
	if not msg:
		self.error = "correct"
		iscorrect=True

	feedbackmsg=' '.join(msg)
	p = re.compile(r'<.*?>')
	feedbackmsg = p.sub('', feedbackmsg)
	#print feedbackmsg
	if message_ids:
		feedbackmsg_id = message_ids[0] # added
	else:
		feedbackmsg_id = ""
	#print feedbackmsg_id
	today=datetime.date.today()
	log_kwargs = {
		'userinput': self.userans,
		'feedback': feedbackmsg,
		'iscorrect': iscorrect,
		'qid': question_id,
		'example': question,
		'game': self.gametype,
		'date': today,
		'lang': language,
		'messageid': feedbackmsg_id,
		'tasklemmas': logtasklemmas
	}
	if self.user:
		log_kwargs['username'] = self.user.username
	if self.user_country:
		log_kwargs['user_country'] = self.user_country
	log = Log.objects.get_or_create(**log_kwargs)
	self.last_log = log
	# was Log.objects.create()
	#log.save() # not needed?		  
		
	variables = []
	variables.append(variable)
	variables.append(constant)
	return msg, dia_msg, variables


class CealkkaSettings(OahpaSettings):

	book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
	level = forms.ChoiceField(initial='13', choices=VASTAS_LEVELS, widget=forms.Select)
	lemmacount = forms.ChoiceField(initial='2', choices=VASTAS_NR_OF_TASKWORDS, widget=forms.Select)

	def __init__(self, *args, **kwargs):
		self.set_settings()
		self.set_default_data()
		self.default_data['gametype'] = 'cealkka',
		super(CealkkaSettings, self).__init__(*args, **kwargs)

class CealkkaQuestion(OahpaQuestion):
	"""
	Questions for cealkka
	"""

	select_words = select_words
	cealkka_is_correct = cealkka_is_correct
		
	def __init__(self, question, qanswer, qwords, awords, dialect, language, userans_val, correct_val, *args, **kwargs):				 

		self.init_variables("", userans_val, [])
		self.dialect = dialect
		self.gametype = "cealkka"
		qtype=question.qtype
		atext = qanswer.string
		# print atext

		question_widget = forms.HiddenInput(attrs={'value' : question.id})
		answer_widget = forms.HiddenInput(attrs={'value' : qanswer.id})  #was: qanswer.id

		super(CealkkaQuestion, self).__init__(*args, **kwargs)

		maxlength=70
		answer_size=70
		self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)
		
		self.fields['answer_id'] = forms.CharField(widget=answer_widget, required=False)

		self.fields['answer'] = forms.CharField(max_length = maxlength, \
												widget=forms.TextInput(\
		attrs={'size': answer_size, 'onkeydown':'javascript:return process(this, event, document.gameform);',}))

		# Select words for the answer
		astring = ""
		print "awords that come in CealkkaQuestion as parameter: "
		print awords
		selected_awords = self.select_words(qwords, awords)
					
		awords = []
		for token in atext.split():	   # det här har jag (Heli) hittat på
			if token.isupper():  # added because of keyerror
				word = selected_awords[token]
				if word.has_key('fullform') and word['fullform']:					
					word['fullform'] = force_unicode(word['fullform'][0])
			else:
				word = {}
				word['fullform'] = token
				word['taskword'] = ""
			awords.append(word)
			astring=astring+" "+force_unicode(word['fullform'])

		astring = astring.lstrip()
		#print astring
		
		self.awords=awords
		
		relaxed = []
		form_list=[]
				
		self.qattrs= {}
		self.aattrs = {}
		for syntax in qwords.keys():
			qword = qwords[syntax]
			if qword.has_key('word'):
				self.qattrs['question_word_' + syntax] = qword['word']
			if qword.has_key('tag') and qword['tag']:
				self.qattrs['question_tag_' + syntax] = qword['tag']
			if qword.has_key('fullform') and qword['fullform']:
				self.qattrs['question_fullform_' + syntax] = qword['fullform'][0]			
		for syntax in selected_awords.keys():
			if selected_awords[syntax].has_key('word'):
				self.aattrs['answer_word_' + syntax] = selected_awords[syntax]['word']
			if selected_awords[syntax].has_key('tag'):
				self.aattrs['answer_tag_' + syntax] = selected_awords[syntax]['tag']
			if selected_awords[syntax].has_key('fullform') and len(selected_awords[syntax]['fullform']) == 1:
				self.aattrs['answer_fullform_' + syntax] = selected_awords[syntax]['fullform'][0]
			if selected_awords[syntax].has_key('taskword'):
				self.aattrs['answer_taskword_' + syntax] = selected_awords[syntax]['taskword']  # to track the taskword attribute
		print question.qid
		print self.awords		
		# Forms question string and answer string out of grammatical elements and other strings.
		qstring = ""

		# Format question string
		qtext = question.string
		for w in qtext.split():
			if not qwords.has_key(w): qstring = qstring + " " + force_unicode(w)
			else:
				if qwords[w].has_key('fullform'):
					qstring = qstring + " " + force_unicode(qwords[w]['fullform'][0])
				else:
					qstring = qstring + " " + force_unicode(w)
		# this is for -guovttos
		qstring=qstring.replace(" -","-");
		qstring=qstring.replace("- ","-");
					
		# Remove leading whitespace and capitalize.
		qstring = qstring.lstrip()
		qstring = qstring[0].capitalize() + qstring[1:]

		qstring = qstring + "?"
		self.question=qstring
	
		self.gametype="cealkka"
		self.messages, jee, joo  = self.cealkka_is_correct(qstring.encode('utf-8'), qwords, awords, language, question.qid)   # was astring, awords for VastaS before
		
		# set correct and error values
		if correct_val == "correct":
			self.error="correct"
			
