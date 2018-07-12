# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.db.models import Q, Count
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from django.http import HttpResponse, Http404

from django import forms
from django.forms.models import formset_factory

from models import Translations2, Word, Tag, Form

from courses.models import UserGrade

# comment this out
# DEBUG = open('/dev/ttys001', 'w')

# Some general notes
# 
# TODO: all of the lists and tuples of tuples which are used for conf
#		iguration take up a lot of space, and should be moved elsewhere.


# TODO: MorfaNum, MorfaAdj

# TODO: improve docstrings http://www.learningpython.com/2010/01/08/introducing-docstrings/



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


	# # #
	# # 
	# #   Forms (move these elsewhere later)
	# #
	# # #


ISO = {
	"fi": "fin",
	"ru": "rus",
	"en": "eng",
	"no": "nob",
	"de": "deu",
	"sma": "sma",
}

def switch_language_code(CODE):
	"""
		Switches language codes from ISO 639-1 to ISO 639-2.
		
		>>> switch_language_code("no")
		"nob"
		
	"""
	try:
		return ISO[CODE]
	except:
		# logger.warning("*** Unidentified language code %s." % CODE)
		print >> sys.stdout, "*** Unidentified language code %s." % CODE
		return settings.LANGUAGE_CODE


	# #
	# 
	#  Settings form classes
	#
	# #


class GameSettings(forms.Form):
	""" Provides some generalized methods to MorfaSettings and LeksaSettings.

		General idea is that the game will call one of the following:
				MorfaS, MorfaV, MorfaAdj, MorfaNum
				LeksaSettings

		MorfaSettings is broken up into subclasses in order to keep things
		easier to debug.

		MorfaSettings has several methods, but no form fields. Form fields
		are on the subforms.

		GameSettings.__init__()
			GameSettings.set_defaults()
				MorfaSettings
					MorfaS
						makeQuery
					getInitialData
		
		Returns initial data to the views, which produce a formset of 5
		Question classes. Question classes are populated by the formset
		using data from MorfaSettings.getInitialData.
	"""
	question_count = 5

	def __init__(self, *args, **kwargs):
		super(GameSettings, self).__init__(*args, **kwargs)
		self.set_defaults()

	def clean(self):
		cleaned_data = self.cleaned_data
		self.makeQuery()
		return cleaned_data
	
	def set_defaults(self):
		""" Set default options on form (in event that it hasn't been requested 
			yet.
		"""
		self.initial_data = dict([(name, unicode(field.initial)) 
									for name, field in self.fields.items()])
		self.makeQuery()
		return


class MorfaSettings(GameSettings):
	""" Morfa settings form.

		The idea here is to subclass this for the varying Morfa games.
		Subclasses, MorfaV, MorfaS, etc., should have fields for forms, and
		the following methods.

			.makeQuery() - constructs Q() & Q() type queries to filter
						   words and tags.
						   must set self.query
						   optionally self.tag_query

		MorfaSettings then produces the initial data for formsets based
		on this query.

	"""
	
	CASE_CONTEXT_CHOICES = (
		('N-NOM-PL', _('plural')),
		('N-ACC', _('accusative')),
		('N-ILL', _('illative')),
		('N-INE', _('inessive')),
		('N-ELA', _('elative')),
		('N-COM', _('comitative')),
		('N-ESS', _('essive')),
	)

	ADJCASE_CHOICES = (
		('NOMPL', _('plural')),
		('ATTR', _('attributive')),
		('N-ACC', _('accusative')),
		('N-ILL', _('illative')),
		('N-INE', _('inessive')),
		('N-ELA', _('elative')),
		('N-COM', _('comitative')),
		('N-GEN', _('genitive')),
		('N-ESS', _('essive')),
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
		('N-INE', _('inessive')),
		('N-ELA', _('elative')),
		('N-COM', _('comitative')),
	)
	
	NUM_LEVEL_CHOICES = (
		('1', _('First level')),
		('2', _('Second level')),
	)


	select = {'widget': forms.Select}

	def makeQuery(self):
		""" This produces the query objects necessary to fetch and prepare words
			in self.getInitialData.

			For Morfa, this should set two attributes, self.query, and self.tag_query.
			MorfaSettings returns nothing, but this is just here for documentation.
		"""

		# TAG_QUERY = Q(pos=pos) & Q(possessive="") & \
					# Q(case=case) & Q(tense=tense) & Q(mood=mood) & \
					# ~Q(personnumber="ConNeg") & Q(attributive=attributive) & \
					# Q(grade=grade) & Q(number__in=number)

		# self.tag_query = TAG_QUERY
		# self.query = QUERY
		return
	
	
	def getInitialData(self):
		""" This works off of self.query and self.tag_query produced by
			subclassed objects makeQuery().
		"""

		tags = Tag.objects.filter(self.tag_query)
		
		if tags.count() < 1:
			# TODO: change 404
			error = "Morfa.get_db_info: Database is improperly loaded.\
					 No tags for the query were found.\n\n"
			raise Tag.DoesNotExist(error)
		
		tag = tags.order_by('?')[0]
		# TODO: max number here should come from global setting
		random_forms = Form.objects.filter(tag__in=tags).order_by('?')[0:5]
		
		inits = []
		for form in random_forms:
			try:
				lemma = form.getBaseform(match_num=True).fullform
			except Form.DoesNotExist:
				lemma = form.word.lemma

			app = {'id': form.word.id,
					'lemma': lemma, # form.word.lemma,
					'translations': [form.fullform]}
			
			inits.append(app)

		return inits


