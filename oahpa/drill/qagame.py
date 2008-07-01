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
        #self.syntax = ('N-ILL','N-LOC','N-ACC','N-GEN','N-COM','N-ESS','OBJ','NOUN','MAINV2','NEG','INTERR')
        self.syntax =('NEG','MAINV','SUBJ','ANSWERSUBJECT')
        self.qtype_verbs = set(['VERB','V-COND','V-IMPRT','V-GO'])

        # Default tense and mood for testing
        self.tense = "Prs"
        self.mood = "Ind"
        self.gametype="morfa"
        
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
        self.PronPNBase={'Sg1':'mun','Sg2':'don','Sg3':'son',\
                         'Pl1':'mun','Pl2':'don','Pl3':'son',\
                         'Du1':'mun','Du2':'don','Du3':'son'}
        self.NounPN=['Sg','Pl']
        self.NountoPronPN={'Sg':'Sg3','Pl':'Pl3'}

    
    # Select a word matching semtype and return full form.
    def get_word(self, qelement, tag_el=None):

        word_ids = []
        if qelement:
            # If word_id is given
            if qelement.word_id:
                print "word found: " + str(qelement.word_id)
                word_ids.append(qelement.word_id)
            else:
                # Only one semtype allowed at the moment.
                # Change this.
                if SemtypeElement.objects.filter(qelement=qelement, game='morfa').count()>0:
                    semtypeelement = SemtypeElement.objects.filter(qelement=qelement, game='morfa')[0]
                    semtype= Semtype.objects.get(id=semtypeelement.semtype_id)
                    semstring=semtype.semtype
                    
                    print "SEMTYPE: " + semstring
                    #remove this!
                    if semstring == "TIME-POINT-GEN-PL" or semstring=="TIME-POINT-ESS":
                        semstring = "TIME"
                    if semstring == "MYTH-HUMAN" or semstring=="MYTH":
                        semstring = "HUMAN"
                    if semstring == "SLIDE-TOOL":
                        semstring = "TOOL"
                    if tag_el:
                        for word in list(Word.objects.filter(Q(semtype__semtype=semstring))):
                            if Form.objects.filter(Q(tag=tag_el.id) & Q(word=word.id)).count()>0:
                                word_ids.append(word.id)

        return word_ids

    def get_element(self, question_element, syntax):

        if self.gametype:
            if QElement.objects.filter(Q(question=question_element) & \
                                       Q(syntax=syntax) &\
                                       Q(gametype=self.gametype)).count()>0:
                return QElement.objects.filter(Q(question=question_element) & \
                                               Q(syntax=syntax) &\
                                               Q(gametype=self.gametype))[0]
            
        if QElement.objects.filter(Q(question=question_element) &\
                                   Q(syntax=syntax)).count()>0:
            return QElement.objects.filter(Q(question=question_element) & \
                                           Q(syntax=syntax))[0]
        return None

    def generate_question(self, question, qtype):
        """
        Generate question for the form.
        Only one question is generated.
        """
        qtext=question.string
        print "QUESTION " + str(question.id) + " " + qtext
        qwords = {}
    
        # Find out syntax elements
        qwords_list=[]
        for w in qtext.split():
            if w== "": continue
            qwords_list.append(w)

        # Handle all grammatical elements one at the time
        # 1. SUBJ-MAINV argreement
        subjnumber=None
        word=None
        subj_el=None
        tag_el=None
        if 'SUBJ' in set(qwords_list):
            
            qwords['SUBJ'] = {}
            
             # Take first subject, change this!
            subj_el=self.get_element(question, 'SUBJ')
            
            tag_el_count = subj_el.tag.count()
            tag_el = subj_el.tag.all()[randint(0, tag_el_count-1)]

            # Get number information fo subject
            subjwords = []
            if tag_el.pos=="Pron":
                subjnumber = tag_el.personnumber
                pronbase = self.PronPNBase[subjnumber]
                subjwords.append(Word.objects.get(Q(lemma=pronbase)).id)
            else:
                subjnumber = tag_el.number
                subjwords = self.get_word(subj_el, tag_el)

            print len(subjwords)
            if tag_el:
                qwords['SUBJ']['tag'] = []
                qwords['SUBJ']['tag'].append(tag_el.id)
            if subjwords:
                qwords['SUBJ']['word'] = []
                qwords['SUBJ']['word'].append(subjwords[randint(0, len(subjwords)-1)])
            if subjnumber:
                qwords['SUBJ']['number'] = subjnumber
            if Form.objects.filter(Q(word__pk=qwords['SUBJ']['word'][0]) &\
                                   Q(tag__pk=tag_el.id)).count()>0:
                qwords['SUBJ']['fullform'] = []
                qwords['SUBJ']['fullform'].append(Form.objects.filter(Q(word__pk=qwords['SUBJ']['word'][0]) &\
                                                                  Q(tag__pk=tag_el.id))[0].fullform)

        if 'MAINV' in set(qwords_list):

            qwords['MAINV'] = {}

            # Resolve answer subject and question mainverb numbers
            # using the number of the subject
            
            mainv_tag=None
            mainv_el=None
            v_number=None
            mainv_word=None
            mainv_el = self.get_element(question,'MAINV')
            if mainv_el:

                # If the tag count is only one it is V+Inf
                # Do not use question verb either if this is verb question.
                if mainv_el.tag.count()==1: 
                    mainv_tag=mainv_el.tag.all()[0]                    
                else:
                    if qwords.has_key('SUBJ'):
                        subjnumber=qwords['SUBJ']['number']
                        v_number = self.SVPN[subjnumber]
                        if qtype in self.qtype_verbs:
                            mainv_tag = mainv_el.tag.filter(Q(personnumber=v_number))[0]
                        else:
                            mainv_tag = mainv_el.tag.filter(Q(personnumber=v_number) & \
                                                            Q(tense=self.tense) & \
                                                            Q(mood=self.mood))[0]

                # Select random mainverb
                mainv_words = self.get_word(mainv_el, mainv_tag)
                if mainv_words:
                    mainv_word = mainv_words[randint(0, len(mainv_words)-1)]

            if mainv_tag:
                qwords['MAINV']['tag'] = []
                qwords['MAINV']['tag'].append(mainv_tag.id)
            if mainv_word:
                qwords['MAINV']['word'] = []
                qwords['MAINV']['word'].append(mainv_word)
            if Form.objects.filter(Q(word__pk=mainv_word) &\
                                   Q(tag__pk=mainv_tag.id)).count() > 0:
                qwords['MAINV']['fullform'] = []
                qwords['MAINV']['fullform'].append(Form.objects.filter(Q(word__pk=mainv_word) &\
                                                                       Q(tag__pk=mainv_tag.id))[0].fullform)
                
        # 2. Other grammatical elements
        # At the moment, agreement is not taken into account
        for s in qwords_list:
            if s in set(self.syntax): continue
            words=[]
            tag_el=None

            qwords[s] = {}
            element = self.get_element(question,s)
            if element:
                tag_el_count = element.tag.count()
                if tag_el_count > 0:
                    tag_el = element.tag.all()[randint(0, tag_el_count-1)]

                # Select random word
                words = self.get_word(element, tag_el)
                if words:
                    word = words[randint(0, len(words)-1)]
                print "WORD ", tag_el.string, word

            # get fullform for the qelement
            fullform=""
            if word and tag_el:
                if Form.objects.filter(Q(word__pk=word) & \
                                       Q(tag__pk=tag_el.id)).count()>0:
                    fullform = Form.objects.filter(Q(word__pk=word) & \
                                                   Q(tag__pk=tag_el.id))[0].fullform
            else:
                fullform = s
            
            if tag_el:
                qwords[s]['tag'] = []
                qwords[s]['tag'].append(tag_el.id)
            if word:
                qwords[s]['word'] = []
                qwords[s]['word'].append(word)
            if fullform:
                qwords[s]['fullform'] = []
                qwords[s]['fullform'].append(fullform)

        return qwords


    def generate_answers_subj(self, answer, question, awords, qwords, qtype):
        
        subj=""
        if awords.has_key('ANSWERSUBJECT'): subj='ANSWERSUBJECT'
        else: subj='SUBJ'
        
        word_ids=[]
        a_number=""
                
        if qwords.has_key('SUBJ'):
            subjtag_id=qwords['SUBJ']['tag'][0]
            subjtag = Tag.objects.get(id=subjtag_id)

            if subjtag.pos=="Pron":
                subjnumber = subjtag.personnumber
            else:
                subjnumber = subjtag.number
            a_number=self.QAPN[subjnumber]
            asubjtag = subjtag.string.replace(subjnumber,a_number)
            asubjtag_el = Tag.objects.get(string=asubjtag)
                                    
            if self.PronPNBase.has_key(a_number):
                pronbase = self.PronPNBase[a_number]
                word_ids.append(Word.objects.get(Q(lemma=pronbase)).id)
                print "SUBJECT: " + Word.objects.get(Q(lemma=pronbase)).lemma

        
        if not word_ids:
            word_ids = qwords['SUBJ']['word'][:]

            # Subject for the answer
            # Check if there are elements
            # that are specified for the answer subject.
            #for ans in answers:
            #    ans_subj = self.get_element(ans,'SUBJ')
            #    if not ans_subj:
            #        ans_subj = self.get_element(ans,'ANSWERSUBJECT')
            #    if ans_subj:
            #        subjwords = self.get_word(ans_subj)
            #        if subjwords:
            #            word_ids.append(subjwords)

        awords[subj]['tag'].append(asubjtag_el.id)
        if a_number:
            awords[subj]['number'] = a_number
        awords[subj]['word'] = word_ids[:]

        if not subj == 'SUBJ':
            awords['SUBJ'] = {'tag' : [], 'word' : []}
            if asubjtag_el:
                awords['SUBJ']['tag'].append(asubjtag_el.id)
            if a_number:
                awords['SUBJ']['number'] = a_number
            awords['SUBJ']['word'] = word_ids[:]

        return awords
    
    def generate_answers_mainv(self, answer, question, awords, qwords, qtype):

        va_number=None
        v_number=None
        amainv_tag=None
        amainv_words=[]
        if awords.has_key('SUBJ') and awords['SUBJ'].has_key('number'):
            a_number=awords['SUBJ']['number']
            va_number=self.SVPN[a_number]
        if qwords.has_key('MAINV') and va_number:
            mainvtag_id=qwords['MAINV']['tag'][0]
            mainvtag = Tag.objects.get(id=mainvtag_id)
            v_number = mainvtag.personnumber
            print v_number, mainvtag_id, va_number
            if Tag.objects.filter(id=mainvtag_id).count()>0:
                mainvtag_string = Tag.objects.filter(id=mainvtag_id)[0].string
                amainvtag_string = mainvtag_string.replace(v_number,va_number)
                amainv_tag = Tag.objects.get(string=amainvtag_string)

        mainv_el = self.get_element(answer,'MAINV')
        if mainv_el:
            print mainv_el.id
            if not amainv_tag:
                amainv_tag=mainv_el.tag.all()[0]

        if not qtype in self.qtype_verbs:
            amainv_words = self.get_word(None, amainv_tag)
        else:
            amainv_words = self.get_word(mainv_el, amainv_tag)

        if not amainv_words and qwords['MAINV'].has_key('word'):
            amainv_words = qwords['MAINV']['word'][:]
        if not amainv_tag and qwords['MAINV'].has_key('tag'):
            amainv_tag = Tag.objects.get(id=qwords['MAINV']['tag'][0])

        #print "mainverb tag selected.. ", amainv_tag.string
        print "mainverb words.. ", amainv_words
        if amainv_tag:
            awords['MAINV']['tag'].append(amainv_tag.id)
        awords['MAINV']['word'] = amainv_words[:]
            
        return awords

    def generate_syntax(self, answer, question, awords, qwords, qtype, s):

        if not awords.has_key(s):
            awords[s] = {}
        
        fullform=""
        words=[]
        tag_el=None
        
        element = self.get_element(answer,s)
        if element:
            if element.agreement:
                agr_id = element.agreement_id
                agr_el = QElement.objects.get(id=agr_id)
                agr_syntax = agr_el.identifier
                if qwords.has_key(agr_syntax) and qwords[agr_syntax].has_key('tag') and \
                       qwords[agr_syntax]['tag'][0]:
                    agr_tag_id = qwords[agr_syntax]['tag'][0]
                    agr_tag = Tag.objects.get(id=agr_tag_id)
                    if agr_tag.personnumber:
                        tag_count = element.tag.filter(personnumber=agr_tag.personnumber).count()
                        if tag_count>0:
                            tag_el = element.tag.filter(personnumber=agr_tag.personnumber)\
                                     [randint(0, tag_count-1)]
                    if agr_tag.number:
                        tag_count= element.tag.filter(number=agr_tag.number).count()
                        if tag_count>0:
                            tag_el = element.tag.filter(number=agr_tag.number)\
                                     [randint(0, tag_count-1)]
            else:
                tag_count = element.tag.count()
                if tag_count > 0:
                    tag_el = element.tag.all()[randint(0, tag_count-1)]
                                
            if tag_el:
                words = self.get_word(element, tag_el)
                
        if not words and qwords.has_key(s) and qwords[s].has_key('word'):
            words = qwords[s]['word'][:]
        if not tag_el and qwords.has_key(s) and qwords[s].has_key('tag') and qwords[s]['tag'][0]:
            awords[s]['tag'].append(qwords[s]['tag'][0])
            
        if tag_el:
            awords[s]['tag'].append(tag_el.id)
        awords[s]['word'] = words[:]

        return awords

    def get_db_info(self, db_info):

        anslist=[]
        pos=self.settings.pos
        if pos == "N": qtype=self.settings.case
        else: qtype=self.settings.vtype
        print "QTYPE: " + qtype

        # If the question id is received from the interface, use that question info
        # Otherwise select random question
        qwords = {}
        if db_info.has_key('question_id'):
            question = Question.objects.get(id=db_info['question_id'])
            qwords=db_info['qwords']
        else:
            q_count=Question.objects.filter(qtype=qtype).count()
            question = Question.objects.filter(qtype=qtype)[randint(0, q_count-1)]
            qwords= self.generate_question(question, qtype)
            db_info['qwords'] = qwords

        qtext = question.string

        # Select answer using the id from the interface.
        # Otherwise select answer that is related to the question.
        if db_info.has_key('answer_id'):
            answer=Question.objects.get(id=db_info['answer_id'])
        else:
            answer=question.answer_set.all()[0]

        # Generate the set of possible answers if they are not coming from the interface
        # Or if the gametype is qa.
        awords = {}
        if db_info.has_key('answer_id') and self.settings.gametype == 'context':
            awords=db_info['awords']
        else:
            # Generate the set of possible answers
            # Here only the text of the first answer is considered!!
            atext=answer.string
            words_strings = set(atext.split())
            
            #Initialize each element identifier
            for w in atext.split():
                if w== "": continue
                print w
                w = w.replace("(","")
                w = w.replace(")","")
                info = {'tag' : [], 'word' : []}
                awords[w] = info

            # Subject and main verb are special cases:
            # There is subject-verb agreement and correspondence with question elements.
            if 'SUBJ' in words_strings or 'ANSWERSUBJECT' in words_strings:
                awords = self.generate_answers_subj(answer, question, awords, qwords, qtype)

            if 'MAINV' in words_strings:
                awords = self.generate_answers_mainv(answer, question, awords, qwords, qtype)

            # Rest of the syntax
            for s in words_strings:
                if s in set(self.syntax): continue
                awords = self.generate_syntax(answer, question, awords, qwords, qtype, s)

        db_info['awords'] = awords

        # Store everything for the html form 
        db_info['question_id'] = question.id
        db_info['answer_id'] = answer.id
        db_info['gametype'] = self.settings.gametype
        
        return db_info

    def create_form(self, db_info, n, data=None):

        question = Question.objects.get(Q(id=db_info['question_id']))
        answer = Question.objects.get(Q(id=db_info['answer_id']))
        print db_info['awords']
        print "awords ...................."
        print db_info['qwords']
        print "qwords ...................."
        form = (QAQuestion(db_info['gametype'], question, answer, \
                           db_info['qwords'], db_info['awords'],\
                           db_info['userans'], db_info['correct'], data, prefix=n))

        self.form_list.append(form)


