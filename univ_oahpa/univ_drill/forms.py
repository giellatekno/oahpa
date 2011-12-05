# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
import univ_oahpa.settings

from univ_oahpa.conf.tools import switch_language_code

from models import *
#from game import * 
#from univ_oahpa.univ_drill.game import relax
import datetime
import sys
import itertools

# TODO: These should be accessible in the admin interface, not hardcoded.

PRONOUNS_LIST = {'Sg1':'manne', 'Sg2':'datne', 'Sg3':'dïhte',
		  'Pl1':'mijjieh', 'Pl2':'dijjieh', 'Pl3':'dah',
		  'Du1':'månnoeh', 'Du2':'dåtnoeh', 'Du3':'dah guaktah'}

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
	('N-INE', _('inessive')),
	('N-ELA', _('elative')),
	('N-COM', _('comitative')),
	('N-GEN', _('genitive')),
	('N-ESS', _('essive')),
)

CASE_CHOICES_PRONOUN = (
	('N-ACC', _('accusative')),
	('N-ILL', _('illative')),
	('N-INE', _('inessive')),
	('N-ELA', _('elative')),
	('N-COM', _('comitative')),
	('N-GEN', _('genitive')),
	# ('N-ESS', _('essive')),
)

CASE_CONTEXT_CHOICES = (
	('N-NOM-PL', _('plural')),
	('N-ACC', _('accusative')),
	('N-GEN', _('genitive')),
	('N-ILL', _('illative')),
	('N-INE', _('inessive')),
	('N-ELA', _('elative')),
	('N-COM', _('comitative')),
	('N-ESS', _('essive')),
	('N-MIX', _('mix')),
)

# 
# No inessive or essive, and no choice between nom sg. and pl, but nom sg and pl come together.
# 
PRON_CONTEXT_CHOICES = (
	('P-NOM', _('nominative')),
	('P-ACC', _('accusative')),
	('P-GEN', _('genitive')),
	('P-ILL', _('illative')),
	('P-ELA', _('elative')),
	('P-COM', _('comitative')),
	('P-MIX', _('mix')),
)

ADJCASE_CHOICES = (
	('N-NOM', _('nominative')),
	('ATTR', _('attributive')),
# 	('PRED', _('predicative')),
)

ADJEX_CHOICES = (
	('A-ATTR', _('attributive')), 	# A+Nom+Sg -> A+Attr
 	('A-COMP', _('comparative')),		# A+Nom+Sg -> Comp	TODO: A+Attr -> Comp
 	('A-SUPERL', _('superlative')),	# A+Nom+Sg -> Superl	TODO: A+Attr -> Comp

)

ADJ_CONTEXT_CHOICES = (
	('ATTRPOS', _('attributive positive')),
	('PREDCOMP', _('predicative comparative')),
	('PREDSUP', _('predicative superlative')),
	('A-MIX', _('mix')),
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
	('N-INE', _('inessive')),
	('N-ELA', _('elative')),
	('N-COM', _('comitative')),
)

NUM_LEVEL_CHOICES = (
	('1', _('First level')),
	('2', _('Second level')),
)

VTYPE_CHOICES = (
	('PRS', _('present')),
	('PRT', _('past')),
	('PRF', _('perfect')),
	('GER', _('gerund')),
# 	('COND', _('conditional')),
	('IMPRT', _('imperative')),
# 	('POT', _('potential')),
)

VTYPE_CONTEXT_CHOICES = (
	('V-PRS', _('present')),
	('V-PRT', _('past')),
	('V-PRF', _('perfect')),
	('V-GER', _('gerund')),
	# ('V-COND', _('conditional')),
	('V-IMPRT', _('imperative')),
	('V-MIX', _('mix')),
	('TEST', _('test questions')),
	# ('V-POT', _('potential')),
 )

LEVEL_CHOICES = (
	('l1', _('Level 1')),
	('l2', _('Level 1-2')),
	('l3', _('Level 1-3')),
	('all', _('All')),
)

FREQUENCY_CHOICES = (
	('common', _('common')),
)

GEOGRAPHY_CHOICES = (
	('mid', _('mid')),
	('north', _('north')),
	('other', _('other')),
	('south', _('south')),
)

VASTA_LEVELS = (
	('1', _('First level')),
	('2', _('Second level')),
	('3', _('Third level')),
)

