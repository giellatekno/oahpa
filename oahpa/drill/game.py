# -*- coding: utf-8 -*-

from django.template import Context, loader
from oahpa.drill.models import *
from oahpa.drill.forms import *
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from random import randint
from django.contrib.admin.views.decorators import _encode_post_data, _decode_post_data
import os,codecs,sys,re

class Info:
    pass

class Game:

    def __init__(self, settings):
        self.form_list = []
        self.count = ""
        self.score = ""
        self.settings = settings
        self.all_correct = ""
        self.show_correct = 0
        self.num_fields = 5

        if self.settings.semtype:
            if self.settings.semtype == 'all':
                self.settings.semtype=self.settings.allsem
            else:
                semtype=self.settings.semtype[:]
                self.settings.semtype=[]
                self.settings.semtype.append(semtype)

        
    def new_game(self):
        self.form_list = []
        for n in range (1, self.num_fields):
            db_info = {}
            db_info['userans'] = ""
            db_info['correct'] = ""
            self.get_db_info(db_info)
            self.create_form(db_info, n, 0)

        if not self.form_list:
            # No questions found, so the quiz_id must have been bad.
            raise Http404('Invalid quiz id.')

    def search_info(self, reObj, string, value, words, type):

        matchObj=reObj.search(string) 
        if matchObj:
            syntax = matchObj.expand(r'\g<syntaxString>')
            if not words.has_key(syntax):
                words[syntax] = {}

            words[syntax][type] = value

        return words


    def check_game(self, data=None):

        db_info = {}

        question_tagObj=re.compile(r'^question_tag_(?P<syntaxString>[\w\-]*)$', re.U)
        question_wordObj=re.compile(r'^question_word_(?P<syntaxString>[\w\-]*)$', re.U)
        question_fullformObj=re.compile(r'^question_fullform_(?P<syntaxString>[\w\-]*)$', re.U)
        answer_tagObj=re.compile(r'^answer_tag_(?P<syntaxString>[\w\-]*)$', re.U)
        answer_wordObj=re.compile(r'^answer_word_(?P<syntaxString>[\w\-]*)$', re.U)
        answer_fullformObj=re.compile(r'^answer_fullform_(?P<syntaxString>[\w\-]*)$', re.U)

        # If POST data was data check, regenerate the form using ids.
        for n in range (1, self.num_fields):
            db_info = {}
            qwords = {}
            awords = {}
            tmpawords = {}

            for d, value in data.items():
                if d.count(str(n) + '-')>0:
                    d = d.lstrip(str(n) + '-')
                    qwords = self.search_info(question_tagObj, d, value, qwords, 'tag')
                    qwords = self.search_info(question_wordObj, d, value, qwords, 'word')
                    qwords = self.search_info(question_fullformObj, d, value, qwords, 'fullform')

                    tmpawords = self.search_info(answer_tagObj, d, value, tmpawords, 'tag')
                    tmpawords = self.search_info(answer_wordObj, d, value, tmpawords, 'word')
                    tmpawords = self.search_info(answer_fullformObj, d, value, tmpawords, 'fullform')

                    db_info[d] = value

            for syntax in qwords.keys():
                if qwords[syntax].has_key('fullform'):
                    qwords[syntax]['fullform'] = [ qwords[syntax]['fullform']]

            for syntax in tmpawords.keys():
                awords[syntax] = []
                info = {}
                if tmpawords[syntax].has_key('word'):
                    info['word'] = tmpawords[syntax]['word']
                    if tmpawords[syntax].has_key('tag'):
                        info['tag'] = tmpawords[syntax]['tag']
                    if tmpawords[syntax].has_key('fullform'):
                        info['fullform'] = [ tmpawords[syntax]['fullform']]
                        
                    awords[syntax].append(info)
                                        
            db_info['qwords'] = qwords
            db_info['awords'] = awords


            new_db_info = {}
            if self.settings.gametype == 'qa' or self.settings.gametype == 'context':
                new_db_info = self.get_db_info(db_info)
            if not new_db_info:
                new_db_info = db_info
            self.create_form(new_db_info, n, data)
            
    def get_score(self, data):

        # Add correct forms for words to the page
        if "show_correct" in data:
            self.show_correct = 1
            for form in self.form_list:
                form.set_correct()
                self.count=2

        # Count correct answers:
        self.all_correct=0
        self.score=""
        i=0
        for form in self.form_list:
            if form.error == "correct":
                i=i+1
                if i == len(self.form_list):
                    self.all_correct=1

        if self.show_correct or self.all_correct:
            self.score = self.score.join([`i`, "/", `len(self.form_list)`])



