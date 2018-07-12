from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')
tls = importlib.import_module(LLL1+'_oahpa.conf.tools')

from django.template import Context, RequestContext, loader
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response, render
from django.utils.translation import ugettext_lazy as _

switch_language_code = tls.switch_language_code

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

# TODO:
# from courses.views import render_to_response
# from courses.decorators import trackGrade
# TODO: comment back in decorator
# TODO: forms requires some additional things for courses gamename
#       tracking

def index(request):
	c = {
		'jee': "joku arvo",
		}
	return render(request, LLL1+'_oahpa_main.html', c)

### def updating(request):
### 	c = RequestContext(request, {
### 		'jee': "joku arvo",
### 		})
### 	return render_to_response('updating.html', c,
### 				context_instance=RequestContext(request))


### class Gameview:
### 	""" A class for handling POST and GET requests, setting up context
### 	variables for the view, and calling the corresponding game object to the
### 	view.
###
### 	This class mainly handles Morfa, but is subclassed for Leksa and Numra.
### 	"""
###
### 	def init_settings(self):
###
### 		show_data=0
### 		self.settings = {}
###
### 		# A list of key value pairs for displaying pretty names in the forms
### 		# value is sent through gettext for localization.
### 		self.gamenames = {
### 			'ATTR' :  _('Practise attributes'),
### 			'A-ATTR' :  _('Practise attributes'),
### 			'A-COMP' :  _('Practise comparative'),
### 			'A-SUPERL' :  _('Practise superlative'),
### 			'ATTRPOS' :  _('Practise attributes in positive'),
### 			'ATTRCOMP' :  _('Practise attributes in comparative'),
### 			'ATTRSUP' :  _('Practise attributes in superlative'),
### 			'PREDPOS' :  _('Practise predicative in positive'),
### 			'PREDCOMP' :  _('Practise predicative in comparative'),
### 			'PREDSUP' :  _('Practise predicative in superlative'),
### 			'NUM-ATTR' :  _('Practise numeral attributes'),
### 			'NOMPL' :  _('Practise plural'),
### 			'NOM' :  _('Practise nominative'),
### 			'N-NOM' :  _('Practise nominative'),
### 			'N-ILL' :  _('Practise illative'),
### 			'N-ACC' :  _('Practise accusative'),
### 			'N-COM' :  _('Practise comitative'),
### 			'N-ESS' :  _('Practise essive'),
### 			'N-GEN' :  _('Practise genitive'),
### 			'N-NOM-PL' :  _('Practise plural'),
### 			'N-INE' :  _('Practise inessive'),
### 			'N-ELA' :  _('Practise elative'),
### 			'N-MIX' :  _('Practise a mix'),
### 			'V-MIX' :  _('Practise a mix'),
### 			'A-MIX' :  _('Practise a mix'),
### 			'P-MIX' :  _('Practise a mix'),
### 			'NUM-ILL' :  _('Practise numerals in illative'),
### 			'NUM-ACC' :  _('Practise numerals in accusative'),
### 			'NUM-COM' :  _('Practise numerals in comitative'),
### 			'NUM-ESS' :  _('Practise numerals in essive'),
### 			'NUM-GEN' :  _('Practise numerals in genitive'),
### 			'NUM-NOM-PL' :  _('Practise numerals in plural'),
### 			'NUM-LOC' :  _('Practise numerals in locative'),
### 			'COLL-NUM' :  _('Practise collective numerals'),
### 			'ORD-NUM' :  _('Practise ordinal numbers'),
### 			'PRS'   :  _('Practise present'),
### 			'PRT'   : _('Practise past'),
### 			'PRF'   : _('Practise perfect'),
### 			'GER'   : _('Practise gerund'),
### 			'COND'  : _('Practise conditional'),
### 			'IMPRT' : _('Practise imperative'),
### 			'POT'   : _('Practise potential'),
### 			'V-PRS'   :  _('Practise present'),
### 			'V-PRT'   : _('Practise past'),
### 			'V-PRF'   : _('Practise perfect'),
### 			'V-GER'   : _('Practise gerund'),
### 			# 'V-COND'  : _('Practise conditional'),
### 			'V-IMPRT' : _('Practise imperative'),
### 			'V-POT'   : _('Practise potential'),
### 			'P-ACC'  : _('Practise accusative'),
### 			'P-COM'  : _('Practise comitative'),
### 			'P-ELA'  : _('Practise elative'),
### 			'P-GEN'  : _('Practise genitive'),
### 			'P-NOM'  : _('Practise nominative'),
### 			'P-ILL'  : _('Practise illative'),
### 		}
###
###
### 	def syll_settings(self,settings_form):
### 		""" Convert settings form values to values that are in the database.
### 		"""
### 		converted_values = {
### 			'bisyllabic': '2syll',
### 			'trisyllabic': '3syll',
### 			'xsyllabic': 'xsyllabic', # not in use in sma
### 			'xsyllabic': 'xsyll', 		# in use in sma
### 		}
###
### 		# If the key is in the settings form, then this option has been set to
### 		# true, otherwise it is not.
###
### 		self.settings['syll'] = [v for k, v in converted_values.items()
### 										if k in settings_form.data]
###
###
### 	def create_morfagame(self, request):
### 		""" Handle the request, and return context variables for the response.
###
### 		Although users are likely to interact with this function by posting
### 		data to the form, we check GET and copy the data over. This is so that
### 		instructors of external courses can create deep links to individual
### 		exercizes.
###
### 		A lot of this code is shared with Quizzview.create_leksagame, so at
### 		some point it might be nice to combine them. In the mean time, changes
### 		made here may need to be done in the corresponding Quizzview method.
### 		"""
###
### 		count, correct = 0, 0
### 		settings_form = MorfaSettings(request.GET)
###
### 		if request.method == 'GET' and len(settings_form.data.keys()) > 0:
### 			post_like_data = request.GET.copy()
### 			if not 'book' in post_like_data:
### 				post_like_data['book'] = 'all'
### 		else:
### 			post_like_data = False
###
### 		# So can I get GET data to make changes to form, but I can't get it to
### 		# load the game with this data.  reason is logic is forked into
### 		# POST/GET, not POST & has game data
###
### 		if request.method == 'POST' or post_like_data:
### 			if post_like_data:
### 				data = post_like_data
### 			else:
### 				data = request.POST.copy()
###
### 			# Settings form is checked and handled.
### 			settings_form = MorfaSettings(data)
###
### 			for k in settings_form.data.keys():
### 				self.settings[k] = settings_form.data[k]
###
### 			if request.session.has_key('dialect'):
### 				self.settings['dialect'] = request.session['dialect']
###
### 			if hasattr(request, 'LANGUAGE_CODE'):
### 				self.settings['language'] = request.LANGUAGE_CODE
###
### 			self.syll_settings(settings_form)
### 			if settings_form.data.has_key('source'):
### 				formsource = settings_form.data['source']
### 				self.settings['source'] = settings_form.source[formsource]
###
### 			self.settings['allcase'] = settings_form.allcase
###
### 			# Create game
### 			if self.settings['gametype'] == "bare":
### 				game = BareGame(self.settings)
### 			else:
### 				# Contextual morfa
### 				game = QAGame(self.settings)
### 				game.init_tags()
###
### 			# If settings are changed, a new game is created
### 			# Otherwise the game is created using the user input.
###
### 			if "settings" in data or post_like_data:
### 				game.new_game()
### 			else:
### 				game.check_game(data)
### 				game.get_score(data)
###
### 			if 'test' in data:
### 				game.count = 1
### 			if "show_correct" in data:
### 				show_correct = 1
###
### 		# If there is no POST data, default settings are applied
### 		else:
### 			settings_form = MorfaSettings()
###
### 			# Find out the default data for this form.
### 			for k in settings_form.default_data.keys():
### 				if not self.settings.has_key(k):
### 					self.settings[k] = settings_form.default_data[k]
###
### 			if self.settings['pos'] != 'Pron':
### 				self.settings['source'] = settings_form.default_data['source']
###
### 			if request.session.has_key('dialect'):
### 				self.settings['dialect'] = request.session['dialect']
###
### 			if hasattr(request, 'LANGUAGE_CODE'):
### 				self.settings['language'] = request.LANGUAGE_CODE
###
### 			if self.settings['gametype'] == "bare":
### 				game = BareGame(self.settings)
### 			else:
### 				# Contextual morfa
### 				game = QAGame(self.settings)
### 				game.init_tags()
### 			game.new_game()
###
### 		PoS, gametype = self.settings['pos'], self.settings['gametype']
###
### 		# The keys referenced here on self.settings correspond to the name of
### 		# the game type, e.g., N-ILL, ATTR, V-PRS, which are set on the form.
### 		# The following code gets these keys, and grabs the corresponding
### 		# gettext'd string.
###
### 		gametype_PoS_settings = {
### 			("bare", "N"): 			self.settings.get('case', False),
### 			("context", "N"): 		self.settings.get('case_context', False),
###
### 			("bare", "Pron"):		self.settings.get('proncase', False),
### 			("context", "Pron"):	self.settings.get('pron_context', False),
###
### 			("bare", "Num"): 		self.settings.get('num_bare', False),
### 			("context", "Num"): 	self.settings.get('num_context', False),
###
### 			("bare", "V"): 			self.settings.get('vtype', False),
### 			("context", "V"): 		self.settings.get('vtype_context', False),
###
### 			("bare", "A"): 			self.settings.get('adjcase', False),
### 			("context", "A"): 		self.settings.get('adj_context', False),
### 		}
###
### 		gamename_key = gametype_PoS_settings[(gametype, PoS)]
### 		self.settings['gamename'] = self.gamenames[gamename_key]
###
### 		c = RequestContext(request, {
### 			'settingsform': settings_form,
### 			'settings' : self.settings,
### 			'forms': game.form_list,
### 			'count': game.count,
### 			'score': game.score,
### 			'comment': game.comment,
### 			'all_correct': game.all_correct,
### 			'show_correct': game.show_correct,
### 			'language' : self.settings['language'],
### 			})
### 		return c

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

		### def safeGetValue(name, v):
		### 	if name == 'wordclass':
		### 		widget = settings_form.fields[name].widget
		### 		wc_val = widget.value_from_datadict(settings_form.data,
		### 											settings_form.files,
		### 											name)
		### 		if wc_val:
		### 			if len(wc_val) > 0:
		### 				if type(wc_val[0]) == list:
		### 					wc_val = wc_val[0]
		### 					return '+'.join(wc_val)
		### 				return '+'.join(wc_val)
		### 		return ''
		### 	else:
		### 		return v

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

		if request.session.has_key('country'):
			self.settings['user_country'] = request.session['country']
		else:
			self.settings['user_country'] = False

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
			}


