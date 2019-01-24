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

hostname = oahpa_module.settings.hostname

from random import randint

from game import *
from forms import *
from qagame import *
from sahka import *
from cealkka import *

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

	def register_logs(self, request, game, settings_form):
		""" Grab all the logs that were generated from a form, and
		append them to the request session """
		request.user_logs_generated = [
			f.last_log for f in game.form_list
			if hasattr(f, 'last_log')
		]
		# Use this to track whether the user switches away from the
		# current exercise, if they do, then we can optionally stop
		# tracking activity.

		exercise_params = request.path_info + self.create_deeplink(game, settings_form)
		request.session['current_exercise_params'] = exercise_params

		request.session['all_correct'] = game.all_correct in [1, True, 'True', 'true']

		request.session['set_completed'] = request.session['all_correct'] or \
											game.show_correct in [1, True, 'True', 'true']

		request.session['new_game'] = game.is_new_game

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
		if request.session.has_key('country'):
			self.settings['user_country'] = request.session['country']
		else:
			self.settings['user_country'] = False

		if request.session.has_key('dialect'):
			self.settings['dialect'] = request.session['dialect']

		if request.session.has_key('django_language'):
			self.settings['language'] = request.session['django_language']
		else:
			self.settings['language'] = request.COOKIES.get("django_language", None)
			if not self.settings['language']:
				self.settings['language'] = request.LANGUAGE_CODE
				request.session['django_language'] = request.LANGUAGE_CODE

                print "get_settings_form language: "+self.settings['language']


		if request.user.is_authenticated():
			request_user = request.user
		else:
			request_user = False

		self.settings['user'] = request_user

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

		if is_new_game:
			game = self.change_game_settings(game)
			game.new_game()
			game.is_new_game = True
		else:
			game = self.change_game_settings(game)
			game.check_game(settings_form.data)
			game.get_score(settings_form.data)
			game.is_new_game = False

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
		self.register_logs(request, game, settings_form)

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
			'hst': hostname,
			}


class LeksaPlaceview(Gameview):

	def additional_settings(self, settings_form):

		def true_false_filter(val):
			if val in ['on', 'On', u'on', u'On']:
				return True
			else:
				return False

		self.settings['allsem'] = []
		self.settings['semtype'] = "PLACE_LEKSA"
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
		self.register_logs(request, game, settings_form)

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
			'hst': hostname,
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
	print sess_lang

	if sess_lang:
		sess_lang = switch_language_code(sess_lang)
		if sess_lang == 'crk':
			sess_lang = 'eng' # was: nob
	else:
		sess_lang = 'eng' # was: nob

	print sess_lang
	default_langpair = 'crk%s' % sess_lang
	print default_langpair

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
		self.register_logs(request, game, settings_form)

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
			'hst': hostname,
		 #   'numstring': numstring,
			}


@trackGrade("Numra clock")
def num_clock(request):

	numgame = Numview(KlokkaSettings, Klokka)
	# numgame.settings['gametype'] = clocktype

	c = numgame.create_game(request)
	c['numra_gametype'] = "clock"

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
	c['numra_gametype'] = "numra_cardinal"

	return render_to_response(request, 'num.html', c)

@trackGrade("Numra dato")
def dato(request):

	datogame = Numview(DatoSettings, Dato)

	c = datogame.create_game(request)
	c['numra_gametype'] = "dato"

	return render_to_response(request, 'dato.html', c)

@trackGrade("Numra money")
def money(request):

	moneygame = Numview(MoneySettings, Money)

	c = moneygame.create_game(request)
	c['numra_gametype'] = "money"

	return render_to_response(request, 'money.html', c)

