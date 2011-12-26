from django.template import Context, RequestContext, loader
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from django.utils.translation import ugettext as _

from univ_oahpa.conf.tools import switch_language_code

from random import randint

from game import *
from forms import *
from qagame import *

# comment this out
# DEBUG = open('/dev/ttys001', 'w')

from univ_oahpa.courses.views import trackGrade

class Gameview:
	def init_settings(self):

		show_data=0
		self.settings = {}

		self.gamenames = {
			'ATTR' :  _('Practise attributes'),
			'A-ATTR' :  _('Practise attributes'),
			'A-COMP' :  _('Practise comparative'),
			'A-SUPERL' :  _('Practise superlative'),
			'ATTRPOS' :  _('Practise attributes in positive'),
			'ATTRCOMP' :  _('Practise attributes in comparative'),
			'ATTRSUP' :  _('Practise attributes in superlative'),
			'PREDPOS' :  _('Practise predicative in positive'),
			'PREDCOMP' :  _('Practise predicative in comparative'),
			'PREDSUP' :  _('Practise predicative in superlative'),
			'NUM-ATTR' :  _('Practise numeral attributes'),
			'NOMPL' :  _('Practise plural'),
			'NOM' :  _('Practise nominative'),
			'N-NOM' :  _('Practise nominative'),
			'N-ILL' :  _('Practise illative'),
			'N-ACC' :  _('Practise accusative'),
			'N-COM' :  _('Practise comitative'),
			'N-ESS' :  _('Practise essive'),
			'N-GEN' :  _('Practise genitive'),
			'N-NOM-PL' :  _('Practise plural'),
			'N-LOC' :  _('Practise locative'),
			'N-MIX' :  _('Practise a mix'),
			'V-MIX' :  _('Practise a mix'),
			'A-MIX' :  _('Practise a mix'),
			'P-MIX' :  _('Practise a mix'),
			'NUM-ILL' :  _('Practise numerals in illative'),
			'NUM-ACC' :  _('Practise numerals in accusative'),
			'NUM-COM' :  _('Practise numerals in comitative'),
			'NUM-ESS' :  _('Practise numerals in essive'),
			'NUM-GEN' :  _('Practise numerals in genitive'),
			'NUM-NOM-PL' :  _('Practise numerals in plural'),
			'NUM-LOC' :  _('Practise numerals in locative'),
			'COLL-NUM' :  _('Practise collective numerals'),
			'ORD-NUM' :  _('Practise ordinal numbers'),
			'PRS'   :  _('Practise present'),
			'PRT'   : _('Practise past'),
			'PRF'   : _('Practise perfect'),
			'GER'   : _('Practise gerund'),
			'COND'  : _('Practise conditional'),
			'IMPRT' : _('Practise imperative'),
			'POT'   : _('Practise potential'),
			'V-PRS'   :  _('Practise present'),
			'V-PRT'   : _('Practise past'),
			'V-PRF'   : _('Practise perfect'),
			'V-GER'   : _('Practise gerund'),
			# 'V-COND'  : _('Practise conditional'),
			'V-IMPRT' : _('Practise imperative'),
			'V-POT'   : _('Practise potential'),
			'P-ACC'  : _('Practise accusative'),
			'P-COM'  : _('Practise comitative'),
			'P-LOC'  : _('Practise locative'),
			'P-GEN'  : _('Practise genitive'),
			'P-NOM'  : _('Practise nominative'),
			'P-ILL'  : _('Practise illative'),
		}


	def syll_settings(self,settings_form):
		self.settings['syll'] = []
		if 'bisyllabic' in settings_form.data:
			self.settings['syll'].append('2syll')
		if 'trisyllabic' in settings_form.data:
			self.settings['syll'].append('3syll')
		if 'contracted' in settings_form.data:
			self.settings['syll'].append('Csyll')
		if 'xsyllabic' in settings_form.data:
			self.settings['syll'].append('xsyll')
		if len(self.settings['syll']) == 0:
			self.settings['syll'].append('2syll')


	def create_morfagame(self, request):
		count, correct = 0, 0
		settings_form = MorfaSettings(request.GET)

		if request.method == 'GET' and len(settings_form.data.keys()) > 0:
			post_like_data = request.GET.copy()
			if not 'book' in post_like_data:
				post_like_data['book'] = 'all'
		else:
			post_like_data = False
		# So can I get GET data to make changes to form, but I can't get
		# it to load the game with this data.
		# reason is logic is forked into POST/GET, not POST & has game
		# data

		if request.method == 'POST' or post_like_data:
			if post_like_data:
				data = post_like_data
			else:
				data = request.POST.copy()

			# Settings form is checked and handled.
			settings_form = MorfaSettings(data)

			for k in settings_form.data.keys():
				self.settings[k] = settings_form.data[k]

			if request.session.has_key('dialect'):
				self.settings['dialect'] = request.session['dialect']

			if hasattr(request, 'LANGUAGE_CODE'):
				self.settings['language'] = request.LANGUAGE_CODE

			self.syll_settings(settings_form)
			if settings_form.data.has_key('source'):
				formsource = settings_form.data['source']
				self.settings['source'] = settings_form.source[formsource]

			self.settings['allcase'] = settings_form.allcase

			# Create game
			if self.settings['gametype'] == "bare":
				game = BareGame(self.settings)
			else:
				# Contextual morfa
				game = QAGame(self.settings)
				game.init_tags()

			# If settings are changed, a new game is created
			# Otherwise the game is created using the user input.

			if "settings" in data or post_like_data:
				game.new_game()
			else:
				game.check_game(data)
				game.get_score(data)

			if 'test' in data:
				game.count = 1
			if "show_correct" in data:
				show_correct = 1

		# If there is no POST data, default settings are applied
		else:
			settings_form = MorfaSettings()

			# Find out the default data for this form.
			for k in settings_form.default_data.keys():
				if not self.settings.has_key(k):
					self.settings[k] = settings_form.default_data[k]

			if self.settings['pos'] != 'Pron':
				self.settings['source'] = settings_form.default_data['source']

			if request.session.has_key('dialect'):
				self.settings['dialect'] = request.session['dialect']

			if hasattr(request, 'LANGUAGE_CODE'):
				self.settings['language'] = request.LANGUAGE_CODE

			if self.settings['gametype'] == "bare":
				game = BareGame(self.settings)
			else:
				# Contextual morfa
				game = QAGame(self.settings)
				game.init_tags()
			game.new_game()

		if self.settings['pos'] == "N":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['case']
			else:
				gamename_key = self.settings['case_context']
		if self.settings['pos'] == "Pron":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['proncase']
			else:
				gamename_key = self.settings['pron_context']
		if self.settings['pos'] == "Num":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['num_bare']
			else:
				gamename_key = self.settings['num_context']
		if self.settings['pos'] == "V":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['vtype']
			else:
				gamename_key = self.settings['vtype_context']
		if self.settings['pos'] == "A":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['adjcase']
			else:
				gamename_key = self.settings['adj_context']

		self.settings['gamename'] = self.gamenames[gamename_key]

		c = RequestContext(request, {
			'settingsform': settings_form,
			'settings' : self.settings,
			'forms': game.form_list,
			'count': game.count,
			'score': game.score,
			'comment': game.comment,
			'all_correct': game.all_correct,
			'show_correct': game.show_correct,
			'language' : self.settings['language'],
			})
		return c


