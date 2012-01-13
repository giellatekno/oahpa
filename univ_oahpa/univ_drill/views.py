from django.template import Context, RequestContext, loader
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404
from django.utils.translation import ugettext as _

from univ_oahpa.conf.tools import switch_language_code

from random import randint

from game import *
from forms import *
from qagame import *

# comment this out
# DEBUG = open('/dev/ttys001', 'w')

# This is some crazy voodoo for course tracking

# render_to_response needs to be imported from here because it
# applies a context attribute to the returned response so that
# the trackGrade decorator can work.

from courses.views import render_to_response
from courses.decorators import trackGrade

def index(request):
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

class Gameview(object):
	""" Gameview is instantiated with a Settings object and a Game object,
	then called with create_game()
	
		game = GameView(drill.forms.Settings, drill.game.Game)
		
		Alter settings as necessary...

		game.settings['pos'] = pos.capitalize8)
		game.settings['gametype'] = "bare"

		Then run create_game with the request, which checks for POST or GET
		data, adjusts settings, and instantiates various
		drill.game/drill.$qagame objects, and returns a context.

		c = game.create_game(request)
	
	If there are any additional settings which are always set, these may be
	set by overriding the additional_settings method. (See documentation on
	that method.)

	"""

	def __init__(self, settingsclass, gameclass):
		self.SettingsClass = settingsclass
		self.GameClass = gameclass

		self.init_settings()

	def init_settings(self):

		show_data = 0
		self.settings = {}

	def deeplink_keys(self, game, settings_form):
		""" Return a list of keys that should be included in the deep link.
		This is not really obligatory to be set on every class, because the
		default behavior is to just display all keys in the deep link.
		"""
		return False

	def create_deeplink(self, game, settings_form):
		""" Produces a string of all of the settings parameters.
		"""
		keys = self.SettingsClass().fields.keys()

		values = {}

		for key in keys:
			val = False

			if key in settings_form.data:
				val = settings_form.data[key]
			elif key in self.settings:
				val = self.settings[key]

			if val:
				if type(val) == list:
					val = ','.join(val)
				values[key] = val

		key_filter = self.deeplink_keys(game, settings_form)

		if key_filter:
			key_values = ['%s=%s' % (k, v) for k, v in values.iteritems()
														if k in key_filter]
		else:
			key_values = ['%s=%s' % k for k in values.iteritems()]

		return '?' + '&'.join(key_values)

	def additional_settings(self, settings_form):
		""" Override this method if any additional settings need to be applied
		to the game before it returns a context. This is called within the
		create_game method, before the game's correspodning Game class is
		instantiated. If for example, default initial frequency, semtype, or
		case settings need to be set, these are set here.

			self.settings['geography'] = 'world'
			self.settings['frequency'] = ['common']

		These settings will of course be overridden by whatever the user
		selects through the user interface.  """

		pass
	
	def set_gamename(self):
		""" Sets the courses log name subtype for the game.
		"""

		if 'gamename_key' not in self.settings:
			self.settings['gamename_key'] = self.settings['gametype']

	def getSettingsForm(self, request, initial_kwargs=False):
		""" Set self.settings and return settings_form (a SettingsForm
		instance) and is_new_game, a boolean value that is True if a user has
		just landed on the particular game, or whether the user has adjusted
		the settings and created a new set.
		
		Goal here is to deal with all of the GET/POST differences, such that
		other methods can act on the resulting data without worrying about
		whether has come via POST or GET.

		This function must be as general as possible, and not contain reference
		to individual SettingsForm fields, since these differ across games.

		initial_kwargs may be specified if the SettingsForm instance is to be
		instantiated with any additional settings, such as initial_transtype.
		"""

		new_game = False

		# Get the form data, or URL get variables.
		if request.method == 'GET':
			data_src = request.GET
			new_game = True      # presence of GET data means always a new game
		elif request.method == 'POST':
			data_src = request.POST

		# Instantiate settings class
		if initial_kwargs:
			settings_form = self.SettingsClass(data_src, **initial_kwargs)
		else:
			settings_form = self.SettingsClass(data_src)
		
		# If the settings form has any data in it, the user has modified
		# settings or just come to Oahpa via a link with GET data. It is most
		# likely that the user has come by link, and thus we need to fill out
		# the settings form values with the default initial values that were
		# not specified in the link.

		if len(settings_form.data.keys()) > 0:
			post_like_data = settings_form.data.copy()

			# set initial values...
			for field, val in self.SettingsClass().fields.iteritems():
				if field not in post_like_data:
					post_like_data[field] = val.initial
		else:
			# User has not arrived by a link, or they have and there were no
			# settings specified.
			post_like_data = False

		if post_like_data:
			# Recreate form with URL variables and default values included
			settings_form = self.SettingsClass(post_like_data)
			settings_source = settings_form.data
		else:
			# Create the form, because none of the above conditions were true
			if initial_kwargs:
				settings_form = self.SettingsClass(**initial_kwargs)
			else:
				settings_form = self.SettingsClass()
			settings_source = settings_form.default_data
			new_game = True
		
		# All form creation operations are complete, so now we copy form values
		# to the game settings object. 
		for k in settings_source.keys():
			if k not in self.settings:
				self.settings[k] = settings_source[k]

		# Settings values which aren't set from the form, but from the session
		if request.session.has_key('dialect'):
			self.settings['dialect'] = request.session['dialect']

		if hasattr(request, 'LANGUAGE_CODE'):
			self.settings['language'] = request.LANGUAGE_CODE

		# TODO: should probably be moved out 
		# to individual game object self.syll_settings(settings_form)

		# If 'settings' exists in data, user has clicked 'new set'
		if 'settings' in settings_form.data:
			new_game = True

		return settings_form, new_game
	
	def create_game(self, request, **init_kwargs):
		""" Instantiate the Game object, check answers and return the context
		for the view. """

		# Grab form POST data, or URL GET data.
		settings_form, is_new_game = self.getSettingsForm(request,
										initial_kwargs=init_kwargs)

		# Apply whatever additional settings need to be made
		self.additional_settings(settings_form)

		# Create the game class. If the game is new, self.settings will not
		# contain any word or wordform data, and thus GameClass will select
		# random words and create the question/answers.  If a game is in
		# progress, it will reselect the existing values from the game form,
		# and check whether or not the answers are correct or incorrect.

		game = self.GameClass(self.settings)

		if is_new_game:
			game.new_game()
		else:
			game.check_game(settings_form.data)
			game.get_score(settings_form.data)

			if 'test' in settings_form.data:
				game.count = 1

			if "show_correct" in settings_form.data:
				game.show_correct = 1

		self.set_gamename()

		return self.context(request, game, settings_form)