# Translation of gamenames takes place in the templates mgame_n.html etc.
# because they have to be available in two different languages - in Saami on the
# interface and in the interface language chosen by the user in the translation
# tooltips.
class Morfaview(Gameview):
	gamenames = {
		#'ATTR': _('Practice attributes'),
		#'A-ATTR': _('Practice attributes'),
		'A-NOM': _('Practice adjectives in nominative'),
		'A-NOM-PL': _('Practice adjectives in plural'),
		'A-LOC': _('Practice adjectives in locative'),
		'A-COMP': _('Practice comparative'),
		'A-SUPERL': _('Practice superlative'),
		'V-DER': _('Practice verb derivation'),
		'V-DER-PASS': _('Practice verb passive derivation'),
		'DER-PASSV': _('Practice verb passive derivation'),
		'A-DER-V': _('Practice adjective to verb derivation'),
		'N-PX-GROUP1': _('Practice possessive nouns.'),
		'N-PX-GROUP2': _('Practice possessive nouns.'),
		'N-PX-GROUP3': _('Practice possessive nouns.'),
		'PX-LOC': _('Practice possessive nouns in locative'),
		'ATTRPOS': _('Practice attributes in positive'),
		'ATTRCOMP': _('Practice attributes in comparative'),
		'ATTRSUP':  _('Practice attributes in superlative'),
		'PREDPOS':  _('Practice predicative in positive'),
		'PREDCOMP':  _('Practice predicative in comparative'),
		'PREDSUP':  _('Practice predicative in superlative'),
		'NUM-ATTR':  _('Practice numeral attributes'),
		'N-PL':  _('Practice plural nouns.'),
		'N-LOC': _('Practice nouns in locative.'),
		'NOM':  _('Practice nominative'),
		'N-REVDIM':  _('Here are diminutive forms.'),
		'N-REVDIM':  _('Here are diminutive forms.'),
		'N-PX':  _('Practice possessive forms.'),
		'N-MIX':  _('Practice a mix'),
		'V-MIX':  _('Practice a mix'),
		'A-MIX':  _('Practice a mix'),
		'P-MIX':  _('Practice a mix'),
		'NUM-NOM-PL':  _('Practice numerals in plural.'),
		'NUM-LOC':  _('Practice numerals in locative.'),
		'COLL-NUM':  _('Practice collective numerals.'),
		'ORD-NUM':  _('Practice ordinal numbers'),
		'ORD-N-NOM-PL':  _('Practice ordinal numerals in plural.'),
		'COLL-NOMPL':  _('Practice collective numerals in plural.'),
		'COLL-N-LOC':  _('Practice collective numerals in locative.'),
		'PRS':  _('Practice verbs in present tense.'),
		'PRT':  _('Practice verbs in past tense.'),
		'PRF':  _('Practice perfect'),
		'GER':  _('Practice gerund'),
		'COND':  _('Practice conditional'),
		'IMPRT':  _('Practice imperative'),
		'POT':  _('Practice potential'),

		'V-II-PRS': _('Practice Inanimate Intransitive (II) verbs in present tense.'),
		'V-AI-PRS':  _('Practice Animate Intransitive (AI) verbs in present tense.'),

		'V-TA-PRS': _('Practice Transitive Animate (TA) verbs in present tense.'),
		'V-TA-PRT': _('Practice Transitive Animate (TA) verbs in past tense.'),
		'V-TA-FUT-DEF': _('Practice Transitive Animate (TA) verbs in future definite form.'),
		'V-TA-FUT-INT': _('Practice Transitive Animate (TA) verbs in future intentional form.'),

		'V-TI-PRS': _('Practice Transitive Inanimate (TI) verbs in present tense.'),
		'V-TI-PRT': _('Practice Transitive Inanimate (TI) verbs in past tense.'),
		'V-TI-FUT-DEF': _('Practice Transitive Inanimate (TI) in future definite form.'),
		'V-TI-FUT-INT': _('Practice Transitive Inanimate (TI) in future intentional form.'),

		'V-TA-CNJ-PRS': _('Practice Transitive Animate (TA) Conjunct in present tense.'),
		'V-TA-CNJ-PRT': _('Practice Transitive Animate (TA) Conjunct in past tense.'),
		'V-TA-CNJ-FUT-INT': _('Practice Transitive Animate (TA) Conjunct future intentional form.'),

		'V-AI-CNJ-PRS': _('Practice Animate Intransitive (AI) Conjunct in present tense.'),
	    'V-AI-CNJ-PRT':  _('Practice Animate Intransitive (AI) Conjunct in past tense.'),
	    'V-AI-CNJ-FUT-INT':  _('Practice Animate Intransitive (AI) Conjunct in future intentional form.'),
		'V-AI-FUT-INT':  _('Practice Animate Intransitive (AI) verbs in the future intentional form.'),
		'V-AI-FUT-DEF':  _('Practice Animate Intransitive (AI) verbs in the future definite form.'),

		'V-TI-CNJ-PRS':  _('Practice Transitive Inanimate (TI) Conjunct in present.'),
		'V-TI-CNJ-PRT':  _('Practice Transitive Inanimate (TI) Conjunct in past tense.'),
		'V-TI-CNJ-FUT-INT':  _('Practice Transitive Inanimate (TI) Conjunct in future intentional form.'),

		'V-AI-PRT':  _('Practice Animate Intransitive (AI) verbs in past tense.'),
		'V-AI-PRF':  _('practice perfect'),

		'V-GER':  _('Practice gerund'),
		'V-COND':  _('practice conditional'),
		'V-IMPRT':  _('practice imperative'),
		'V-POT':  _('practice potential'),
		'P-PERS':  _('practice personal pronouns'),
		'P-RECIPR':  _('practice reciprocative pronouns'),
		'P-REFL':  _('practice reflexive pronouns'),
		'P-REL': _('practice relative pronouns'),
		'P-DEM':  _('Practice demonstrative pronouns.'),
		# 'P-DEM-CRK':  _('practice translating demonstrative pronouns'),
	}

	def syll_settings(self,settings_form):

		def true_false_filter(val):
			if val in ['on', 'On', u'on', u'On','True']:
				return True
			else:
				return False

		bisyl = settings_form.data.get('bisyllabic', None)
		trisyl = settings_form.data.get('trisyllabic', None)
		cont = settings_form.data.get('contracted', None)

		if 'syll' not in self.settings:
			self.settings['syll'] = []

		# Special treatment of settings_form.data['bisyllabic'] since
		# it is set by default.

		if true_false_filter(bisyl):
			self.settings['syll'].append('2syll')
			settings_form.data['bisyllabic'] = 'on'
		else:
			settings_form.data['bisyllabic'] = None

		if true_false_filter(trisyl):
			self.settings['syll'].append('3syll')
			settings_form.data['trisyllabic'] = 'on'
		else:
			settings_form.data['trisyllabic'] = None

		if true_false_filter(cont):
			self.settings['syll'].append('Csyll')
			settings_form.data['contracted'] = 'on'
		else:
			settings_form.data['contracted'] = None

		if len(self.settings['syll']) == 0:
			self.settings['syll'].append('2syll')

		self.settings['syll'] = list(set(self.settings['syll']))


	def deeplink_keys(self, game, settings_form):
		""" The MorfaSettings form has a lot of values in it, so we need to
		prune the deeplink values down a bit. The reason there is a need for
		logic here is because all of the values in the MorfaSettings form are
		set regardless of what game type it is. Other game types only have the
		corresponding values set to each subtype.
		"""

		if self.settings['gametype'] == "bare":
			if self.settings['pos'] == 'N':
				return ['case', 'bisyllabic', 'trisyllabic', 'contracted',
						'book',]
			if self.settings['pos'] == 'V':
				return ['vtype', 'bisyllabic', 'trisyllabic', 'contracted',
						'book',]
			if self.settings['pos'] == 'A':
				return ['adjcase', 'grade', 'bisyllabic', 'trisyllabic',
						'contracted', 'book',]
			if self.settings['pos'] == 'Pron':
				return ['pron_type', 'proncase']
			if self.settings['pos'] == 'Num':
				return ['num_bare', 'num_level', 'num_type', 'book'] # added num_type
		else:
			if self.settings['pos'] == 'N':
				return ['case_context']
			if self.settings['pos'] == 'V':
				return ['vtype_context']
			if self.settings['pos'] == 'A':
				return ['adj_context']
			if self.settings['pos'] == 'Pron':
				return ['pron_context', 'wordform_type']
			if self.settings['pos'] == 'Num':
				return ['num_context']

	def context(self, request, game, settings_form):
		self.register_logs(request, game, settings_form)

		return {
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
			'oahpa': 'oahpa.html',
			'lll1': LLL1,
			'hst': hostname,
			}

	def additional_settings(self, settings_form):

		self.settings['allcase'] = settings_form.allcase
		self.syll_settings(settings_form)
		self.settings['allnum_type'] = settings_form.allnum_type  # added by Heli

	def set_gamename(self):
		subname = False
		# Create a gamename which will be used in log entries.

		# N-ILL
		if self.settings['pos'] == "N":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['case']
			else:
				gamename_key = self.settings['case_context']

		# N-ILL, etc.
		if self.settings['pos'] == "Pron":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['proncase']
				subname = self.settings['pron_type'] # dem, recipr, etc.
			else:
				gamename_key = self.settings['pron_context']
				# TODO: reciprocative, wordform_type?

		# N-LOC - level 1/2
		if self.settings['pos'] == "Num":
			if self.settings['gametype'] == "bare":
				if not self.settings['num_type'] or self.settings['num_type'] == 'CARD':
					gamename_key = self.settings['num_bare']
				else:
					gamename_key = '%s-%s' % (self.settings['num_type'], self.settings['num_bare'])
				subname = 'level %s' % str(self.settings['num_level'])
			else:
				gamename_key = self.settings['num_context']

		# PRS
		if self.settings['pos'] == "V":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['vtype']

			else:
				v_trans_anim_context = self.settings['v_trans_anim_context']
				v_mode_context = self.settings['v_mode_context']
				v_tense_context = self.settings['v_tense_context']
				params = ('V', v_trans_anim_context, v_mode_context,
							v_tense_context)
				gamename_key = V_TYPE_FILTER_OPTIONS.get(params)

		# ATTR - COMP
		if self.settings['pos'] == "A":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['adjcase']
				subname = self.settings['grade']
			else:
				gamename_key = self.settings['adj_context']

		# A-DER-V
		if self.settings['pos'] == "Der":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['derivation_type']
			else:
				gamename_key = self.settings['derivation_type_context']

		# Px
		if self.settings['pos'] == "Px":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['possessive_type']
			else:
				gamename_key = self.settings['possessive_case_context']

		self.settings['gamename'] = self.gamenames[gamename_key]
		names = [self.settings['pos'], gamename_key]

		if subname:
			names.append(subname)

		# 2syll/3syll/Csyll
		if 'syll' in self.settings:
			sylls = '/'.join(self.settings['syll'])
		else:
			sylls = ''

		# Append syllable types if set
		if sylls and self.settings['pos'] not in ["Pron", "Num"]:
			names.append(sylls)

		#if 'num_type' in self.settings:  # added by Heli. I am not sure if it works.
		#	num_type = self.settings['num_type']
		#	names.append(num_type)

		self.settings['gamename_key'] = ' - '.join(names)

