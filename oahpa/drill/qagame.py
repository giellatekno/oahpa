# -*- coding: utf-8 -*-

from django.template import Context, loader
from oahpa.drill.models import *
from oahpa.drill.forms import *
from oahpa.drill.game import Game
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from random import randint
#from django.contrib.admin.views.decorators import _encode_post_data, _decode_post_data
import os,codecs,sys,re

class Info:
    pass

class QAGame(Game):

    def init_tags(self):
        """
        Initialize the grammatical information.
        This information should be moved to parameters
        """
        self.num_fields = 3
        #self.syntax = ('N-ILL','N-LOC','N-ACC','N-GEN','N-COM','N-ESS','OBJ','NOUN','MAINV2','NEG','INTERR')
        self.syntax =('MAINV','SUBJ','ANSWERSUBJECT','CONNEG','PRFPRC')
        self.qtype_verbs = set(['MAINV','V-COND','V-IMPRT','V-GO'])
        self.numerals = ['NUM-ATTR']

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

    def get_qword(self, qelement, tag_el):

        max = 50
        i=0
        form_list=None
        while not form_list and i<max:
            i= i+1
            word_count = WordQElement.objects.filter(qelement=qelement).count()
            qw_el = WordQElement.objects.filter(qelement=qelement)[randint(0,word_count-1)]
            word_el = qw_el.word
            
            form_list = Form.objects.filter(Q(tag=tag_el.id) & Q(word=word_el.id))

        if not form_list:
            return None
    
        fullform = form_list[0].fullform
        info = { 'word' : word_el.id, 'tag' : tag_el.id, 'fullform' : [ fullform ], 'qelement' : qelement }
        return info
    
    # Select a word matching semtype and return full form.
    def get_words(self, qelement, tag_el=None, lemma=None, word_id=None):
        """
        Select word from possible options in the element.
        """

        words = []

        # If there are no information available for these elements, try to use other info.
        word = None
        if lemma and tag_el:
            word = Word.objects.filter(lemma=lemma)[0]
        else:
            if word_id and tag_el:
                word = Word.objects.filter(id=word_id)[0]
        if word:
            if Form.objects.filter(Q(tag=tag_el.id) & Q(word=word.id)).count()>0:
                fullform = Form.objects.filter(Q(tag=tag_el.id) & Q(word=word.id))[0].fullform
                info = {'word': word.id, 'tag' : tag_el.id, 'fullform' : [ fullform ] }
                words.append(info)                    

        return words

    def get_elements(self, question_element, identifier):

        if self.gametype:
            if QElement.objects.filter(Q(question=question_element) & \
                                       Q(identifier=identifier) &\
                                       Q(gametype=self.gametype)).count()>0:
                return QElement.objects.filter(Q(question=question_element) & \
                                               Q(identifier=identifier) &\
                                               Q(gametype=self.gametype))

        else:
            print "NO GAMETYPE!"
        return None

    def generate_question(self, question, qtype):
        """
        Generate question for the form.
        Only one question is generated.
        """
        qtext=question.string
        #print "QUESTION " + str(question.id) + " " + qtext
        qwords = {}
    
        # Find out syntax elements
        qwords_list=[]
        for w in qtext.split():
            if w== "": continue
            qwords_list.append(w)

        # Handle all grammatical elements one at the time
        # 1. SUBJ-MAINV argreement

        if 'SUBJ' in set(qwords_list):
            
            qwords['SUBJ'] = {}
            
            # Select randomly an element, if there are more than one available.
            # This way there is only one subject and tag for each question.
            subj_elements=self.get_elements(question, 'SUBJ')
            subj_el = subj_elements[randint(0, len(subj_elements)-1)]
            tag_el_count = subj_el.tags.count()

            # If there was no tag elements, there is nothing to do.
            # Subject tag is needed for everything else. 
            if tag_el_count == 0:
                return None
            
            tag_el = subj_el.tags.all()[randint(0, tag_el_count-1)]
            
            # Get number information for subject
            subjword = {}
            if tag_el.pos=="Pron":
                subjnumber = tag_el.personnumber 
                pronbase = self.PronPNBase[subjnumber]
                word_el=Word.objects.filter(Q(lemma=pronbase))[0]
                info = self.get_words(None, tag_el, None, word_el.id)[0]
            else:
                subjnumber = tag_el.number 
                info = self.get_qword(subj_el, tag_el)

            if not info: return None
            
            subjword = info
            subjword['number'] = subjnumber
            qwords['SUBJ'] = subjword


        if 'MAINV' in set(qwords_list):

            qwords['MAINV'] = {}
            mainv_word = None
            
            # Select one mainverb element for question.
            mainv_elements = self.get_elements(question,'MAINV')
            if mainv_elements:
                mainv_el = mainv_elements[randint(0, len(mainv_elements)-1)]
                
                # If there is only on tag element, then there are no choices for agreement.
                tag_el_count = mainv_el.tags.count()
                if tag_el_count == 1:
                    tag_el=mainv_el.tags.all()[0]
                else:
                    # Subject-verb agreement
                    if qwords.has_key('SUBJ') and qwords['SUBJ'].has_key('number'):
                        subjnumber=qwords['SUBJ']['number']
                        v_number = self.SVPN[subjnumber]
                        if qtype in self.qtype_verbs:
                            mainv_tags = mainv_el.tags.filter(Q(personnumber=v_number))
                        else:
                            mainv_tags = mainv_el.tags.filter(Q(personnumber=v_number) & \
                                                            Q(tense=self.tense) & \
                                                            Q(mood=self.mood))
                    # If there is no subject element
                    # then select random tag from all tags.
                    else:
                        mainv_tag_count = mainv_el.tags.count()
                        mainv_tags = mainv_el.tags.all()

                    tag_el = mainv_tags[randint(0, mainv_tags.count()-1)]

                # Select random mainverb
                info = self.get_qword(mainv_el, tag_el)
                mainv_word = info

                if not mainv_word:
                    return None
                    #qwords['MAINV'] = { 'fullform' : ["MAINV"] }
                else:
                    qwords['MAINV'] = mainv_word

            if not mainv_word:
                return None
                #qwords['MAINV'] = { 'fullform' : ["MAINV"] }

        # 2. Other grammatical elements
        # At the moment, agreement is not taken into account
        for s in qwords_list:
            if s in set(self.syntax): continue

            tag_el=None
            word = {}
            
            elements = self.get_elements(question,s)
            if elements:
                element = elements[randint(0, len(elements)-1)]                
                tag_el_count = element.tags.count()
                if tag_el_count > 0:
                    tag_el = element.tags.all()[randint(0, tag_el_count-1)]

                # Select random word
                info = self.get_qword(element, tag_el)
                word = info
                
                #print "WORD ", s, tag_el.string, word

            if not word:
                word['fullform'] = []
                word['fullform'].append(s)
            
            qwords[s] = word

        # Return the ready qwords list.
        return qwords


    def generate_answers_subj(self, answer, question, awords, qwords, qtype):
        
        subj=""
        if awords.has_key('ANSWERSUBJECT'): subj='ANSWERSUBJECT'
        else: subj='SUBJ'
        
        words=[]
        word_ids=[]
        a_number=""

        # If there is subject in the question, there is agreement.
        if qwords.has_key('SUBJ'):
            qword = qwords['SUBJ']
            subjtag_id=qword['tag']
            subjtag = Tag.objects.get(id=subjtag_id)

            # Take into account that answer may start with pronoun!!!
            if subjtag.pos=="Pron":
                subjnumber = subjtag.personnumber
            else:
                subjnumber = subjtag.number

            a_number=self.QAPN[subjnumber]
            asubjtag = subjtag.string.replace(subjnumber,a_number)
            asubjtag_el = Tag.objects.get(string=asubjtag)

            # If pronoun, get the correct form
            if self.PronPNBase.has_key(a_number):
                pronbase = self.PronPNBase[a_number]
                words = self.get_words(None, asubjtag_el, pronbase)

                for word in words:
                    word['number'] = a_number
                    
            if not words:
                words.append(qwords['SUBJ'])

        # Check if there are elements specified for the answer subject.
        else:
            subj_elements = self.get_elements(answer,subj)
            if subj_elements:
                subj_el = subj_elements[randint(0, len(subj_elements)-1)]                
                tag_el_count = subj_el.tags.count()
                if tag_el_count > 0:
                    tag_el = subj_el.tags.all()[randint(0, tag_el_count-1)]

                if tag_el.pos=="Pron":
                    a_number = tag_el.personnumber 
                else:
                    a_number = tag_el.number 

                # No word specified.                
                info = { 'qelement': subj_el.id, 'tag' : tag_el.id, 'number' : a_number }
                word = info
                words.append(word)
                
                for word in words:
                    word['number'] = a_number

        # Copy if subject was answersubj, copy information to SUBJ to ensure agreement.
        awords[subj] = words[:]
        if not subj == 'SUBJ':
            awords['SUBJ'] = words[:]

        return awords
    
    def generate_answers_mainv(self, answer, question, awords, qwords, qtype, eltype):

        mainv_elements = self.get_elements(answer,eltype)

        mainv_words = []
        mainv_tag = None
        mainv_tags = []

        # It is assumed that all subjects cause the same inflection
        # for verb, so it does not matter which subject is selected.
        if awords.has_key('SUBJ') and len(awords['SUBJ']) > 0:
            # mainverb number depends on the number of the subject.
            asubj = awords['SUBJ'][0]
            a_number=asubj['number']
            va_number=self.SVPN[a_number]

            # Take qwords mainverb tag as basis
            # If there is no subject, then the number of the question
            # mainverb determines the number.
            if qwords.has_key('MAINV') and qwords['MAINV']:
                qmainv = qwords['MAINV']
                
                qmainvtag_id = qmainv['tag']
                qmainvtag = Tag.objects.get(id=qmainvtag_id)
                qmainvtag_string = qmainvtag.string
                v_number = qmainvtag.personnumber
                amainvtag_string = qmainvtag_string.replace(v_number,va_number)
                
                mainv_tag = Tag.objects.get(string=amainvtag_string)
                mainv_tags.append(mainv_tag)
            
        # Mainverb word if needed:
        if qwords.has_key('MAINV'):
            #print "ON VERBI"
            mainv_word = qwords['MAINV']['word']

        # If the main verb is under question, then generate full list.
        if qtype in self.qtype_verbs:
            mainv_words = []
            if mainv_elements:
                for mainv_el in mainv_elements:
                    if mainv_el.tags.count()>0:
                        mainv_tags = mainv_el.tags.filter(Q(personnumber=va_number))
                        for t in mainv_tags:
                            info = { 'qelement' : mainv_el.id, 'tag' : t.id }
                            mainv_words.append(info)
                    else:
                        info = { 'qelement' : mainv_el.id, 'tag' : mainv_tag.id }
                        mainv_words.append(info)

            else:
                if mainv_word:
                    mainv_words.extend(self.get_words(None, mainv_tag, None, mainv_word))
                    
        # Otherwise take only one element
        else:
            if mainv_elements:
                mainv_element = mainv_elements[randint(0, len(elements)-1)]                
                tag_el_count = mainv_element.tags.count()
                if tag_el_count > 0:
                    mainv_tags = mainv_el.tags.filter(Q(personnumber=va_number))
                for tag in mainv_tags:
                    info = { 'qelement' : mainv_element.id, 'tag' : mainv_tag.id }
                    mainv_words.append(info)

            else:
                for tag in mainv_tags:
                    info = { 'tag' : mainv_tag.id, 'word' : mainv_word }
                    mainv_words.append(info)
                    
        if not mainv_words and qwords.has_key(eltype):
            mainv_words.append(qwords[eltype])

        #print "mainverb words.. ", mainv_words
        awords[eltype] = mainv_words
            
        return awords

    def generate_syntax(self, answer, question, awords, qwords, qtype, s):

        if not awords.has_key(s):
            awords[s] = []

        if (s=='MAINV' and qtype == "MAINV") or s=='NEG':
            return awords

        # In these cases, the question mainverb is normally
        # copied and inflected.
        word_id=None
        if s=="PRFPRC" or s=="CONNEG":
            # Mainverb word if needed:
            if qwords.has_key('MAINV'):
                word_id = qwords['MAINV']['word']
        
        tag_elements = None
        #print "generating syntax", s
        # Temporary array for words
        swords = []
        elements = self.get_elements(answer,s)
        if elements:
            for element in elements:
                if element.agreement:
                    agr_id = element.agreement_id
                    agr_el = QElement.objects.get(id=agr_id)
                    agr_syntax = agr_el.identifier
                    if qwords.has_key(agr_syntax):
                        qword = qwords[agr_syntax]
                        if qword.has_key('tag'):
                            agr_tag_id = qword['tag']
                            agr_tag = Tag.objects.get(id=agr_tag_id)
                            if agr_tag.personnumber:
                                tag_count = element.tags.filter(personnumber=agr_tag.personnumber).count()
                                if tag_count>0:
                                    tag_elements = element.tags.filter(personnumber=agr_tag.personnumber)

                            if agr_tag.number:
                                tag_count= element.tags.filter(number=agr_tag.number).count()
                                if tag_count>0:
                                    tag_elements = element.tags.filter(number=agr_tag.number)
                                
                # if no agreement, take all tags.
                else:
                    tag_count = element.tags.count()
                    if tag_count > 0:
                        tag_elements = element.tags.all()

                # Take word forms for all tags
                if tag_elements:
                    for tag_el in tag_elements:

                        # Special treatment for numerals.
                        if (qtype == "NUM-ATTR" and element.identifier=="NUM-ATTR"):
                            w_count=Word.objects.filter(Q(pos="Num")).count()
                            word_id=Word.objects.filter(Q(pos="Num"))[randint(0,w_count-1)].id
                            info = {'word' : word_id, 'tag' : tag_el.id  }                            
                            swords.append(info)

                        else:
                            info = { 'qelement' : element.id, 'word' : word_id, 'tag' : tag_el.id  }
                            swords.append(info)

        awords[s] = swords
        
        return awords

    def get_db_info(self, db_info,default_qtype=None):

        anslist=[]
        pos=self.settings['pos']

        #print self.gametype
        # Select random question type.
        if not default_qtype:
            if pos == "N":
                if self.gametype == 'qa':
                    qtype = self.settings['allcase'][randint(0, len(self.settings['allcase'])-1)]
                else:
                    qtype = self.settings['case']
            if pos == "V":
                if self.gametype == 'qa':
                    qtype = self.settings['allcase'][randint(0, len(self.settings['allcase'])-1)]
                else:                    
                    qtype=self.settings['vtype']
            if pos == "Num":
                if self.gametype == 'qa':
                    qtype = self.settings['allcase'][randint(0, len(self.settings['allcase'])-1)]
                else:                                            
                    qtype=self.settings['num_context']
        #if pos == "A":

        if default_qtype: qtype = default_qtype
 
        #print "QTYPE: " + qtype

        # If the question id is received from the interface, use that question info
        # Otherwise select random question
        qwords = {}
        if db_info.has_key('question_id'):
            question = Question.objects.get(id=db_info['question_id'])
            qwords=db_info['qwords']
        else:
            q_count=Question.objects.filter(qtype=qtype).count()
            max = 50
            i=0
            while not qwords and i<max:
                i = i+1
                qnum = randint(0, q_count-1)
                # TESTING
                #qnum = 3
                #print "qnum:", qnum
                question = Question.objects.filter(qtype=qtype)[qnum]
                if question.gametype and not question.gametype == self.gametype: continue
                qwords = None
                qwords= self.generate_question(question, qtype)
            db_info['qwords'] = qwords

        qtext = question.string
        #print "QWORDS1", qwords

        # Select answer using the id from the interface.
        # Otherwise select answer that is related to the question.
        if db_info.has_key('answer_id'):
            answer=Question.objects.get(id=db_info['answer_id'])
        else:
            answer_count=question.answer_set.count()
            answer=question.answer_set.all()[randint(0,answer_count-1)]

        # Generate the set of possible answers if they are not coming from the interface
        # Or if the gametype is qa.
        awords = {}
        if db_info.has_key('answer_id') and self.settings['gametype'] == 'context':
            awords=db_info['awords']
        else:
            # Generate the set of possible answers
            # Here only the text of the first answer is considered!!
            atext=answer.string
            words_strings = set(atext.split())

            #print words_strings
            
            #Initialize each element identifier
            for w in atext.split():
                if w== "": continue
                #print w
                w = w.replace("(","")
                w = w.replace(")","")
                info = {}
                awords[w] = info

            # Subject and main verb are special cases:
            # There is subject-verb agreement and correspondence with question elements.
            if 'SUBJ' in words_strings or 'ANSWERSUBJECT' in words_strings:
                awords = self.generate_answers_subj(answer, question, awords, qwords, qtype)

            if 'MAINV' in words_strings:
                awords = self.generate_answers_mainv(answer, question, awords, qwords, qtype, 'MAINV')
            #else:
            #    if 'MAINV2' in words_strings:
            #        awords = self.generate_answers_mainv(answer, question, awords, qwords, qtype, 'MAINV2')
            if 'NEG' in words_strings:
                awords = self.generate_answers_mainv(answer, question, awords, qwords, qtype, 'NEG')
                
            # Rest of the syntax
            for s in words_strings:
                if s in set(self.syntax): continue
                awords = self.generate_syntax(answer, question, awords, qwords, qtype, s)

        db_info['awords'] = awords

        # Store everything for the html form 
        db_info['question_id'] = question.id
        db_info['answer_id'] = answer.id
        db_info['gametype'] = self.settings['gametype']
        
        return db_info

    def create_form(self, db_info, n, data=None):

        question = Question.objects.get(Q(id=db_info['question_id']))
        answer = Question.objects.get(Q(id=db_info['answer_id']))
        #print "awords:", db_info['awords']
        #print "awords ...................."
        #print "qwords:", db_info['qwords']
        #print "qwords ...................."
        form = (QAQuestion(db_info['gametype'], question, answer, \
                           db_info['qwords'], db_info['awords'],\
                           db_info['userans'], db_info['correct'], data, prefix=n))

        self.form_list.append(form)