class MorfaS(MorfaSettings):
	""" Morfa for substantive/nouns
		Fields for case, syllables and book.
	"""
	POS = "N"
	select = {'widget': forms.Select}

	casetable = {
		'NOMPL' : 'Nom', 
		'ATTR': 'Attr', 
		'N-ILL': 'Ill', 
		'N-ESS': 'Ess', 
		'N-GEN': 'Gen',
		'N-INE': 'Ine', 
		'N-ELA': 'Ela',
		'N-ACC': 'Acc', 
		'N-COM': 'Com',
		'': ''
	}

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
	
	case = forms.ChoiceField(initial='N-ILL', choices=CASE_CHOICES, **select)
	book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, **select) 
	bisyllabic = forms.BooleanField(required=False, initial=True)
	trisyllabic = forms.BooleanField(required=False,initial=False)
	xsyllabic = forms.BooleanField(required=False,initial=False)

	def makeQuery(self):
		""" Produces the query for nouns, setting self.query and self.tag_query
			for use by self.getInitialData.
		"""
		if self.is_valid():
			options = self.cleaned_data
		else:
			options = self.initial_data
		
		_POS = Q(pos=self.POS)
		_POSS = Q(possessive="")

		syll = ''
		if 'bisyllabic' in options:
			syll = 'bisyllabic'
		elif 'trisyllabic' in options:
			syll = 'trisyllabic'
		elif 'xsyllabic' in options:
			syll = 'xsyllabic'

		_SYLL = Q(stem__in=syll)
		
		if 'book' in options:
			book = options['book']
		else:
			book = ''
		
		_SOURCE = Q(source__name=book)

		if 'case' in options:
			case = self.casetable[options['case']]
		_CASE = Q(case=case)

		numbers = ["Sg", "Pl", ""]
		if case == "Nom": numbers = ["Pl"]
		_NUMBER = Q(number__in=numbers)

		TAG_QUERY = _POS & _POSS & _CASE & _NUMBER
		QUERY = _POS & _SYLL

		if book and book not in ['all', 'All', '']:
			QUERY = QUERY & _SOURCE
		
		self.query = QUERY
		self.tag_query = TAG_QUERY