class Leksaview(Gameview):

	def additional_settings(self, settings_form):
		self.settings['allsem'] = settings_form.allsem
		self.settings['frequency'] = None
		self.settings['geography'] = None

		# settings_form.default_data['transtype'] = default_langpair

	def set_gamename(self):
		transtype = self.settings['transtype']
		semtype = self.settings['semtype']

		if type(semtype) == list:
			semtype = ', '.join(semtype)

		self.settings['gamename_key'] = "%s - %s" % (semtype, transtype)
		
	def context(self, request, game, settings_form):
		return Context({
			'settingsform': settings_form,
			'settings' : self.settings,
			'forms': game.form_list,
			'count': game.count,
			'score': game.score,
			'comment': game.comment,
			'all_correct': game.all_correct,
			'show_correct': game.show_correct,
			'deeplink': self.create_deeplink(game, settings_form),
			})


class LeksaPlaceview(Gameview):

	def additional_settings(self, settings_form):
		self.settings['allsem'] = []
		self.settings['semtype'] = "PLACE_LEKSA"
		self.settings['geography'] = 'world'
		self.settings['frequency'] = ['common'] # added

		self.settings['allsem'] = settings_form.allsem
		# settings_form.default_data['transtype'] = default_langpair

		self.settings['frequency'] = []
		if 'common' in settings_form.data:
			self.settings['frequency'].append('common')
		if 'rare' in settings_form.data:
			self.settings['frequency'].append('rare')
