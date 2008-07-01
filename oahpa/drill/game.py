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

        if self.settings.books:
            if self.settings.books == 'all':
                self.settings.books=self.settings.allbooks
            else:
                books=self.settings.books
                self.settings.books=[]
                self.settings.books.append(books)
                
        if self.settings.semtype:
            if self.settings.semtype == 'all':
                self.settings.semtype=self.settings.allsem
            else:
                semtype=self.settings.semtype
                self.settings.semtype=[]
                self.settings.semtype.append(semtype)

        
    def new_game(self):
        self.form_list = []
        for n in range (0, self.num_fields):
            db_info = Info()
            db_info.userans = ""
            db_info.correct = ""
            self.get_db_info(db_info)
            self.create_form(db_info, n, 0)

        if not self.form_list:
            # No questions found, so the quiz_id must have been bad.
            raise Http404('Invalid quiz id.')

    def check_game(self, data=None):

        db_info = Info()

        # If POST data was data check, regenerate the form using ids.
        for n in range (0, self.num_fields):
            if n == 0:
                n_word_id = "word_id"
                n_tag_id = "tag_id"
                n_question_id = "question_id"
                n_numeral_id = "numeral_id"
                n_qstring = "qstring"
                n_astring = "astring"
                n_userans = "userans"
                n_correct = "correct"
            else:
                n_word_id = str(n) + "-word_id"
                n_tag_id = str(n) + "-tag_id"
                n_question_id = str(n) + "-question_id"
                n_numeral_id = str(n) + "-numeral_id"
                n_qstring = str(n) + "-qstring"
                n_astring = str(n) + "-astring"
                n_userans = str(n) + "-userans"
                n_correct = str(n) + "-correct"

            if "word_id" in data:
                db_info.word_id=data[n_word_id]
            if "question_id" in data:
                db_info.question_id=data[n_question_id]
            if "tag_id" in data:
                db_info.tag_id=data[n_tag_id]
            if "numeral_id" in data:
                db_info.numeral=data[n_numeral_id]

            if "qstring" in data:
                db_info.qstring=data[n_qstring]
            if "astring" in data:
                db_info.astring=data[n_astring]
                
            db_info.userans = data[n_userans]
            db_info.correct = data[n_correct]

            self.create_form(db_info, n, data)
            
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
                db_info.word_id = word_id
                db_info.tag_id = tag_id
                db_info.question_id = question_id
                return

    def create_form(self, db_info, n, data=None):

        word_id = db_info.word_id
        tag_id = db_info.tag_id
        question_id = db_info.question_id

        form_list=Form.objects.filter(Q(word__pk=word_id) & Q(tag__pk=tag_id))
        if not form_list:
            return HttpResponse("No forms found.")
        
        word = Word.objects.filter(Q(id=word_id))[0]
        tag = Tag.objects.filter(Q(id=tag_id))[0]
        question_list = Question.objects.filter(Q(id=question_id))
        tr_list=Translationnob.objects.filter(Q(word__pk=word_id))
        
        morph = (MorphQuestion(word, tag, form_list, tr_list, question_list[0], db_info.userans, db_info.correct, data, prefix=n))
        self.form_list.append(morph)