class MorfaV(MorfaSettings):
	""" Settings object for Morfa Verbs.

		TODO: insert pronouns?
		TODO: COND, IMPRT, POT don't work
	"""
	POS = 'V'
	select = {'widget': forms.Select}
	
	VTYPE_CHOICES = (
		('PRS', _('present')),
		('PRT', _('past')),
		('COND', _('conditional')),
		('IMPRT', _('imperative')),
		('POT', _('potential')),
	)
	
	VTYPE_CONTEXT_CHOICES = (
		('PRS', _('present')),
		('PRT', _('past')),
		('V-COND', _('conditional')),
		('V-IMPRT', _('imperative')),
		('V-POT', _('potential')),
	)
	
	POS_MOOD_TENSE = {
		"PRS":	("Ind", "Prs"),
		"PRT":	("Ind", "Prt"),
		"COND":   ("Cond", "Prs"), # TODO: query not working
		"IMPRT":  ("Imprt", "Prs"), # TODO: query not working
		"POT":	("Pot", "Prs") # TODO: query not working
	}
	
	vtype = forms.ChoiceField(initial='PRS', choices=VTYPE_CHOICES, **select)
	book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, **select) 
	bisyllabic = forms.BooleanField(required=False, initial=True)
	trisyllabic = forms.BooleanField(required=False,initial=False)

	def makeQuery(self):
		if self.is_valid():
			options = self.cleaned_data
		else:
			options = self.initial_data
		
		_POS = Q(pos=self.POS)
		
		syll = ''
		if 'bisyllabic' in options:
			syll = 'bisyllabic'
		elif 'trisyllabic' in options:
			syll = 'trisyllabic'
		elif 'contracted' in options:
			syll = 'contracted'
		
		_SYLL = Q(stem__in=syll)
		
		if 'book' in options:
			book = options['book']
		else:
			book = ''
		
		_SOURCE = Q(source__name=book)

		if 'vtype' in options:
			mood, tense = self.POS_MOOD_TENSE[options['vtype']]
		_MOOD, _TENSE = Q(mood=mood), Q(tense=tense)

		TAG_QUERY = _POS & _MOOD & _TENSE & ~Q(personnumber="ConNeg")
		QUERY = _POS & _SYLL

		if book and book not in ['all', 'All', '']:
			QUERY = QUERY & _SOURCE
		
		self.query = QUERY
		self.tag_query = TAG_QUERY


class MorfaNum(MorfaSettings):
	""" Placeholder for stuff for MorfaNum
	"""
	POS = 'Num'
	# num_bare = forms.ChoiceField(initial='N-ILL', choices=NUM_BARE_CHOICES, **select) 
	# num_level = forms.ChoiceField(initial='1', choices=NUM_LEVEL_CHOICES, **select) 
	# num_context = forms.ChoiceField(initial='NUM-ATTR', choices=NUM_CONTEXT_CHOICES, **select) 

	def makeQuery(self):
		num_bare = options['num_bare']
		num_level = options['num_level']
		
		if self.is_valid():
			options = self.cleaned_data
		else:
			options = self.initial_data
		
		_POS = Q(pos=self.POS)

		if options.has_key('num_level') and str(options['num_level']) == "1":
			smallnum = ["1","2","3","4","5","6","7","8","9","10"]
			QUERY = Q(pos__iexact=pos) & Q(presentationform__in=smallnum)
		else:
			QUERY = Q(pos__iexact=pos)
		return
	


class MorfaAdj(MorfaSettings):
	""" Stuff for MorfaAdj
	"""
	POS = 'Adj'
	select = {'widget': forms.Select}
	# adjcase = forms.ChoiceField(initial='ATTR', choices=ADJCASE_CHOICES, **select)
	# adj_context = forms.ChoiceField(initial='ATTR', choices=ADJ_CONTEXT_CHOICES,  **select)
	# grade = forms.ChoiceField(initial='POS', choices=GRADE_CHOICES,  **select)

	def makeQuery(self):
		if case == "Attr":
			attributive = "Attr"
			case = ""
		
		if grade == "POS":	 grade = ""
		if grade == "COMP":	grade = "Comp"
		if grade == "SUPERL":  grade = "Superl"

	

