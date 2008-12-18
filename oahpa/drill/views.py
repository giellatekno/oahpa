from django.template import Context, RequestContext, loader
from forms import *
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from random import randint
from django.utils.translation import ugettext as _
#from django.contrib.admin.views.decorators import _encode_post_data, _decode_post_data
from sahka import *
from game import *
from qagame import *


class Gameview:

    def init_settings(self):

        show_data=0
        self.settings = {}

        self.gamenames = {
            'ATTR' :  _('Practise attributes'),\
            'ATTRPOS' :  _('Practise attributes in positive'),\
            'ATTRCOMP' :  _('Practise attributes in comparative'),\
            'ATTRSUP' :  _('Practise attributes in superlative'),\
            'PREDPOS' :  _('Practise predicative in positive'),\
            'PREDCOMP' :  _('Practise predicative in comparative'),\
            'PREDSUP' :  _('Practise predicative in superlative'),\
            'NUM-ATTR' :  _('Practise numeral attributes'),\
            'NOMPL' :  _('Practise plural'),\
            'N-ILL' :  _('Practise illative'),\
            'N-ACC' :  _('Practise accusative'),\
            'N-COM' :  _('Practise comitative'),\
            'N-ESS' :  _('Practise essive'),\
            'N-GEN' :  _('Practise genitive'),\
            'N-NOM-PL' :  _('Practise plural'),\
            'N-LOC' :  _('Practise locative'),\
            'NUM-ILL' :  _('Practise numerals in illative'),\
            'NUM-ACC' :  _('Practise numerals in accusative'),\
            'NUM-COM' :  _('Practise numerals in comitative'),\
            'NUM-ESS' :  _('Practise numerals in essive'),\
            'NUM-GEN' :  _('Practise numerals in genitive'),\
            'NUM-NOM-PL' :  _('Practise numerals in plural'),\
            'NUM-LOC' :  _('Practise numerals in locative'),\
            'COLL-NUM' :  _('Practise collective numerals'),\
            'PRS'   :  _('Practise present'),\
            'PRT'   : _('Practise past'),\
            'COND'  : _('Practise conditional'), \
            'IMPRT' : _('Practise imperative'),\
            'POT'   : _('Practise potential'), \
            'V-COND'  : _('Practise conditional'), \
            'V-IMPRT' : _('Practise imperative'),\
            'V-POT'   : _('Practise potential') }

        
    def syll_settings(self,settings_form):

        self.settings['syll'] = []
        if 'bisyllabic' in settings_form.data:
            self.settings['syll'].append('bisyllabic')
        if 'trisyllabic' in settings_form.data:
            self.settings['syll'].append('trisyllabic')
        if 'contracted' in settings_form.data:
            self.settings['syll'].append('contracted')
        if len(self.settings['syll']) == 0:
            self.settings['syll'].append('bisyllabic')        


    def create_mgame(self,request):

        count=0
        correct=0


        if request and request.method == 'POST':
            data = request.POST.copy()
            
            #print request.POST
            # Settings form is checked and handled.
            settings_form = MorfaSettings(request.POST)
            for k in settings_form.data.keys():
                self.settings[k] = settings_form.data[k]
				
            if request.session.has_key('dialect'):
                self.settings['dialect'] = request.session['dialect']
                
            self.syll_settings(settings_form)
            if settings_form.data.has_key('book'):
                self.settings['book'] = settings_form.books[settings_form.data['book']]
                
            self.settings['allcase']=settings_form.allcase
                
            # Create game
            if self.settings['gametype'] == "bare":
                game = BareGame(self.settings)
            else:
                # Contextual morfa
                game = QAGame(self.settings)
                game.init_tags()
            
            # If settings are changed, a new game is created
            # Otherwise the game is created using the user input.
            if "settings" in data:
                game.new_game()
            else:
                game.check_game(data)
                game.get_score(data)

            if 'test' in data:
                game.count=1
            if "show_correct" in data:
                show_correct = 1

        # If there is no POST data, default settings are applied
        else:
            settings_form = MorfaSettings()

            # Find out the default data for this form.
            for k in settings_form.default_data.keys():
                if not self.settings.has_key(k):
                    self.settings[k] = settings_form.default_data[k]
            self.settings['book'] = settings_form.books[settings_form.default_data['book']]
				
            if request.session.has_key('dialect'):
                self.settings['dialect'] = request.session['dialect']

            if self.settings['gametype'] == "bare":
                game = BareGame(self.settings)        
            else:
                # Contextual morfa
                game = QAGame(self.settings)
                game.init_tags()
                
            game.new_game()


            
        if self.settings['pos'] == "N":
            if self.settings['gametype'] == "bare":
                self.settings['gamename'] = self.gamenames[self.settings['case']]
            else:
                self.settings['gamename'] = self.gamenames[self.settings['case_context']]
        if self.settings['pos'] == "Num":
            if self.settings['gametype'] == "bare":
                self.settings['gamename'] = self.gamenames[self.settings['adjcase']]
            else:
                self.settings['gamename'] = self.gamenames[self.settings['num_context']]                
        if self.settings['pos'] == "V":
            if self.settings['gametype'] == "bare":
                self.settings['gamename'] = self.gamenames[self.settings['vtype']]
            else:
                self.settings['gamename'] = self.gamenames[self.settings['vtype_context']]
        if self.settings['pos'] == "A":
            if self.settings['gametype'] == "bare":
                self.settings['gamename'] = self.gamenames[self.settings['adjcase']]
            else:
                self.settings['gamename'] = self.gamenames[self.settings['adj_context']]


        c = RequestContext(request, {
            'settingsform': settings_form,
            'settings' : self.settings,
            'forms': game.form_list,
            'count': game.count,
            'score': game.score,
            'comment': game.comment,
            'all_correct': game.all_correct,
            'show_correct': game.show_correct,
            })
        return c


