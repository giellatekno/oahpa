# -*- coding: utf-8 -*-
import string
import sys
from django import newforms as forms
from django.http import Http404
from django.db.models import Q
from django.utils.translation import ugettext as _
from models import Word, Form, Question


POS_CHOICES = (
    ('N', _('noun')),
    ('V', _('verb')),
#    ('A', _('adjective')),
)

CASE_CHOICES = (
    ('N-ACC', _('accusative')),
    ('N-ILL', _('illative')),
    ('N-LOC', _('locative')),
    ('N-COM', _('comitative')),
    ('N-GEN', _('genitive')),
    ('N-ESS', _('essive')),
)

BOOK_CHOICES = (
    ('d1', _('Davvin 1')),
    ('d2', _('Davvin 1-2')),
    ('d3', _('Davvin 1-3')),
    ('d4', _('Davvin 1-4')),
    ('álgu', _('algu')),
    ('sárá', _('sara')),
    ('bures', _('Bures bures fas')),
    ('oaidnalit', _('Oaidnalit')),
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

LANGUAGE_CHOICES = (
    ('sme', _('North Sami')),
    ('smj', _('Lule Sami')),
    ('sma', _('South Sami')),
    ('smn', _('Inari Sami')),
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
    case = forms.ChoiceField(initial='N-ILL', choices=CASE_CHOICES, widget=forms.Select)
    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
    gametype = forms.ChoiceField(initial='bare', choices=GAME_CHOICES, widget=forms.Select)
    bisyllabic = forms.BooleanField(required=False, initial='1')
    trisyllabic = forms.BooleanField(required=False,initial='1')
    contracted = forms.BooleanField(required=False,initial='1')
    default_data = {'pos': 'N'}
    allbooks = []
    for b in BOOK_CHOICES:
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

        if tag.pos=="N":
            if tag.number=="Sg":
                self.lemma = word.lemma
            else:
                self.lemma = Form.objects.filter(Q(word__pk=word.id) & Q(tag__string="N+Pl+Nom"))[0].fullform
                
        self.correct_answers =""
        self.case = ""
        self.userans = userans_val
        self.correct_anslist = []
        self.error="empty"
        self.translations = []
        for item in tr_list:
            self.translations.append(item.translation)
        
        for item in fullforms:
            self.correct_anslist.append(item.fullform)
        
        if tag.pos=="N":
            self.tag = ""
            self.case = tag.case
        else:
            self.tag = tag.string

        self.is_correct()

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"

class QuizzForm(forms.Form):
    semtype = forms.ChoiceField(initial='all', choices=SEMTYPE_CHOICES, widget=forms.Select)
    transtype = forms.ChoiceField(initial='smenob', choices=TRANS_CHOICES, widget=forms.Select)
    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
    allbooks = []
    for b in BOOK_CHOICES:
        allbooks.append(b[0])
    allsem = []
    for b in SEMTYPE_CHOICES:
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

class NumForm(forms.Form):
    maxnum = forms.ChoiceField(initial='10', choices=NUM_CHOICES, widget=forms.RadioSelect)
    numgame = forms.ChoiceField(initial='numeral', choices=NUMGAME_CHOICES, widget=forms.RadioSelect)
    language = forms.ChoiceField(initial='sme', choices=LANGUAGE_CHOICES, widget=forms.RadioSelect)

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
    
    def __init__(self, word, tag, fullforms, qstring, question, astring, userans_val, correct_val, *args, **kwargs):

        question_widget = forms.HiddenInput(attrs={'value' : question.id})
        qstring_widget = forms.HiddenInput(attrs={'value' : qstring})
        astring_widget = forms.HiddenInput(attrs={'value' : astring})
        lemma_widget = forms.HiddenInput(attrs={'value' : word.id})
        tag_widget = forms.HiddenInput(attrs={'value' : tag.id})

        super(QAQuestion, self).__init__(*args, **kwargs)

        self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)
        self.fields['qstring'] = forms.CharField(widget=qstring_widget, required=False)
        self.fields['astring'] = forms.CharField(widget=astring_widget, required=False)
        self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
        self.fields['tag_id'] = forms.CharField(widget=tag_widget, required=False)

        if tag.pos=="N":
            if tag.number=="Sg":
                self.lemma = word.lemma
            else:
                self.lemma = Form.objects.filter(Q(word__pk=word.id) & Q(tag__string="N+Pl+Nom"))[0].fullform

        self.question=qstring
        astrings = astring.split('Q')
        if astrings[0]:
            self.answertext1=astrings[0]
        if astrings[1]:
            self.answertext2=astrings[1]
        
        self.userans = userans_val
        self.correct_anslist = []
        self.correct_answers =""
        self.error="empty"

        for item in fullforms:
            self.correct_anslist.append(item.fullform)

            
        self.is_correct()

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"

