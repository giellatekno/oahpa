# -*- coding: utf-8 -*-
from django import forms
from django.db.models import Q
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
import settings

from conf.tools import switch_language_code

from models import *
from smadrill.game import relax
import datetime
import sys

# key-value pairs for pronouns that match up with person
# tags in the analyzer/generator.

PRONOUNS_LIST = {
	'Sg1': 'manne', 
	'Sg2': 'datne', 
	'Sg3': 'dïhte',
	'Pl1': 'mijjieh', 
	'Pl2': 'dijjieh', 
	'Pl3': 'dah',
	'Du1': 'månnoeh', 
	'Du2': 'dåtnoeh', 
	'Du3': 'dah guaktah'
}

##
## Form Choices
##
##    These are all tuples of tuples. The first value is the form
##    key, and the second is a display name. The display name is
##    wrapped in _(), which is a shortcut to ugettext_lazy, the
##    method for translating strings via the internationalization
##    module.

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
	('A-ATTR', _('attributive')), 			# A+Nom+Sg -> A+Attr
 	('A-COMP', _('comparative')),			# A+Attr -> Comp
 	('A-SUPERL', _('superlative')),			# A+Attr -> Super

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

VERB_NUMBER_CHOICES = (
    ('Sg', _('Singular')),
	('Du', _('Dual')),
	('Pl', _('Plural')),
	('all', _('All')),
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

# Keys here must be six characters, and use the 3-character
# language code.

TRANS_CHOICES = (
	('smanob', _('South Sami to Norwegian')),
	('nobsma', _('Norwegian to South Sami')),
#	('smasme', _('South Sami to North Sami')),
#	('smesma', _('North Sami to South Sami')),
	('smaswe', _('South Sami to Swedish')),
	('swesma', _('Swedish to South Sami')),
	('smafin', _('South Sami to Finnish')),
	('finsma', _('Finnish to South Sami')),
#	('smaeng', _('South Sami to English')),
#	('engsma', _('English to South Sami')),
#	('smadeu', _('South Sami to German')),
#	('deusma', _('German to South Sami')),
)

NUMLANGUAGE_CHOICES = (
	('sma', _('South Sami')),
)

SEMTYPE_CHOICES = (
	('HUMAN', _('Human')),
	('RELATIVES', _('Relatives')),
	('WORKERS', _('Professions')),
	('HUMAN_DOING', _('Human doings')),
	('FOOD/DRINK', _('Food/drink')),
	('ANIMAL', _('Animal')),
	('BIRD_FISH', _('Bird/fish')),
	('OBJECT', _('Object')),
	('CONCRETES', _('Concretes')),
	('BODY', _('Body')),
	('CLOTHES', _('Clothes')),
	('BUILDINGS/ROOMS', _('Buildings/rooms')),
	('NATUREWORDS', _('Nature words')),
	('PLANTS', _('Plants')),
	('WEATHERTYPES', _('Weather')),
	('LEISURETIME/AT_HOME', _('Leisuretime/at home')),
	('TRAVEL', _('Traveling')),
	('ABSTRACTS', _('Abstracts')),
	('WORK/ECONOMY/TOOLS', _('Work/economy/tools')),
	('TIMEEXPRESSIONS', _('Timeexpressions')),
	('LITERATURE/TEXT', _('Literature/text')),
	('SCHOOL/EDUCATION', _('School/education')),
	('REINDEER/HERDING', _('Reindeerherding')),
	('TRADITIONAL', _('Traditional')),
	('DUEDTIE', _('Duedtie')),
	# ('PRONOUNS', _('Pronouns')),
	('MULTIWORD', _('Multiword')),
#	('YYY', _('YYY')),
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
	('a1', _(u'Aalkoe')),
	('dej', _(u'Dejpeladtje vætnoeh vuekieh')),
	('s1', _(u'Saemesth amma 1')),
	('s2', _(u'Saemesth amma 2')),
	('s3', _(u'Saemesth amma 3')),
	('s4', _(u'Saemesth amma 4')),
	('åa1', _(u'Åarjel-saemien 1')),
	('åa2', _(u'Åarjel-saemien 2')),
	('åa3', _(u'Åarjel-saemien 3')),
	('åa4', _(u'Åarjel-saemien 4')),
	('åa5', _(u'Åarjel-saemien 5')),
	('åa6', _(u'Åarjel-saemien 6')),
	('all', _(u'All')),
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
	NUM_CONTEXT_CHOICES,
	NUM_LEVEL_CHOICES,
	POS_CHOICES,
	PRON_CONTEXT_CHOICES,
	SEMTYPE_CHOICES,
	TRANS_CHOICES,
	VASTA_LEVELS,
	VERB_CLASSES,
	VTYPE_CHOICES,
	VTYPE_CONTEXT_CHOICES,
]
# #
#
# Form validation
#
# #


import re

from settings import INFINITIVE_SUBTRACT
from settings import INFINITIVE_ADD


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
	""" Apply all setting keys to form object for easy access.
	"""

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
	self.wordclasses = dict(VERB_CLASSES).keys()



def get_feedback(self, word, tag, wordform, language, dialect):
	"""
		#MORFAC, #MORFAS, #MORFAB, #MORFAR

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
		inflectional information from Tag object pertaining to mood, tense,
		personnumber.
		
		FEEDBACK DATA STRUCTURE
		
		Remember that this code runs once per word, and not on a huge set of
		words, so it should ideally be returning only one Feedback object.
		
		Feedback objects are then linked to Feedbackmsg objects, which contain
		message IDs, such as soggi_o, class_1, which then link to Feedbacktext
		objects which contain the corresponding messages in other languages.
		
		Feedback objects should be linked to multiple Feedbackmsg items
		(typically, 3) which individually contain class, syllable and umlaut
		information.
		
		Feedback.messages.all()
		
		CHANGES
		
		Altering the way the code functions should be as simple as adding new
		attributes to the dictionary objects below, and making sure that they
		have access to the variable with the data to be included.
		
				word_attrs = {
					'POS': {
						'soggi' : word.soggi,
					},
				}
		
	"""
	
	# Dictionaries here contain mapping of attributes, and where the data is
	# stored in django objects.
	
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
	
	# Now make POS-specific changes to FILTERS.
	if POS == 'V':

		# stem and wordclass are in complementary distribution, so when one is
		# set the other is not. All 2syll verbs have class information, but all
		# 3syll verbs do not.
		
		# TODO: wordclass
		if FILTERS['stem'] == '3syll':
			FILTERS.pop('wordclass')
		elif FILTERS['stem'] == '2syll':
			FILTERS.pop('stem')
	
	language = switch_language_code(language)
	
	if FILTERS:
		feedbacks = Feedback.objects.filter(**FILTERS)
	
	try:
		baseform = wordform.getBaseform()
	except:
		baseform = word
	
	message_list = []
	if feedbacks:
		for f in feedbacks:
			msgs = f.messages.all()
			for m in msgs:
				messages = m.feedbacktext_set.filter(language=language)
				if messages.count() > 0:
					text = messages[0].message
					text = text.replace('WORDFORM', '"%s"' % baseform.lemma)
					message_list.append(text)
	
	self.feedback = ' \n '.join(message_list)
	

def select_words(self, qwords, awords):
	"""
		#MORFAC, #MORFAR

		Fetch words and tags from the database.
		
		This function is kind of messy, so anyone willing to clean it up more
		should definitely do so. 

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
							).exclude(dialects__dialect='NG')

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
							 'syll' : ['2syll'], 
							 'bisyllabic': True,
							 'trisyllabic': False,
							 'xsyllabic': False,
							 'wordclass': ['I', 'II', 'III',],
							 'level' : 'all',
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
							 'source' : 'all',
							 'singular_only_noun' : False,  # Morfa-S noun
							 }



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
		# if self.user:
		# 	log_kwargs['username'] = self.user.username
		log_kwargs = {
			'userinput': self.answer,
			'correct': ','.join(self.correct_anslist),
			'iscorrect': self.iscorrect,
			'example': self.example,
			'game': self.game,
			'date': today,
		}
		if self.user_country:
			log_kwargs['user_country'] = self.user_country
		
		log, c = Log.objects.get_or_create(**log_kwargs)
	
	def __init__(self, *args, **kwargs):
		correct_val = False
		if 'correct_val' in kwargs:
			correct_val = kwargs.get('correct_val')
			kwargs.pop('correct_val')
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
			if self.translang == 'sma':
				# Relax spellings.
				accepted_answers = [force_unicode(item) for item in accepted_answers]
				forms = sum([relax(force_unicode(item)) for item in accepted_answers], [])
				# need to subtract legal answers and make an only relaxed list.
				relaxings = [item for item in forms if force_unicode(item) not in accepted_answers]
			else:

				# add infinitives as possible answers
				if self.word.pos == 'V':
					if self.translang in INFINITIVE_SUBTRACT and INFINITIVE_ADD:
						infin_s = INFINITIVE_SUBTRACT[self.translang]
						infin_a = INFINITIVE_ADD[self.translang]

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
	source = forms.ChoiceField(initial='all', choices=BOOK_CHOICES)
	default_data = {
		'gametype': 'bare', 
		'language': 'sma', 
		'dialogue': 'GG', 
		'syll': [], 
		'source': 'all',
		'semtype': 'HUMAN',
		'geography': 'south',
	}
	
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
	
	def __init__(self, tcomms, stat_pref, preferred, possible, transtype, word,
		correct, translations, question, userans_val, correct_val, *args,
		**kwargs):

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
			if word.language in INFINITIVE_SUBTRACT and INFINITIVE_ADD:
				infin_s = INFINITIVE_SUBTRACT[word.language]
				infin_a = INFINITIVE_ADD[word.language]

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

		# Displayed answer also needs infinitive marking, which needs to happen
		# last because of stat_pref. Infinitive regular expressions come from
		# settings.py.

		if word.pos.upper() == 'V':
			if self.translang in INFINITIVE_SUBTRACT and INFINITIVE_ADD:
				infin_s = INFINITIVE_SUBTRACT[self.translang]
				infin_a = INFINITIVE_ADD[self.translang]
		
				lemma = re.compile(infin_s)

				apply_inf = lambda x: lemma.sub(infin_a, force_unicode(x))
				
				self.correct_ans = map(apply_inf, self.correct_ans)
				self.correct_ans = map(force_unicode, self.correct_ans)
		
	


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

	book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
	singular_only_noun = forms.BooleanField(required=False, initial=False)
	verb_number = forms.ChoiceField(initial='all', choices=VERB_NUMBER_CHOICES, widget=forms.Select)
	bisyllabic = forms.BooleanField(required=False, initial=True)
	trisyllabic = forms.BooleanField(required=False, initial=False)
	xsyllabic = forms.BooleanField(required=False, initial=False)

	wordclass_i = forms.BooleanField(required=False, initial=False, label=_('I'))
	wordclass_ii = forms.BooleanField(required=False, initial=False, label=_('II'))
	wordclass_iii = forms.BooleanField(required=False, initial=False, label=_('III'))
	wordclass_iv = forms.BooleanField(required=False, initial=False, label=_('IV'))
	wordclass_v = forms.BooleanField(required=False, initial=False, label=_('V'))
	wordclass_vi = forms.BooleanField(required=False, initial=False, label=_('VI'))
	wordclass_odd = forms.BooleanField(required=False, initial=False, label=_('Odd'))

    # Practiclaly using this widget would be easier, but it doesn't seem
    # to work as specified, and is a lot of work to debug.

	# wordclass = forms.MultipleChoiceField(
	# 	widget=forms.widgets.CheckboxSelectMultiple,
	# 	choices=VERB_CLASSES,
	# )
	
	def __init__(self, *args, **kwargs):
		self.set_settings()
		self.set_default_data()
		super(MorfaSettings, self).__init__(*args, **kwargs)
		self.wordclass_names = [
			('wordclass_i', 'I'),
			('wordclass_ii', 'II'),
			('wordclass_iii', 'III'),
			('wordclass_iv', 'IV'),
			('wordclass_v', 'V'),
			('wordclass_vi', 'VI'),
			('wordclass_odd', 'Odd'),
		]


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
	""" Subclass here only adds form fields, but otherwise does not alter
	functionality of methods.
	"""

	maxnum = forms.ChoiceField(initial='10', choices=NUM_CHOICES, widget=forms.RadioSelect)
	numgame = forms.ChoiceField(initial='string', choices=NUMGAME_CHOICES, widget=forms.RadioSelect)
	numlanguage = forms.ChoiceField(initial='sma', choices=NUMLANGUAGE_CHOICES, widget=forms.RadioSelect)

	default_data = {
		'language': 'nob',
		'numlanguage': 'sma',
		'dialogue': 'GG',
		'maxnum': '10',
		'numgame': 'string'
	}
					
	def __init__(self, *args, **kwargs):
		self.set_settings
		super(NumSettings, self).__init__(*args, **kwargs)


class NumQuestion(OahpaQuestion):
	""" Questions for numeral quiz, must override OahpaQuestion.is_correct,
	because this deals with numbers, not words, also __init__.
	"""
	game_log_name = 'numra'

	def answer_relax(self, answer):
		""" Method for relaxing answers. Override if needed, method here is
		empty just so that the code in child classes can be more general.
		"""

		return answer

	def is_correct(self, game, example=None):
		""" Check if answer is correct, and also log the user response.
		"""
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
		""" Set up default variables, and create relaxed answers, also check
		if answer is correct or not, and apply Form correct variable.
		"""
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
	default_data = {
		'language': 'nob',
		'numlanguage': 'sma',
		'dialogue': 'GG',
		'gametype': 'kl1',
		'numgame': 'string'
	}
					
	def __init__(self, *args, **kwargs):
		self.set_settings()
		super(KlokkaSettings, self).__init__(*args, **kwargs)


class KlokkaQuestion(NumQuestion):
	"""
	Questions for numeral quizz
	"""
	game_log_name = "klokka"

	def __init__(self, *args, **kwargs):
		""" Set variables, check correctness, and log output.
		"""

		# Evaluate args and kwargs
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

		# Set default values
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
	""" Very simple class, basically the same as KlokkaSettings, minus the default
	data.
	"""
	gametype = None # Disable gametype (easy, medium, hard)

	default_data = {
		'language': 'nob',
		'numlanguage': 'sma',
		'numgame': 'string'
	}


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
		word = answer_word_el
		tag = answer_tag_el
		baseform = word.form_set.filter(tag=tag)[0].getBaseform()
		self.get_feedback(word=word, tag=tag, wordform=baseform.fullform,
							language=language, dialect=dialect)

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

