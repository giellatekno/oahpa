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
        self.num_fields = 5

        
    def new_game(self):
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

        morph_list=[]
        db_info = Info()

        # If POST data was data check, regenerate the form using ids.
        for n in range (0, self.num_fields):
            if n == 0:
                n_word_id = "word_id"
                n_tag_id = "tag_id"
                n_question_id = "question_id"
                n_numeral_id = "numeral_id"
                n_userans = "userans_stored"
                n_correct = "correct"
            else:
                n_word_id = str(n) + "-word_id"
                n_tag_id = str(n) + "-tag_id"
                n_question_id = str(n) + "-question_id"
                n_numeral_id = str(n) + "-numeral_id"
                n_userans = str(n) + "-userans_stored"
                n_correct = str(n) + "-correct"

            if "word_id" in data:
                db_info.word_id=data[n_word_id]
            if "question_id" in data:
                db_info.question_id=data[n_question_id]
            if "tag_id" in data:
                db_info.tag_id=data[n_tag_id]
            if "numeral_id" in data:
                db_info.numeral=data[n_numeral_id]
            db_info.userans = data[n_userans]
            db_info.correct = data[n_correct]

            self.create_form(db_info, n, data)
            
    def get_score(self, data):

        # Add correct forms for words to the page
        if "show_correct" in data:
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

        if "show_correct" in data or self.all_correct:
            self.score = self.score.join([`i`, "/", `len(self.form_list)`])



class ContextGame(Game):
    
    def get_db_info(self, db_info):

        question_list=[]
        morph_list=[]

        tag_list=Tag.objects.filter(pos=settings.partofsp)
        num_tags=len(tag_list)

        syll = self.settings.syll
        partofsp = self.settings.partofsp
        semtype = self.settings.semtype

        while True:
            tag_id = tag_list[randint(0, len(tag_list)-1)].id

            question_list=Question.objects.filter(tag__pk=tag_id)
            if not question_list:
                continue
            random_question = question_list[randint(0, len(question_list)-1)]
            question_id = random_question.id
            qtype=random_question.semtype

            if len(syll) == 1:
                word_list=Word.objects.filter(Q(pos=partofsp) & Q(stem=syll[0]) & Q(semtype=qtype))
            else:
                word_list=Word.objects.filter(Q(pos=partofsp) & Q(stem__in=syll) & Q(semtype=qtype))
                word_id = word_list[randint(0, len(word_list)-1)].id
                
                form_list = Form.objects.filter(Q(word__pk=word_id) & Q(tag__pk=tag_id))
                if word_list and form_list:
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
        
        word_list = Word.objects.filter(Q(id=word_id))
        tag_list = Tag.objects.filter(Q(id=tag_id))
        question_list = Question.objects.filter(Q(id=question_id))
        tr_list=Translationnob.objects.filter(Q(word__pk=word_id))
        
        morph = (MorphQuestion(word_list[0], tag_list[0], form_list, tr_list, question_list[0], db_info.userans, db_info.correct, data, prefix=n))
        self.form_list.append(morph)


class BareGame(Game):

    def get_db_info(self, db_info):

        word_list=[]

        syll = self.settings.syll
        partofsp = self.settings.partofsp
        semtype = self.settings.semtype

        tag_list=Tag.objects.filter(Q(pos=partofsp) & Q(possessive=""))
        num_tags=len(tag_list)

        while True:
            tag_id = tag_list[randint(0, num_tags-1)].id

            if len(syll) == 1:
                word_list=Word.objects.filter(Q(pos=partofsp) & Q(stem=syll[0]))
            else:
                word_list=Word.objects.filter(Q(pos=partofsp) & Q(stem__in=syll))
            
            word_id = word_list[randint(0, len(word_list)-1)].id
                
            form_list = Form.objects.filter(Q(word__pk=word_id) & Q(tag__pk=tag_id))
            if word_list and form_list:
                db_info.word_id = word_id
                db_info.tag_id = tag_id
                return


    def create_form(self, db_info, n, data=None):

        word_id = db_info.word_id
        tag_id = db_info.tag_id

        form_list=Form.objects.filter(Q(word__pk=word_id) & Q(tag__pk=tag_id))
        if not form_list:
            return HttpResponse("No forms found.")
        
        word_list = Word.objects.filter(Q(id=word_id))
        tag_list = Tag.objects.filter(Q(id=tag_id))
        tr_list=Translationnob.objects.filter(Q(word__pk=word_id))

        morph = (MorphQuestion(word_list[0], tag_list[0], form_list, tr_list, "", db_info.userans, db_info.correct, data, prefix=n))
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


        numstring =""
        # Add generator call here
        fstdir="/opt/smi/sme/bin"
        gen_norm_fst = fstdir + "/sme-num.fst"
        gen_norm_lookup = "echo " + str(db_info.numeral) + " | /usr/local/bin/lookup -flags mbTT -utf8 -d " + gen_norm_fst
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

        word_list=[]
        morph_list=[]
        question_list=[]
        
        partofsp = self.settings.partofsp
        semtype = self.settings.semtype

        while True:
            word_list=Word.objects.filter(Q(pos=partofsp) & Q(semtype=semtype))
            word_list=Word.objects.filter(Q(pos=partofsp))
            random_word = word_list[randint(0, len(word_list)-1)]
            word_id=random_word.id
			
            tr_list=random_word.translation.all()
            if tr_list:
                db_info.word_id = word_id
                db_info.question_id = ""
                return db_info

    def create_form(self, db_info, n, data=None):

        word_id = db_info.word_id

        tr_list=Translationnob.objects.filter(Q(word__pk=word_id))
        if not tr_list:
            return HttpResponse("No forms found.")
        
        word_list = Word.objects.filter(Q(id=word_id))
        question_list=[]
        #if db_info.question_id:
        #    question_list = Question.objects.filter(Q(id=db_info.question_id))
            
        form = (QuizzQuestion(word_list[0], tr_list, question_list, db_info.userans, db_info.correct, data, prefix=n))
        self.form_list.append(form)


