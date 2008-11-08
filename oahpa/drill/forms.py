# -*- coding: utf-8 -*-
import string
import sys
import os
import re
from django import newforms as forms
from django.http import Http404
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from random import randint
from models import *
import time
import datetime
import socket

POS_CHOICES = (
    ('N', _('noun')),
    ('V', _('verb')),
    ('A', _('adjective')),
    ('Num', _('numeral')),
)

CASE_CHOICES = (
    ('NOMPL', _('plural')),
    ('N-ACC', _('accusative')),
    ('N-ILL', _('illative')),
    ('N-LOC', _('locative')),
    ('N-COM', _('comitative')),
    ('N-GEN', _('genitive')),
    ('N-ESS', _('essive')),
)

CASE_CONTEXT_CHOICES = (
    ('N-NOM-PL', _('plural')),
    ('N-ACC', _('accusative')),
    ('N-ILL', _('illative')),
    ('N-LOC', _('locative')),
#    ('N-COM', _('comitative')),
    ('N-ESS', _('essive')),
)

ADJCASE_CHOICES = (
    ('NOMPL', _('plural')),
    ('ATTR', _('attributive')),
    ('N-ACC', _('accusative')),
    ('N-ILL', _('illative')),
    ('N-LOC', _('locative')),
    ('N-COM', _('comitative')),
    ('N-GEN', _('genitive')),
    ('N-ESS', _('essive')),
)

ADJ_CONTEXT_CHOICES = (
    ('ATTRPOS', _('attributive positive')),
    ('ATTRCOMP', _('attributive comparative')),
    ('ATTRSUP', _('attributive superlative')),
    ('PREDPOS', _('predicative positive')),
    ('PREDCOMP', _('predicative comparative')),
    ('PREDSUP', _('predicative superlative')),
)

GRADE_CHOICES = (
    ('POS', _('positive')),
    ('COMP', _('comparative')),
    ('SUPERL', _('superlative')),
)

NUM_CONTEXT_CHOICES = (
    ('NUM-ATTR', _('attributive')),
    ('NUM-NOM-PL', _('plural')),
    ('NUM-ACC', _('accusative')),
    ('NUM-ILL', _('illative')),
    ('NUM-LOC', _('locative')),
    ('NUM-COM', _('comitative')),
    ('COLL-NUM', _('collective')),
)


VTYPE_CHOICES = (
    ('PRS', _('present')),
    ('PRT', _('past')),
    ('COND', _('conditional')),
    ('IMPRT', _('imperative')),
    ('POT', _('potential')),
)

VTYPE_CONTEXT_CHOICES = (
    ('PRS', _('present')),
    ('PRT', _('past')),
    ('V-COND', _('conditional')),
    ('V-IMPRT', _('imperative')),
    ('V-POT', _('potential')),
)


BOOK_CHOICES = (
    ('d1', _('Davvin 1')),
    ('d2', _('Davvin 1-2')),
    ('d3', _('Davvin 1-3')),
    ('d4', _('Davvin 1-4')),
    ('algu', _('algu')),
    ('sara', _('sara')),
    ('bures', _('Bures bures fas')),
    ('oaidnalit', _('Oaidnalit')),
    ('all', _('All')),
)

FREQUENCY_CHOICES = (
    ('rare', _('rare')),
    ('common', _('common')),
)

GEOGRAPHY_CHOICES = (
    ('world', _('world')),
    ('sápmi', _('sapmi')),
)

GAME_CHOICES = (
    ('bare', _('bare')),
    ('context', _('context')),
)

TRANS_CHOICES = (
    ('smenob', _('North Sami to Norwegian')),
    ('nobsme', _('Norwegian to North Sami')),
)

LANGUAGE_CHOICES = (
    ('sme', _('North Sami')),
    ('smj', _('Lule Sami')),
    ('sma', _('South Sami')),
    ('smn', _('Inari Sami')),
)