# @timeit
@trackGrade("Morfa")
def morfa_game(request, pos):
	"""
		View for Morfa game. Requires pos argument, ['N', 'V', 'A', 'Num', 'Px']
	"""

	mgame = Morfaview(MorfaSettings, BareGame)

	mgame.settings['pos'] = pos.capitalize()
	mgame.settings['gametype'] = "bare"

	if pos == 'Num':
		template = 'mgame_l.html'
	elif pos == 'Der':
		template = 'mgame_der.html'
	else:
		template = 'mgame_%s.html' % pos.lower()[0]

	c = mgame.create_game(request)

	return render_to_response(request, template, c)


### Contextual Morfas

# @timeit
@trackGrade("Contextual Morfa")
def cmgame(request, pos):

	mgame = Morfaview(MorfaSettings, QAGame)

	mgame.settings['pos'] = pos.capitalize()
	mgame.settings['gametype'] = "context"

	if pos in ['Num', 'num']:
		p = 'l'
	elif pos == 'Der':
		p = 'der'
        elif pos == 'Px':
		  p = 'px'
	else:
		p = pos.lower()[0]

	template = "mgame_%s.html" % p
	c = mgame.create_game(request)

	return render_to_response(request, template, c)


class Vastaview(Gameview):

	def additional_settings(self, settings_form):
		self.settings['level'] = settings_form.data.get('level', '1')

	def change_game_settings(self, game):
		# These are set before new_game is called
		game.gametype = "qa"
		game.num_fields = 2
		return game

	def set_gamename(self):
		if 'gamename_key' not in self.settings:
			gamename = 'level %s' % self.settings['level']
			self.settings['gamename_key'] = gamename

	def context(self, request, game, settings_form):
		self.register_logs(request, game, settings_form)

		c = {
			'settingsform': settings_form,
			'settings': self.settings,
			'forms': game.form_list,
			'messages': game.form_list[0].messages,
			'count': game.count,
			'score': game.score,
			'comment': game.comment,
			'all_correct': game.all_correct,
			'show_correct': game.show_correct,
			'gametype': "qa",
			'deeplink': self.create_deeplink(game, settings_form),
			'hst': hostname,
			}
		return c