# 		if len(self.settings['frequency']) == 0:
# 			self.settings['frequency'].append('common')
			
		self.settings['geography'] = []

		if 'geography' in settings_form.data:
			self.settings['geography'] = settings_form.data['geography']

	def deeplink_keys(self, game, settings_form):
		return ['semtype', 'geography', 'common', 'rare', 'transtype', 'source']
	
	def set_gamename(self):
		geog = self.settings['geography']
		freq = ', '.join(self.settings['frequency'])
		self.settings['gamename_key'] = "Place - %s - %s" % (geog, freq)

	def context(self, request, game, settings_form):
		return Context({
			'settingsform': settings_form,
			'settings' : self.settings,
			'forms': game.form_list,
			'count': game.count,
			'score': game.score,
			'comment': game.comment,
			'all_correct': game.all_correct,
			'show_correct': game.show_correct,
			'deeplink': self.create_deeplink(game, settings_form),
			})

	

@trackGrade("Leksa")
def leksa_game(request, place=False):

	if place:
		leksagame = LeksaPlaceview(LeksaSettings, QuizzGame)
		template = 'leksa_place.html'
	else:
		leksagame = Leksaview(LeksaSettings, QuizzGame)
		template = 'leksa.html'

	sess_lang = request.session.get('django_language')

	if sess_lang:
		sess_lang = switch_language_code(sess_lang)
		if sess_lang == 'sme':
			sess_lang = 'nob'
	else:
		sess_lang = 'nob'

	default_langpair = 'sme%s' % sess_lang

	c = leksagame.create_game(request, initial_transtype=default_langpair)

	return render_to_response(template, c,
				context_instance=RequestContext(request))


class Numview(Gameview):
	
	def set_gamename(self):
		self.settings['gamename_key'] = ''
	
	def deeplink_keys(self, game, settings_form):
		keys = ['numgame', 'maxnum']

		if self.GameClass == Klokka:
			keys.append('gametype')

		return keys

	def context(self, request, game, settings_form):

		return Context({
			'settingsform': settings_form,
			'settings' : self.settings,
			'forms': game.form_list,
			'count': game.count,
			'score': game.score,
			'comment': game.comment,
			'all_correct': game.all_correct,
			'show_correct': game.show_correct,
			'gametype': self.settings['numgame'],
			'deeplink': self.create_deeplink(game, settings_form),
		 #   'numstring': numstring,
			})


@trackGrade("Numra clock")
def num_clock(request):

	numgame = Numview(KlokkaSettings, Klokka)
	# numgame.settings['gametype'] = clocktype

	c = numgame.create_game(request)

	return render_to_response('clock.html', c,
				context_instance=RequestContext(request))

@trackGrade("Numra ordinal")
def num_ord(request):

	numgame = Numview(NumSettings, NumGame)
	numgame.settings['gametype'] = "ord"

	c = numgame.create_game(request)

	return render_to_response('num_ord.html', c,
				context_instance=RequestContext(request))


@trackGrade("Numra cardinal")
def num(request):
	numgame = Numview(NumSettings, NumGame)
	numgame.settings['gametype'] = "card"

	c = numgame.create_game(request)

	return render_to_response('num.html', c,
				context_instance=RequestContext(request))

@trackGrade("Numra dato")
def dato(request):

	datogame = Numview(DatoSettings, Dato)

	c = datogame.create_game(request)

	return render_to_response('dato.html', c,
				context_instance=RequestContext(request))