SEMTYPE_CHOICES = (
    ('FAMILY', _('family')),
    ('PROFESSION', _('profession')),
    ('HUMAN-LIKE', _('human-like')),
    ('ANIMAL', _('animal')),
    ('FOOD/DRINK', _('food/drink')),
    ('TIME', _('time')),
    ('CONCRETES', _('concretes')),
    ('BODY', _('body')),
    ('CLOTHES', _('clothes')),
    ('BUILDINGS/ROOMS', _('buildings/rooms')),
    ('NATUREWORDS', _('naturewords')),
    ('LEISURETIME/AT_HOME', _('leisuretime/at_home')),
    ('PLACES', _('places')),
    ('LITERATURE', _('literature')),
    ('SCHOOL/EDUCATION', _('school/education')),
    ('ABSTRACTS', _('abstracts')),
    ('WORK/ECONOMY/TOOLS', _('work/economy/tools')),
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

def is_correct(self, game, example=None):
    """
    Determines if the given answer is correct (for a bound form).
    """
    #print "GAME", game
    if not self.is_valid():
        return False

    self.userans = self.cleaned_data['answer']
    answer = self.userans.rstrip()
    answer = answer.lstrip()
    answer = answer.rstrip('.!?,')
    
    self.error = "error"
    iscorrect = False

    #print "ANSWER", answer
    if answer in set(self.correct_anslist) or \
           answer.lower() in set(self.correct_anslist) or \
           answer.upper() in set(self.correct_anslist):
        self.error = "correct"
        iscorrect = True

    # Log information about user answers.
    correctlist = ",".join(self.correct_anslist)
    today=datetime.date.today()
    log, c = Log.objects.get_or_create(userinput=answer,correct=correctlist,iscorrect=iscorrect,\
                                       example=example,game=game,date=today)
    log.save()

def set_correct(self):
    """
    Adds correct wordforms to the question form.
    """
    
    if self.correct_anslist:
        self.correct_answers = self.correct_anslist[0]


def set_settings(self):

    # Construct arrays for book choices.
    self.books = {}
    self.books['all'] = []
    for b in BOOK_CHOICES:
        if b[0] != 'all':
            self.books[b[0]] = []
            self.books['all'].append(b[0])

        self.books[b[0]].append(b[0])

        
    self.books['d2'].append('d1')
    for b in ['d1', 'd2']:
        self.books['d3'].append(b)
    for b in ['d1', 'd2', 'd3']:
        self.books['d4'].append(b)

    self.allsem = []
    for b in SEMTYPE_CHOICES:
        self.allsem.append(b[0])        
        
    self.allcase = []
    for b in CASE_CHOICES:
        self.allcase.append(b[0])                

    self.allcase_context = []
    for b in CASE_CONTEXT_CHOICES:
        self.allcase_context.append(b[0])                

    self.allvtype_context = []
    for b in VTYPE_CONTEXT_CHOICES:
        self.allvtype_context.append(b[0])                

    self.alladj_context = []
    for b in ADJ_CONTEXT_CHOICES:
        self.alladj_context.append(b[0])                

    self.allnum_context = []
    for b in NUM_CONTEXT_CHOICES:
        self.allnum_context.append(b[0])                

            
class MorphForm(forms.Form):

    set_settings = set_settings

    num_context = forms.ChoiceField(initial='NUM-ATTR', choices=NUM_CONTEXT_CHOICES, widget=forms.Select)
    case = forms.ChoiceField(initial='N-ILL', choices=CASE_CHOICES, widget=forms.Select)
    case_context = forms.ChoiceField(initial='N-ILL', choices=CASE_CONTEXT_CHOICES, widget=forms.Select)
    adjcase = forms.ChoiceField(initial='ATTR', choices=ADJCASE_CHOICES, widget=forms.Select)
    adj_context_choices = forms.ChoiceField(initial='ATTR', choices=ADJ_CONTEXT_CHOICES, widget=forms.Select)
    vtype = forms.ChoiceField(initial='PRS', choices=VTYPE_CHOICES, widget=forms.Select)
    vtype_context = forms.ChoiceField(initial='PRS', choices=VTYPE_CONTEXT_CHOICES, widget=forms.Select)
    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
    gametype = forms.ChoiceField(initial='bare', choices=GAME_CHOICES, widget=forms.Select)
    bisyllabic = forms.BooleanField(required=False, initial='1')
    trisyllabic = forms.BooleanField(required=False,initial=0)
    contracted = forms.BooleanField(required=False,initial=0)
    grade = forms.ChoiceField(initial='POS', choices=GRADE_CHOICES, widget=forms.Select)
    default_data = {'language' : 'sme', \
                    'syll' : ['bisyllabic'], 'book' : 'all', \
                    'case': 'N-ILL', 'pos' : 'N', \
                    'case_context' : 'N-ILL', \
                    'vtype' : 'PRS', 'vtype_context' : 'PRS', \
                    'num_context' : 'NUM-ATTR', \
                    'adj_context' : 'ATTRPOS', \
                    'adjcase' : 'ATTR', 'grade' : 'POS'}


    def __init__(self, *args, **kwargs):
        self.set_settings()
        super(MorphForm, self).__init__(*args, **kwargs)
        
class MorphQuestion(forms.Form):
    """
    Questions for morphology game 
    """
    is_correct = is_correct
    set_correct = set_correct
    
    #answer = forms.CharField()

    def get_feedback(self,word,tag,wordform):
        
        feedbacks=None
        
        if tag.pos=="N" or tag.pos=="Num":
            #print "filtering feedbacks"
            #print "stem:", word.stem, "gradation:", word.gradation, "diphthong:", word.diphthong, "rime:", word.rime, "soggi:", word.soggi,tag.case,tag.pos,tag.number

            feedbacks = Feedback.objects.filter(Q(stem=word.stem) & Q(gradation=word.gradation) & \
                                                Q(diphthong=word.diphthong) & Q(rime=word.rime) & \
                                                Q(soggi=word.soggi) & Q(case2=tag.case) & \
                                                Q(pos=tag.pos) &\
                                                Q(number = tag.number))
        if tag.pos=="A":
            #print "........filtering feedbacks for adjectives"

            grade =""
            if tag.grade: grade = tag.grade                
            else: grade = "Pos"

            attrsuffix = ""
            if tag.attributive:
                attributive = "Attr"
                attrsuffix = word.attrsuffix
            else: attributive = "NoAttr"
                
            #print "stem:", word.stem, "gradation:", word.gradation, "diphthong:", word.diphthong, "rime:", word.rime, "soggi:", word.soggi, "attrsuffix:", word.attrsuffix
            #print tag.case, tag.pos, tag.number, tag.attributive

            feedbacks = Feedback.objects.filter(Q(stem=word.stem) & Q(gradation=word.gradation) & \
                                                Q(diphthong=word.diphthong) & Q(rime=word.rime) & \
                                                Q(soggi=word.soggi) & Q(case2=tag.case) & \
                                                Q(pos=tag.pos) & Q(grade=grade) &\
                                                Q(attributive=attributive) & Q(attrsuffix=attrsuffix) & \
                                                Q(number = tag.number))

        if tag.pos == "V":

            #print "stem:", word.stem, "gradation:", word.gradation, "diphthong:", word.diphthong, "rime:", word.rime, "soggi:", word.soggi
            #print tag.pos, tag.personnumber, tag.tense, tag.mood

            feedbacks = Feedback.objects.filter(Q(stem=word.stem) & \
                                               Q(diphthong=word.diphthong) & Q(soggi=word.soggi) & \
                                               Q(mood=tag.mood) & Q(tense=tag.tense) & \
                                               Q(personnumber = tag.personnumber))
            
        if feedbacks:
            for f in feedbacks:
                msgs = f.messages.all()
                for m in msgs:
                    self.feedback = self.feedback + " " + m.message
            self.feedback = self.feedback.replace("WORDFORM", "\"" + wordform + "\"") 
            #print "FEEDBACK", self.feedback


    def __init__(self, word, tag, baseform, fullforms, translations, question, userans_val, correct_val, *args, **kwargs):

        lemma_widget = forms.HiddenInput(attrs={'value' : word.id})
        tag_widget = forms.HiddenInput(attrs={'value' : tag.id})

        super(MorphQuestion, self).__init__(*args, **kwargs)
        answer_size = 20
        self.fields['answer'] = forms.CharField(max_length = answer_size, \
                                                widget=forms.TextInput(attrs={'size': answer_size, 'onkeypress':'return process(this, event);',}))

        self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
        self.fields['tag_id'] = forms.CharField(widget=tag_widget, required=False)
        self.lemma=baseform.fullform

        # Get lemma and feedback
        self.feedback=""
        messages = []

        # Retrieve feedback information
        self.get_feedback(word,tag,baseform.fullform)
            
        self.correct_answers =""
        self.case = ""
        self.userans = userans_val
        self.correct_anslist = []
        self.error="empty"
        self.problems="error"
        self.pron=""
        self.pron_imp=""
        self.PronPNBase={'Sg1':'mun','Sg2':'don','Sg3':'son',\
                         'Pl1':'mun','Pl2':'don','Pl3':'son',\
                         'Du1':'mun','Du2':'don','Du3':'son'}
        
        # Take only the first translation for the tooltip
        if len(translations)>0:
            self.translations = translations[0].lemma
			
        for item in fullforms:
            self.correct_anslist.append(force_unicode(item.fullform))
        
        if tag.pos=="N":
            #self.tag = ""
            self.case = tag.case
        #if tag.pos=="V":
        #    self.tag = ""
        #else:
        self.tag = tag.string

        if tag.pos=="V" and tag.personnumber and not tag.personnumber == "ConNeg" :
            pronbase = self.PronPNBase[tag.personnumber]
            self.pron = Form.objects.filter(Q(word__lemma=pronbase) & \
                                            Q(tag__string="Pron+Pers+" +tag.personnumber+ "+Nom"))[0].fullform

            if self.pron and tag.mood=="Imprt":
                self.pron_imp= "(" + self.pron + ")"
                self.pron=""

        self.is_correct("morfa" + "_" + tag.pos, self.lemma + "+" + self.tag)

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"


class QuizzForm(forms.Form):

    set_settings = set_settings

    semtype = forms.ChoiceField(initial='NATUREWORDS', choices=SEMTYPE_CHOICES, widget=forms.Select)
    transtype = forms.ChoiceField(initial='smenob', choices=TRANS_CHOICES, widget=forms.Select)

    # For placename quizz
    common = forms.BooleanField(required=False, initial='1')
    rare = forms.BooleanField(required=False,initial=0)
    sapmi = forms.BooleanField(required=False, initial='1')
    world = forms.BooleanField(required=False,initial=0)
    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
    default_data = {'gametype' : 'bare', 'language' : 'sme', \
                    'syll' : [], 'book' : 'all', \
                    'semtype' : 'NATUREWORDS', \
                    'frequency' : ['common'], 'geography' : ['sapmi'], \
                    'transtype' : 'smenob' }


    def __init__(self, *args, **kwargs):
        self.set_settings()
        super(QuizzForm, self).__init__(*args, **kwargs)


class QuizzQuestion(forms.Form):
    """
    Questions for word quizz
    """

    is_correct = is_correct
    set_correct = set_correct
    
    def __init__(self, transtype, word, translations, question, userans_val, correct_val, *args, **kwargs):

        lemma_widget = forms.HiddenInput(attrs={'value' : word.id})
        super(QuizzQuestion, self).__init__(*args, **kwargs)
        answer_size=20
        self.fields['answer'] = forms.CharField(max_length = answer_size, \
                                                widget=forms.TextInput(attrs={'size': answer_size, 'onkeypress':'return process(this, event);',}))
        self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
        self.lemma = word.lemma
        self.userans = userans_val
        self.correct_anslist = []
        self.correct_answers =""
        self.error="empty"
        self.problems="error"
        oo = "å "
        
        if word.pos == 'V' and transtype=="nobsme":
            self.lemma = oo.decode('utf-8') + self.lemma
            
        for item in translations:
            self.correct_anslist.append(force_unicode(item.lemma))

        self.is_correct("leksa", self.lemma)

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"

class NumForm(forms.Form):

    set_settings = set_settings

    maxnum = forms.ChoiceField(initial='10', choices=NUM_CHOICES, widget=forms.RadioSelect)
    numgame = forms.ChoiceField(initial='numeral', choices=NUMGAME_CHOICES, widget=forms.RadioSelect)
    language = forms.ChoiceField(initial='sme', choices=LANGUAGE_CHOICES, widget=forms.RadioSelect)
    default_data = {'language' : 'sme', 'maxnum' : '10', 'numgame': 'numeral'}
                    
    def __init__(self, *args, **kwargs):
        self.set_settings
        super(NumForm, self).__init__(*args, **kwargs)

class NumQuestion(forms.Form):
    """
    Questions for numeral quizz
    """

    is_correct = is_correct
    set_correct = set_correct
    
    def __init__(self, numeral, num_string, num_list, gametype, userans_val, correct_val, *args, **kwargs):

        numeral_widget = forms.HiddenInput(attrs={'value' : numeral})
        super(NumQuestion, self).__init__(*args, **kwargs)
        answer_size=20
        self.fields['answer'] = forms.CharField(max_length = answer_size, \
                                                widget=forms.TextInput(attrs={'size': answer_size, 'onkeypress':'return process(this, event);',}))

        self.fields['numeral_id'] = forms.CharField(widget=numeral_widget, required=False)
        if gametype == "string":
            self.numstring = num_string
        self.numeral = numeral
        self.userans = userans_val
        self.correct_anslist = []
        self.correct_answers =""
        self.error="empty"
        self.problems="error"

        if gametype == "string":
            self.correct_anslist.append(force_unicode(numeral))
            example = num_string
        else:
            example = numeral
            for item in num_list:
                self.correct_anslist.append(force_unicode(item))

        self.is_correct("numra", example)

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"


def select_words(self, qwords, awords):
    """
    Fetch words and tags from the database.
    """

    selected_awords = {}

    for syntax in awords.keys():
        #print "SYNTAX", syntax
        word = None        
        tag = None
        selected_awords[syntax] = {}

        # Select answer words and fullforms for interface
        # Use first the answer elements, but if there are none,
        # take the corresponding question element        
        if awords.has_key(syntax) and len(awords[syntax]) > 0:
            aword = awords[syntax][randint(0,len(awords[syntax])-1)]
            if aword.has_key('tag'):
                selected_awords[syntax]['tag'] = aword['tag']
            if aword.has_key('word') and aword['word']:
                selected_awords[syntax]['word'] = aword['word']
            else:
                if aword.has_key('qelement') and selected_awords[syntax].has_key('tag'):

                    form_list = None
                    max=50
                    i=0
                    while not form_list and i<max:
                        i=i+1
                        word_count = WordQElement.objects.filter(qelement__id=aword['qelement']).count()
                        if word_count>0:
                            wqel = WordQElement.objects.filter(qelement__id=aword['qelement'])[randint(0,word_count-1)]
                            selected_awords[syntax]['word'] = wqel.word.id
                            form_list = Form.objects.filter(Q(word__id=selected_awords[syntax]['word']) &\
                                                            Q(tag__id=selected_awords[syntax]['tag']))
                    if form_list:
                        fullf=[]
                        for f in form_list:
                            fullf.append(f.fullform)
                        selected_awords[syntax]['fullform'] = fullf[:]

                if not selected_awords[syntax].has_key('fullform'):
                    if aword.has_key('fullform') and len(aword['fullform'])>0:
                        selected_awords[syntax]['fullform'] = aword['fullform'][:]
        else:
            # If there was no word form, take the same word form as in question
            if qwords.has_key(syntax):
                qword = qwords[syntax]
                if qwords[syntax].has_key('word'):
                    selected_awords[syntax]['word'] = qwords[syntax]['word']
                if qwords[syntax].has_key('tag'):
                    selected_awords[syntax]['tag'] = qwords[syntax]['tag']
                
        if not selected_awords[syntax].has_key('fullform'):
            if selected_awords[syntax].has_key('word') and selected_awords[syntax].has_key('tag'):

                form_list = None
                max=50
                i=0
                while not form_list and i<max:
                    i=i+1
                    form_list = Form.objects.filter(Q(word__id=selected_awords[syntax]['word']) &\
                                                    Q(tag__id=selected_awords[syntax]['tag']))
                if form_list:
                    fullf=[]
                    for f in form_list:
                        fullf.append(f.fullform)
                    selected_awords[syntax]['fullform'] = fullf[:]
                        
        # make sure that theres is something to print
        if not selected_awords[syntax].has_key('fullform'):
            selected_awords[syntax]['fullform'] = []
            selected_awords[syntax]['fullform'].append(syntax)

    #print "SELECTED2:", selected_awords
    return selected_awords



class QAForm(forms.Form):

    set_settings = set_settings

    num_context = forms.ChoiceField(initial='NUM-ATTR', choices=NUM_CONTEXT_CHOICES, widget=forms.Select)
    vtype_context = forms.ChoiceField(initial='MAINV', choices=VTYPE_CONTEXT_CHOICES, widget=forms.Select)
    vtype = forms.ChoiceField(initial='PRS', choices=VTYPE_CHOICES, widget=forms.Select)
    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
    default_data = {'gametype' : 'qa', 'language' : 'sme', \
                    'syll' : ['bisyllabic'], 'book' : 'all', \
                    'case': 'N-ILL', 'pos' : 'N', \
                    'vtype' : 'PRS', 'vtype_context' : 'PRS', \
                    'num_context' : 'NUM-ATTR', \
                    'adjcase' : 'ATTR', 'grade' : 'POS'}

    def __init__(self, *args, **kwargs):
        self.set_settings()
        super(QAForm, self).__init__(*args, **kwargs)



class QAQuestion(forms.Form):
    """
    Questions for vasta
    """

    select_words = select_words
    set_correct = set_correct
    is_correct = is_correct
    qtype_verbs = set(['PRS', 'PRT', 'V-COND','V-IMPRT'])

        
    def __init__(self, gametype, question, qanswer, \
                 qwords, awords, userans_val, correct_val, *args, **kwargs):

        self.userans = userans_val
        self.correct_anslist = []
        self.qa_correct_anslist = {}
        self.correct_answers =""
        self.error='empty'
        self.problems="error"
        self.lemma = ""
        self.pron = ""
        
        qtype=question.qtype
        if qtype in self.qtype_verbs:
            qtype = 'PRS'

        question_widget = forms.HiddenInput(attrs={'value' : question.id})
        answer_widget = forms.HiddenInput(attrs={'value' : qanswer.id})
        atext = qanswer.string
        task = qanswer.task

        super(QAQuestion, self).__init__(*args, **kwargs)

        answer_size = 20

        self.fields['answer'] = forms.CharField(max_length = answer_size, \
                                                widget=forms.TextInput(attrs={'size': answer_size, 'onkeypress':'return process(this, event);',}))

        self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)
        self.fields['answer_id'] = forms.CharField(widget=answer_widget, required=False)

        # Select words for the the answer
        selected_awords = self.select_words(qwords, awords)

        # In qagame, all words are considered as answers.
        #print awords
        form_list=[]
        
        if (gametype == 'context'):
            if len(selected_awords[task]['fullform'])>0:
                for f in selected_awords[task]['fullform']:				
                    self.correct_anslist.append(force_unicode(f))
                self.is_correct("contextual morfa")
                            
        self.qattrs= {}
        self.aattrs= {}        
        for syntax in qwords.keys():
            qword = qwords[syntax]
            if qword.has_key('word'):
                self.qattrs['question_word_' + syntax] = qword['word']
            if qword.has_key('tag') and qword['tag']:
                self.qattrs['question_tag_' + syntax] = qword['tag']
            if qword.has_key('fullform') and qword['fullform']:
                self.qattrs['question_fullform_' + syntax] = qword['fullform'][0]

        for syntax in selected_awords.keys():
            if selected_awords[syntax].has_key('word'):
                self.aattrs['answer_word_' + syntax] = selected_awords[syntax]['word']
            if selected_awords[syntax].has_key('tag'):
                self.aattrs['answer_tag_' + syntax] = selected_awords[syntax]['tag']
            if selected_awords[syntax].has_key('fullform') and len(selected_awords[syntax]['fullform']) == 1:
                self.aattrs['answer_fullform_' + syntax] = selected_awords[syntax]['fullform'][0]

        # Forms question string and answer string out of grammatical elements and other strings.
        qstring = ""
        astring= ""

        # Format question string
        qtext = question.string
        #print qwords
        for w in qtext.split():
            if not qwords.has_key(w): qstring = qstring + " " + w
            else:
                if qwords[w].has_key('fullform'):
                    qstring = qstring + " " + qwords[w]['fullform'][0]
                else:
                    qstring = qstring + " " + w
        qstring=qstring.replace(" -","-");
                    
        answer_word = selected_awords[task]['word']
        answer_tag = selected_awords[task]['tag']
        selected_awords[task]['fullform'][0] = 'Q'
        
        # Get lemma for contextual morfa
        answer_word_el = Word.objects.get(id=answer_word)
        answer_tag_el = Tag.objects.get(id=answer_tag)
        self.lemma = answer_word_el.lemma
            
        # If the asked word is in Pl, generate nominal form
        if answer_tag_el.pos=="N":
            if answer_tag_el.number=="Sg":
                self.lemma = answer_word_el.lemma
            else:
                #print answer_word_el.lemma
                if Form.objects.filter(Q(word__pk=answer_word) & \
                                       Q(tag__string="N+Pl+Nom")).count()>0:                        
                    self.lemma = Form.objects.filter(Q(word__pk=answer_word) & \
                                                     Q(tag__string="N+Pl+Nom"))[0].fullform
                else:
                    self.lemma = answer_word_el.lemma + " (plural) fix this"
                
        # Format answer string
        #print "SELECTED", selected_awords
        for w in atext.split():
            if w.count("(") > 0: continue
            
            if not selected_awords.has_key(w) or not selected_awords[w].has_key('fullform'):
                astring = astring + " " + w
            else:
                astring = astring + " " + selected_awords[w]['fullform'][0]
                    
        # Remove leading whitespace and capitalize.
        astring = astring.lstrip()
        qstring = qstring.lstrip()
        astring = astring[0].capitalize() + astring[1:]
        qstring = qstring[0].capitalize() + qstring[1:]

        qstring = qstring + "?"
        # Add dot if the last word is not the open question.
        if astring.count("!")==0 and not astring[-1]=="Q":
            astring = astring + "."
        self.question=qstring

        # Format answer strings for context
        q_count = astring.count('Q')
        if q_count > 0:
            astrings = astring.split('Q')
            if astrings[0]:
                self.answertext1=astrings[0]
            if astrings[1]:
                self.answertext2=astrings[1]

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"