def univ_oahpa(request):
	c = RequestContext(request, {
		'jee': "joku arvo",
		})
	return render_to_response('univ_oahpa_main.html', c,
				context_instance=RequestContext(request))

def updating(request):
	c = RequestContext(request, {
		'jee': "joku arvo",
		})
	return render_to_response('updating.html', c,
				context_instance=RequestContext(request))

class Quizzview(Gameview):
	def placename_settings(self, settings_form):

		self.settings['frequency'] = []
		self.settings['geography'] = []

		if 'frequency' in settings_form.data:
			self.settings['frequency'] = settings_form.data['frequency']
		if 'geography' in settings_form.data:
			self.settings['geography'] = settings_form.data['geography']


	def create_leksagame(self, request, default_langpair):
		settings_form = LeksaSettings(request.GET,
							initial_transtype=default_langpair)

		if request.method == 'GET' and len(settings_form.data.keys()) > 0:
			post_like_data = request.GET.copy()
			if not 'source' in post_like_data:
				post_like_data['source'] = 'all'
			if not 'transtype' in post_like_data:
				post_like_data['transtype'] = 'smenob'
			if not 'semtype' in post_like_data:
				post_like_data['semtype'] = 'all'
			if not 'geography' in post_like_data:
				post_like_data['geography'] = 'world'
            if not 'frequency' in post_like_data:
                post_like_data['frequency'] = 'common'
		else:
			post_like_data = False

		# So can I get GET data to make changes to form, but I can't get
		# it to load the game with this data.
		# reason is logic is forked into POST/GET, not POST & has game
		# data

		if request.method == 'POST' or post_like_data:
			if post_like_data:
				data = post_like_data
			else:
				data = request.POST.copy()

			# Settings form is checked and handled.
			settings_form = LeksaSettings(data)
			# Possible old form should be passed here
			for k in settings_form.data.keys():
				if not self.settings.has_key(k):
					self.settings[k] = settings_form.data[k]

			if request.session.has_key('dialect'):
				self.settings['dialect'] = request.session['dialect']

			if hasattr(request, 'LANGUAGE_CODE'):
				self.settings['language'] = request.LANGUAGE_CODE

			self.placename_settings(settings_form)
			self.settings['allsem'] = settings_form.allsem

			game = QuizzGame(self.settings)

			if "settings" in data or post_like_data:
				game.new_game()
			else:
				game.check_game(data)
				game.get_score(data)

			if 'test' in data:
				game.count = 1
			if "show_correct" in data:
				game.show_correct = 1

		# If there is no POST data, default settings are applied
		else:
			settings_form = LeksaSettings(initial_transtype=default_langpair)
			self.placename_settings(settings_form)
			settings_form.default_data['transtype'] = default_langpair

			self.settings['transtype'] = default_langpair

			for k in settings_form.default_data.keys():
				if not self.settings.has_key(k):
					self.settings[k] = settings_form.default_data[k]

			if request.session.has_key('dialect'):
				self.settings['dialect'] = request.session['dialect']

			if hasattr(request, 'LANGUAGE_CODE'):
				self.settings['language'] = request.LANGUAGE_CODE

			game = QuizzGame(self.settings)
			game.new_game()


		c = Context({
			'settingsform': settings_form,
			'forms': game.form_list,
			'count': game.count,
			'score': game.score,
			'comment': game.comment,
			'all_correct': game.all_correct,
			'show_correct': game.show_correct,
			})

		return c

