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
        self.settings.books=[]
        self.settings.semtype="NATURE"
        self.settings.allbooks=[]
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

            self.settings.books = settings_form.data['book']
                
            if settings_form.allbooks:
                self.settings.allbooks=settings_form.allbooks
                
            if settings_form.data['gametype']:
                self.settings.gametype= settings_form.data['gametype']
                        
            # Create game
            if self.settings.gametype == "bare":
                game = BareGame(self.settings)
            else:
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
            self.settings.books="all"

            if settings_form.allbooks:
                self.settings.allbooks=settings_form.allbooks
            
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


            
def quizz(request):

    mgame = Gameview()
    mgame.init_settings()
    
    mgame.settings.transtype="nobsme"
    mgame.settings.books="all"
    mgame.settings.allbooks=[]
    mgame.settings.allsem=[]

    if request.method == 'POST':
        data = request.POST.copy()

        # Settings form is checked and handled.
        settings_form = QuizzForm(request.POST)
        
        mgame.settings.semtype = settings_form.data['semtype']
        mgame.settings.transtype = settings_form.data['transtype']
        mgame.settings.books = settings_form.data['book']

        if settings_form.allbooks:
            mgame.settings.allbooks=settings_form.allbooks
        if settings_form.allsem:
            mgame.settings.allsem=settings_form.allsem


        game = QuizzGame(mgame.settings)

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
        if settings_form.allbooks:
            mgame.settings.allbooks=settings_form.allbooks
        if settings_form.allsem:
            mgame.settings.allsem=settings_form.allsem
        game = QuizzGame(mgame.settings)
        game.new_game()


    c = Context({
        'settingsform': settings_form,
        'forms': game.form_list,
        'count': game.count,
        'score': game.score,
        'all_correct': game.all_correct,
        'show_correct': game.show_correct,
    })

    return render_to_response('quizz.html', c)


def numgame(request):

    mgame = Gameview()
    mgame.init_settings()

    mgame.settings.maxnum = 10
    mgame.settings.numgame = "numeral"
    mgame.settings.books = []
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


