from django.template import Context, loader
from forms import *
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from random import randint
from django.utils.translation import ugettext as _
#from django.contrib.admin.views.decorators import _encode_post_data, _decode_post_data
from game import *
from qagame import *

class Info:
    pass

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
            'N-LOC' :  _('Practise locative'),\
            'NUM-ILL' :  _('Practise numerals in illative'),\
            'NUM-ACC' :  _('Practise numerals in accusative'),\
            'NUM-COM' :  _('Practise numerals in comitative'),\
            'NUM-ESS' :  _('Practise numerals in essive'),\
            'NUM-GEN' :  _('Practise numerals in genitive'),\
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
            settings_form = MorphForm(request.POST)
            for k in settings_form.data.keys():
                self.settings[k] = settings_form.data[k]
                #print k, settings_form.data[k]
                
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
            settings_form = MorphForm()
            
            # Find out the default data for this form.
            for k in settings_form.default_data.keys():
                if not self.settings.has_key(k):
                    self.settings[k] = settings_form.default_data[k]
            self.settings['book'] = settings_form.books[settings_form.default_data['book']]

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
            self.settings['gamename'] = self.gamenames[self.settings['adjcase']]

        #print self.settings['gamename']


        c = Context({
            'settingsform': settings_form,
            'settings' : self.settings,
            'forms': game.form_list,
            'count': game.count,
            'score': game.score,
            'all_correct': game.all_correct,
            'show_correct': game.show_correct,
            })
        return c

def mgame_n(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "N"
    mgame.settings['gametype'] = "bare"

    c = mgame.create_mgame(request)
    return render_to_response('mgame_n.html', c)


def mgame_v(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "V"
    mgame.settings['gametype'] = "bare"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_v.html', c)

def mgame_a(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "A"
    mgame.settings['gametype'] = "bare"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_a.html', c)

def mgame_l(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "Num"
    mgame.settings['gametype'] = "bare"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_l.html', c)


### Contextual Morfas

def cmgame_n(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "N"
    mgame.settings['gametype'] = "context"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_n.html', c)


def cmgame_v(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "V"
    mgame.settings['gametype'] = "context"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_v.html', c)

def cmgame_a(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "A"
    mgame.settings['gametype'] = "context"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_a.html', c)

def cmgame_l(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings['pos'] = "Num"
    mgame.settings['gametype'] = "context"
    
    c = mgame.create_mgame(request)
    return render_to_response('mgame_l.html', c)



class Vastaview:

    def init_settings(self):

        show_data=0
        self.settings=Info()
        
    def create_vastagame(self,request):

        count=0
        correct=0

        if request.method == 'POST':
            data = request.POST.copy()
            
            # Settings form is checked and handled.
            settings_form = QAForm(request.POST)

            for k in settings_form.data.keys():
                self.settings[k] = settings_form.data[k]

            self.settings['allsem']=settings_form.allsem
            self.settings.allcase=settings_form.allcase

            if settings_form.data['book']:
                self.settings.book = settings_form.books[settings_form.data['book']]

            self.settings.gametype = "qa"
            # Vasta
            game = QAGame(self.settings)
            game.init_tags()

            game.gametype="qa"

            # If settings are changed, a new game is created
            # Otherwise the game is created using the user input.
            if "settings" in data:
                game.new_game()
            else:
                game.check_game(data)
                game.get_score(data)

            if 'test' in data:
                game.count=1
            if 'show_correct' in data:
                show_correct = 1

        # If there is no POST data, default settings are applied
        else:
            settings_form = QAForm()

            for k in settings_form.default_data.keys():
                self.settings[k] = settings_form.default_data[k]

            # Vasta
            game = QAGame(self.settings)
            game.init_tags()
            game.gametype="qa"

            game.new_game()

        c = Context({
            'settingsform': settings_form,
            'forms': game.form_list,
            'count': game.count,
            'score': game.score,
            'all_correct': game.all_correct,
            'show_correct': game.show_correct,
            })
        return c


def vasta(request):

    vastagame = Vastaview()
    vastagame.init_settings()

    c = vastagame.create_vastagame(request)
    return render_to_response('vasta.html', c)

def vasta_n(request):

    vastagame = Vastaview()
    vastagame.init_settings()
    vastagame.settings['pos']="N"
    
    c = vastagame.create_vastagame(request)
    return render_to_response('vasta.html', c)

            
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
            settings_form = QuizzForm(request.POST)
            for k in settings_form.data.keys():
                if not self.settings.has_key(k):
                    self.settings[k] = settings_form.data[k]

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
            settings_form = QuizzForm()
            self.placename_settings(settings_form)
            
            for k in settings_form.default_data.keys():
                if not self.settings.has_key(k):
                    self.settings[k] = settings_form.default_data[k]

            game = QuizzGame(self.settings)
            game.new_game()


        c = Context({
            'settingsform': settings_form,
            'forms': game.form_list,
            'count': game.count,
            'score': game.score,
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

    return render_to_response('quizz_n.html', c)

def quizz(request):

    quizzgame = Quizzview()
    quizzgame.init_settings()

    c = quizzgame.create_quizzgame(request)
    return render_to_response('quizz.html', c)

def numgame(request):

    mgame = Gameview()
    mgame.init_settings()

    if request.method == 'POST':
        data = request.POST.copy()

        # Settings form is checked and handled.
        settings_form = NumForm(request.POST)
                    
        for k in settings_form.data.keys():
            mgame.settings[k] = settings_form.data[k]

        game = NumGame(mgame.settings)

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
        settings_form = NumForm()
        
        for k in settings_form.default_data.keys():
            mgame.settings[k] = settings_form.default_data[k]

        game = NumGame(mgame.settings)
        game.new_game()


    c = Context({
        'settingsform': settings_form,
        'forms': game.form_list,
        'count': game.count,
        'score': game.score,
        'all_correct': game.all_correct,
        'show_correct': game.show_correct,
    })

    return render_to_response('num.html', c)