# _OUT = open('/dev/ttys004', 'w')

## def timeit(method):
## 	import time
## #
## 	def timed(*args, **kw):
## 		ts = time.time()
## 		result = method(*args, **kw)
## 		te = time.time()
## #
## 		print '%r %2.2f sec' % \
## 			(method.__name__, te-ts)
## 		return result
## #
## 	return timed

def leksa_game(request, place=False):
	# from django.db import connection
	# time = 1.0

	leksagame = Quizzview()
	leksagame.init_settings()

	template = 'leksa.html'

	if place:
		leksagame.settings['allsem'] = []
		leksagame.settings['semtype'] = "PLACE_LEKSA"
		leksagame.settings['geography'] = 'world'
		leksagame.settings['frequency'] = 'common' # added
		template = 'leksa_place.html'

	sess_lang = request.session.get('django_language')

	if sess_lang:
		sess_lang = switch_language_code(sess_lang)
		if sess_lang == 'sme':
			sess_lang = 'nob'
	else:
		sess_lang = 'nob'

	default_langpair = 'sme%s' % sess_lang

	c = leksagame.create_leksagame(request, default_langpair)
	# Not true or false
	# trackGrade('Leksa', request, c)

	# querytime = [float(q['time']) for q in connection.queries]
	# count = len(querytime)
	# querytime = sum(querytime)
	# print >> _OUT, '%d queries in %s seconds' % (count, str(querytime))

	return render_to_response(template, c,
				context_instance=RequestContext(request))