class Morfaview(Gameview):
	gamenames = {
		'ATTR' :  _('Practise attributes'),
		'A-ATTR' :  _('Practise attributes'),
		#'A' : _('Practise adjectives'),  # added by Heli
		'A-NOM' :  _('Practise adjectives in nominative'),
		'A-ILL' :  _('Practise adjectives in illative'),
		'A-ACC' :  _('Practise adjectives in accusative'),
		'A-COM' :  _('Practise adjectives in comitative'),
		'A-ESS' :  _('Practise adjectives in essive'),
		'A-GEN' :  _('Practise adjectives in genitive'),
		'A-NOM-PL' :  _('Practise adjectives in plural'),
		'N-LOC' :  _('Practise adjectives in locative'),
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
		'V-COND'  : _('Practise conditional'),
		'V-IMPRT' : _('Practise imperative'),
		'V-POT'   : _('Practise potential'),
		'P-PERS'  : _('Practise '),
    	'P-RECIPR': _('Practise reciprocative pronouns'),
    	'P-REFL':  _('Practise reflexive pronouns'),
    	'P-DEM':   _('Practise demonstrative pronouns'),
	}

	def syll_settings(self,settings_form):

		self.settings['syll'] = []

		if 'bisyllabic' in settings_form.data:
			self.settings['syll'].append('2syll')
		if 'trisyllabic' in settings_form.data:
			self.settings['syll'].append('3syll')
		if 'contracted' in settings_form.data:
			self.settings['syll'].append('Csyll')
		if len(self.settings['syll']) == 0:
			self.settings['syll'].append('2syll')
	
	def deeplink_keys(self, game, settings_form):
		""" The MorfaSettings form has a lot of values in it, so we need to
		prune the deeplink values down a bit. The reason there is a need for
		logic here is because all of the values in the MorfaSettings form are
		set regardless of what game type it is. Other game types only have the
		corresponding values set to each subtype.
		"""

		if self.settings['gametype'] == "bare":
			if self.settings['pos'] == 'N':
				return ['case' 'bisyllabic', 'trisyllabic', 'contracted',
						'book',]
			if self.settings['pos'] == 'V':
				return ['vtype' 'bisyllabic', 'trisyllabic', 'contracted',
						'book',]
			if self.settings['pos'] == 'A':
				return ['adjcase', 'grade', 'bisyllabic', 'trisyllabic',
						'contracted', 'book',]
			if self.settings['pos'] == 'Pron':
				return ['pron_type', 'proncase']
			if self.settings['pos'] == 'Num':
				return ['num_bare', 'num_level', 'book']
		else:
			if self.settings['pos'] == 'N':
				return ['case_context']
			if self.settings['pos'] == 'V':
				return ['vtype_context']
			if self.settings['pos'] == 'A':
				return ['adj_context']
			if self.settings['pos'] == 'Pron':
				return ['pron_context']
			if self.settings['pos'] == 'Num':
				return ['num_context']


	def context(self, request, game, settings_form):
		return RequestContext(request, {
			'settingsform': settings_form,
			'settings' : self.settings,
			'forms': game.form_list,
			'count': game.count,
			'score': game.score,
			'comment': game.comment,
			'all_correct': game.all_correct,
			'show_correct': game.show_correct,
			'language' : self.settings['language'],
			'deeplink': self.create_deeplink(game, settings_form),
			})
	
	def additional_settings(self, settings_form):

		self.settings['allcase'] = settings_form.allcase
		self.syll_settings(settings_form)

	def set_gamename(self):
		subname = False
		# Create a gamename which will be used in log entries.
		if self.settings['pos'] == "N":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['case']
			else:
				gamename_key = self.settings['case_context']
		if self.settings['pos'] == "Pron":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['proncase']
				subname = self.settings['pron_type'] # dem, recipr, etc.
			else:
				gamename_key = self.settings['pron_context']
		if self.settings['pos'] == "Num":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['num_bare']
				subname = 'level %s' % str(self.settings['num_level'])
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
				subname = self.settings['grade']
			else:
				gamename_key = self.settings['adj_context']

		self.settings['gamename'] = self.gamenames[gamename_key]
		names = [self.settings['pos'], gamename_key]

		if subname:
			names.append(subname)

		self.settings['gamename_key'] = ' - '.join(names) 


# @timeit
@trackGrade("Morfa")
def morfa_game(request, pos):
	"""
		View for Morfa game. Requires pos argument, ['N', 'V', 'A', 'Num']
	"""
	mgame = Morfaview(MorfaSettings, BareGame)

	mgame.settings['pos'] = pos.capitalize()
	mgame.settings['gametype'] = "bare"

	if pos == 'Num':
		template = 'mgame_l.html'
	else:
		template = 'mgame_%s.html' % pos.lower()[0]

	c = mgame.create_game(request)

	return render_to_response(template, c,
				context_instance=RequestContext(request))



### Contextual Morfas

# @timeit
@trackGrade("Contextual Morfa")
def cmgame(request, pos):

	mgame = Morfaview(MorfaSettings, QAGame)

	mgame.settings['pos'] = pos.capitalize()
	mgame.settings['gametype'] = "context"

	if pos in ['Num', 'num']:
		pos = 'l'

	template = "mgame_%s.html" % pos.lower()[0]
	c = mgame.create_game(request)

	return render_to_response(template, c,
				context_instance=RequestContext(request))

