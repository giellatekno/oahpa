from django.template import Context, loader
from forms import *
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from random import randint
from django.contrib.admin.views.decorators import _encode_post_data, _decode_post_data
from game import *
#from qagame import *


class Info:
    pass

def mgame(request):
    
    count=0
    correct=0

    show_data=0
    settings = Info()
    settings.syll = []
    settings.partofsp="N"
    settings.books=[]
    gametype="bare"
    settings.semtype="NATURE"
    settings.allbooks=[]

    if request.method == 'POST':
        data = request.POST.copy()

        # Settings form is checked and handled.
        settings_form = MorphForm(request.POST)
        
        if 'bisyllabic' in settings_form.data:
            settings.syll.append('bisyllabic')
        if 'trisyllabic' in settings_form.data:
            settings.syll.append('trisyllabic')
        if 'contracted' in settings_form.data:
            settings.syll.append('contracted')
        if len(settings.syll) == 0:
            settings.syll.append('bisyllabic')

        if settings_form.data['pos']:
            settings.partofsp= settings_form.data['pos']

        settings.books = settings_form.data['book']

        if settings_form.allbooks:
            settings.allbooks=settings_form.allbooks

        if settings_form.data['gametype']:
            settings.gametype= settings_form.data['gametype']

        # Create game
        if gametype == "bare":
            game = BareGame(settings)
        else:
            game = ContextGame(settings)

        # If settings are changed, a new game is created
        # Otherwise the game is created using the user input.
        if "settings" in data:
            game.new_game()
        else:
            game.check_game(data)
            game.get_score(data)

        print "OK"
        if 'test' in data:
            game.count=1
        if "show_correct" in data:
            show_correct = 1

    # If there is no POST data, default settings are applied
    else:
        settings_form = MorphForm()
        settings.syll.append('bisyllabic')
        settings.books="all"

        if settings_form.allbooks:
            settings.allbooks=settings_form.allbooks

            
        game = BareGame(settings)
        game.new_game()

    c = Context({
        'settingsform': settings_form,
        'syllabic': settings.syll,
        'forms': game.form_list,
        'count': game.count,
        'gametype': gametype,
        'score': game.score,
        'all_correct': game.all_correct,
        'show_correct': game.show_correct,
    })
    return render_to_response('mgame.html', c)


            
def quizz(request):

    settings = Info()
    settings.semtype="NATURE"
    settings.transtype="nobsme"
    settings.books="all"
    settings.allbooks=[]
    settings.allsem=[]

    if request.method == 'POST':
        data = request.POST.copy()

        # Settings form is checked and handled.
        settings_form = QuizzForm(request.POST)
        
        settings.semtype = settings_form.data['semtype']
        settings.transtype = settings_form.data['transtype']
        settings.books = settings_form.data['book']

        if settings_form.allbooks:
            settings.allbooks=settings_form.allbooks
        if settings_form.allsem:
            settings.allsem=settings_form.allsem


        game = QuizzGame(settings)

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
            settings.allbooks=settings_form.allbooks
        if settings_form.allsem:
            settings.allsem=settings_form.allsem
        game = QuizzGame(settings)
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

    settings = Info()
    settings.maxnum = 10
    settings.numgame = "numeral"
    settings.books = []
    settings.semtype=""

    if request.method == 'POST':
        data = request.POST.copy()

        # Settings form is checked and handled.
        settings_form = NumForm(request.POST)
        
        settings.maxnum = settings_form.data['maxnum']
        settings.numgame = settings_form.data['numgame']

        game = NumGame(settings)

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
        game = NumGame(settings)
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


def qagame(request):

    settings = Info()
    settings.maxnum = 10
    settings.numgame = "numeral"

    if request.method == 'POST':
        data = request.POST.copy()

        # Settings form is checked and handled.
        settings_form = NumForm(request.POST)
        
        settings.maxnum = settings_form.data['maxnum']
        settings.numgame = settings_form.data['numgame']

        game = QAGame(settings)
        game.init_tags()

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
        settings_form = QAForm()
        game = QAGame(settings)
        game.init_tags()
        game.new_game()


    c = Context({
        'settingsform': settings_form,
        'forms': game.form_list,
        'count': game.count,
        'score': game.score,
        'all_correct': game.all_correct,
        'show_correct': game.show_correct,
    })

    return render_to_response('qa.html', c)

