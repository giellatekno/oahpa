# -*- coding: utf-8 -*-
from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')
tls = importlib.import_module(LLL1+'_oahpa.conf.tools')
cvs = importlib.import_module(LLL1+'_oahpa.courses.views')
cds = importlib.import_module(LLL1+'_oahpa.courses.decorators')

from django.template import Context, RequestContext, loader
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404
from django.utils.translation import ugettext_lazy as _

switch_language_code = tls.switch_language_code

from random import randint

from game import *
from forms import *

# comment this out
# DEBUG = open('/dev/ttys001', 'w')

# This is some crazy voodoo for course tracking

# render_to_response needs to be imported from here because it
# applies a context attribute to the returned response so that
# the trackGrade decorator can work.

render_to_response = cvs.render_to_response
trackGrade = cds.trackGrade

def index(request):
	c = {
		'jee': "joku arvo",
		}
	return render_to_response(request, 'oahpa_main.html', c)

def updating(request):
	c = {
		'jee': "joku arvo",
		}
	return render_to_response(request, 'updating.html', c)

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

	def change_game_settings(self, game):
		""" If any settings need to be set before Game.new_game is called,
		they are set here. """

		return game

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
			new_game = True  	# presence of GET data means always a new game
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

		if request.session.has_key('django_language'):
			self.settings['language'] = request.session['django_language']
		else:
			self.settings['language'] = request.COOKIES.get("django_language", None)
			if not self.settings['language']:
				self.settings['language'] = request.LANGUAGE_CODE
				request.session['django_language'] = request.LANGUAGE_CODE


		#if hasattr(request, 'LANGUAGE_CODE'):
		#	self.settings['language'] = request.LANGUAGE_CODE

		# TODO: should probably be moved out
		# to individual game object self.syll_settings(settings_form)

		# If 'settings' exists in data, user has clicked 'new set'
		if 'settings' in settings_form.data:
			new_game = True

		return settings, settings_form, new_game

	def create_game(self, request, **init_kwargs):
		""" Instantiate the Game object, check answers and return the context
		for the view. """

		# Grab form POST data, or URL GET data.
		settings, settings_form, is_new_game = self.getSettingsForm(request,
										initial_kwargs=init_kwargs)

		# Apply whatever additional settings need to be made

		self.additional_settings(settings_form)

		# Create the game class. If the game is new, self.settings will not
		# contain any word or wordform data, and thus GameClass will select
		# random words and create the question/answers.  If a game is in
		# progress, it will reselect the existing values from the game form,
		# and check whether or not the answers are correct or incorrect.

		game = self.GameClass(self.settings)

		self.set_gamename()

		if is_new_game:
			game = self.change_game_settings(game)
			game.new_game()
		else:
			game = self.change_game_settings(game)
			game.check_game(settings_form.data)
			game.get_score(settings_form.data)

			if 'test' in settings_form.data:
				game.count = 1

			if "show_correct" in settings_form.data:
				game.show_correct = 1



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

		return {
			'settingsform': settings_form,
			'settings' : self.settings,
			'forms': game.form_list,
			'count': game.count,
			'score': game.score,
			'comment': game.comment,
			'all_correct': game.all_correct,
			'show_correct': game.show_correct,
			'deeplink': self.create_deeplink(game, settings_form),
			'oahpa': 'oahpa.html',
			'lll1': LLL1,
			}


class LeksaPlaceview(Gameview):

	def additional_settings(self, settings_form):

		def true_false_filter(val):
			if val in ['on', 'On', u'on', u'On']:
				return True
			else:
				return False

		self.settings['allsem'] = []
		self.settings['semtype'] = "NAME"
		self.settings['geography'] = 'world'
		self.settings['frequency'] = ['common'] # added

		self.settings['allsem'] = settings_form.allsem
		# settings_form.default_data['transtype'] = default_langpair

		self.settings['frequency'] = []

		# NOTE: Checkboxes as choices seem to be weird, thus more complex logic
		# I wonder if the problem is that the form is not being validated
		# Because it seems like there's a lot of code getting around this fact

		if 'common' in settings_form.data:
			if true_false_filter(settings_form.data['common']):
				self.settings['frequency'].append('common')
				settings_form.data['common'] = 'on'
			else:
				settings_form.data['common'] = None

		if 'rare' in settings_form.data:
			self.settings['frequency'].append('rare')
			if true_false_filter(settings_form.data['rare']):
				self.settings['frequency'].append('rare')
				settings_form.data['rare'] = 'on'
			else:
				settings_form.data['rare'] = None


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
		return {
			'settingsform': settings_form,
			'settings' : self.settings,
			'forms': game.form_list,
			'count': game.count,
			'score': game.score,
			'comment': game.comment,
			'all_correct': game.all_correct,
			'show_correct': game.show_correct,
			'deeplink': self.create_deeplink(game, settings_form),
			'oahpa': 'oahpa.html',
			'lll1': LLL1,
			}



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
		if sess_lang == LLL1:
			sess_lang = 'rus'  # was: nob
	else:
		sess_lang = 'nob'

	default_langpair = LLL1+'%s' % sess_lang

	c = leksagame.create_game(request, initial_transtype=default_langpair)

	return render_to_response(request, template, c)

class Numview(Gameview):

	def set_gamename(self):
		self.settings['gamename_key'] = ''

	def deeplink_keys(self, game, settings_form):
		keys = ['numgame', 'maxnum']

		if self.GameClass == Klokka:
			keys.append('gametype')

		return keys

	def context(self, request, game, settings_form):

		return {
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
			'oahpa': 'oahpa.html',
			'lll1': LLL1,
		 #   'numstring': numstring,
			}


@trackGrade("Numra clock")
def num_clock(request):

	numgame = Numview(KlokkaSettings, Klokka)
	# numgame.settings['gametype'] = clocktype

	c = numgame.create_game(request)

	return render_to_response(request, 'clock.html', c)

@trackGrade("Numra ordinal")
def num_ord(request):

	numgame = Numview(NumSettings, NumGame)
	numgame.settings['gametype'] = "ord"

	c = numgame.create_game(request)

	return render_to_response(request, 'num_ord.html', c)


@trackGrade("Numra cardinal")
def num(request):
	numgame = Numview(NumSettings, NumGame)
	numgame.settings['gametype'] = "card"

	c = numgame.create_game(request)

	return render_to_response(request, 'num.html', c)

@trackGrade("Numra dato")
def dato(request):

	datogame = Numview(DatoSettings, Dato)

	c = datogame.create_game(request)

	return render_to_response(request, 'dato.html', c)