TRANS_CHOICES = (
	('smenob', _('South Sami to Norwegian')),
	('nobsme', _('Norwegian to South Sami')),
#	('smasme', _('South Sami to North Sami')),
#	('smesma', _('North Sami to South Sami')),
	('smeswe', _('South Sami to Swedish')),
	('swesme', _('Swedish to South Sami')),
	('smefin', _('South Sami to Finnish')),
	('finsme', _('Finnish to South Sami')),
#	('smaeng', _('South Sami to English')),
#	('engsma', _('English to South Sami')),
#	('smadeu', _('South Sami to German')),
#	('deusma', _('German to South Sami')),
)

NUMLANGUAGE_CHOICES = (
	('sme', _('North Sami')),
)

SEMTYPE_CHOICES = (
	('FAMILY', _('family')),
    ('PROFESSION', _('profession')),
    ('HUMAN-LIKE', _('human-like')),
    ('ANIMAL', _('animal')),
    ('FOOD/DRINK', _('food/drink')),
    ('TIME', _('time')),
    ('CONCRETES', _('concretes')),
    ('BODY', _('body')),
    ('CLOTHES', _('clothes')),
    ('BUILDINGS/ROOMS', _('buildings/rooms')),
    ('NATUREWORDS', _('naturewords')),
    ('LEISURETIME/AT_HOME', _('leisuretime/at_home')),
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

# # 
#
# Morfa-S choices
#
# #

BOOK_CHOICES = (
	('d1', _('Davvin 1')),
    ('d2', _('Davvin 1-2')),
    ('d3', _('Davvin 1-3')),
    ('d4', _('Davvin 1-4')),
    ('sam1031_1', _('SAM-1031-1')),
    ('sam1031_2', _('SAM-1031-2')),
    ('algu', _('algu')),
    ('sara', _('sara')),
    ('bures', _('Bures bures fas')),
    ('oaidnalit', _('Oaidnalit')),
    ('all', _('All')),
)

# BOOK_CHOICES = tuple(
# 	[(source.name, source.name) for source in Source.objects.all()] + \
# 	[('all', _('ALL'))]
# )

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
	self.alladj_context = dict(ADJ_CONTEXT_CHOICES).keys()
	self.allnum_context = dict(NUM_CONTEXT_CHOICES).keys()
	self.allnum_bare = dict(NUM_BARE_CHOICES).keys()
	self.sources = dict(BOOK_CHOICES).keys()
	self.geography = dict(GEOGRAPHY_CHOICES).keys()


# comment
# DEBUG = open('/dev/ttys001', 'w')
# DEBUG = open('/dev/null', 'w')


def get_feedback(self, word, tag, wordform, language, dialect):
	"""
		FEEDBACK AND XML-SOURCE
		
		Nouns: attributes required: pos, soggi, stem, case/case2, number

			<l> nodes in messages.xml and n_smanob must match for
				pos, soggi, stem
			
			Remaining inflectional items, case and number, come from the tag.
						
			feedback_nouns.xml: 
			
			<feedback pos="N">
			  <stems>
				<l stem="2syll">
				  <msg pos="n">bisyllabic_stem</msg>
				</l>
				<l stem="3syll">
				  <msg pos="n">trisyllabic_stem</msg>
				</l>

				<l stem="3syll" soggi="a">
				  <msg case="Ill">soggi_a</msg>
				  <msg case="Ine">soggi_a</msg>
				  <msg case="Ela">soggi_a</msg>
				  <msg case="Com" number="Sg">soggi_a</msg>
				  <msg case="Ess">soggi_a</msg>
				  <note>daktarasse, vuanavasse, e/o > a</note>
				</l>
			 </stems>
			</feedback>
			
			
			n_smanob.xml:
			
			<e>
			  <lg>
				 <l margo="e" pos="n" soggi="e" stem="3syll">aagkele</l>
			  </lg>
			  { ... SNIP ... }
			</e>
			
		Verbs: Mostly the same. <l/>s match for class, stem, pos
		inflectional information from Tag object pertaining to mood, tense, personnumber.
		
		FEEDBACK DATA STRUCTURE
		
		Remember that this code runs once per word, and not on a huge set of words,
		so it should ideally be returning only one Feedback object.
		
		Feedback objects are then linked to Feedbackmsg objects, which contain
		message IDs, such as soggi_o, class_1, which then link to Feedbacktext objects
		which contain the corresponding messages in other languages.
		
		Feedback objects should be linked to multiple Feedbackmsg items (typically, 3)
		which individually contain class, syllable and umlaut information.
		
		Feedback.messages.all()
		
		CHANGES
		
		Altering the way the code functions should be as simple as adding new attributes
		to the dictionary objects below, and making sure that they have access to the
		variable with the data to be included.
		
				word_attrs = {
					'POS': {
						'soggi' : word.soggi,
					},
				}
		
	"""
	
	# Dictionaries here contain mapping of attributes, and where the data is stored.

	
	# Word -> Feedback
	word_attrs = {
		'N': {
			'pos': word.pos,
			'soggi': word.soggi,
			'stem': word.stem,
		},
		'V': {
			'wordclass': word.wordclass,
			'stem': word.stem,
			'pos': word.pos,
		},
	}
	
	# Tag -> Feedback
	tag_attrs = {
		'N': {
			'case2': tag.case,
			'number': tag.number,
		},
		'V': {
			'mood': tag.mood,
			'tense': tag.tense,
			'personnumber': tag.personnumber,
		}
	}
		
	if tag.pos in ["N", "Num"]:
		POS = 'N'
		# build Q for noun
	elif tag.pos == "A":
		return
		# build Q for verb
	elif tag.pos == "V":
		POS = 'V'
	else:
		POS = tag.pos

	# Combine the filter sets...
	try:
		FILTERS = dict(word_attrs[POS], **tag_attrs[POS])
	except KeyError:
		return False
	
	# Now make changes.
	if POS == 'V':
		# stem and wordclass are in complementary distribution
		# when one is set the other is not. All 2syll verbs
		# have class information, but all 3syll verbs do not.
		
		if FILTERS['stem'] == '3syll':
			FILTERS.pop('wordclass')
		elif FILTERS['stem'] == '2syll':
			FILTERS.pop('stem')
	
	# Adopt this to new code.
	# elif tag.pos == "A":
	# 	if tag.grade: 
	# 		grade = tag.grade
	# 	else:
	# 		grade = "Pos"
	# 	
	# 	if tag.attributive:
	# 		attributive = "Attr"
	# 		attrsuffix = word.attrsuffix
	# 	else:
	# 		attributive = "NoAttr"
	# 	
	# 	FEEDBACK_Q = Q(case2=tag.case) & \
	# 					Q(pos=tag.pos) & Q(grade=grade) &\
	# 					Q(attributive=attributive) & Q(attrsuffix=attrsuffix) & \
	# 					Q(number=tag.number)
	# 
	
	language = switch_language_code(language)
	
	if FILTERS:
		feedbacks = Feedback.objects.filter(**FILTERS)
	
	message_list = []
	if feedbacks:
		for f in feedbacks:
			msgs = f.messages.all()
			for m in msgs:
				messages = m.feedbacktext_set.filter(language=language)
				if messages.count() > 0:
					text = messages[0].message
					text = text.replace('WORDFORM', '"%s"' % wordform)
					message_list.append(text)
	
	self.feedback = ' \n '.join(message_list)
	

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
			if aword.has_key('word') and aword['word']:
				selected_awords[syntax]['word'] = aword['word']
			else:
				if aword.has_key('qelement') and selected_awords[syntax].has_key('tag'):
					form_list = None
					max=50
					i=0
					while not form_list and i<max:
						i=i+1
						word_count = WordQElement.objects.filter(qelement__id=aword['qelement']).count()
						if word_count>0:
							wqel = WordQElement.objects.filter(qelement__id=aword['qelement']).order_by('?')[0]
							selected_awords[syntax]['word'] = wqel.word.id
							form_list = Form.objects.filter(Q(word__id=selected_awords[syntax]['word']) &\
															Q(tag__id=selected_awords[syntax]['tag']))
					if form_list:
						fullf=[]
						for f in form_list:
							fullf.append(f.fullform)
						selected_awords[syntax]['fullform'] = fullf[:]

				if not selected_awords[syntax].has_key('fullform'):
					if aword.has_key('fullform') and len(aword['fullform'])>0:
						selected_awords[syntax]['fullform'] = aword['fullform'][:]

		if not selected_awords[syntax].has_key('fullform'):
			if selected_awords[syntax].has_key('word') and selected_awords[syntax].has_key('tag'):
				form_list = Form.objects.filter(word__id=selected_awords[syntax]['word'],
												tag__id=selected_awords[syntax]['tag'])\
										.exclude(dialects__dialect='NG')
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
	
	def set_default_data(self):
		self.default_data = {'language' : 'rus',
							 'syll' : ['2syll'], 'level' : 'all',
							 'case': 'N-ILL', 'pos' : 'N',
							 'vtype' : 'PRS',
							 'adjcase' : 'ATTR',
							 'proncase' : 'N-ILL',
							 'grade' : '',
							 'case_context' : 'N-ILL',
							 'vtype_context' : 'V-PRS',
							 'pron_context' : 'P-ILL',
							 'num_context' : 'NUM-ATTR',
							 'num_level' : '1',
							 'geography': 'south',
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
			if self.translang == 'sma':
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



# #
#
# Leksa Forms
#
# #

class LeksaSettings(OahpaSettings):
	semtype = forms.ChoiceField(initial='HUMAN', choices=SEMTYPE_CHOICES)
	transtype = forms.ChoiceField(choices=TRANS_CHOICES, widget=forms.Select)
	# For placename quizz
	geography = forms.ChoiceField(initial='south', choices=GEOGRAPHY_CHOICES)
	# common = forms.BooleanField(required=False, initial='1')
	# rare = forms.BooleanField(required=False,initial=0)
	# sapmi = forms.BooleanField(required=False, initial='1')
	# world = forms.BooleanField(required=False,initial=0)
	# suopma = forms.BooleanField(required=False,initial=0)
	source = forms.ChoiceField(initial='all', choices=BOOK_CHOICES)
	# level = forms.ChoiceField(initial='all', choices=LEVEL_CHOICES, widget=forms.Select(attrs={'onchange':'javascript:return SetIndex(document.gameform.semtype,this.value);',}))
	
	default_data = {'gametype' : 'bare', 'language' : 'sma', 'dialogue' : 'GG', 
					'syll' : [], 'source': 'all',
					'semtype' : 'HUMAN',
					'geography' : 'south',
					}

	
	# TODO: set default language pair from session language setting.
	def __init__(self, *args, **kwargs):
		if 'initial_transtype' in kwargs:
			initial_transtype = kwargs.pop('initial_transtype')
		else:
			initial_transtype = False

		self.set_settings()
		super(LeksaSettings, self).__init__(*args, **kwargs)

		if initial_transtype:
			self.fields['transtype'].initial = initial_transtype
	

class LeksaQuestion(OahpaQuestion):
	"""
	Questions for word quizz
	"""
	
	def __init__(self, tcomms, stat_pref, preferred, possible, transtype, word, correct, translations, 
				 question, userans_val, correct_val, *args, **kwargs):
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
		
		# TODO: insert infinitives with settings.INFINITIVES
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
	case = forms.ChoiceField(initial='N-ILL', choices=CASE_CHOICES, widget=forms.Select)
	proncase = forms.ChoiceField(initial='N-ILL', choices=CASE_CHOICES_PRONOUN, widget=forms.Select)
	adjcase = forms.ChoiceField(initial='ATTR', choices=ADJEX_CHOICES, widget=forms.Select)
	vtype = forms.ChoiceField(initial='PRS', choices=VTYPE_CHOICES, widget=forms.Select)
	num_bare = forms.ChoiceField(initial='N-ILL', choices=NUM_BARE_CHOICES, widget=forms.Select)
	num_level = forms.ChoiceField(initial='1', choices=NUM_LEVEL_CHOICES, widget=forms.Select)
	num_context = forms.ChoiceField(initial='NUM-ATTR', choices=NUM_CONTEXT_CHOICES, widget=forms.Select)
	case_context = forms.ChoiceField(initial='N-ILL', choices=CASE_CONTEXT_CHOICES, widget=forms.Select)
	adj_context = forms.ChoiceField(initial='ATTR', choices=ADJ_CONTEXT_CHOICES, widget=forms.Select)
	vtype_context = forms.ChoiceField(initial='V-PRS', choices=VTYPE_CONTEXT_CHOICES, widget=forms.Select)
	pron_context = forms.ChoiceField(initial='P-ILL', choices=PRON_CONTEXT_CHOICES, widget=forms.Select)
	# Was BOOK_CHOICES
	book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
	bisyllabic = forms.BooleanField(required=False, initial='1')
	trisyllabic = forms.BooleanField(required=False, initial=0)
	xsyllabic = forms.BooleanField(required=False, initial=0)
	# contracted = forms.BooleanField(required=False, initial=0)
# 	grade = forms.ChoiceField(initial='POS', choices=GRADE_CHOICES, widget=forms.Select)
	
	def __init__(self, *args, **kwargs):
		self.set_settings()
		self.set_default_data()
		super(MorfaSettings, self).__init__(*args, **kwargs)


class MorfaQuestion(OahpaQuestion):
	"""
	Questions for morphology game. 
	"""
	
	def __init__(self, word, tag, baseform, correct, fullforms, present, translations, question, dialect, language, userans_val, correct_val, *args, **kwargs):
		
		lemma_widget = forms.HiddenInput(attrs={'value': word.id})
		tag_widget = forms.HiddenInput(attrs={'value': tag.id})
		self.translang = 'sma'
		kwargs['correct_val'] = correct_val
		super(MorfaQuestion, self).__init__(*args, **kwargs)
		
		# initialize variables
		self.init_variables(possible=[], userans_val=userans_val, accepted_answers=fullforms)
		# init_variables(self, possible, userans_val, accepted_answers, preferred=False):
		
		self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
		self.fields['tag_id'] = forms.CharField(widget=tag_widget, required=False)
		self.lemma = baseform.fullform
		self.wordclass = word.wordclass
		
		# print self.lemma, correct
		# print baseform.tag, correct.tag
		
		# Retrieve feedback information
		self.get_feedback(word=word, tag=tag, wordform=baseform.fullform,
							language=language, dialect=dialect.dialect)
		
		# Take only the first translation for the tooltip
		if len(translations) > 0:
			self.translations = translations[0]
			
		if tag.pos == "N":
			self.case = tag.case

		if tag.pos == 'Pron':
			self.case = tag.case
		
		self.tag = tag.string
		
		if tag.pos=="V" and tag.personnumber and not tag.personnumber == "ConNeg":
			pronbase = self.PronPNBase[tag.personnumber]
			pronoun = pronbase
			self.pron = pronoun
			
			if self.pron and tag.mood == "Imprt":
				self.pron_imp = "(" + self.pron + ")"
				self.pron = ""
		
		self.is_correct("morfa" + "_" + tag.pos, self.lemma + "+" + self.tag)
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
		
		self.correct_ans = present
# #
#
# Numra Forms
#
# #


class NumSettings(OahpaSettings):
	maxnum = forms.ChoiceField(initial='10', choices=NUM_CHOICES, widget=forms.RadioSelect)
	numgame = forms.ChoiceField(initial='string', choices=NUMGAME_CHOICES, widget=forms.RadioSelect)
	numlanguage = forms.ChoiceField(initial='sma', choices=NUMLANGUAGE_CHOICES, widget=forms.RadioSelect)
	default_data = {'language' : 'nob', 'numlanguage' : 'sma', 'dialogue' : 'GG', 'maxnum' : '10', 'numgame': 'string'}
					
	def __init__(self, *args, **kwargs):
		self.set_settings
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
	default_data = {'language' : 'nob', 'numlanguage' : 'sma', 'dialogue' : 'GG', 'gametype' : 'kl1', 'numgame': 'string'}
					
	def __init__(self, *args, **kwargs):
		self.set_settings()
		super(KlokkaSettings, self).__init__(*args, **kwargs)


class KlokkaQuestion(NumQuestion):
	"""
	Questions for numeral quizz
	"""
	game_log_name = "klokka"

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
		
		if gametype == "string":
			self.numstring = num_string
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
	


# #
#
# Dato Forms
#
# #

class DatoSettings(KlokkaSettings):
	gametype = None # Disable gametype (easy, medium, hard)

	default_data = {'language' : 'nob', 'numlanguage' : 'sma', 'numgame': 'string'}

# TODO: Relax answer format if number? Accept other things than DD.MM.?
# DD.MM
# DD/MM


class DatoQuestion(KlokkaQuestion):
	
	game_log_name = "dato"

	def answer_relax(self, answer):
		""" TODO: any need to relax the date?
			
			TODO: perhaps relax MM.DD. to MM.D. if one digit
				  is a zero?
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
	
	def __init__(self, question, qanswer, \
				 qwords, awords, dialect, language, userans_val, correct_val, *args, **kwargs):
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
			self.is_correct("contextual morfa")
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
		if answer_tag_el.pos=="N":
			# For collective numerals, take the presentationform
			if qtype=="COLL-NUM":
				self.lemma = answer_word_el.presentationform
			else:
				if answer_tag_el.number=="Sg" or answer_tag_el.case=="Ess" or qtype=="N-NOM-PL":
					self.lemma = answer_word_el.lemma
				else:
					nplforms = Form.objects.filter(word__pk=answer_word, tag__string='N+Pl+Nom')
					if nplforms.count() > 0:
						self.lemma = nplforms[0].fullform
					else:
						self.lemma = answer_word_el.lemma + " (plural) fix this"
		if answer_tag_el.pos=="A":
			self.lemma=""

		if qtype=="ORD-NUM":
			self.lemma=answer_word_el.presentationform
		# Retrieve feedback information
		self.get_feedback(answer_word_el,answer_tag_el,self.lemma,dialect,language)

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
				self.answertext1=astrings[0]
			if astrings[1]:
				self.answertext2=astrings[1]

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