class ContextGame(Game):
    
    def get_db_info(self, db_info):

        syll = self.settings.syll
        pos = self.settings.pos
        semtype = self.settings.semtype
        tag_count=Tag.objects.filter(pos=settings.pos).count()

        while True:

            tag_id = Tag.objects.filter(pos=settings.pos)[randint(0, tag_count-1)].id

            q_count=Question.objects.filter(tag__pk=tag_id).count()
            if q_count==0:
                continue
            random_question = Question.objects.filter(tag__pk=tag_id)[randint(0, q_count-1)]
            question_id = random_question.id
            qtype=random_question.semtype

            w_count=Word.objects.filter(Q(pos=pos) & Q(stem__in=syll) & Q(semtype=qtype)).count()
            word_id=Word.objects.filter(Q(pos=pos)&Q(stem__in=syll)&Q(semtype=qtype))[randint(0,w_count-1)].id
            
            form_count = Form.objects.filter(Q(word__pk=word_id) & Q(tag__pk=tag_id)).count()
            if word_id and form_count>0:
                db_info['word_id'] = word_id
                db_info['tag_id'] = tag_id
                db_info['question_id'] = question_id
                return

    def create_form(self, db_info, n, data=None):

        word_id = db_info['word_id']
        tag_id = db_info['tag_id']
        question_id = db_info['question_id']

        form_list=Form.objects.filter(Q(word__pk=word_id) & Q(tag__pk=tag_id))
        if not form_list:
            return HttpResponse("No forms found.")
        
        word = Word.objects.filter(Q(id=word_id))[0]
        tag = Tag.objects.filter(Q(id=tag_id))[0]
        question_list = Question.objects.filter(Q(id=question_id))
        translations=word.translations.all()
        
        morph = (MorphQuestion(word, tag, form_list, translations, question_list[0], db_info['userans'], db_info['correct'], data, prefix=n))
        self.form_list.append(morph)


class BareGame(Game):

    casetable = {'N-ILL':'Ill', 'N-ESS':'Ess', 'N-GEN':'Gen', 'N-LOC':'Loc', 'N-ACC':'Acc', 'N-COM':'Com'}

    def get_db_info(self, db_info):

        syll = self.settings.syll
        pos = self.settings.pos
        books=self.settings.book
        case=self.settings.case
        if self.settings.pos == "N" or self.settings.pos == "Num":
            case = self.casetable[case]
        else:
            case = ""
        
        if self.settings.pos == "V":
            if self.settings.vtype_bare == "PRS":
                mood = "Ind"
                tense = "Prs"
            if self.settings.vtype_bare == "PRT":
                mood = "Ind"
                tense = "Prt"
            if self.settings.vtype_bare == "COND":
                mood = "Cond"
                tense = "Prs"
            if self.settings.vtype_bare == "IMPRT":
                mood = "Imprt"
                tense = "Prs"
            if self.settings.vtype_bare == "POT":
                mood = "Pot"
                tense = "Prs"
        else:
            mood=""
            tense=""
            
        tag_count=Tag.objects.filter(Q(pos=pos) & Q(possessive="") & Q(case=case) & Q(tense=tense) & Q(mood=mood) & ~Q(personnumber="ConNeg")).count()

        while True:
            tag_id = Tag.objects.filter(Q(pos=pos) & Q(possessive="") & Q(case=case) & Q(tense=tense) & Q(mood=mood) & ~Q(personnumber="ConNeg"))[randint(0,tag_count-1)].id
            
            if self.settings.pos == "Num":
                if self.settings.case == "Attr":
                    tag_id = Tag.objects.filter(Q(pos="Num") & Q(attributive="Attr"))[randint(0,tag_count-1)].id
                    f_count=Form.objects.filter(Q(tag__pk=tag_id)).count()
                    form=Form.objects.filter(Q(tag__pk=tag_id))[randint(0,f_count-1)]
                    word_id = form.word.id
                else:
                    w_count=Word.objects.filter(Q(pos=pos)).count()
                    word_id=Word.objects.filter(Q(pos=pos))[randint(0,w_count-1)].id
            else:
                w_count=Word.objects.filter(Q(pos=pos) & Q(stem__in=syll) & Q(source__name__in=books)).count()
                word_id=Word.objects.filter(Q(pos=pos) & Q(stem__in=syll) & Q(source__name__in=books))[randint(0,w_count-1)].id
                
            form_count = Form.objects.filter(Q(word__pk=word_id) & Q(tag__pk=tag_id)).count()
            if word_id and form_count>0:
                db_info['word_id'] = word_id
                db_info['tag_id'] = tag_id
                return


    def create_form(self, db_info, n, data=None):

        word_id = db_info['word_id']
        tag_id = db_info['tag_id']

        form_list=Form.objects.filter(Q(word__pk=word_id) & Q(tag__pk=tag_id))
        if not form_list:
            return HttpResponse("No forms found.")
        
        word = Word.objects.get(Q(id=word_id))
        tag = Tag.objects.get(Q(id=tag_id))
        translations=word.translations.all()
        morph = (MorphQuestion(word, tag, form_list, translations, "", db_info['userans'], db_info['correct'], data, prefix=n))
        self.form_list.append(morph)