def oahpa(request):

    c = RequestContext(request, {
        'jee': "joku arvo",
        })
    return render_to_response('oahpa_main.html', c, context_instance=RequestContext(request))

def sahka_main(request):

    c = RequestContext(request, {
        'gametype': "sahka",
        })
    return render_to_response('sahka_main.html', c, context_instance=RequestContext(request))


def mgame_n(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "N"
    mgame.settings['gametype'] = "bare"

    c = mgame.create_mgame(request)
    return render_to_response('mgame_n.html', c, context_instance=RequestContext(request))


def mgame_v(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "V"
    mgame.settings['gametype'] = "bare"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_v.html', c, context_instance=RequestContext(request))

def mgame_a(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "A"
    mgame.settings['gametype'] = "bare"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_a.html', c, context_instance=RequestContext(request))

def mgame_l(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "Num"
    mgame.settings['gametype'] = "bare"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_l.html', c, context_instance=RequestContext(request))


### Contextual Morfas

def cmgame_n(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "N"
    mgame.settings['gametype'] = "context"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_n.html', c, context_instance=RequestContext(request))


def cmgame_v(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "V"
    mgame.settings['gametype'] = "context"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_v.html', c, context_instance=RequestContext(request))

def cmgame_a(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "A"
    mgame.settings['gametype'] = "context"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_a.html', c, context_instance=RequestContext(request))


def cmgame_l(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "Num"
    mgame.settings['gametype'] = "context"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_l.html', c, context_instance=RequestContext(request))



class Vastaview:

    def init_settings(self):

        show_data=0
        self.settings = {}
        
    def create_vastagame(self,request):

        count=0
        correct=0

        self.settings['gametype'] = "qa"
        
        if request.method == 'POST':
            data = request.POST.copy()

            # Settings form is checked and handled.
            settings_form = VastaSettings(request.POST)

            for k in settings_form.data.keys():
                self.settings[k] = settings_form.data[k]

            if request.session.has_key('dialect'):
                self.settings['dialect'] = request.session['dialect']

            self.settings['allcase_context']=settings_form.allcase_context
            self.settings['allvtype_context']=settings_form.allvtype_context
            self.settings['allnum_context']=settings_form.allnum_context
            self.settings['alladj_context']=settings_form.alladj_context
            self.settings['allsem']=settings_form.allsem

            if settings_form.data.has_key('book'):
                self.settings['book'] = settings_form.books[settings_form.data['book']]

            # Vasta
            game = QAGame(self.settings)
            game.init_tags()
            game.num_fields = 2

            game.gametype="qa"

            # If settings are changed, a new game is created
            # Otherwise the game is created using the user input.
            if "settings" in data:
                game.new_game()
            else:
                game.check_game(data)
                game.get_score(data)

        # If there is no POST data, default settings are applied
        else:
            settings_form = VastaSettings()

            self.settings['allsem']=settings_form.allsem
            self.settings['allcase_context']=settings_form.allcase_context
            self.settings['allvtype_context']=settings_form.allvtype_context
            self.settings['allnum_context']=settings_form.allnum_context
            self.settings['alladj_context']=settings_form.alladj_context

            for k in settings_form.default_data.keys():
                self.settings[k] = settings_form.default_data[k]

            if request.session.has_key('dialect'):
                self.settings['dialect'] = request.session['dialect']

            # Vasta
            game = QAGame(self.settings)
            game.init_tags()
            game.gametype="qa"
            game.num_fields = 2

            game.new_game()


        c = Context({
            'settingsform': settings_form,
            'forms': game.form_list,
            'messages': game.form_list[0].messages,
            'count': game.count,
            'score': game.score,
            'comment': game.comment,
            })
        return c


def vasta(request):

    vastagame = Vastaview()
    vastagame.init_settings()

    c = vastagame.create_vastagame(request)
    return render_to_response('vasta.html', c, context_instance=RequestContext(request))

            
class Quizzview(Gameview):

    def placename_settings(self, settings_form):

        self.settings['frequency'] = []
        self.settings['geography']= []

        if 'common' in settings_form.data:
            self.settings['frequency'].append('common')
        if 'rare' in settings_form.data:
            self.settings['frequency'].append('rare')
        if 'world' in settings_form.data:
            self.settings['geography'].append('world')
        if 'sapmi' in settings_form.data:
            self.settings['geography'].append('sapmi')

        if len(self.settings['frequency']) == 0:
            self.settings['frequency'].append('common')        
        if len(self.settings['geography']) == 0:
            self.settings['geography'].append('sapmi')        


    def create_quizzgame(self,request):

        if request.method == 'POST':
            data = request.POST.copy()

            # Settings form is checked and handled.
            settings_form = QuizzSettings(request.POST)
            for k in settings_form.data.keys():
                if not self.settings.has_key(k):
                    self.settings[k] = settings_form.data[k]

            if request.session.has_key('dialect'):
                self.settings['dialect'] = request.session['dialect']

            self.placename_settings(settings_form)
            self.settings['allsem']=settings_form.allsem
            self.settings['book'] = settings_form.books[settings_form.data['book']]
            
            game = QuizzGame(self.settings)
                
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
            settings_form = QuizzSettings()
            self.placename_settings(settings_form)
            
            for k in settings_form.default_data.keys():
                if not self.settings.has_key(k):
                    self.settings[k] = settings_form.default_data[k]

            if request.session.has_key('dialect'):
                self.settings['dialect'] = request.session['dialect']

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

def quizz_n(request):

    quizzgame = Quizzview()
    quizzgame.init_settings()
    quizzgame.settings['allsem']=[]
    quizzgame.settings['semtype'] = "PLACE-NAME-LEKSA"

    c = quizzgame.create_quizzgame(request)
    return render_to_response('quizz_n.html', c, context_instance=RequestContext(request))

def quizz(request):

    quizzgame = Quizzview()
    quizzgame.init_settings()

    c = quizzgame.create_quizzgame(request)
    return render_to_response('quizz.html', c, context_instance=RequestContext(request))


class Numview(Gameview):
    
    def create_numgame(self,request):
        
        if request.method == 'POST':
            data = request.POST.copy()
            
            # Settings form is checked and handled.
            settings_form = NumSettings(request.POST)
            
            for k in settings_form.data.keys():
                if not self.settings.has_key(k):
                    self.settings[k] = settings_form.data[k]
                
            if request.session.has_key('dialect'):
                self.settings['dialect'] = request.session['dialect']


            game = NumGame(self.settings)
                
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
            settings_form = NumSettings()
        
            for k in settings_form.default_data.keys():
                if not self.settings.has_key(k):
                    self.settings[k] = settings_form.default_data[k]

            game = NumGame(self.settings)
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

def num(request):

    numgame = Numview()
    numgame.init_settings()
    numgame.settings['gametype'] = "ord"
    
    c = numgame.create_numgame(request)
    return render_to_response('num.html', c, context_instance=RequestContext(request))

def num_ord(request):

    numgame = Numview()
    numgame.init_settings()
    numgame.settings['gametype'] = "card"
    
    c = numgame.create_numgame(request)
    return render_to_response('num_ord.html', c, context_instance=RequestContext(request))


class Sahkaview:

    def init_settings(self):

        show_data=0
        self.settings = {}
        
    def create_sahkagame(self,request):

        count=0
        correct=0

        self.settings['gametype'] = "sahka"
        if request.session.has_key('dialect'):
            self.settings['dialect'] = request.session['dialect']

        # With post data, continue the dialogue
        if request.method == 'POST':
            data = request.POST.copy()
            # Settings form is checked and handled.
            settings_form = SahkaSettings(request.POST)

            for k in settings_form.data.keys():
                self.settings[k] = settings_form.data[k]

            # Vasta
            game = SahkaGame(self.settings)

            # If settings are changed, a new game is created
            # Otherwise the game is created using the user input.
            if "settings" in data:
                game.settings['topicnumber']=0
                game.settings['image']="sahka.png"
                game.settings['wordlist']=""
                game.num_fields=1
                game.update_game(1)
            else:
                game.num_fields = int(settings_form.data['num_fields'])
                #print "num_fields", game.num_fields
                game.check_game(data)
                # If the last answer was correct, add new field
                if game.form_list[game.num_fields-2].error == "correct":
                    game.update_game(len(game.form_list)+1, game.form_list[game.num_fields-2])

            settings_form.init_hidden(game.settings['topicnumber'],game.num_fields,\
									  game.settings['dialogue'],game.settings['image'],game.settings['wordlist'])

            errormsg=""
            for f in game.form_list:
                errormsg = errormsg + f.errormsg
                
            c = Context({
                'settingsform': settings_form,
                'forms': game.form_list,
                'messages': game.form_list[-1].messages,
                'errormsg': errormsg,
                'count': game.count,
                'score': game.score,
                'comment': game.comment,
                'topicnumber' : game.settings['topicnumber'],
                'num_fields' : game.num_fields,
                'gametype' : "sahka",
                'image' : game.settings['image'],
                'wordlist' : game.settings['wordlist'],
                'dialogue' : game.settings['dialogue'],
                })
            return c

        # If there is no POST data, present the dialogue selection page
        else:
            settings_form = SahkaSettings()
            for k in settings_form.default_data.keys():
                self.settings[k] = settings_form.default_data[k]

            if request.session.has_key('dialect'):
                self.settings['dialect'] = request.session['dialect']

            c = Context({
                'settingsform': settings_form,
                'gametype' : "sahka",
                })
            return c


def sahka(request):

    sahkagame = Sahkaview()
    sahkagame.init_settings()

    c = sahkagame.create_sahkagame(request)
    return render_to_response('sahka.html', c, context_instance=RequestContext(request))

            