@trackGrade("Vasta F")
def vasta(request):

	vastagame = Vastaview(VastaSettings, QAGame)

	c = vastagame.create_game(request)
	return render_to_response(request, 'vasta.html', c)


class Cealkkaview(Gameview):
	""" View for Cealkka, main difference here is context, and cealkka requires
	one form set.
	"""

	def deeplink_keys(self, game, settings_form):
		return ['level']  # removed lemmacount

	def additional_settings(self, settings_form):
		self.settings['gametype'] = "cealkka"

	def change_game_settings(self, game):
		""" This is run before Game.new_game() is called.
		"""
		game.num_fields = 2
		return game

	def set_gamename(self):
		self.settings['gamename_key'] = 'level %s' % str(self.settings['level'])

	def context(self, request, game, settings_form):
		self.register_logs(request, game, settings_form)
		# TODO: seems to be fine, but settings['level'] on the first visit is
		# all, not 1, even though the menu shows level 1

		c = {
			'settingsform': settings_form,
			'settings': self.settings,
			'forms': game.form_list,
			'messages': game.form_list[0].messages,
			'count': game.count,
			'score': game.score,
			'comment': game.comment,
			'all_correct': game.all_correct,
			'show_correct': game.show_correct,
			'gametype': "cealkka",
			'deeplink': self.create_deeplink(game, settings_form),
			'hst': hostname,
			}
		return c



