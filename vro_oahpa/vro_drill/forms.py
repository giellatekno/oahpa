# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
import vro_oahpa.settings as settings

from vro_oahpa.conf.tools import switch_language_code

from models import *
#from game import *
#from vro_oahpa.vro_drill.game import relax
import datetime
import socket
import sys, os
import itertools
from random import choice

# TODO: These should be accessible in the admin interface, not hardcoded.

PRONOUNS_LIST = {'Sg1':u'ma', 'Sg2':u'sa', 'Sg3':u'tä',
		  'Pl1':u'mi', 'Pl2':u'ti', 'Pl3':u'nä'}

# DEMONSTRATIVE_PRESENTATION plus Sg3/Pl3
PASSIVE_PRONOUNS_LIST = {'Sg1':u'ma', 'Sg2':u'sa', 'Sg3':u'tä',
                         'Pl1':u'mi', 'Pl2':u'ti', 'Pl3':u'nä'} # possibly wrong


NEGATIVE_VERB_PRES = {'Sg1':'in', 'Sg2':'it', 'Sg3':'ii',
		  'Pl1':'eat', 'Pl2':'ehpet', 'Pl3':'eai'}

TENSE_PRESENTATION = {
	'Prt': u'eiläq',  # possibly wrong
	'Prs': u'täämbä',
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
)

NUMBER_CHOICES = (
	('Sg', _('singular')),
	('Pl', _('plural')),
)


CASE_CHOICES = (
    #('N-NOM-PL', _('Nominative Plural')),
    ('N-GEN', _('Genitive')),
    ('N-PAR', _('Partitive')),
    ('N-ILL', _('Illative')),
    ('N-INE', _('Inessive')),
    ('N-ELA', _('Elative')),
    ('N-ALL', _('Allative')),
    ('N-ADE', _('Adessive')),
    ('N-ABL', _('Ablative')),
    ('N-TRA', _('Translative')),
    ('N-TER', _('Terminative')),
    ('N-ABESS', _('Abessive')),
    ('N-COM', _('Comitative')),
)

# For now this is just a part of a test, used in game.Game.get_db_info_new
# I wanted a very general way to specify question/answers.

NOUN_QUESTION_ANSWER = {
	# gametype			question		answer
	'N-GEN': [('N+NumberN+Nom', 'N+NumberN+Gen')],
	'N-PAR': [('N+NumberN+Nom', 'N+NumberN+Par')],
	'N-ILL': [('N+NumberN+Nom', 'N+NumberN+Ill')],
	'N-INE': [('N+NumberN+Nom', 'N+NumberN+Ine')],
	'N-ELA': [('N+NumberN+Nom', 'N+NumberN+Ela')],
	'N-ADE': [('N+NumberN+Nom', 'N+NumberN+Ade')],
	'N-ABL': [('N+NumberN+Nom', 'N+NumberN+Abl')],
	'N-ALL': [('N+NumberN+Nom', 'N+NumberN+All')],
}

NOUN_FILTER_DEFINITION = ['animacy', 'declension', 'gender', 'source']

# Pers - akk, gen, ill, lok, kom
# Dem - akk, gen, ill, lok, kom
CASE_CHOICES_PRONOUN = (
	('NOMPL', _('plural')),
	('N-GEN', _('Genitive')),
    ('N-PAR', _('Partitive')),
    ('N-ILL', _('Illative')),
    ('N-INE', _('Inessive')),
    ('N-ELA', _('Elative')),
    #('N-ADE', _('Adessive')),
    #('N-ABL', _('Ablative')),
    #('N-ALL', _('Allative')),
)

# 	('N-ACC', _('accusative')),
# 	('N-ILL', _('illative')),
# 	('N-LOC', _('locative')),
# 	('N-COM', _('comitative')),
# 	('N-GEN', _('genitive')),
# 	# ('N-ESS', _('essive')),
# )

PRONOUN_QUESTION_ANSWER = {
	# gametype			question		answer
	'N-PAR': [('Pron+Subclass+NumberN+Nom', 'Pron+Subclass+NumberN+Par')],
	'N-ILL': [('Pron+Subclass+NumberN+Nom', 'Pron+Subclass+NumberN+Ill')],
#	'N-LOC': [('Pron+Subclass+NumberN+Nom', 'Pron+Subclass+NumberN+Loc')],
#	'N-COM': [('Pron+Subclass+NumberN+Nom', 'Pron+Subclass+NumberN+Com')],
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
   # ('N-GEN', _('Genitive')),
    ('N-PAR', _('Partitive')),
    #('N-ILL', _('Illative')),
    #('N-INE', _('Inessive')),
    #('N-ELA', _('Elative')),
    #('N-ADE', _('Adessive')),
    #('N-ABL', _('Ablative')),
    #('N-ALL', _('Allative')),
#	('N-MIX', _('mix')),
)

NOUN_TYPE_CHOICES =(
	('N-FEM-other', _(u'feminine in -a/-я')),
	('N-FEM-8', _(u'feminine in -ь')),
	('N-MASC-INANIM', _('masculine inanimate')),
	('N-MASC-ANIM', _('masculine animate')),
	('N-NEUT', _('neuter')),
	('all', _('All')),
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
	('A-GEN', _('Genitive')),
    ('A-PAR', _('Partitive')),
    ('A-ILL', _('Illative')),
    ('A-INE', _('Inessive')),
    ('A-ELA', _('Elative')),
    ('A-ADE', _('Adessive')),
    ('A-ABL', _('Ablative')),
    ('A-ALL', _('Allative')),)