class LeksaSettings(GameSettings):
	""" Leksa settings form.
	
		TODO: Method to set session data according to settings.
	
	"""

	# Form options, leaving some out for easy devel.
	SEMTYPE_CHOICES = (
		('FAMILY', _('family')),
		('FOOD/DRINK', _('Food/drink')),
		('ANIMAL', _('Animal')),
		('OBJECT', _('Object')),
		('CONCRETES', _('Concretes')),
		('BODY', _('Body')),
		('CLOTHES', _('Clothes')),
		('BUILDINGS/ROOMS', _('Buildings/rooms')),
		('NATUREWORDS', _('Nature words')),
		('LEISURETIME/AT_HOME', _('Leisuretime/at home')),
		('PLACES', _('Places')),
		('ABSTRACTS', _('Abstracts')),
		('WORK/ECONOMY/TOOLS', _('Work/economy/tools')),
		('TIMEEXPRESSIONS', _('Timeexpressions')),
		('LITERATURE/TEXT', _('Literature/text')),
		('SCHOOL/EDUCATION', _('School/education')),
		('REINDEER/HERDING', _('Reindeerherding')),
		('TRADITIONAL', _('Traditional')),
		('all', _('all')),
	)
	
	TRANS_CHOICES = (
		('smanob', _('South Sami to Norwegian')),
		('nobsma', _('Norwegian to South Sami')), 
	)
	
	select = {'widget': forms.Select}
	
	semtype = forms.ChoiceField(label=_('Set'),
									initial='FAMILY',
									choices=SEMTYPE_CHOICES,
									**select)
	
	transtype = forms.ChoiceField(label=_('Language pair'),
									initial='smanob',
									choices=TRANS_CHOICES, 
									**select)
	
	def makeQuery(self):
		if self.is_valid():
			options = self.cleaned_data
		else:
			options = self.initial_data
		
		if options['semtype'] == 'all':
			QUERY = Q()
		else:
			QUERY = Q(semtype__semtype=options['semtype'])
		
		self.query = QUERY
		return True
	
	def getInitialData(self):
		""" Get initial data to populate formsets.
		"""
		if self.is_valid():
			options = self.cleaned_data
		else:
			options = self.initial_data

		answer_language = options['transtype'][-3::]
		question_language = options['transtype'][0:3]
		
		if answer_language == 'sma':
			transl = Translations2(question_language)
		else:
			transl = Translations2(answer_language)

		initialwords = Word.objects.annotate(num_trans=Count(transl))\
						.filter(num_trans__gt=0)

		initialwords = initialwords.filter(self.query)\
						.order_by('?')[0:self.question_count]
		
		if answer_language == 'sma':
			inits = []
			for word in initialwords:
				translations = word.translations2(question_language).all()[0]
				app = {'id': word.id,
						'lemma': translations.definition,
						'translations': [word.lemma]}
				inits.append(app)
		else:
			inits = []
			for word in initialwords:
				xls = word.translations2(answer_language).all()
				translations = [x.definition for x in xls if x.definition.strip()]
				app = {'id': word.id,
						'lemma': word.lemma,
						'translations': translations}
				inits.append(app)
		return inits


# TODO: make custom validators/fields? re django.core.validators
# http://docs.djangoproject.com/en/dev/ref/forms/validation/

	# #
	# 
	#  Question classes
	#
	# #

class Question(forms.Form):
	""" Question meta-class. Some methods will be moved in here which end up 
		being common across question-types.

		For now this Question class works mostly unadulterated on LeksaQuestion
		and MorfaQuestion.

		Question.__init__()

		Validation process:
			Follows Django documentation, with custom versions of following:
				clean_answers
				clean
			Additional customization is in LeksaQuestion/MorfaQuestions' 
			check_answer methods.
			
			When the form is validated, it runs clean_answers, and then
			clean. The clean method then calls check_answer() which
			does the actual answer checking, producing validation errors.
	
	"""
	# Shortcut
	hide = {'widget': forms.HiddenInput()}
	
	# Set up fields
	lemma = forms.CharField(max_length=50, **hide)
	userans = forms.CharField(max_length=50, required=False)
	word_id = forms.IntegerField(**hide)
	correct = forms.NullBooleanField(required=False, **hide)
	answers = forms.CharField(max_length=250, required=False, **hide)

	class Errors:
		""" Global question error responses.
		"""
		try_again = _(u'Try again!')
		empty_answers = _(u'No possible answers.')
		blank_user_answer = _(u'No answer given.')
	
	def __init__(self, *args, **kwargs):
		# Make compatible with old form names
		if kwargs.has_key('initial'):
			kwargs['initial']['word_id'] = kwargs['initial']['id']
			kwargs['initial']['answers'] = ', '.join(kwargs['initial']['translations'])
			
			# Keep the lemma available in templates.
			self.lemma_value = kwargs['initial']['lemma']
				
		super(Question, self).__init__(*args, **kwargs)
	
	def clean_answers(self):
		""" This method cleans answers from database, and will run before .clean()
		
			Here we try to cut off limits in Leksa entries, e.g.:
				tremenninger (innbyrdes) -> tremenninger

			For Morfa, this isn't necessary, as MorfaSettings.getInitialData 
			supplies only lemmas matching tags: ['girjjis']
		"""
		
		answers = self.cleaned_data.get("answers").split(', ')
		answers = [a.strip() for a in answers if a.strip()]
		
		# Remove parentheticals
		answers = [a.partition('(')[0].strip() for a in answers]
		
		if len(answers) == 0:
			raise forms.ValidationError(self.Errors.empty_answers)
		
		return answers

	def clean(self):
		""" Prepare form data and raise validation errors. Validation errors 
			are raised if the user provides a wrong answer.
			
			Leksa and Morfa are essentially the same, since .GetInitialData()
			supplies the correct answers.
			
			This method depends on results from .clean_answers(), which runs
			first.			
		"""
		cleaned_data = self.cleaned_data
		
		user_answer = cleaned_data.get("userans")
		answers = cleaned_data.get("answers")
				
		# Making sure that the lemma and answers always show up in the form.
		self.lemma_value = cleaned_data['lemma']
		try:
			self.answer_list = ', '.join(answers)
		except TypeError:
			print answers
			if type(answers) != list:
				raise Http404('Answers missing from one of the questions...?')
		self.answer_list_as_list = answers

		# Always return cleaned data.
		self.check_answer()
		return cleaned_data
	

