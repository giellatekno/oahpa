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
#    ('COLL-NUM', _('collective')),
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

VASTA_LEVELS = (
    ('1', _('First level')),
    ('2', _('Second level')),
    ('3', _('Third level')),
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
    ('sjd', _('Kildin Sami')),
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

DIALOGUE_CHOICES = (
    ('visit', _('Visit')),
    ('firstmeeting', _('First meeting')),
    ('grocery', _('Grocery')),
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
        self.correct_answers = self.correct_ans


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


class OahpaSettings(forms.Form):
    set_settings = set_settings

    def set_default_data(self):
		self.default_data = {'language' : 'sme', 'dialogue' : 'GG',\
                             'syll' : ['bisyllabic'], 'book' : 'all', \
                             'case': 'N-ILL', 'pos' : 'N', \
                             'vtype' : 'PRS', \
                             'adjcase' : 'ATTR', 'grade' : 'POS', \
                             'case_context' : 'N-ILL', \
                             'vtype_context' : 'PRS', \
                             'num_context' : 'NUM-ATTR', \
                             'adj_context' : 'ATTRPOS'}


class OahpaQuestion(forms.Form):

    is_correct = is_correct
    set_correct = set_correct
    get_feedback = get_feedback

    def init_variables(self, correct, userans_val, fullforms):
        # Get lemma and feedback
        self.feedback=""
        self.messages = []
        self.correct_ans = correct
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
        
        for item in fullforms:
            self.correct_anslist.append(force_unicode(item))

    def generate_fields(self,answer_size, maxlength):
        self.fields['answer'] = forms.CharField(max_length = maxlength, \
                                                widget=forms.TextInput(\
            attrs={'size': answer_size, 'onkeypress':'return process(this, event,document.theform);',}))

            
class MorfaSettings(OahpaSettings):

    case = forms.ChoiceField(initial='N-ILL', choices=CASE_CHOICES, widget=forms.Select)
    adjcase = forms.ChoiceField(initial='ATTR', choices=ADJCASE_CHOICES, widget=forms.Select)
    vtype = forms.ChoiceField(initial='PRS', choices=VTYPE_CHOICES, widget=forms.Select)
    num_context = forms.ChoiceField(initial='NUM-ATTR', choices=NUM_CONTEXT_CHOICES, widget=forms.Select)
    case_context = forms.ChoiceField(initial='N-ILL', choices=CASE_CONTEXT_CHOICES, widget=forms.Select)
    adj_context = forms.ChoiceField(initial='ATTR', choices=ADJ_CONTEXT_CHOICES, widget=forms.Select)
    vtype_context = forms.ChoiceField(initial='PRS', choices=VTYPE_CONTEXT_CHOICES, widget=forms.Select)

    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
    bisyllabic = forms.BooleanField(required=False, initial='1')
    trisyllabic = forms.BooleanField(required=False,initial=0)
    contracted = forms.BooleanField(required=False,initial=0)
    grade = forms.ChoiceField(initial='POS', choices=GRADE_CHOICES, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        self.set_settings()
        self.set_default_data()
        super(MorfaSettings, self).__init__(*args, **kwargs)

        
class MorfaQuestion(OahpaQuestion):
    """
    Questions for morphology game 
    """

    def __init__(self, word, tag, baseform, correct, fullforms, translations, question, userans_val, correct_val, *args, **kwargs):

        lemma_widget = forms.HiddenInput(attrs={'value' : word.id})
        tag_widget = forms.HiddenInput(attrs={'value' : tag.id})

        super(MorfaQuestion, self).__init__(*args, **kwargs)

        ##### initialize variables
        self.init_variables(correct.fullform, userans_val, fullforms)
        self.generate_fields(30,30)

        self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
        self.fields['tag_id'] = forms.CharField(widget=tag_widget, required=False)
        self.lemma=baseform.fullform

        # Retrieve feedback information
        self.get_feedback(word,tag,baseform.fullform)

        # Take only the first translation for the tooltip
        if len(translations)>0:
            self.translations = translations[0]

        if tag.pos=="N":
            self.case = tag.case
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


class QuizzSettings(OahpaSettings):

    semtype = forms.ChoiceField(initial='NATUREWORDS', choices=SEMTYPE_CHOICES, widget=forms.Select)
    transtype = forms.ChoiceField(initial='smenob', choices=TRANS_CHOICES, widget=forms.Select)

    # For placename quizz
    common = forms.BooleanField(required=False, initial='1')
    rare = forms.BooleanField(required=False,initial=0)
    sapmi = forms.BooleanField(required=False, initial='1')
    world = forms.BooleanField(required=False,initial=0)
    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
    default_data = {'gametype' : 'bare', 'language' : 'sme', 'dialogue' : 'GG', \
                    'syll' : [], 'book' : 'all', \
                    'semtype' : 'NATUREWORDS', \
                    'frequency' : ['common'], 'geography' : ['sapmi'], \
                    'transtype' : 'smenob' }


    def __init__(self, *args, **kwargs):
        self.set_settings()
        super(QuizzSettings, self).__init__(*args, **kwargs)


class QuizzQuestion(OahpaQuestion):
    """
    Questions for word quizz
    """
    
    def __init__(self, transtype, word, correct, translations, question, userans_val, correct_val, *args, **kwargs):

        lemma_widget = forms.HiddenInput(attrs={'value' : word.id})
        super(QuizzQuestion, self).__init__(*args, **kwargs)

        # Initialize variables
        self.init_variables(correct, userans_val, translations)

        self.generate_fields(30,30)
        self.fields['word_id'] = forms.CharField(widget=lemma_widget, required=False)
        self.lemma = word.lemma
        oo = "å "
        
        if word.pos == 'V' and transtype=="nobsme":
            self.lemma = oo.decode('utf-8') + self.lemma

        self.is_correct("leksa", self.lemma)

        # set correct and error values
        if correct_val == "correct":
            self.error="correct"

class NumSettings(OahpaSettings):

    maxnum = forms.ChoiceField(initial='10', choices=NUM_CHOICES, widget=forms.RadioSelect)
    numgame = forms.ChoiceField(initial='numeral', choices=NUMGAME_CHOICES, widget=forms.RadioSelect)
    language = forms.ChoiceField(initial='sme', choices=LANGUAGE_CHOICES, widget=forms.RadioSelect)
    default_data = {'language' : 'sme', 'dialogue' : 'GG', 'maxnum' : '10', 'numgame': 'numeral'}
                    
    def __init__(self, *args, **kwargs):
        self.set_settings
        super(NumSettings, self).__init__(*args, **kwargs)

class NumQuestion(OahpaQuestion):
    """
    Questions for numeral quizz
    """
    
    def __init__(self, numeral, num_string, num_list, gametype, userans_val, correct_val, *args, **kwargs):

        numeral_widget = forms.HiddenInput(attrs={'value' : numeral})
        super(NumQuestion, self).__init__(*args, **kwargs)

        # Initialize variables
        if gametype == "string":
            self.init_variables(force_unicode(numeral), userans_val, [ numeral ])
            example = num_string
        else:
            self.init_variables(force_unicode(num_list[0]), userans_val, num_list)
            example = numeral

        self.generate_fields(30,30)

        self.fields['numeral_id'] = forms.CharField(widget=numeral_widget, required=False)
        if gametype == "string":
            self.numstring = num_string
        self.numeral = numeral

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
        word = None        
        tag = None
        selected_awords[syntax] = {}

        # Select answer words and fullforms for interface
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
                
        if not selected_awords[syntax].has_key('fullform'):
            if selected_awords[syntax].has_key('word') and selected_awords[syntax].has_key('tag'):
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

    return selected_awords


class ContextMorfaQuestion(OahpaQuestion):
    """
    Questions for contextual morfa
    """

    select_words = select_words
    qtype_verbs = set(['PRS', 'PRT', 'V-COND','V-IMPRT'])

        
    def __init__(self, question, qanswer, \
                 qwords, awords, userans_val, correct_val, *args, **kwargs):

        self.init_variables("", userans_val, [])
        self.lemma = ""
        
        qtype=question.qtype
        if qtype in self.qtype_verbs:
            qtype = 'PRS'

        question_widget = forms.HiddenInput(attrs={'value' : question.id})
        answer_widget = forms.HiddenInput(attrs={'value' : qanswer.id})
        atext = qanswer.string
        task = qanswer.task
        if not task:
            raise Http404(atext)			

        super(ContextMorfaQuestion, self).__init__(*args, **kwargs)

        answer_size = 20
        maxlength = 30

        self.generate_fields(20,30)

        self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)
        self.fields['answer_id'] = forms.CharField(widget=answer_widget, required=False)

        # Select words for the the answer
        selected_awords = self.select_words(qwords, awords)


        form_list=[]        
        if len(selected_awords[task]['fullform'])>0:
            for f in selected_awords[task]['fullform']:				
                self.correct_anslist.append(force_unicode(f))
            self.is_correct("contextual morfa")
            self.correct_ans = self.correct_anslist[0]
                
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
        for w in qtext.split():
            if not qwords.has_key(w): qstring = qstring + " " + force_unicode(w)
            else:
                if qwords[w].has_key('fullform'):
                    qstring = qstring + " " + force_unicode(qwords[w]['fullform'][0])
                else:
                    qstring = qstring + " " + force_unicode(w)
        qstring=qstring.replace(" -","-");
        qstring=qstring.replace(" .",".");
                    
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
                if Form.objects.filter(Q(word__pk=answer_word) & \
                                       Q(tag__string="N+Pl+Nom")).count()>0:                        
                    self.lemma = Form.objects.filter(Q(word__pk=answer_word) & \
                                                     Q(tag__string="N+Pl+Nom"))[0].fullform
                else:
                    self.lemma = answer_word_el.lemma + " (plural) fix this"
        if answer_tag_el.pos=="A":
            self.lemma=""

        # Format answer string
        for w in atext.split():
            if w.count("(") > 0: continue
            
            if not selected_awords.has_key(w) or not selected_awords[w].has_key('fullform'):
                astring = astring + " " + force_unicode(w)
            else:
                astring = astring + " " + force_unicode(selected_awords[w]['fullform'][0])
                    
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


def vasta_is_correct(self,question,qwords,utterance_name=None):
    """
    Analyzes the answer and returns a message.
    """
    if not self.is_valid():
        return None, None, None

    lookup_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lookup_client.connect(("localhost", 9000))

    # Analyzer..
    #lookup2cg = " | /Users/saara/gt/script/lookup2cg"
    #cg3 = "/usr/local/bin/vislcg3"
    #preprocess = " | /Users/saara/gt/script/preprocess "
    #dis_bin = "/Users/saara/ped/sme/src/sme-ped.cg3"

    fstdir = "/opt/smi/sme/bin"
    lookup2cg = " | lookup2cg"
    cg3 = "/usr/local/bin/vislcg3"
    preprocess = " | /usr/local/bin/preprocess "
    dis_bin = "/home/saara/ped/sme/src/sme-ped.cg3"
    dis_bin = fstdir + "/sme-ped.cg3"

    vislcg3 = " | " + cg3 + " --grammar " + dis_bin + " -C UTF-8"

    self.userans = self.cleaned_data['answer']
    answer = self.userans.rstrip()
    answer = answer.lstrip()
    answer = answer.rstrip('.!?,')

    self.error = "error"
                
    qtext = question
    qtext = qtext.rstrip('.!?,')
    
    analysis = ""
    data_lookup = "echo \"" + qtext + "\"" + preprocess
    words = os.popen(data_lookup).readlines()
    for w in words:
        cohort=""
        if qwords and qwords.has_key(w):
            qword = qwords[w]
            if qword.has_key('word'):
                if qword.has_key('fullform') and qword['fullform']:
                    cohort = cohort + "\"<" + qword['fullform'][0].encode('utf-8') + ">\"\n"
                    lemma = Word.objects.filter(id=qword['word'])[0].lemma
                    cohort = cohort + "\t\"" + lemma + "\""
                if qword.has_key('tag') and qword['tag']:
                    string = Tag.objects.filter(id=qword['tag'])[0].string
                    tag = string.replace("+"," ")
                    cohort = cohort + " " + tag + "\n"
            else:
                w=w.lstrip().rstrip()
                lookup_client.send(w)
                cohort = lookup_client.recv(512)
        else:
            w=w.lstrip().rstrip()
            lookup_client.send(w)
            cohort = lookup_client.recv(512)

        if not cohort:
            cohort = w + "\n"
	
        analysis = analysis + cohort

    if self.gametype=="sahka":
        analysis = analysis + "\"<^qdl_id>\"\n\t\"^sahka\" QDL " + utterance_name +"\n"
    else:
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
    analysis2=analysis
    analysis = analysis.rstrip()
    analysis = analysis.replace("\"","\\\"")

    ped_cg3 = "echo \"" + analysis + "\"" + vislcg3
    checked = os.popen(ped_cg3).readlines()

    wordformObj=re.compile(r'^\"<(?P<msgString>.*)>\".*$', re.U)
    messageObj=re.compile(r'^.*(?P<msgString>&(grm|err)[\w-]*)\s*$', re.U)
    targetObj=re.compile(r'^.*\"(?P<targetString>[\wáÁæÆåÅáÁšŠŧŦŋŊøØđĐžZčČ-]*)\".*dia-.*$', re.U)
    diaObj=re.compile(r'^.*(?P<targetString>&dia-[\w]*)\s*$', re.U)

    spelling = False
    msgstrings = {}
    diastring = "jee"
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

        matchObj=targetObj.search(line)
        if matchObj:
            msgstring = matchObj.expand(r'\g<targetString>')
            msgstrings[wordform]['dia-target'] = msgstring

        matchObj=diaObj.search(line)
        if matchObj:
            msgstring = matchObj.expand(r'\g<targetString>')
            msgstrings[wordform][msgstring] = 1
            diastring=msgstring			
            
    msg=[]
    dia_msg = []
    target = ""
    variable=""
    found=False
    for w in msgstrings.keys():
        if found: break
        for m in msgstrings[w].keys():
            if spelling and m.count("spelling") == 0: continue
            m = m.replace("&","") 
            if Feedbackmsg.objects.filter(msgid=m).count() > 0:
                message = Feedbackmsg.objects.filter(msgid=m)[0].message
                message = message.replace("WORDFORM","\"" + w + "\"") 
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
            if m.count("dia-") > 0:
                dia_msg.append(m)
        if msgstrings[w].has_key('dia-target'):
            variable = msgstrings[w]['dia-target']			
                    
    if not msg:
        self.error = "correct"

    lookup_client.send("q")
    lookup_client.close()
    return msg, dia_msg, variable


class VastaSettings(OahpaSettings):

    book = forms.ChoiceField(initial='all', choices=BOOK_CHOICES, widget=forms.Select)
    level = forms.ChoiceField(initial='1', choices=VASTA_LEVELS, widget=forms.Select)

    def __init__(self, *args, **kwargs):
        self.set_settings()
        self.set_default_data()
        self.default_data['gametype'] = 'qa',
        super(VastaSettings, self).__init__(*args, **kwargs)


class VastaQuestion(OahpaQuestion):
    """
    Questions for vasta
    """

    select_words = select_words
    vasta_is_correct = vasta_is_correct
        
    def __init__(self, question, qwords, userans_val, correct_val, *args, **kwargs):                 

        self.init_variables("", userans_val, [])
        
        question_widget = forms.HiddenInput(attrs={'value' : question.id})

        super(VastaQuestion, self).__init__(*args, **kwargs)

        maxlength=50
        answer_size=50
        self.fields['answer'] = forms.CharField(max_length = maxlength, \
                                                widget=forms.TextInput(\
			attrs={'size': answer_size, 'onkeypress':'return process(this, event, document.theform);',}))

        self.fields['question_id'] = forms.CharField(widget=question_widget, required=False)

        # In qagame, all words are considered as answers.

        self.gametype="vasta"
        self.messages, jee, joo = self.vasta_is_correct(question.string, qwords, None)
        
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
            if not qwords.has_key(w): qstring = qstring + " " + force_unicode(w)
            else:
                if qwords[w].has_key('fullform'):
                    qstring = qstring + " " + force_unicode(qwords[w]['fullform'][0])
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


def sahka_is_correct(self,utterance,targets):
    """
    Analyzes the answer and returns a message.
    """
    if not self.is_valid():
        return False

    if not self.cleaned_data.has_key('answer'):
        return
    qwords = {}
    # Split the question to words for analaysis.

    self.messages, self.dia_messages,  self.variable = self.vasta_is_correct(utterance.utterance, None, utterance.name)
    if self.target:
        if not self.messages:
            self.error = "correct"
    else:
        for answer in self.dia_messages:
            answer = answer.lstrip("&dia-")
            if not self.messages:
                self.error = "correct"
            self.target = answer

    #self.error = "correct"
    
class SahkaSettings(OahpaSettings):

    dialogue = forms.ChoiceField(initial='firstmeeting', choices=DIALOGUE_CHOICES, widget=forms.Select)
    
    def __init__(self, *args, **kwargs):
        self.set_settings()
        self.set_default_data()
        self.default_data['gametype'] = 'sahka'
        self.default_data['dialogue_id'] = '1'
        self.default_data['dialogue'] = 'firstmeeting'
        self.default_data['topicnumber'] = '0'
        super(SahkaSettings, self).__init__(*args, **kwargs)

    def init_hidden(self, topicnumber, num_fields, dialogue):
        
        # Store topicnumber as hidden input to keep track of topics.
        #print "topicnumber", topicnumber
        #print "num_fields", num_fields
        topicnumber = topicnumber
        num_fields = num_fields
        dialogue = dialogue


class SahkaQuestion(OahpaQuestion):
    """
    Sahka: Dialogue game
    """

    select_words = select_words
    sahka_is_correct = sahka_is_correct
    vasta_is_correct = vasta_is_correct

    def __init__(self, utterance, qwords, targets, global_targets, userans_val, correct_val, *args, **kwargs):                 
        
        self.init_variables("", userans_val, [])

        utterance_widget = forms.HiddenInput(attrs={'value' : utterance.id})        
        
        super(SahkaQuestion, self).__init__(*args, **kwargs)

        if utterance.utttype == "question":
            maxlength=50
            answer_size=50
            self.fields['answer'] = forms.CharField(max_length = maxlength, \
                                                    widget=forms.TextInput(\
            attrs={'size': answer_size, 'onkeypress':'return process(this, event, document.theform);',}))

        self.fields['utterance_id'] = forms.CharField(widget=utterance_widget, required=False)

        self.global_targets = global_targets
        self.utterance =""
        self.qattrs={}

        if utterance:
            self.utterance_id=utterance.id
            #self.utterance=utterance.utterance

            # Forms question string and answer string out of grammatical elements and other strings.
            qstring = ""
            
            # Format question string
            qtext = utterance.utterance
            for w in qtext.split():
                if not qwords.has_key(w):
                    qstring = qstring + " " + force_unicode(w)
                    self.qattrs['question_fullform_' + w] = force_unicode(w)
                else:
                    if qwords[w].has_key('fullform'):
                        qstring = qstring + " " + force_unicode(qwords[w]['fullform'][0])
                        self.qattrs['question_fullform_' + w] = qwords[w]['fullform'][0]
                    else:
                        qstring = qstring + " " + w
                        self.qattrs['question_fullform_' + w] = w

            # this is for -guovttos
            qstring=qstring.replace(" -","-");
            qstring=qstring.replace("- ","-");
                    
            # Remove leading whitespace and capitalize.
            qstring=qstring.replace(" .",".");
            qstring=qstring.replace(" ?","?");
            qstring=qstring.replace(" !","!");

            qstring = qstring.lstrip()
            if len(qstring)>0:
                qstring = qstring[0].capitalize() + qstring[1:]

            self.utterance=qstring

        self.target=""
        self.dia_messages = ""		
        self.gametype="sahka"
        self.sahka_is_correct(utterance,targets)
        if self.target:
            variable=""
            if utterance.links.filter(target=self.target).count()>0:
                variable = utterance.links.filter(target=self.target)[0].variable
                if variable:
                    self.qattrs['target_' + variable] = self.variable
                    self.global_targets[variable] = { 'target' : self.variable }
        for t in self.global_targets.keys():
            if not self.qattrs.has_key(t):
                self.qattrs['target_' + t] = self.global_targets[t]['target']
							
        #self.error="correct"
        self.errormsg = ""

        if correct_val == "correct":
            self.error="correct"