@trackGrade("Cealkka")
def cealkka(request):

	cealkkagame = Cealkkaview(CealkkaSettings, CealkkaGame)
	cealkkagame.init_settings()

	c = cealkkagame.create_game(request)
	return render_to_response(request, 'vasta.html', c)


class Sahkaview(Cealkkaview):
	""" Sahka is a bit different: it has a main view page (topicnumber = 0) and
	has separate methods to call the creation of a new game and to continue
	with an existing game. There are also some attributes that must always be
	set, such as the image, and wordlist.  """

	def deeplink_keys(self, game, settings_form):
		return ['dialogue', 'topicnumber']

	def set_gamename(self):
		if 'gamename_key' not in self.settings:
			game_name = ' - '.join([self.settings['gametype'],
									self.settings['dialogue']])

			self.settings['gamename_key'] = game_name

	def additional_settings(self, settings_form):
		self.settings['gametype'] = 'sahka'
		self.settings['image'] = settings_form.data.get('image')
		self.settings['wordlist'] = settings_form.data.get('wordlist')
		self.settings['dialogue'] = settings_form.data.get('dialogue', '')
		self.settings['attempts'] = int(settings_form.data.get('attempts',0))

		if 'topicnumber' not in self.settings:
			self.settings['topicnumber'] = 0

	def create_game(self, request, **init_kwargs):

		# Grab form POST data, or URL GET data.
		#
		settings, settings_form, is_new_game = self.getSettingsForm(request,
										initial_kwargs=init_kwargs)

		# Apply whatever additional settings need to be made
		#
		self.additional_settings(settings_form)

		# Create the game class. If the game is new, self.settings will not
		# contain any word or wordform data, and thus GameClass will select
		# random words and create the question/answers.  If a game is in
		# progress, it will reselect the existing values from the game form,
		# and check whether or not the answers are correct or incorrect.
		#
		game = self.GameClass(self.settings)

		if is_new_game:
			# Set default topic number, clear wordlist.
			#
			game.settings['dialogue'] = settings_form.data.get('dialogue', '')
			game.settings['topicnumber'] = 0
			game.settings['wordlist'] = ""
			game.settings['attempts'] = 0
			game.num_fields = 1
			game.update_game(1)
		else:
			game.num_fields = int(settings_form.data.get('num_fields', 1))

			game.check_game(settings_form.data)
			#game.get_score(settings_form.data)

			if "show_correct" in settings_form.data:
				game.show_correct = 1

			# If the last answer was correct, add new field
			#
			if game.form_list[game.num_fields-2].error == "correct":
				game.update_game(
					len(game.form_list)+1,
					game.form_list[game.num_fields-2])
				game.settings['attempts'] = 0
			else:
				game.settings['attempts'] = game.settings['attempts'] + 1

		self.set_gamename()

		settings_form.init_hidden(
			game.settings['topicnumber'],
			game.num_fields,
  			game.settings['dialogue'],
  			game.settings['image'],
  			game.settings['wordlist'],
  			game.settings['attempts'])
  		#print game.num_fields," nr of attempts ",game.settings['attempts']

		return self.context(request, game, settings_form)


	def context(self, request, game, settings_form):
		self.register_logs(request, game, settings_form)

		def getmessages(g):
			if len(g.form_list) > 0:
				return g.form_list[-1].messages
			else:
				return []

		errormsg = ""
		for f in game.form_list:
			errormsg = errormsg + f.errormsg

		c = {
			'settingsform': settings_form,
			'settings': self.settings,
			'forms': game.form_list,
			'messages': getmessages(game),
			'errormsg': errormsg,
			'count': game.count,
			'attempts': game.settings['attempts'],
			'score': game.score,
			'comment': game.comment,
			'gametype': self.settings['gametype'],
			'topicnumber' : game.settings['topicnumber'],
			'num_fields' : game.num_fields,
			'image' : game.settings['image'],
			'show_correct': game.show_correct,
			'all_correct': game.all_correct,
			'wordlist' : game.settings['wordlist'],
			'dialogue' : game.settings['dialogue'],
			# 'deeplink': self.create_deeplink(game, settings_form),
			'oahpa': 'oahpa.html',
			'lll1': LLL1,
			'hst': hostname,
			}
		return c




@trackGrade("Sahka")
def sahka(request):

	sahkagame = Sahkaview(SahkaSettings, SahkaGame)
	sahkagame.init_settings()

	c = sahkagame.create_game(request)
	return render_to_response(request, 'sahka.html', c)