class Numview(Gameview):

	def __init__(self, settingsclass, gameclass):
		self.SettingsClass = settingsclass
		self.GameClass = gameclass

	def create_numgame(self, request):
		if request.method == 'POST':
			data = request.POST.copy()

			# Settings form is checked and handled.
			settings_form = self.SettingsClass(data)

			for k in settings_form.data.keys():
				if not self.settings.has_key(k):
					self.settings[k] = settings_form.data[k]

			if request.session.has_key('dialect'):
				self.settings['dialect'] = request.session['dialect']

			if hasattr(request, 'LANGUAGE_CODE'):
				self.settings['language'] = request.LANGUAGE_CODE

			game = self.GameClass(self.settings)

			if "settings" in data:
				game.new_game()
			else:
				game.check_game(data)
				game.get_score(data)

			if 'test' in data:
				game.count=1
			if "show_correct" in data:
				game.show_correct = 1


		# If there is no POST data, default settings are applied
		else:
			settings_form = self.SettingsClass()

			for k in settings_form.default_data.keys():
				if not self.settings.has_key(k):
					self.settings[k] = settings_form.default_data[k]

			game = self.GameClass(self.settings)
			game.new_game()

		c = Context({
			'settingsform': settings_form,
			'forms': game.form_list,
			'count': game.count,
			'score': game.score,
			'comment': game.comment,
			'all_correct': game.all_correct,
			'show_correct': game.show_correct,
			'gametype': self.settings['numgame'],
		 #   'numstring': numstring,
			})
		return c



def num_clock(request):

	numgame = Numview(KlokkaSettings, Klokka)
	numgame.init_settings()
	# numgame.settings['gametype'] = clocktype

	c = numgame.create_numgame(request)

	# trackGrade('Numra clock', request, c)
	return render_to_response('clock.html', c,
				context_instance=RequestContext(request))

def num_ord(request):

	numgame = Numview(NumSettings, NumGame)
	numgame.init_settings()
	numgame.settings['gametype'] = "ord"

	c = numgame.create_numgame(request)

	# trackGrade('Numra ordinal', request, c)
	return render_to_response('num_ord.html', c,
				context_instance=RequestContext(request))



def num(request):
	numgame = Numview(NumSettings, NumGame)
	numgame.init_settings()
	numgame.settings['gametype'] = "card"

	c = numgame.create_numgame(request)

	# trackGrade('Numra', request, c)

	return render_to_response('num.html', c,
				context_instance=RequestContext(request))

def dato(request):

	datogame = Numview(DatoSettings, Dato)
	datogame.init_settings()

	c = datogame.create_numgame(request)

	return render_to_response('dato.html', c,
				context_instance=RequestContext(request))

# @timeit
def morfa_game(request, pos):
	"""
		View for Morfa game. Requires pos argument, ['N', 'V', 'A', 'Num']
	"""
	mgame = Gameview()
	mgame.init_settings()
	mgame.settings['pos'] = pos.capitalize()
	mgame.settings['gametype'] = "bare"

	template = 'mgame_%s.html' % pos.lower()[0]
	c = mgame.create_morfagame(request)

	# trackGrade('Morfa', request, c)

	return render_to_response(template, c,
				context_instance=RequestContext(request))



### Contextual Morfas

# @timeit
def cmgame(request, pos):

	mgame = Gameview()
	mgame.init_settings()
	mgame.settings['pos'] = pos.capitalize()
	mgame.settings['gametype'] = "context"

	if pos in ['Num', 'num']:
		pos = 'l'

	template = "mgame_%s.html" % pos.lower()[0]
	c = mgame.create_morfagame(request)

	# trackGrade('Contextual Morfa', request, c)

	return render_to_response(template, c,
				context_instance=RequestContext(request))