def qa_is_correct(self,question,qwords):
    """
    Analyzes the answer and returns a message.
    """
    if not self.is_valid():
        return False

    lookup_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lookup_client.connect(("localhost", 9000))

    # Analyzer..
    #fstdir="/Users/saara/gt/sme/bin"
    #lo = "/Users/saara/bin/lookup"
    #lookup2cg = " | /Users/saara/gt/script/lookup2cg"
    #cg3 = "/usr/local/bin/vislcg3"
    #preprocess = " | /Users/saara/gt/script/preprocess "
    #dis = "/Users/saara/ped/sme/src/sme-ped.cg3"

    fstdir="/opt/smi/sme/bin"
    lo = "/opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/lookup"
    lookup2cg = " | lookup2cg"
    cg3 = "/usr/local/bin/vislcg3"
    preprocess = " | /usr/local/bin/preprocess "
    dis_bin = "/home/saara/ped/sme/src/sme-ped.cg3"
    #dis_bin = fstdir + "/sme-ped.cg3.bin"

    fst = fstdir + "/sme.fst"
    lookup = " | " + lo + " -flags mbTT -utf8 -d " + fst        
    vislcg3 = " | " + cg3 + " --grammar " + dis_bin + " -C UTF-8"

    self.userans = self.cleaned_data['answer']
    answer = self.userans.rstrip()
    answer = answer.lstrip()
    answer = answer.rstrip('.!?,')

    self.error = "error"
                
    qtext = question.string
    qtext = qtext.rstrip('.!?,')
    
    analysis = ""
    for w in qtext.split():
        cohort=""
        if qwords.has_key(w):
            qword = qwords[w]
            if qword.has_key('word'):
                if qword.has_key('fullform') and qword['fullform']:
                    cohort = cohort + "\"<" + qword['fullform'][0].encode('utf-8') + ">\"\n"
                    lemma = Word.objects.filter(id=qword['word'])[0].lemma
                    cohort = cohort + "\t\"" + lemma.encode('utf-8') + "\""
                if qword.has_key('tag') and qword['tag']:
                    string = Tag.objects.filter(id=qword['tag'])[0].string
                    tag = string.replace("+"," ")
                    cohort = cohort + " " + tag.encode('utf+8') + "\n"
            else:
                w=w.lstrip().rstrip()
                lookup_client.send(w.encode('utf-8'))
                cohort = lookup_client.recv(512)

        if not cohort:
            cohort = w + "\n"
        
        analysis = analysis + cohort
    analysis = analysis + cohort
        
    analysis = analysis + "\"<^qst>\"\n\t\"^qst\" QDL\n"

    ans_cohort=""
    data_lookup = "echo \"" + answer.encode('utf-8') + "\"" + preprocess
    word = os.popen(data_lookup).readlines()
    analyzed=""
    for c in word:
        c=c.rstrip().lstrip()

        lookup_client.send(c)
        analyzed = analyzed + lookup_client.recv(512)

    analysis = analysis + analyzed
    #print analysis
    analysis = analysis.rstrip()
    analysis = analysis.replace("\"","\\\"")

    ped_cg3 = "echo \"" + analysis + "\"" + vislcg3
    checked = os.popen(ped_cg3).readlines()

    wordformObj=re.compile(r'^\"<(?P<msgString>.*)>\".*$', re.U)
    messageObj=re.compile(r'^.*(?P<msgString>&[\w-]*)\s*$', re.U)

    spelling = False
    msgstrings = {}

    for line in checked:
        line = line.strip()

        matchObj=wordformObj.search(line)
        if matchObj:
            wordform = matchObj.expand(r'\g<msgString>')
            msgstrings[wordform] = {}
            
        matchObj=messageObj.search(line)
        if matchObj:
            msgstring = matchObj.expand(r'\g<msgString>')
            if msgstring.count("spellingerror") > 0:
                spelling = True
            msgstrings[wordform][msgstring] = 1
            
    msg=[]
    found=False
    for w in msgstrings.keys():
        if found: break
        for m in msgstrings[w].keys():
            if spelling and m.count("spelling") == 0: continue
            m = m.replace("&","") 
            if Feedbackmsg.objects.filter(msgid=m).count() > 0:
                message = Feedbackmsg.objects.filter(msgid=m)[0].message
                message = message.replace("WORDFORM","\"" + w.decode('utf-8') + "\"") 
                msg.append(message)
                if not spelling:
                    found=True
                    break				
            else:
                if m.count("dia-") == 0:
                    msg.append(m)
                    if not spelling:
                        found=True
                        break				

    if not msg:
        self.error = "correct"

    lookup_client.send("q")
    lookup_client.close()
    return msg


