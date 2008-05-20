# -*- coding: utf-8 -*-
import string
import sys
from django import newforms as forms
from django.http import Http404
from django.db.models import Q
from django.utils.translation import gettext as _
from models import Word, Form, Question

POS_CHOICES = (
    ('N', _('noun')),
    ('V', _('verb')),
#    ('A', _('adjective')),
)

BOOK_CHOICES = (
    ('d1', _('Davvin 1')),
    ('d2', _('Davvin 2')),
    ('d3', _('Davvin 3')),
    ('d4', _('Davvin 4')),
    ('álgu', _('algu')),
    ('sárá', _('sara')),
    ('bures', _('Bures')),
    ('oaidnalit', _('Oaidnalid')),
    ('all', _('All')),
)

GAME_CHOICES = (
    ('bare', _('bare')),
    ('context', _('context')),
)

TRANS_CHOICES = (
    ('nobsme', _('Norwegian to North Sami')),
    ('smenob', _('North Sami to Norwegian')),
)

SEMTYPE_CHOICES = (
    ('NATURE', _('nature')),
    ('PROFESSION', _('profession')),
    ('FAMILY', _('family')),
    ('all', _('all')),
)

NUM_CHOICES = (
    ('10', _('0-10')),
    ('20', _('0-20')),
    ('100', _('0-100')),
    ('1000', _('0-1000')),
#    ('ALL', _('all')),
)

NUMGAME_CHOICES = (
    ('numeral', _('Numeral to string')),
    ('string', _('String to numeral')),
)



def is_correct(self):
    """
    Determines if the given answer is correct (for a bound form).
    """
    if not self.is_valid():
        return False

    self.userans = self.cleaned_data['answer']

    self.error = "error"
    for item in self.correct_anslist:
        if self.cleaned_data['answer'] == item:
            self.error = "correct"

            
def set_correct(self):
    """
    Adds correct wordforms to the question form.
    """    
    for e in self.correct_anslist:
        self.correct_answers += " "+e
        

class MorphForm(forms.Form):
    pos = forms.ChoiceField(initial='N', choices=POS_CHOICES, widget=forms.RadioSelect)
    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.RadioSelect)
    gametype = forms.ChoiceField(initial='bare', choices=GAME_CHOICES, widget=forms.RadioSelect)
    bisyllabic = forms.BooleanField(required=False, initial='1')
    trisyllabic = forms.BooleanField(required=False,initial='1')
    contracted = forms.BooleanField(required=False,initial='1')
    default_data = {'pos': 'N'}
    allbooks = []
    for b in BOOK_CHOICES:
        print b[0]
        allbooks.append(b[0])

class MorphQuestion(forms.Form):
    """
    Questions for morphology game 
    """
    is_correct = is_correct
    set_correct = set_correct

    answer = forms.CharField()

    def __init__(self, word, tag, fullforms, tr_list, question, userans_val, correct_val, *args, **kwargs):

        #print >> sys.stderr, userans_val
        #print >> sys.stderr, correct_val
        #sys.stderr.flush()

        lemma_widget = forms.HiddenInput(attrs={'value' : word.id})
        tag_widget = forms.HiddenInput(attrs={'value' : tag.id})

        super(MorphQuestion, self).__init__(*args, **kwargs)
        self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
        self.fields['tag_id'] = forms.CharField(widget=tag_widget, required=False)

        self.lemma = word.lemma
        self.correct_answers =""
        self.userans = userans_val
        self.correct_anslist = []
        self.error="empty"
        self.translations = []
        for item in tr_list:
            self.translations.append(item.translation)
        
        for item in fullforms:
            self.correct_anslist.append(item.fullform)

        if question:
            self.question = question.question
            question_widget = forms.HiddenInput(attrs={'value' : question.id})
            self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)
        else:
            self.tag = tag.string

        self.is_correct()

        # set correct and error values
        if correct_val == "correct":
            print "settings correct.. "
            self.error="correct"

class QuizzForm(forms.Form):
    semtype = forms.ChoiceField(initial='all', choices=SEMTYPE_CHOICES, widget=forms.RadioSelect)
    transtype = forms.ChoiceField(initial='smenob', choices=TRANS_CHOICES, widget=forms.RadioSelect)
    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.RadioSelect)
    allbooks = []
    for b in BOOK_CHOICES:
        print b[0]
        allbooks.append(b[0])
    allsem = []
    for b in SEMTYPE_CHOICES:
        print b[0]
        allsem.append(b[0])        

class QuizzQuestion(forms.Form):
    """
    Questions for word quizz
    """
    answer = forms.CharField()

    is_correct = is_correct
    set_correct = set_correct
    
    def __init__(self, word, translations, question, userans_val, correct_val, *args, **kwargs):

        lemma_widget = forms.HiddenInput(attrs={'value' : word.id})
        super(QuizzQuestion, self).__init__(*args, **kwargs)
        self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
        if question:
            self.question = question.question
            question_widget = forms.HiddenInput(attrs={'value' : question.id})
            self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)
        self.lemma = word.lemma
        self.userans = userans_val
        self.correct_anslist = []
        self.correct_answers =""
        self.error="empty"

        for item in translations:
            self.correct_anslist.append(item.translation)

        self.is_correct()

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"
        if correct_val == "error":
            self.error="error"

class NumForm(forms.Form):
    maxnum = forms.ChoiceField(initial='10', choices=NUM_CHOICES, widget=forms.RadioSelect)
    numgame = forms.ChoiceField(initial='numeral', choices=NUMGAME_CHOICES, widget=forms.RadioSelect)

class NumQuestion(forms.Form):
    """
    Questions for numeral quizz
    """
    answer = forms.CharField()

    is_correct = is_correct
    set_correct = set_correct
    
    def __init__(self, numeral, num_string, num_list, gametype, userans_val, correct_val, *args, **kwargs):

        numeral_widget = forms.HiddenInput(attrs={'value' : numeral})
        super(NumQuestion, self).__init__(*args, **kwargs)
        self.fields['numeral_id'] = forms.CharField(widget=numeral_widget, required=False)
        if gametype == "string":
            self.numstring = num_string
        self.numeral = numeral
        self.userans = userans_val
        self.correct_anslist = []
        self.correct_answers =""
        self.error="empty"

        if gametype == "string":
            self.correct_anslist.append(numeral)
        else:
            for item in num_list:
                self.correct_anslist.append(item)
                
        self.is_correct()

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"
        if correct_val == "error":
            self.error="error"

class QAForm(forms.Form):
    maxnum = forms.ChoiceField(initial='10', choices=NUM_CHOICES, widget=forms.RadioSelect)
    numgame = forms.ChoiceField(initial='numeral', choices=NUMGAME_CHOICES, widget=forms.RadioSelect)

class QAQuestion(forms.Form):
    """
    Questions for numeral quizz
    """
    answer = forms.CharField()

    is_correct = is_correct
    set_correct = set_correct
    
    def __init__(self, qstring, question, userans_val, correct_val, *args, **kwargs):

        question_widget = forms.HiddenInput(attrs={'value' : question.id})
        super(QAQuestion, self).__init__(*args, **kwargs)
        self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)
        self.question=qstring
        self.userans = userans_val
        self.correct_anslist = []
        self.correct_answers =""
        self.error="empty"

        self.is_correct()

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"
        if correct_val == "error":
            self.error="error"

