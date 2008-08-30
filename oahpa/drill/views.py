from django.template import Context, loader
from forms import *
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from random import randint
from django.contrib.admin.views.decorators import _encode_post_data, _decode_post_data
from game import *
from qagame import *

class Info:
    pass


class Gameview:

    def init_settings(self):

        show_data=0
        self.settings=Info()
        self.settings.syll = []
        self.settings.pos="N"
        self.settings.case="N-ILL"
        self.settings.mood="Ind"
        self.settings.tense="Prs"
        self.settings.book = []
        self.settings.semtype="NATURE"
        self.settings.language="sme"
        self.settings.gametype="bare"
        self.settings.vtype_bare="PRS"
        self.settings.vtype="VERB"

    def syll_settings(self,settings_form):

        if 'bisyllabic' in settings_form.data:
            self.settings.syll.append('bisyllabic')
        if 'trisyllabic' in settings_form.data:
            self.settings.syll.append('trisyllabic')
        if 'contracted' in settings_form.data:
            self.settings.syll.append('contracted')
        if len(self.settings.syll) == 0:
            self.settings.syll.append('bisyllabic')        


    def create_mgame(self,request):

        count=0
        correct=0

        if request.method == 'POST':
            data = request.POST.copy()
            
            # Settings form is checked and handled.
            settings_form = MorphForm(request.POST)
            
            self.syll_settings(settings_form)
            
            if settings_form.data.has_key('case'):
                self.settings.case= settings_form.data['case']

            if settings_form.data.has_key('vtype'):
                self.settings.vtype= settings_form.data['vtype']

            if settings_form.data.has_key('vtype_bare'):
                self.settings.vtype_bare= settings_form.data['vtype_bare']

            if settings_form.data.has_key('book'):
                self.settings.book = settings_form.books[settings_form.data['book']]
                
            if settings_form.data.has_key('gametype'):
                self.settings.gametype= settings_form.data['gametype']
            self.settings.allcase=settings_form.allcase
            
            # Create game
            if self.settings.gametype == "bare":
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
            self.settings.syll.append('bisyllabic')
            self.settings.syll.append('trisyllabic')
            self.settings.syll.append('contracted')
            self.settings.allcase=settings_form.allcase
            self.settings.book=settings_form.books['all']

            game = BareGame(self.settings)

            game.new_game()

        c = Context({
            'settingsform': settings_form,
            'syllabic': self.settings.syll,
            'forms': game.form_list,
            'count': game.count,
            'gametype': self.settings.gametype,
            'score': game.score,
            'case': self.settings.case,
            'all_correct': game.all_correct,
            'show_correct': game.show_correct,
            })
        return c



def mgame_n(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings.pos = "N"

    c = mgame.create_mgame(request)
    return render_to_response('mgame_n.html', c)


def mgame_v(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings.pos = "V"

    c = mgame.create_mgame(request)
    return render_to_response('mgame_v.html', c)

def mgame_a(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings.pos = "A"

    c = mgame.create_mgame(request)
    return render_to_response('mgame_a.html', c)

def mgame_l(request):

    mgame = Gameview()
    mgame.init_settings()
    mgame.settings.pos = "Num"

    c = mgame.create_mgame(request)
    return render_to_response('mgame_l.html', c)



class Vastaview:

    def init_settings(self):

        show_data=0
        self.settings=Info()
        self.settings.syll = ['bisyllabic', 'trisyllabic', 'contracted']
        self.settings.pos="N"
        self.settings.book = []
        self.settings.semtype='all'
        self.settings.language="sme"
        self.settings.vtype_bare="PRS"
        self.settings.vtype="VERB"

    def create_vastagame(self,request):

        count=0
        correct=0

        if request.method == 'POST':
            data = request.POST.copy()
            
            # Settings form is checked and handled.
            settings_form = QAForm(request.POST)

            self.settings.allsem=settings_form.allsem
            self.settings.allcase=settings_form.allcase

            if settings_form.data.has_key('vtype'):
                self.settings.vtype= settings_form.data['vtype']

            if settings_form.data.has_key('vtype_bare'):
                self.settings.vtype_bare= settings_form.data['vtype_bare']

            if settings_form.data['book']:
                self.settings.book = settings_form.books[settings_form.data['book']]

            self.settings.gametype = "qa"
                        
            # Vasta
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
            settings_form = QAForm()
            self.settings.book=settings_form.books['all']
            self.settings.allsem=settings_form.allsem
            self.settings.allcase=settings_form.allcase
            self.settings.gametype = "qa"

            # Vasta
            game = QAGame(self.settings)
            game.init_tags()
            game.new_game()

        c = Context({
            'settingsform': settings_form,
            'forms': game.form_list,
            'count': game.count,
            'score': game.score,
            #'case': self.settings.case,
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
    vastagame.settings.pos="N"
    
    c = vastagame.create_vastagame(request)
    return render_to_response('vasta.html', c)

            
class Quizzview(Gameview):

    def create_quizzgame(self,request):

        if request.method == 'POST':
            data = request.POST.copy()
            
            # Settings form is checked and handled.
            settings_form = QuizzForm(request.POST)
            
            self.settings.semtype = settings_form.data['semtype']
            self.settings.transtype = settings_form.data['transtype']
            self.settings.book = settings_form.books[settings_form.data['book']]
            self.settings.books = settings_form.books
            
            if settings_form.allsem:
                self.settings.allsem=settings_form.allsem
                
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
            self.settings.allsem=settings_form.allsem
            self.settings.book = settings_form.books['all']
            self.settings.books = settings_form.books
        
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
    quizzgame.settings.transtype="smenob"
    quizzgame.settings.allsem=[]

    quizzgame.settings.semtype = "PLACE-NAME-LEKSA"

    c = quizzgame.create_quizzgame(request)
    return render_to_response('quizz_n.html', c)

def quizz(request):

    quizzgame = Quizzview()
    quizzgame.init_settings()
    quizzgame.settings.transtype="smenob"
    quizzgame.settings.allsem=[]

    c = quizzgame.create_quizzgame(request)
    return render_to_response('quizz.html', c)

def numgame(request):

    mgame = Gameview()
    mgame.init_settings()

    mgame.settings.maxnum = 10
    mgame.settings.numgame = "numeral"
    mgame.settings.book = []
    mgame.settings.semtype=""
    mgame.settings.language="sme"

    if request.method == 'POST':
        data = request.POST.copy()

        # Settings form is checked and handled.
        settings_form = NumForm(request.POST)
        
        mgame.settings.maxnum = settings_form.data['maxnum']
        mgame.settings.numgame = settings_form.data['numgame']
        mgame.settings.language = settings_form.data['language']

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