class BareGame(Game):

    casetable = {'N-ILL':'Ill', 'N-ESS':'Ess', 'N-GEN':'Gen', 'N-LOC':'Loc', 'N-ACC':'Acc', 'N-COM':'Com'}

    def get_db_info(self, db_info):

        syll = self.settings.syll
        pos = self.settings.pos
        books=self.settings.books
        case=self.settings.case
        if self.settings.pos == "N":
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
            
        tag_count=Tag.objects.filter(Q(pos=pos) & Q(possessive="") & Q(case=case) & Q(tense=tense) & Q(mood=mood) & Q(conneg="")).count()

        while True:
            tag_id = Tag.objects.filter(Q(pos=pos) & Q(possessive="") & Q(case=case) & Q(tense=tense) & Q(mood=mood) & Q(conneg=""))[randint(0,tag_count-1)].id

            w_count=Word.objects.filter(Q(pos=pos) & Q(stem__in=syll) & Q(source__name__in=books)).count()
            word_id=Word.objects.filter(Q(pos=pos) & Q(stem__in=syll) & Q(source__name__in=books))[randint(0,w_count-1)].id
                
            form_count = Form.objects.filter(Q(word__pk=word_id) & Q(tag__pk=tag_id)).count()
            if word_id and form_count>0:
                db_info.word_id = word_id
                db_info.tag_id = tag_id
                return


    def create_form(self, db_info, n, data=None):

        word_id = db_info.word_id
        tag_id = db_info.tag_id

        form_list=Form.objects.filter(Q(word__pk=word_id) & Q(tag__pk=tag_id))
        if not form_list:
            return HttpResponse("No forms found.")
        
        word = Word.objects.get(Q(id=word_id))
        tag = Tag.objects.get(Q(id=tag_id))
        tr_list=Translationnob.objects.filter(Q(word__pk=word_id))
        morph = (MorphQuestion(word, tag, form_list, tr_list, "", db_info.userans, db_info.correct, data, prefix=n))
        self.form_list.append(morph)


class NumGame(Game):

    def get_db_info(self, db_info):

        numeral=""
        num_list = []

        while True:
            random_num = randint(0, int(self.settings.maxnum))

            if random_num:
                db_info.numeral = random_num
                return 

    def create_form(self, db_info, n, data=None):

        language=self.settings.language
        numstring =""
        # Add generator call here
        #fstdir="/Users/saara/gt/" + language + "/bin"        
    
        fstdir="/opt/smi/" + language + "/bin"
        gen_norm_fst = fstdir + "/" + language + "-num.fst"
        
        gen_norm_lookup = "echo " + str(db_info.numeral) + " | /usr/local/bin/lookup -flags mbTT -utf8 -d " + gen_norm_fst
        #gen_norm_lookup = "echo " + str(db_info.numeral) + " | /Users/saara/bin/lookup -flags mbTT -utf8 -d " + gen_norm_fst
        print gen_norm_lookup
        num_tmp = os.popen(gen_norm_lookup).readlines()
        num_list=[]
        for num in num_tmp:
            line = num.strip()
            if line:
                nums = line.split('\t')
                num_list.append(nums[1].decode('utf-8'))
        numstring = num_list[0]
        form = (NumQuestion(db_info.numeral, numstring, num_list, self.settings.numgame, db_info.userans, db_info.correct, data, prefix=n))
        self.form_list.append(form)


class QuizzGame(Game):

    def get_db_info(self, db_info):

        semtypes=self.settings.semtype
        books=self.settings.books
        while True:
            w_count=Word.objects.filter(Q(semtype__semtype__in=semtypes) & Q(source__name__in=books)).count()
            random_word=Word.objects.filter(Q(semtype__semtype__in=semtypes) & Q(source__name__in=books))[randint(0,w_count-1)]
                
            word_id=random_word.id

            tr_list=random_word.translation.all()
            if tr_list:
                db_info.word_id = word_id
                db_info.question_id = ""
                return db_info

    def create_form(self, db_info, n, data=None):

        word_id = db_info.word_id
        translations=Translationnob.objects.filter(Q(word__pk=word_id))
        word_list = Word.objects.filter(Q(id=word_id))
        question_list=[]

        if not translations:
            return HttpResponse("No forms found.")        

        word = word_list[0]
        tr_list = translations
            
        #if db_info.question_id:
        #    question_list = Question.objects.filter(Q(id=db_info.question_id))
            
        form = (QuizzQuestion(word, tr_list, question_list, db_info.userans, db_info.correct, data, prefix=n))
        self.form_list.append(form)