#def sma_oahpa(request):
	""" The front page view. """

#	c = {
#		'jee': "joku arvo",
	#	}

	#return render(request, LLL1+'_oahpa_main.html', c)



# @trackGrade("Leksa")
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
		if sess_lang == 'sma':
			sess_lang = 'nob'
	else:
		sess_lang = 'nob'

	default_langpair = 'sma%s' % sess_lang
	print 'default_langpair=', default_langpair

	c = leksagame.create_game(request, initial_transtype=default_langpair)

	return render(request, template, c)

###
###  Numra
###
###

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
		 #   'numstring': numstring,
			}


# @trackGrade("Numra clock")
def num_clock(request):

	numgame = Numview(KlokkaSettings, Klokka)
	# numgame.settings['gametype'] = clocktype

	c = numgame.create_game(request)

	return render(request, 'clock.html', c)

# @trackGrade("Numra ordinal")
def num_ord(request):

	numgame = Numview(NumSettings, NumGame)
	numgame.settings['gametype'] = "ord"

	c = numgame.create_game(request)

	return render(request, 'num_ord.html', c)


# @trackGrade("Numra cardinal")
def num(request):
	numgame = Numview(NumSettings, NumGame)
	numgame.settings['gametype'] = "card"

	c = numgame.create_game(request)

	return render(request, 'num.html', c)