class NumGame(Game):

    def get_db_info(self, db_info):

        numeral=""
        num_list = []

        while True:
            random_num = randint(0, int(self.settings.maxnum))

            if random_num:
                db_info['numeral_id'] = random_num
                return db_info
        
        
    def create_form(self, db_info, n, data=None):

        language=self.settings.language
        numstring =""
        # Add generator call here
        fstdir="/Users/saara/gt-cvs/" + language + "/bin"        
        lookup ="/Users/saara/bin/lookup"
        
        #fstdir="/opt/smi/" + language + "/bin"
        #lookup = "/usr/local/bin/lookup"
        gen_norm_fst = fstdir + "/" + language + "-num.fst"
        
        
        gen_norm_lookup = "echo " + str(db_info['numeral_id']) + " | lookup -flags mbTT -utf8 -d " + gen_norm_fst

        num_tmp = os.popen(gen_norm_lookup).readlines()
        num_list=[]
        for num in num_tmp:
            line = num.strip()
            if line:
                nums = line.split('\t')
                num_list.append(nums[1].decode('utf-8'))
        numstring = num_list[0]
        form = (NumQuestion(db_info['numeral_id'], numstring, num_list, self.settings.numgame, db_info['userans'], db_info['correct'], data, prefix=n))
        self.form_list.append(form)


class QuizzGame(Game):

    def get_db_info(self, db_info):

        books=self.settings.book
        semtypes=self.settings.semtype

        while True:
            # smenob
            if self.settings.transtype == "smenob":            
                if semtypes:
                    if self.settings.book.count('all') > 0:
                        w_count=Word.objects.filter(Q(semtype__semtype__in=semtypes)).count()
                        random_word=Word.objects.filter(Q(semtype__semtype__in=semtypes))[randint(0,w_count-1)]
                    else:
                        w_count=Word.objects.filter(Q(semtype__semtype__in=semtypes) &\
                                                    Q(source__name__in=books)).count()
                        random_word=Word.objects.filter(Q(semtype__semtype__in=semtypes) & \
                                                        Q(source__name__in=books))[randint(0,w_count-1)]
                else:
                    w_count=Word.objects.filter( Q(source__name__in=books)).count()
                    random_word=Word.objects.filter( Q(source__name__in=books))[randint(0,w_count-1)]

            # nobsme
            else:
                if semtypes:
                    if self.settings.book.count('all') > 0:
                        w_count=Wordnob.objects.filter(Q(semtype__semtype__in=semtypes)).count()
                        random_word=Wordnob.objects.filter(Q(semtype__semtype__in=semtypes))[randint(0,w_count-1)]
                    else:
                        w_count=Wordnob.objects.filter(Q(semtype__semtype__in=semtypes) &\
                                                    Q(source__name__in=books)).count()
                        random_word=Wordnob.objects.filter(Q(semtype__semtype__in=semtypes) & \
                                                           Q(source__name__in=books))[randint(0,w_count-1)]
                else:
                    w_count=Wordnob.objects.filter( Q(source__name__in=books)).count()
                    random_word=Wordnob.objects.filter( Q(source__name__in=books))[randint(0,w_count-1)]
                
            word_id=random_word.id
            print word_id
            translations=random_word.translations.all()
            
            if translations:
                db_info['word_id'] = word_id
                db_info['question_id'] = ""
                return db_info

    def create_form(self, db_info, n, data=None):

        word_id = db_info['word_id']
        if self.settings.transtype == "smenob":
            word=Word.objects.get(Q(id=word_id))
            translations=word.translations.all()
        else:
            print "jee", word_id
            word=Wordnob.objects.get(id=word_id)
            translations=word.translations.all()

        question_list=[]

        if not translations:
            return HttpResponse("No forms found.")        
            
        form = (QuizzQuestion(self.settings.transtype, word, translations, question_list, db_info['userans'], db_info['correct'], data, prefix=n))
        self.form_list.append(form)