ADJECTIVE_QUESTION_ANSWER = {
	# gametype			question		answer
	'NOMPL': [('A+Sg+Nom', 'A+Pl+Nom')],
	'ATTR': [('A+Sg+Nom', 'A+Attr')],
	'N-ACC': [('A+NumberA+Nom', 'A+NumberN+Acc')],
#	'N-ILL': [('A+NumberA+Nom', 'A+NumberN+Ill')],
	'N-LOC': [('A+NumberA+Nom', 'A+NumberN+Loc')],
#	'N-COM': [('A+NumberA+Nom', 'A+NumberN+Com')],
	'N-GEN': [('A+NumberA+Nom', 'A+NumberN+Gen')],
#	'N-ESS': [('A+NumberA+Nom', 'A+Ess')],
}

ADJECTIVE_FILTER_DEFINITION = ['grade', 'stem', 'source']

ADJEX_CHOICES = (
	('A-ATTR', _('attributive')), 	# A+Nom+Sg -> A+Attr
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
#	('NUM-ILL', _('illative')),
	('NUM-LOC', _('locative')),
#	('NUM-COM', _('comitative')),
	('COLL-NUM', _('collective')),
	('ORD-NUM', _('ordinals')),
)

NUM_BARE_CHOICES = (
	('NOMPL', _('plural')),
	('N-ACC', _('accusative')),
#	('N-ILL', _('illative')),
	('N-LOC', _('locative')),
#	('N-COM', _('comitative')),
)

NUMERAL_QUESTION_ANSWER = {
	# gametype			question		answer
#	'N-ESS': [('Num+NumberN+Nom', 'Num+Ess')],
	'N-LOC': [('Num+NumberN+Nom', 'Num+NumberN+Loc')],
#	'N-ILL': [('Num+NumberN+Nom', 'Num+NumberN+Ill')],
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
#	('PRF', _('perfect')),
#	('GER', _('gerund')),
#	('COND', _('conditional')),
#	('IMPRT', _('imperative')),
#	('POT', _('potential')),
)

VERB_QUESTION_ANSWER = {
	'V-PRS': [('V+Inf', 'V+Ind+Prs+Person-Number')],
	'V-PRT': [('V+Inf', 'V+Ind+Prt+Person-Number')],
#	'PRS': [('V+Inf', 'V+Ind+Prs+Person-Number')],
#	'PRT': [('V+Inf', 'V+Ind+Prt+Person-Number')],
#	'PRF': [('V+Inf', 'V+PrfPrc')],
#	'GER': [('V+Inf', 'V+Ger')],
#	'COND': [('V+Inf', 'V+Cond+Prs+Person-Number')],
#	'IMPRT': [('V+Inf', 'V+Imprt+Person-Number')],
#	'POT': [('V+Inf', 'V+Pot+Prs+Person-Number')],
}

VERB_FILTER_DEFINITION = ['stem', 'source']