# @trackGrade("Numra dato")
def dato(request):

	datogame = Numview(DatoSettings, Dato)

	c = datogame.create_game(request)

	return render(request, 'dato.html', c)


###
### Morfa views
###
###

class Morfaview(Gameview):
	gamenames = {
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
        'N-INE' :  _('Practise inessive'),
        'N-ELA' :  _('Practise elative'),
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
        'P-ELA'  : _('Practise elative'),
        'P-GEN'  : _('Practise genitive'),
        'P-NOM'  : _('Practise nominative'),
        'P-ILL'  : _('Practise illative'),
	}

	def syll_settings(self,settings_form):

		def true_false_filter(val):
			if val in ['on', 'On', u'on', u'On']:
				return True
			else:
				return False

		bisyl = settings_form.data.get('bisyllabic', None)
		trisyl = settings_form.data.get('trisyllabic', None)
		xsyl = settings_form.data.get('xsyllabic', None)

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
		if true_false_filter(xsyl):
			self.settings['syll'].append('xsyll')
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
				return ['case', 'bisyllabic', 'trisyllabic', 'xsyllabic',
						'book',]
			if self.settings['pos'] == 'V':
				return ['vtype'] + [a for a, _ in settings_form.wordclass_names]
			if self.settings['pos'] == 'A':
				return ['adjcase', 'bisyllabic', 'trisyllabic', 'xsyllabic',
						'xsyllabic', 'book',]
			if self.settings['pos'] == 'Pron':
				return ['proncase']
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
				return ['pron_context', 'wordform_type']
			if self.settings['pos'] == 'Num':
				return ['num_context']


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
			'language' : self.settings['language'],
			'deeplink': self.create_deeplink(game, settings_form),
			}

	### def wordclass_settings(self, settings_form):
	### 	""" Ugly hack, because for some reason Django will only return the last
	### 	value in the list otherwise, however if we get it through the
	### 	widget, it does work.
	### 	"""
	### 	widget = settings_form.fields['wordclass'].widget
	### 	wc_val = widget.value_from_datadict(settings_form.data,
	### 										settings_form.files,
	### 										'wordclass')
	### 	# For some reason a null value is [None], not [] as specified in
	### 	# docs, and when form is not present, value_from_datadict
	### 	# returns None
	### 	if wc_val is not None:
	### 		if len(wc_val) > 0:
	### 			if wc_val[0] == None:
	### 				wc_val = False
	### 	else:
	### 		wc_val = False
	### 	self.settings['wordclass'] = wc_val

	def wordclass_settings(self, settings_form):
		wordclass_names = settings_form.wordclass_names

		# TODO: on / True normalization
		def true_false_filter(val):
			if val in ['on', 'On', u'on', u'On']:
				return True
			else:
				return False

		if 'wordclass' not in self.settings:
			self.settings['wordclass'] = []

		for name, v in wordclass_names:
			val = settings_form.data.get(name, None)
			if val is not None:
				if true_false_filter(val):
					self.settings['wordclass'].append(v)
					settings_form.data[name] = 'on'
				else:
					settings_form.data[name] = None

		self.settings['wordclass'] = list(set(self.settings['wordclass']))

	def additional_settings(self, settings_form):

		self.settings['allcase'] = settings_form.allcase
		self.settings['wordclasses'] = settings_form.wordclasses
		self.wordclass_settings(settings_form)
		self.syll_settings(settings_form)
        # NOTE: not present in sma
		# self.settings['allnum_type'] = settings_form.allnum_type  # added by Heli

    ### TODO: set gamename for sma, test all.
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
				# NOTE: not in sma
                # subname = self.settings['pron_type'] # dem, recipr, etc.
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
				gamename_key = self.settings['vtype_context']

		# ATTR - COMP
		if self.settings['pos'] == "A":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['adjcase']
			else:
				gamename_key = self.settings['adj_context']

		# A-DER-V
		if self.settings['pos'] == "Der":
			if self.settings['gametype'] == "bare":
				gamename_key = self.settings['derivation_type']
			else:
				gamename_key = self.settings['derivation_type_context']

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

		self.settings['gamename_key'] = ' - '.join(names)


# @trackGrade("Morfa")
def morfa_game(request, pos):
	"""
		View for Morfa game. Requires pos argument, ['N', 'V', 'A', 'Num']
	"""
	# print >> PTS, request.path
	# print >> PTS, request.path_info
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

	return render(request, template, c)



###
### Contextual Morfas / Morfa-C
###
###

# @trackGrade("Contextual Morfa")
def cmgame(request, pos):

	mgame = Morfaview(MorfaSettings, QAGame)

	mgame.settings['pos'] = pos.capitalize()
	mgame.settings['gametype'] = "context"

	if pos in ['Num', 'num']:
		p = 'l'
	elif pos == 'Der':
		p = 'der'
	else:
		p = pos.lower()[0]

	template = "mgame_%s.html" % p
	c = mgame.create_game(request)

	return render(request, template, c)

# vim: set ts=4 sw=4 tw=72 syntax=python noexpandtab :
