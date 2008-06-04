# -*- coding: utf-8 -*-

from django.template import Context, loader
from oahpa.drill.models import *
from oahpa.drill.forms import *
from oahpa.drill.game import Game
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from random import randint
from django.contrib.admin.views.decorators import _encode_post_data, _decode_post_data
import os,codecs,sys,re

class Info:
    pass

class QAGame(Game):

    def init_tags(self):

        self.num_fields = 3
        self.tagset = {}
        self.tagclasses = {}
        self.syntax = ('N-ILL','N-LOC','N-ACC','N-GEN','N-COM','N-ESS','INTERR','OBJ','NOUN')

        # Default tense and mood for testing
        self.tense = "Prs"
        self.mood = "Ind"

        # Extract available tags and tagclasses
        # Move this information to the database!
        
        tagfile="/Users/saara/ped/sme/src/tags.txt"
        tags =[]
        fileObj = codecs.open(tagfile, "r", "utf-8" )
        tags = fileObj.readlines()
        fileObj.close()
        
        classObj=re.compile(r'^#\s*(?P<typeString>[\w\-]*)\s*$', re.U)
        stringObj=re.compile(r'^(?P<tagString>[\w]*)\s*$', re.U)

        tagclass=""
        for line in tags:
            line.strip()
            matchObj=classObj.search(line) 
            if matchObj:
                tagclass = matchObj.expand(r'\g<typeString>')
                if not self.tagclasses.has_key(tagclass):
                    self.tagclasses[tagclass] = []
            else:
                matchObj=stringObj.search(line)
                if matchObj:
                    string = matchObj.expand(r'\g<tagString>')
                    self.tagset[string]=tagclass
                    self.tagclasses[tagclass].append(string)
                    
        # Values for pairs QPN-APN
        self.QAPN={'Sg':'Sg','Sg1':'Sg2','Sg2':'Sg1','Sg3':'Sg3',\
                   'Pl':'Pl','Pl1':'Pl2','Pl2':'Pl1','Pl3':'Pl3',\
                   'Du1':'Du2','Du2':'Du1','Du3':'Du3'}

        # Values for subject-verb agreement:
        # e.g. Subject with N+Sg+Nom requires verb with Sg3.
        self.SVPN={'Sg1':'Sg1','Sg2':'Sg2','Sg3':'Sg3','Sg':'Sg3',\
                   'Pl1':'Pl1','Pl2':'Pl2','Pl3':'Pl3','Pl':'Pl3',\
                   'Du1':'Du1','Du2':'Du2','Du3':'Du3'}

        # Available values for Number
        self.PronPN=['Sg1','Sg2','Sg3','Pl1','Pl2','Pl3','Du1','Du2','Du3']
        self.NounPN=['Sg','Pl']

    # Find a value for a tag.
    def get_tagvalue(self, t, pnval, pos):
        
        # If the string is a tag
        if self.tagset.has_key(t):
            return t
        
        if t == "Tense" and self.tense:
            return self.tense
        if t == "Mood" and self.mood:
            return self.mood

        if t=="Number":
            random_tag = self.NounPN[randint(0, len(self.NounPN)-1)]
            return random_tag

        if t=="Person-Number":
            return pnval
        
        # If only the tagclass is given, select a random tag
        # from the class.
        if self.tagclasses.has_key(t):
            
            ttmp=self.tagclasses[t]
            random_tag = ttmp[randint(0, len(ttmp)-1)]
            print "random tag " + random_tag
            return random_tag

    # Select a word matching semtype and return full form.
    def get_word(self, qelement, tagstring, word_id=None):

        word = None
        if qelement:
            if qelement.word_id:
                print "word found: " + str(qelement.word_id)
                word = Word.objects.get(id=qelement.word_id)
            else:
                if word_id:
                    word = Word.objects.get(id=word_id)
                else:
                    if qelement.semtype_id:
                        semtype= Semtype.objects.get(id=qelement.semtype_id)
                        if semtype.semtype == "HUMAN":
                            semstring="FAMILY"
                        else:
                            if semtype.semtype == "OBJECT":
                                semstring="THING"
                            else:
                                semstring=semtype.semtype
                            
                        print "SEMTYPE: " + semstring                    
                        while True:
                            w_count = Word.objects.filter(Q(semtype__semtype=semstring)).count()
                            if w_count == 0: break
                            word = Word.objects.filter(Q(semtype__semtype=semstring))[randint(0,w_count-1)]
                            if word:
                                f_count = Form.objects.filter(Q(tag__string=tagstring) & Q(word=word.id)).count()
                            if f_count > 0: break
                        
        if not word and word_id:
            word = Word.objects.get(id=word_id)
        if word:
            fcount=Form.objects.filter(Q(tag__string=tagstring) & Q(word=word.id)).count()
            if fcount > 0:
                form=Form.objects.filter(Q(tag__string=tagstring) & Q(word=word.id))[0]
                print form.fullform
                
                return form.fullform, word

        return "", word

    def get_element(self, question, syntax, elementtype, word_id=None, pnval=None, tagvalue=None):

        pos=""
        tagspec=""
        if not pnval:
            el_count=Element.objects.filter(Q(qelement__question=question) \
                                            & Q(qelement__elementtype=elementtype) \
                                            & Q(syntax=syntax)).count()
            if el_count > 0:
                elem = Element.objects.filter(Q(qelement__question=question) \
                                              & Q(qelement__elementtype=elementtype)\
                                              & Q(syntax=syntax))[0]
                if elem.pos=="Pron":
                    pnval = self.PronPN[randint(0, len(self.PronPN)-1)]
                else:
                    if elem.pos=="N":
                        pnval = self.NounPN[randint(0, len(self.NounPN)-1)]
                    else:
                        pnval = self.NounPN[randint(0, len(self.NounPN)-1)]
                pos=elem.pos
                
        tags = []
        tagstring =""
        qelement=None
        qelement_count = QElement.objects.filter(Q(question=question) \
                                           & Q(elementtype=elementtype) \
                                           & Q(element__syntax=syntax)).count()
        if qelement_count > 0:
            qelement = QElement.objects.filter(Q(question=question) \
                                               & Q(elementtype=elementtype) \
                                               & Q(element__syntax=syntax))[0]
            element = Element.objects.filter(Q(qelement__question=question)\
                                             & Q(qelement__elementtype=elementtype)\
                                             & Q(syntax=syntax))[0]
            if not element.tagspec:
                print "ERROR TAGSPEC"

            tagspec = element.tagspec
            
        if not tagspec:
            if tagvalue:
                tagspec=tagvalue
                
        if tagspec:
            for t in tagspec.split('+'):
                #print "TAG " + t
                tagstr = self.get_tagvalue(t, pnval, pos)
                tags.append(tagstr)
            
            tagstring= "+".join(tags)
        
        print "Correct tagstring " + tagstring
        fullform, word = self.get_word(qelement, tagstring, word_id)
        return fullform, word, tagstring
        
        return "", None
        

    def get_db_info(self, db_info):

        anslist=[]        
        qtype=self.settings.case

        qelement = None
        if True:
            # Limit number of questions for testing
            q_count=Question.objects.filter(qtype=qtype).count()
            question = Question.objects.filter(qtype=qtype)[randint(0, q_count-1)]
            question_id=question.id
            print "QUESTION_ID " + str(question_id)

            question=Question.objects.get(id=question_id)
            qtext=question.question
            atext=question.answer

            qstring = ""
            astring=""
            qwords = {}
            awords = {}
            
            #Initialize each word.
            for w in qtext.split(' '):
                qwords[w] = w
            for w in atext.split(' '):
                w = w.replace("(","")
                w = w.replace(")","")
                awords[w] = w

            # Create question and answer in parallel.
            # Handle all grammatical elements one at the time
            # 1. SUBJ-MAINV argreement
            subjumber=None
            word=None
            if qwords.has_key('SUBJ'):
                subj_el = Element.objects.filter(Q(qelement__question__id=question_id) \
                                                 & Q(qelement__elementtype="question") \
                                                 & Q(syntax="SUBJ"))[0]
                if subj_el.pos=="Pron":
                    subjnumber = self.PronPN[randint(0, len(self.PronPN)-1)]
                else:
                    subjnumber = self.NounPN[randint(0, len(self.NounPN)-1)]                    
                fullform, subjword, subjtag  = self.get_element(question, 'SUBJ', "question", None, subjnumber)
                if subjtag.count('Sg+')>0 or subjtag.count('Pl+')>0:
                    dbtag = Tag.objects.filter(Q(string=subjtag))[0]
                    if dbtag.number: subjnumber= dbtag.number
                    if dbtag.personnumber: subjnumber= dbtag.personnumber
                if fullform:
                    print "FULLFORM: " + fullform
                    qwords['SUBJ'] = fullform
                else:
                    qwords['SUBJ'] = "SUBJ+" + subjnumber

            # Subject for the answer
            a_number=None
            if subjnumber:
                print "SUBJNUMBER " + subjnumber
                a_number=self.QAPN[subjnumber]
                v_number = self.SVPN[subjnumber]
                asubjtag = subjtag.replace(v_number,a_number)
                
            if awords.has_key('SUBJ'):

                # Check first if there are elements
                # that are specified for the answer subject.
                ans_subj_count = Element.objects.filter(Q(qelement__question__id=question_id) \
                                                & Q(qelement__elementtype="answer") \
                                                & Q(syntax="SUBJ")).count()
                if ans_subj_count > 0:
                    fullform, asubj_word, asubjtag = \
                              self.get_element(question, 'SUBJ', "answer", None, a_number)

                # Otherwise search answer subject using question subject
                else:
                    if subjword:
                        fullform, asubj_word, asubjtag = \
                                  self.get_element(question, 'SUBJ', "answer", subjword.id, a_number, asubjtag)
                    else:
                        print "FATAL ERROR 0"

                if fullform:
                    awords['SUBJ'] = fullform
                else:
                    awords['SUBJ'] = "SUBJ+" + a_number
                    
            if qwords.has_key('MAINV'):
                fullform, mainv_word, mainvtag = self.get_element(question, 'MAINV', 'question', None, v_number)
                if fullform:
                    qwords['MAINV'] = fullform
                    print "FULLFORM: " + fullform
                else:
                    qwords['MAINV'] = "MAINV+" + subjnumber

            # The same mainverb for both question and answer.

            if awords.has_key('MAINV'):
                if a_number:
                    va_number=self.SVPN[a_number]
                    print "va_number " + va_number
                else:
                    va_number=None
                if mainv_word:
                    amainvtag = mainvtag.replace(v_number,va_number)
                    fullform, ans_word, amainvtag= \
                              self.get_element(question, 'MAINV', 'answer', mainv_word.id, v_number, amainvtag)
                else:
                     fullform, ans_word, amainvtag=self.get_element(question, 'MAINV', 'answer', None, v_number)
                if fullform:
                     awords['MAINV'] = fullform
                else:
                    awords['MAINV'] = "MAINV+" + a_number
                    
            # 2. Other grammatical elements
            for s in self.syntax:
                fullform=""
                word=None
                if qwords.has_key(s):
                    fullform, word,stag = self.get_element(question, s, "question")
                    if fullform:
                        qwords[s] = fullform
                        print "FULLFORM: " + fullform
                    else:
                        qwords[s] = s
                        
                if awords.has_key(s):
                    if not fullform:
                        fullform, word, stag = self.get_element(question, s, "answer")
                    if fullform:
                        awords[s] = fullform
                    else:
                        awords[s] = s

            # Handle answer element separately
            awords[qtype] = "Q"
            fullform, word, stag = self.get_element(question, qtype, "answer")                
            if not fullform:
                print "FATAL ERROR"
            if not word:
                print "FATAL ERROR2"
            if not stag:
                print "FATAL ERROR3"
            db_info.word_id=word.id
            db_info.tag_id=Tag.objects.get(string=stag).id

            # Forms question string out of grammatical elements and other strings.
            for w in qtext.split(' '):
                print "W " + w
                if not qwords.has_key(w):
                    qstring = qstring + " " + w
                else:
                    qstring = qstring + " " + qwords[w]

            for w in atext.split(' '):
                print "AW " + w
                if w.count("(") > 0:
                    w = w.replace("(","")
                    w = w.replace(")","")
                    if w!='SUBJ': continue
                        
                if not awords.has_key(w):
                    astring = astring + " " + w
                else:
                    print w, awords[w]
                    astring = astring + " " + awords[w]

            # Remove leading whitespace
            astring = astring.lstrip()
            qstring = qstring.lstrip()
            
            # Store everything for the html form 
            db_info.question_id = question_id
            db_info.qstring = qstring + "?"
            db_info.astring = astring 

            return db_info

    def create_form(self, db_info, n, data=None):

        question = Question.objects.get(Q(id=db_info.question_id))
        word = Word.objects.get(Q(id=db_info.word_id))
        tag = Tag.objects.get(Q(id=db_info.tag_id))
        form_list=Form.objects.filter(Q(word__pk=word.id) & Q(tag__pk=tag.id))
        
        form = (QAQuestion(word, tag, form_list, db_info.qstring, question, db_info.astring, db_info.userans, db_info.correct, data, prefix=n))
        self.form_list.append(form)