VTYPE_CONTEXT_CHOICES = (
	('V-PRS', _('present')),
	('V-PRT', _('past')),
#	('V-PRF', _('perfect')),
#	('V-GER', _('gerund')),
#	('V-COND', _('conditional')),
#	('V-IMPRT', _('imperative')),
#	('V-POT', _('potential')),
#	('V-MIX', _('mix')),
#	('TEST', _('test questions')),
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

DERIVATION_QUESTION_ANSWER = {
	'A-DER-V': [('A+Sg+Nom', 'A+Der/AV+V+Ind+Prs+Person-Number')],

}

DERIVATION_FILTER_DEFINITION = False

DERIVATION_CHOICES_CONTEXT = (
 	('A-DER-V', _('adjective->verb derivation')),
	('DER-PASSV', _('passive derivation')),
)

BOOK_CHOICES = (
    ('tyypsonad', _(u'Tüüpsõnad')),
    ('all', _(u'all')),
    #('K2', _('Book 2')),
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

VASTAS_NR_OF_TASKWORDS = (
	('2', _('2')),
	('3', _('3')),
	('4', _('4')),
)

TRANS_CHOICES = (
        ('vroest', _(u'Võro to Estonian')),
        ('estvro', _(u'Estonian to Võro')),
	    ('vrofin', _(u'Võro to Finnish')),
        ('finvro', _(u'Finnish to Võro')),
        ('vroeng', _(u'Võro to English')),
	    ('engvro', _(u'English to Võro')),           
        ('vrodeu', _(u'Võro to German')),
        ('deuvro', _(u'German to Võro')),
        ('vrosme', _(u'Võro to North Saami')),
        ('smevro', _(u'North Saami to Võro')),
        ('vroswe', _(u'Võro to Swedish')),
        ('swevro', _(u'Swedish to Võro')),
        ('vronob', _(u'Võro to Norwegian')),
        ('nobvro', _(u'Norwegian to Võro')), 
)

NUMLANGUAGE_CHOICES = (
	('vro', _('Võro')),
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
	('NATUREWORDS', _('nature')),
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

#BOOK_CHOICES = tuple(
# 	[(source.name, source.name) for source in Source.objects.all()] +
# 	[('all', _('ALL'))]
#)


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
	VTYPE_CONTEXT_CHOICES]


GAME_TYPE_DEFINITIONS = {
	'A': ADJECTIVE_QUESTION_ANSWER,
	'Der': DERIVATION_QUESTION_ANSWER,
	'N': NOUN_QUESTION_ANSWER,
	'Num': NUMERAL_QUESTION_ANSWER,
	'Pron': PRONOUN_QUESTION_ANSWER,
	'V': VERB_QUESTION_ANSWER,
}

GAME_FILTER_DEFINITIONS = {
	'A': ADJECTIVE_FILTER_DEFINITION,
	'Der': DERIVATION_FILTER_DEFINITION,
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

from vro_oahpa.settings import INFINITIVE_SUBTRACT as infinitives_sub
from vro_oahpa.settings import INFINITIVE_ADD as infinitives_add

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
		# For Russian: spellrelax for 'е' vs 'ё', vowels with and without stress marks
		# The spell-relax rules for Võro:
	   u'b́' : u'bʼ',
	   u'b' : u'bʼ',
	   u'd́': u'dʼ',
	   u'd': u'dʼ',
	   u'f ́': u'fʼ',
	   u'f': u'fʼ',
	   u'ǵ': u'gʼ',
	   u'g': u'gʼ', 
	   u'h́': u'hʼ',
	   u'h': u'hʼ',
	   u'ḱ': u'kʼ',
	   u'k': u'kʼ',
	   u'ĺ': u'lʼ',
	   u'l': u'lʼ',
	   u'ḿ': u'mʼ',
	   u'm' : u'mʼ',
	   u'ń' :  u'nʼ',
	   u'n' : u'nʼ',
	   u'ṕ' : u'pʼ',
	   u'p' : u'pʼ',
	   u'ŕ' : u'rʼ',
	   u'r' : u'rʼ',
	   u'ś' : u'sʼ',
	   u's' : u'sʼ',
	   u't́' : u'tʼ',
	   u't' : u'tʼ',
	   u'v́' : u'vʼ',
	   u'v' : u'vʼ',
	   # different apostrophy-like characters are accepted:
	   u'\'' : u'ʼ', # the regular apostrophy
	   u'´' : u'ʼ', # acute
	   u'`' : u'ʼ', # gravis
	   u'’' : u'ʼ', # right single apostrophy
	   # spell-relax for glottal stop denoted by q
	   u'ʼ' : u'q', # modifier letter apostrophy
	   u'\'' : u'q', # the regular apostrophy
	   u'´' : u'q', # acute
	   u'`' : u'q', # gravis
	   u'’' : u'q', # right single apostrophy
	}

	# Create an iterator. We want to generate as many possibilities as
	# possible (very fast), so more relaxed options are available.
	searches = relax_pairs.items()
	# HU: Commented out the following complex code because it was causing an infinite loop or similar. And the generation of relaxed forms works fine without it. :)
	#print "searches composed", searches
	#permutations = itertools.chain(itertools.permutations(searches))
	#print "permutations composed"
	#perms_flat = sum([list(a) for a in permutations], [])
	#print "list of permutations ",perms_flat

	# Individual possibilities
	relaxed_perms = [sub_str(relaxed, R, S) for S, R in searches]
	#print relaxed_perms

	# Possibilities applied one by one
	#for S, R in perms_flat:
	#	relaxed = sub_str(relaxed, R, S)
	#	relaxed_perms.append(relaxed)

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
	self.allnoun_type = dict(NOUN_TYPE_CHOICES).keys() # added by Pavel


# comment
# DEBUG = open('/dev/ttys001', 'w')
# DEBUG = open('/dev/null', 'w')


def get_feedback(self, wordform, language):

	language = switch_language_code(language)

	feedbacks = wordform.feedback.filter(feedbacktext__language=language).order_by('feedbacktext__order')

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
					'language' : 'vro',  # sme in univ_oahpa
					'syll' : ['2syll'], # syllabicity not relevant, change this
					'bisyllabic': 'on',
					'trisyllabic': False,
					'contracted': False,
					'level' : 'all',
					'lemmacount' : '2',
					'case': 'N-PAR',
					'pos' : 'N',
					'vtype' : 'PRS',
					'adjcase' : 'NOM',
					'number' : '',
					'pron_type': 'Pers',
					'proncase' : 'N-NOM', # Need a new default case here
					'grade' : '',  # was: '' 'Pos' is not a good idea beacuse it is implicit in the database.
					'case_context' : 'N-PAR',
					'vtype_context' : 'V-PRS',
					'pron_context' : 'P-PERS',
					'num_context' : 'NUM-ATTR',
					'num_level' : '1',
					'num_type' : 'CARD',  # added by Heli
					'derivation_type' : 'V-DER-PASS',
					'derivation_type_context' : 'DER-PASSV', # was V-DER
					'geography': 'world',
					'frequency' : [],
					'num_bare' : 'N-NOM', # Need a new default case here
					'adj_context' : 'ATTRPOS',
					'book' : 'all',
					'noun_type': 'N-MASC-INANIM',
					'singular_only' : False}




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
		if hasattr(self, 'translang'): # commented out these two lines, because otherwise relax was not working in Morfa
			if self.translang == 'vro': # caused a problem in Numra, as NumQuestion does not have the attribute translang 
				# Relax spellings.
			
				accepted_answers = [force_unicode(item) for item in accepted_answers]
				forms = sum([relax(force_unicode(item)) for item in accepted_answers], [])
                                #print "relaxed forms: ", forms
				# need to subtract legal answers and make an only relaxed list.
				relaxings = [item for item in forms if force_unicode(item) not in accepted_answers]
		if (hasattr(self, 'gametype') and self.gametype == 'leksa'): # this applies only to Leksa, was: elif
			# PI: commented out at this stage
			# # add infinitives as possible answers
			if self.word.pos == 'V':
				if self.translang in infinitives_sub and infinitives_add:
					infin_s = infinitives_sub[self.translang]
				        infin_a = infinitives_add[self.translang]
				        lemma = re.compile(infin_s)
				        infins = [lemma.sub(infin_a, force_unicode(ax)) for ax in accepted_answers]
				        accepted_answers = infins + accepted_answers

                #forms = accepted_answers  # This is wrong: the relaxed pairs are overwritten!

		self.correct_anslist = [force_unicode(item) for item in accepted_answers] + [force_unicode(f) for f in forms]
		print "correct_anslist:",self.correct_anslist
		self.relaxings = relaxings

		#def generate_fields(self,answer_size, maxlength):
		#	self.fields['answer'] = forms.CharField(max_length = maxlength, \
         #                                       widget=forms.TextInput(\
          #  attrs={'size': answer_size, 'onkeydown':'javascript:return process(this, event,document.gameform);',}))  # copied from old-oahpa

# #
#
# Leksa Forms
#
# #

class LeksaSettings(OahpaSettings):
	semtype = forms.ChoiceField(initial='all', choices=SEMTYPE_CHOICES) # was: HUMAN
	transtype = forms.ChoiceField(choices=TRANS_CHOICES, widget=forms.Select)
	# For placename quizz
	#geography = forms.ChoiceField(initial='world', choices=GEOGRAPHY_CHOICES)
	#frequency = forms.MultipleChoiceField(required=False, widget=CheckboxSelectMultiple, choices=FREQUENCY_CHOICES)  # added
	#common = forms.BooleanField(required=False, initial='1')
	#rare = forms.BooleanField(required=False,initial=0)
	# sapmi = forms.BooleanField(required=False, initial='1')
	# world = forms.BooleanField(required=False,initial=0)
	# suopma = forms.BooleanField(required=False,initial=0)
	source = forms.ChoiceField(initial='all', choices=BOOK_CHOICES)
	# level = forms.ChoiceField(initial='all', choices=LEVEL_CHOICES, widget=forms.Select(attrs={'onchange':'javascript:return SetIndex(document.gameform.semtype,this.value);',}))
	
	default_data = {'gametype' : 'leksa', 'language' : 'vro', 'dialogue' : 'GG',
			#'syll' : [],
			#'bisyllabic': False,
			#'trisyllabic': False,
			#'bisyllabic': False,
			#'contracted': False,
			'source': 'all',
			'semtype' : 'all', # was: 'HUMAN',
			#'geography' : 'world',
			#'frequency' : ['common'] # added
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
		self.sourcelang = transtype[0:3]
		self.word = word
		self.audio = word.audio # pronounciation
		self.gametype = 'leksa'
		kwargs['correct_val'] = correct_val
		super(LeksaQuestion, self).__init__(*args, **kwargs)

		self.tcomm = None
		if tcomms:
			if userans_val in tcomms:
				self.tcomm = True
			else:
				self.tcomm = None


		self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)

        # If we want stress marks in Leksa then we have to use lemma_stressed instead of lemma.
		
		if type(word) == Word: 
                    if self.sourcelang == 'rus':
                        self.lemma = word.lemma_stressed  # for Rusian the words will be presented with stress marks
                    else:
                        self.lemma = word.lemma # for other languages 'lemma_stressed' does not exist
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
			# always accept relaxed spelling
			#if userans_val in self.relaxings:
				self.is_relaxed = "relaxed"
				self.strict = 'Strict form'
			#else:
			#	self.is_relaxed = ""

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

		PI: this is quite hardcoded (and it wasn't exactly
		easy finding where the N-ILL default value in
		$home/morfa/ came from, because instead of an
		exception there was a relatively unhelpful 404 error.
	"""
	case = forms.ChoiceField(initial='N-PAR', choices=CASE_CHOICES, widget=forms.Select)
	number = forms.ChoiceField(initial='Sg', choices=NUMBER_CHOICES, widget=forms.Select)
	pron_type = forms.ChoiceField(initial='PERS', choices=PRONOUN_SUBCLASSES, widget=forms.Select)
	proncase = forms.ChoiceField(initial='N-NOM-PL', choices=CASE_CHOICES_PRONOUN, widget=forms.Select)
	adjcase = forms.ChoiceField(initial='ATTR', choices=ADJCASE_CHOICES, widget=forms.Select)  # was ADJEX_CHOICES
	vtype = forms.ChoiceField(initial='PRS', choices=VTYPE_CHOICES, widget=forms.Select)
	num_bare = forms.ChoiceField(initial='N-GEN', choices=NUM_BARE_CHOICES, widget=forms.Select)
	num_level = forms.ChoiceField(initial='1', choices=NUM_LEVEL_CHOICES, widget=forms.Select)
	num_type = forms.ChoiceField(initial='CARD',choices=NUM_TYPE_CHOICES, widget=forms.Select)
	derivation_type = forms.ChoiceField(initial='V-DER-PASS', choices=DERIVATION_CHOICES, widget=forms.Select)
	derivation_type_context = forms.ChoiceField(initial='DER-PASSV', choices=DERIVATION_CHOICES_CONTEXT, widget=forms.Select)
	num_context = forms.ChoiceField(initial='NUM-ATTR', choices=NUM_CONTEXT_CHOICES, widget=forms.Select)
	case_context = forms.ChoiceField(initial='N-NOM-PL', choices=CASE_CONTEXT_CHOICES, widget=forms.Select)
	adj_context = forms.ChoiceField(initial='ATTR', choices=ADJ_CONTEXT_CHOICES, widget=forms.Select)
	vtype_context = forms.ChoiceField(initial='V-PRS', choices=VTYPE_CONTEXT_CHOICES, widget=forms.Select)
	pron_context = forms.ChoiceField(initial='P-PERS', choices=PRON_CONTEXT_CHOICES, widget=forms.Select)
	wordform_type = forms.ChoiceField(initial='', choices=WORDFORM_TYPE_CHOICES, widget=forms.Select)
	book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
	bisyllabic = forms.BooleanField(required=False, initial=True)
	trisyllabic = forms.BooleanField(required=False, initial=False)
	contracted = forms.BooleanField(required=False, initial=False)
	grade = forms.ChoiceField(initial='POS', choices=GRADE_CHOICES, widget=forms.Select)

	# PI added
	noun_type = forms.ChoiceField(initial='N-MASC-INANIM', choices=NOUN_TYPE_CHOICES, widget=forms.Select)
	# HU added
	singular_only = forms.BooleanField(required=False, initial=True)

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
			# Gen2 and Loc2 mostly exist for masculine nouns:
			#if 'case' in post_data:
			#	if post_data['case'] in ['Par', 'Loc']:
			#	    self.settings['noun_type'] = "N-MASC-INANIM"
			#	    self.fields['noun_type'] = 'N-MASC-INANIM'
			# Use a restricted choice set for pronoun case for Refl and Recipr
			if 'pron_type' in post_data:
				if post_data['pron_type'].lower() in ['refl', 'recipr']:
					self.fields['proncase'].choices = RECIP_REFL_CHOICES




class MorfaQuestion(OahpaQuestion):
	"""
	Questions for morphology game.
	"""

	def __init__(self, word, tag, baseform, correct, accepted_answers,
					answer_presentation, translations, question, dialect, language,
					userans_val, correct_val, conneg, *args, **kwargs):

		lemma_widget = forms.HiddenInput(attrs={'value': word.id})
		tag_widget = forms.HiddenInput(attrs={'value': tag.id})
		self.translang = 'vro'
		self.gametype = 'morfa'
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

		# self.wordclass = word.wordclass
		# PI: seems to be only used for verbs at this point, so just commenting out
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
				self.pron = ' '.join([time, pronoun])

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
			#if userans_val in self.relaxings: let's make the spelling always relaxed
                self.is_relaxed = "relaxed"
                self.strict = 'Strict form'
			#else:
			#	self.is_relaxed = ""

		self.correct_ans = answer_presentation
# #
#
# Numra Forms
#
# #


class NumSettings(OahpaSettings):
	maxnum = forms.ChoiceField(initial='10', choices=NUM_CHOICES, widget=forms.RadioSelect)
	numgame = forms.ChoiceField(initial='numeral', choices=NUMGAME_CHOICES, widget=forms.RadioSelect)
	#numlanguage = forms.ChoiceField(initial='sjd', choices=NUMLANGUAGE_CHOICES, widget=forms.RadioSelect)
	# TODO: remove mandatory need to set default data, should be done through 'initial' field setting.
	default_data = {'language' : 'vro', 'numlanguage' : 'vro', 'dialogue' : 'GG', 'maxnum' : '10', 'numgame': 'numeral'}

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
                self.gametype = gametype
                self.translang = 'vro'

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
	default_data = {'language' : 'vro', 'numlanguage' : 'vro', 'dialogue' : 'GG', 'gametype' : 'kl1', 'numgame': 'string'}

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

	default_data = {'language' : 'vro', 'numlanguage' : 'vro', 'numgame': 'string'}


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
	qtype_verbs = set(['MAINV', 'V-PRS', 'V-PRT', 'V-COND','V-IMPRT', 'TEST']) # added MAINV for liv

	def generate_fields(self,answer_size, maxlength):
		self.fields['answer'] = forms.CharField(max_length = maxlength, \
												widget=forms.TextInput(\
			attrs={'size': answer_size,}))

			# 'onkeydown':'javascript:return process(this, event,document.gameform);'

	def __init__(self, question, qanswer, \
				 qwords, awords, dialect, language, userans_val, correct_val, *args, **kwargs):
		self.init_variables("", userans_val, [])
		self.lemma = ""
		self.dialect = dialect
		self.translang = 'vro'
		self.gametype = 'morfac' # not sure if this is ok

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
		selected_awords = self.select_words(qwords, awords)

		relaxed = []
		form_list=[]

		if not selected_awords.has_key(task):
			raise Http404(task + " " + atext + " " + str(qanswer.id))
		if len(selected_awords[task]['fullform'])>0:
			for f in selected_awords[task]['fullform']:
				self.correct_anslist.append(force_unicode(f))

			accepted = sum([relax(force_unicode(item)) for item in self.correct_anslist], [])
			self.relaxings = [item for item in accepted if item not in self.correct_anslist]
			self.correct_anslist.extend(self.relaxings)
			log_w = Word.objects.get(id=selected_awords[task]['word'])
			w_str = log_w.lemma
			w_pos = log_w.pos
			t_str = Tag.objects.get(id=selected_awords[task]['tag']).string
			log_name = "contextual_morfa_" + w_pos
			log_value = '%s+%s' % (w_str, t_str)
			self.is_correct(log_name, log_value)
			self.correct_ans = self.correct_anslist[0]

		self.correct_anslist = [force_unicode(item) for item in accepted]

		self.qattrs = {}
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

		# Forms question string and answer string out of grammatical elements and other strings.
		qstring = ""
		astring= ""

		# Format question string
		qtext = question.string
		for w in qtext.split():
			if not qwords.has_key(w):
				qstring = qstring + " " + force_unicode(w)
			else:
				if qwords[w].has_key('fullform'):
					qstring = qstring + " " + force_unicode(qwords[w]['fullform'][0])
				else:
					qstring = qstring + " " + force_unicode(w)
		qstring=qstring.replace(" -","-")
		qstring=qstring.replace(" .",".")


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

		# if answer_word_el.pos == 'V':
		# 	self.wordclass = answer_word_el.wordclass

		# If the asked word is in Pl, generate nominal form

		if answer_tag_el.pos == "N":
			if qtype == "COLL-NUM":
				self.lemma = answer_word_el.lemma
			else:
				if answer_tag_el.number=="Sg" or answer_tag_el.case=="Ess" or answer_tag_el.case=="Nom":  #was: qtype="N-NOM-PL"
					self.lemma = answer_word_el.lemma
				else:
					nplforms = Form.objects.filter(word__pk=answer_word, tag__string='N+Pl+Nom')
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
			answer_word_form = Form.objects.exclude(dialects__dialect='NG')\
										.filter(word__pk=answer_word,
												tag=answer_tag_el,
												dialects__dialect=self.dialect)
			answer_word_form = answer_word_form[0]
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
    if not self.is_valid():
        return None, None, None

    noanalysis=False

    fstdir = "/opt/smi/sme/bin"
    #fstdir = settings.FST_DIRECTORY
    fst = fstdir + "/ped-sme.fst"
    lo = "/opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/lookup" # on victorio
    #lo="/Users/mslm/bin/lookup" # on Heli's machine
    lookup = " | " + lo + " -flags mbTT -utf8 -d " + fst # on Heli's machine
    #lookup2cg = " | /Users/pyry/gtsvn/gt/script/lookup2cg" # on Ryan's machine
    lookup2cg = " | /usr/local/bin/lookup2cg " # on victorio
    cg3 = "/usr/local/bin/vislcg3"
    preprocess = " | /opt/sami/cg/bin/preprocess " # on victorio
    #preprocess = " | /Users/mslm/main/gt/script/preprocess "
    dis_bin = "/opt/smi/sme/bin/sme-ped.cg3" # on victorio
    #dis_bin = "../sme/src/sme-ped.cg3" # on Heli's machine TODO: add to settings.py

    vislcg3 = " | " + cg3 + " --grammar " + dis_bin + " -C UTF-8"

    self.userans = self.cleaned_data['answer']
    answer = self.userans.rstrip()
    answer = answer.lstrip()
    answer = answer.rstrip('.!?,')

    self.error = "error"

    qtext = question
    qtext = qtext.rstrip('.!?,')

    #logfile = open('/home/vro_oahpa/vro_oahpa/vro_drill/vastaF_log.txt','w')

    host = 'localhost'
    port = 9000  # was: 9000, TODO - add to settings.py
    size = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host,port)) # on victorio
        sys.stdout.write('%')

        analysis = ""
        question_lookup = "echo \"" + qtext + "\"" + preprocess
        words = os.popen(question_lookup).readlines()
        for qword in words: # or qwords ?
            cohort=""
            w = qword.lstrip().rstrip()
            s.send(w)  # on victorio
            cohort = s.recv(size)

            if not cohort or cohort == w:
                cohort = w + "\n"
            if cohort=="error":
                raise Http500
            analysis = analysis + cohort

        if self.gametype=="sahka":
            analysis = analysis + "\"<^qdl_id>\"\n\t\"^sahka\" QDL " + utterance_name +"\n"
        else:
            analysis = analysis + "\"<^qst>\"\n\t\"^qst\" QDL\n"

	   #logfile.write(analysis+"\n")
        data_lookup = "echo \"" + answer.encode('utf-8') + "\"" + preprocess
        words = os.popen(data_lookup).readlines()
        analyzed=""
        for w in words:
            w=w.strip()
            s.send(w)  # on vic
            analyzed = analyzed + s.recv(size)
        s.send("q")  # on vic
        s.close()

    except socket.error:    # port 9000 not available => morph. analysis will be done by ped-sme.fst
        # analyse words in the question
        analysis = ""
        question_lookup = "echo \"" + qtext + "\"" + preprocess
        words = os.popen(question_lookup).readlines()
        for qword in words: # or qwords ?
            cohort=""
            w = qword.lstrip().rstrip()
            word_lookup = "echo \"" + force_unicode(w).encode('utf-8') + "\"" + lookup + lookup2cg  # on Heli's machine
            morfanal = os.popen(word_lookup).readlines()
            for row in morfanal:
                row = row.strip()
                cohort = cohort + row + "\n" + "\t"
            if not cohort or cohort == w:
                cohort = w + "\n"
            if cohort=="error":
                raise Http500
            analysis = analysis + cohort

        if self.gametype=="sahka":
            analysis = analysis + "\"<^qdl_id>\"\n\t\"^sahka\" QDL " + utterance_name +"\n"
        else:
            analysis = analysis + "\"<^qst>\"\n\t\"^qst\" QDL\n"

	    #logfile.write(analysis+"\n")

		# analyse words in the answer

        data_lookup = "echo \"" + answer.encode('utf-8') + "\"" + preprocess
        words = os.popen(data_lookup).readlines()
        analyzed=""
        for w in words:
            w=w.strip()
            word_lookup = "echo \"" + force_unicode(w).encode('utf-8') + "\"" + lookup + lookup2cg  # on Heli's machine
            morfanal = os.popen(word_lookup).readlines()
            ans_cohort=""
            for row in morfanal:
                row = row.strip()
                ans_cohort = ans_cohort + row + "\n" + "\t"
            analyzed = analyzed + ans_cohort
   # except socket.timeout:
    #    raise Http404("Technical error, please try again later.")

    #logfile.write(analyzed+"\n")
    analysis = analysis + analyzed
    analysis = analysis + "\"<.>\"\n\t\".\" CLB"
    analysis = analysis.rstrip()
    analysis = analysis.replace("\"","\\\"")

    ped_cg3 = "echo \"" + analysis + "\"" + vislcg3
    checked = os.popen(ped_cg3).readlines()

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
            if msgstring.count("spellingerror") > 0:
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
    dia_msg = []
    target = ""
    variable=""
    constant=""
    found=False
    #Interface language
    if not language: language = "est" # was: nob
    language = switch_language_code(language)
    #if language == "no" : language = "nob"
    #if language == "fi" : language = "fin"
    #if language == "en" : language = "eng"
    if not language in ["est","lat","fin","eng","rus","vro"]: language="est" # was: nob
    for w in msgstrings.keys():
        if found: break
        for m in msgstrings[w].keys():
            if spelling and m.count("spelling") == 0: continue
            m = m.replace("&","")
            if Feedbackmsg.objects.filter(msgid=m).count() > 0:
                msg_el = Feedbackmsg.objects.filter(msgid=m)[0]
                message = Feedbacktext.objects.filter(feedbackmsg=msg_el,language=language)[0].message
                message = message.replace("WORDFORM","\"" + w + "\"")
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
    today=datetime.date.today()
    log = Log.objects.create(userinput=self.userans,feedback=feedbackmsg,iscorrect=iscorrect,\
                                       example=question,game=self.gametype,date=today)
    log.save()

    variables = []
    variables.append(variable)
    variables.append(constant)
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

        maxlength=50
        answer_size=50
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

        # In qagame, all words are considered as answers.
        self.gametype="vasta"
        self.messages, jee, joo  = self.vasta_is_correct(qstring.encode('utf-8'), qwords, language)

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
        super(SahkaSettings, self).__init__(*args, **kwargs)

        # Link to grammatical explanation for each page
        self.grammarlinkssme = Grammarlinks.objects.filter(language="sme")
        self.grammarlinksno = Grammarlinks.objects.filter(language="no")

    def init_hidden(self, topicnumber, num_fields, dialogue, image, wordlist):

        # Store topicnumber as hidden input to keep track of topics.
        #print "topicnumber", topicnumber
        #print "num_fields", num_fields
        topicnumber = topicnumber
        num_fields = num_fields
        dialogue = dialogue
        image = image
        wordlist = wordlist


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

        super(SahkaQuestion, self).__init__(*args, **kwargs)

        if utterance.utttype == "question":
            maxlength=50
            answer_size=50
            self.fields['answer'] = forms.CharField(max_length = maxlength, \
                                                    widget=forms.TextInput(\
            attrs={'size': answer_size, 'onkeydown':'javascript:return process(this, event, document.gameform);',}))

        self.fields['utterance_id'] = forms.CharField(widget=utterance_widget, required=False)

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

    fstdir = "/opt/smi/sme/bin"
    #fstdir = settings.FST_DIRECTORY
    fst = fstdir + "/ped-sme.fst"
    lo = "/opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/lookup"# on victorio
    #lo="/Users/mslm/bin/lookup" # on Heli's machine
    lookup = " | " + lo + " -flags mbTT -utf8 -d " + fst # on Heli's machine
    lookup2cg = " | /usr/local/bin/lookup2cg " # on victorio
    cg3 = "/usr/local/bin/vislcg3"
    preprocess = " | /opt/sami/cg/bin/preprocess " # on victorio
    #preprocess = " | /Users/mslm/main/gt/script/preprocess " # on Heli's machine
    dis_bin = "/opt/smi/sme/bin/sme-ped.cg3" # on victorio
    #dis_bin = "/Users/mslm/main/ped/sme/src/sme-ped.cg3" # on Heli's machine TODO: add to settings.py

    vislcg3 = " | " + cg3 + " --grammar " + dis_bin + " -C UTF-8"

    self.userans = self.cleaned_data['answer']
    answer = self.userans.rstrip()
    answer = answer.lstrip()
    answer = answer.rstrip('.!?,')
    #print answer

    self.error = "error"

    qtext = question
    qtext = qtext.rstrip('.!?,')

    #logfile = open('/home/vro_oahpa/vro_oahpa/vro_drill/vastas_log.txt', 'w')
    host = 'localhost'
    port = 9000  # was: 9000, TODO - add to settings.py
    size = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host,port)) # on vic
        sys.stdout.write('%')

        analysis = ""
        data_lookup = "echo \"" + qtext + "\"" + preprocess
        words = os.popen(data_lookup).readlines()
        print question_id
        #print words
        #print qwords
        for word in words:
            w=""
            cohort=""
            print word
            # All the words will go through morph.analyser, even if they have a tag-attribute already. We do it to avoid problems with compound words.
            w = force_unicode(word).encode('utf-8')
            w=w.lstrip().rstrip()
            s.send(w) # on victorio
            cohort = s.recv(size)
            analysis = analysis + cohort
            #logfile.write(analysis+"\n")
            print analysis
        ### Lemmas and POS tags of task words are gathered into the variables
        ### tasklemmas and taskpos respectively. Tasklemmas and taskpos will be
        ### sent to CG together with the morph. analysed question and answer.
        tasklemmas = ""
        for aword in awords:
            print aword
	        #logfile.write(aword)
            if aword.has_key('taskword') and aword['taskword']:
                tlemma = aword['fullform']
                tlemma = force_unicode(tlemma).encode('utf-8')
                tlemma = tlemma.strip()
                print tlemma
		        #logfile.write(tlemma+" ")
                tasktag = Tag.objects.filter(id=aword['tag'])
                tasktagstring = tasktag[0].string
                taskpos = tasktag[0].pos
                ttag = tasktagstring.replace("+"," ")
                print ttag
		        #logfile.write(ttag+"\n")
                s.send(tlemma)  # on vic
                word_lookup = s.recv(size)  # on vic
		        #logfile.write(word_lookup)
                ans_cohort=""
                #print rows
                rows = word_lookup.split("\n")  # on vic
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
                        print malemmas
			             #logfile.write(malemma+"\n")
                        print malemma
                        print malemma_without_hash
                        tasklemmas = tasklemmas + "\n\t\"" + malemma + "\" "+taskpos
                    morfanal = morfanal + ans_cohort  # END

        analysis = analysis + "\"<^vastas>\"\n\t\"^vastas\" QDL " + question_id + " " + tasklemmas + "\n"
        #####
        print analysis
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
            print word
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
        for aword in awords:
            print aword
	       #logfile.write(aword)
            if aword.has_key('taskword') and aword['taskword']:
                tlemma = aword['fullform']
                tlemma = force_unicode(tlemma).encode('utf-8')
                tlemma = tlemma.strip()
                print tlemma
		        #logfile.write(tlemma+" ")
                tasktag = Tag.objects.filter(id=aword['tag'])
                tasktagstring = tasktag[0].string
                taskpos = tasktag[0].pos
                ttag = tasktagstring.replace("+"," ")
                print ttag
		        #logfile.write(ttag+"\n")
                ans_cohort = ""
                word_lookup = "echo \"" + tlemma + "\"" + lookup + lookup2cg  # on Heli's machine
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
                        print malemmas
			             #logfile.write(malemma+"\n")
                        print malemma
                        print malemma_without_hash
                        tasklemmas = tasklemmas + "\n\t\"" + malemma + "\" "+taskpos
                    morfanal = morfanal + ans_cohort  # END

        analysis = analysis + "\"<^vastas>\"\n\t\"^vastas\" QDL " + question_id + " " + tasklemmas + "\n"
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

    #except socket.timeout:
        #raise Http404("Technical error, please try again later.")


    analysis = analysis + analyzed
    analysis = analysis + "\"<.>\"\n\t\".\" CLB"
    analysis = analysis.rstrip()
    analysis = analysis.replace("\"","\\\"")
    print analysis
    #logfile.write(analysis)
    ped_cg3 = "echo \"" + analysis + "\"" + vislcg3
    checked = os.popen(ped_cg3).readlines()
    #print checked

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
            if msgstring.count("spellingerror") > 0:
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
    target = ""
    variable=""
    constant=""
    found=False
    #Interface language
    if not language: language = "est"
    language = switch_language_code(language)
    #if language == "no" : language = "nob"
    #if language == "fi" : language = "fin"
    #if language == "en" : language = "eng"
    if not language in ["rus","est","fin","eng","lat","vro"]: language="est"

    for w in msgstrings.keys():
        if found: break
        for m in msgstrings[w].keys():
            if spelling and m.count("spelling") == 0: continue
            m = m.replace("&","")
            if Feedbackmsg.objects.filter(msgid=m).count() > 0:
                msg_el = Feedbackmsg.objects.filter(msgid=m)[0]
                message = Feedbacktext.objects.filter(feedbackmsg=msg_el,language=language)[0].message
                message = message.replace("WORDFORM","\"" + w + "\"")
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
    today=datetime.date.today()
    log = Log.objects.create(userinput=self.userans,feedback=feedbackmsg,iscorrect=iscorrect,\
                                       example=question,game=self.gametype,date=today)
    log.save()

    variables = []
    variables.append(variable)
    variables.append(constant)
    return msg, dia_msg, variables


class CealkkaSettings(OahpaSettings):

    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
    level = forms.ChoiceField(initial='1', choices=VASTA_LEVELS, widget=forms.Select)
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

        maxlength=50
        answer_size=50
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
                    qstring = qstring + " " + w
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