class MorfaQuestion(Question):
	""" Creates a Morfa question. Most of the functionality here is in parent
		classes, except for answer validation (check_answer).
		
	"""
	
	def check_answer(self):
		""" Gets analyses based on forms supplied and settingsform and compares
			to user input

			TODO: make validator
		
			This question should be used in a Formset.
		"""
		
		answers = self.cleaned_data.get("answers")
		user_answer = self.cleaned_data.get("userans")
		if answers:
			if user_answer not in answers:
				self._errors["userans"] = self.Errors.try_again
				self.correct = False
			else:
				self.correct = True
		else:
			self._errors = self.Errors.empty_answers

		if not user_answer:
			self._errors["userans"] = self.Errors.blank_user_answer

		return
	

class LeksaQuestion(Question):
	""" This is the Leksa question class. It produces only one question,
		and has methods to validate whether this question is correct or not.
		
		Incorrect answers throw validation errors and provide a reason as the
		error message.
		
		This question should be used in a Formset.

		Most of the functionality is in the Question parent class, except for 
		check_anwer.
	
	"""
	
	def check_answer(self):
		""" Check answers.
		
			TODO: Turn this into a validator.
		
		"""
		answers = self.cleaned_data.get("answers")
		user_answer = self.cleaned_data.get("userans")
		
		if answers:
			if user_answer not in answers:
				self._errors["userans"] = self.Errors.try_again
				self.correct = False
			else:
				self.correct = True
		else:
			self._errors = self.Errors.empty_answers
		
		if not user_answer:
			self._errors["userans"] = self.Errors.blank_user_answer
		
		return
	

	# # #
	# # 
	# #   Views
	# #
	# # #

def Game(request, gametype, question_count=5):
	""" This view renders the forms and handles form post data. Forms are
		validated, but invalid forms do not provide a difference in behavior.
	"""

	settings_objects = {'MORFAS': (MorfaS, MorfaQuestion, 'New Morfa'),
						'MORFAV': (MorfaV, MorfaQuestion, 'New Morfa'),
						'LEKSA': (LeksaSettings, LeksaQuestion, 'New Leksa')}
	
	GameSettings, GameQuestion, GameName = settings_objects[gametype]

	target_language = switch_language_code(request.LANGUAGE_CODE)
	target_language = 'nob'

	if len(request.GET.keys()) > 0:
		settings = GameSettings(request.GET) 
	else:
		settings = GameSettings() 
	
	if settings.is_valid():
		options = settings.cleaned_data
	else:
		options = settings.initial_data
	
	# target_language = options['transtype'][-3::] 
	
	QuestionSet = formset_factory(GameQuestion, extra=0) 

	score = False
	show_correct = False

	if request.method == 'POST':
		formset = QuestionSet(request.POST, request.FILES)

		if formset.is_valid():
			pass

		score = sum([1 for f in formset.forms if f.correct == True])

		if formset.data.get('show_correct'):
			show_correct = True
		elif formset.data.get('test'):
			show_correct = False
	else:
		show_correct = False
		initial_data = settings.getInitialData()
		formset = QuestionSet(initial=initial_data)
	
	if score == len(formset.forms):
		all_correct = True
	else:
		all_correct = False
	
	context = RequestContext(request, {
		'formset': formset,
		'show_correct': show_correct,
		'count': len(formset.forms),
		'score': score,
		'language' :  target_language,
		'settings_form': settings,
		'all_correct': all_correct,
	})


	if context['show_correct']:
		if request.user.is_authenticated:
			points = context['score']
			total = context['count']
			new_grade = UserGrade.objects.create(user=request.user.get_profile(),
												game=GameName, 
												score=points,
												total=total)
	
	return render_to_response('new_form.html', context, 
								context_instance=RequestContext(request))