class VastaForm(forms.Form):

    set_settings = set_settings

    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
    default_data = {'gametype' : 'qa', 'language' : 'sme', \
                    'syll' : ['bisyllabic'], 'book' : 'all', \
                    'case': 'N-ILL', 'case_context':'N-ILL',\
                    'pos' : 'V', \
                    'vtype' : 'PRS', 'vtype_context' : 'PRS', \
                    'num_context' : 'NUM-ATTR', \
                    'adjcase' : 'ATTR', 'grade' : 'POS'}

    def __init__(self, *args, **kwargs):
        self.set_settings()
        super(VastaForm, self).__init__(*args, **kwargs)


class VastaQuestion(forms.Form):
    """
    Questions for vasta
    """

    select_words = select_words
    set_correct = set_correct
    qa_is_correct = qa_is_correct
        
    def __init__(self, gametype, question, qwords, userans_val, correct_val, *args, **kwargs):                 

        self.userans = userans_val
        self.correct_anslist = []
        self.qa_correct_anslist = {}
        self.error='empty'
        self.problems="error"
        
        question_widget = forms.HiddenInput(attrs={'value' : question.id})

        super(VastaQuestion, self).__init__(*args, **kwargs)
        answer_size=50
        self.fields['answer'] = forms.CharField(max_length = answer_size, \
                                                widget=forms.TextInput(attrs={'size': answer_size,'onkeypress':'processvasta(event)',}))
        self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)

        # In qagame, all words are considered as answers.
        form_list=[]
        self.messages = self.qa_is_correct(question, qwords)
        
        self.qattrs= {}
        for syntax in qwords.keys():
            qword = qwords[syntax]
            if qword.has_key('word'):
                self.qattrs['question_word_' + syntax] = qword['word']
            if qword.has_key('tag') and qword['tag']:
                self.qattrs['question_tag_' + syntax] = qword['tag']
            if qword.has_key('fullform') and qword['fullform']:
                self.qattrs['question_fullform_' + syntax] = qword['fullform'][0]

        # Forms question string and answer string out of grammatical elements and other strings.
        qstring = ""

        # Format question string
        qtext = question.string
        for w in qtext.split():
            if not qwords.has_key(w): qstring = qstring + " " + w
            else:
                if qwords[w].has_key('fullform'):
                    qstring = qstring + " " + qwords[w]['fullform'][0]
                else:
                    qstring = qstring + " " + w
        # this is for -guovttos
        qstring=qstring.replace(" -","-");
        qstring=qstring.replace("- ","-");
                    
        # Remove leading whitespace and capitalize.
        qstring = qstring.lstrip()
        qstring = qstring[0].capitalize() + qstring[1:]

        qstring = qstring + "?"
        self.question=qstring

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"
