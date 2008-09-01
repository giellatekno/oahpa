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
        """
        Initialize the grammatical information.
        This information should be moved to parameters
        """
        self.num_fields = 3
        #self.syntax = ('N-ILL','N-LOC','N-ACC','N-GEN','N-COM','N-ESS','OBJ','NOUN','MAINV2','NEG','INTERR')
        self.syntax =('NEG','MAINV','SUBJ','ANSWERSUBJECT')
        self.qtype_verbs = set(['VERB','V-COND','V-IMPRT','V-GO'])
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

    
    # Select a word matching semtype and return full form.
    def get_words(self, qelement, tag_el=None, lemma=None):
        """
        Select word from possible options in the element.
        """

        words = []

        print "LEMMA", lemma
        if qelement:
            # If word_id is given
            if qelement.word_id:
                info = { 'word': qelement.word_id }
                if tag_el:
                    info['tag'] = tag_el.id
                if Form.objects.filter(Q(tag=tag_el.id) & Q(word=qelement.word_id)).count()>0:
                    fullforms = Form.objects.filter(Q(tag=tag_el.id) & Q(word=qelement.word_id))
                    fullf = []
                    for f in fullforms:
                        fullf.append(f.fullform)
                    info = { 'word': qelement.word_id, 'tag' : tag_el.id, 'fullform': fullf[:] }
                words.append(info)

            else:
                # Otherwise use semantic classes for searching the word.
                # Only one semtype allowed at the moment.
                # Change this !!!
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
                                fullforms = Form.objects.filter(Q(tag=tag_el.id) & Q(word=word.id))
                                fullf = []
                                for f in fullforms:
                                    fullf.append(f.fullform)
                                    info = { 'word': word.id, 'tag' : tag_el.id, 'fullform': fullf[:] }
                                    words.append(info)
                          #  else:   
                          #      info = { 'word': word.id, 'tag' : tag_el.id }
                          #      words.append(info)

        else:
            if lemma and tag_el:
                word = Word.objects.filter(lemma=lemma)[0]
                if Form.objects.filter(Q(tag=tag_el.id) & Q(word=word.id)).count()>0:
                    fullforms = Form.objects.filter(Q(tag=tag_el.id) & Q(word=word.id))
                    fullf = []
                    for f in fullforms:
                        fullf.append(f.fullform)
                    info = { 'word': word.id, 'tag' : tag_el.id, 'fullform': fullf[:] }
                    words.append(info)
                
                
        return words

    def get_elements(self, question_element, syntax):

        #if self.gametype:
        #    if QElement.objects.filter(Q(question=question_element) & \
        #                               Q(syntax=syntax) &\
        #                               Q(gametype=self.gametype)).count()>0:
        #        return QElement.objects.filter(Q(question=question_element) & \
        #                                       Q(syntax=syntax) &\
        #                                       Q(gametype=self.gametype))[0]
            
        if QElement.objects.filter(Q(question=question_element) &\
                                   Q(syntax=syntax)).count()>0:
            return QElement.objects.filter(Q(question=question_element) & \
                                           Q(syntax=syntax))
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

        if 'SUBJ' in set(qwords_list):
            
            qwords['SUBJ'] = {}
            
            # Select randomly an element, if there are more than one available.
            # This way there is only one subject and tag for each question.
            subj_elements=self.get_elements(question, 'SUBJ')
            subj_element = subj_elements[randint(0, len(subj_elements)-1)]
            tag_el_count = subj_element.tag.count()

            # If there was no tag elements, there is nothing to do.
            # Subject tag is needed for everything else. 
            if tag_el_count == 0:
                return None
            
            tag_el = subj_element.tag.all()[randint(0, tag_el_count-1)]
            
            # Get number information for subject
            subjword = {}
            if tag_el.pos=="Pron":
                subjnumber = tag_el.personnumber 
                pronbase = self.PronPNBase[subjnumber]
                possible_subjwords=get_words(None, tag_el, pronbase)
            else:
                subjnumber = tag_el.number 
                possible_subjwords = self.get_words(subj_element, tag_el)
                
            subjword = possible_subjwords[randint(0, len(possible_subjwords)-1)]
            print "OK:", subjword['word'], subjnumber
            subjword['number'] = subjnumber
            qwords['SUBJ'] = subjword


        if 'MAINV' in set(qwords_list):

            qwords['MAINV'] = {}

            # Select one mainverb element for question.
            mainv_elements = self.get_elements(question,'MAINV')
            if mainv_elements:
                mainv_el = mainv_elements[randint(0, len(mainv_elements)-1)]
                
                # If there is only on tag element, then there are no choices for agreement.
                tag_el_count = mainv_el.tag.count()
                if tag_el_count == 1:
                    tag_el=mainv_el.tag.all()[0]
                else:
                    # Subject-verb agreement
                    if qwords.has_key('SUBJ') and qwords['SUBJ'].has_key('number'):
                        subjnumber=qwords['SUBJ']['number']
                        v_number = self.SVPN[subjnumber]
                        if qtype in self.qtype_verbs:
                            mainv_tags = mainv_el.tag.filter(Q(personnumber=v_number))
                        else:
                            mainv_tags = mainv_el.tag.filter(Q(personnumber=v_number) & \
                                                            Q(tense=self.tense) & \
                                                            Q(mood=self.mood))
                    # If there is no subject element
                    # then select random tag from all tags.
                    else:
                        mainv_tag_count = mainv_el.tag.count()
                        mainv_tags = mainv_el.tag.all()

                    tag_el = mainv_tags[randint(0, mainv_tags.count()-1)]

                # Select random mainverb
                possible_mainv_words = self.get_words(mainv_el, tag_el)
                if possible_mainv_words:
                    mainv_word = possible_mainv_words[randint(0, len(possible_mainv_words)-1)]

                qwords['MAINV'] = mainv_word


        # 2. Other grammatical elements
        # At the moment, agreement is not taken into account
        for s in qwords_list:
            if s in set(self.syntax): continue

            tag_el=None
            word = {}
            
            elements = self.get_elements(question,s)
            if elements:
                element = elements[randint(0, len(elements)-1)]                
                tag_el_count = element.tag.count()
                if tag_el_count > 0:
                    tag_el = element.tag.all()[randint(0, tag_el_count-1)]

                # Select random word
                words = self.get_words(element, tag_el)
                if words:
                    word = words[randint(0, len(words)-1)]

                print "WORD ", s, tag_el.string, word

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
                words = get_words(None, asubjtag_el, pronbase)

                for word in words:
                    word['number'] = a_number
                    
            if not words:
                words.append(qwords['SUBJ'])

        # Check if there are elements specified for the answer subject.
        else:
            subj_elements = self.get_elements(answer,subj)
            if subj_elements:
                subj_element = subj_elements[randint(0, len(elements)-1)]                
                tag_el_count = subj_element.tag.count()
                if tag_el_count > 0:
                    tag_el = element.tag.all()[randint(0, tag_el_count-1)]

                if tag_el.pos=="Pron":
                    a_number = tag_el.personnumber 
                else:
                    a_number = tag_el.number 

                words = self.get_words(subj_element, tag_el)
                
                for word in words:
                    word['number'] = a_number

        # Copy if subject was answersubj, copy information to SUBJ to ensure agreement.
        awords[subj] = words[:]
        if not subj == 'SUBJ':
            awords['SUBJ'] = words[:]


        return awords
    
    def generate_answers_mainv(self, answer, question, awords, qwords, qtype):

        mainv_elements = self.get_elements(answer,'MAINV')
        amainv_words = []
        
        # It is assumed that all subjects cause the same inflection
        # for verb, so it does not matter which subject is selected.
        if awords.has_key('SUBJ') and len(awords['SUBJ']) > 0:
            print "subject", len(awords['SUBJ'])
            # mainverb number depends on the number of the subject.
            asubj = awords['SUBJ'][0]
            a_number=asubj['number']
            va_number=self.SVPN[a_number]
            

        # Take qwords mainverb tag as basis
        # If there is no subject, then the number of the question
        # mainverb determines the number.
        else:
            if qwords.has_key('MAINV') and qwords['MAINV']:
                qmainv = qwords['MAINV']
                
                mainvtag_id = qmainv['tag']
                mainvtag = Tag.objects.get(id=mainvtag_id)
                v_number = mainvtag.personnumber
            
                if Tag.objects.filter(id=mainvtag_id).count()>0:
                    mainvtag_string = Tag.objects.filter(id=mainvtag_id)[0].string
                    amainvtag_string = mainvtag_string.replace(v_number,v_number)
                    amainv_tag = Tag.objects.get(string=amainvtag_string)

        # If the main verb is under question, then generate full list.
        if qtype in self.qtype_verbs:
            for mainv_el in mainv_elements:
                amainv_words = []
                if not amainv_tag:
                    amainv_tags=mainv_el.tag.all()
                    amainv_words.append(self.get_words(mainv_el, amainv_tag))

        # Otherwise take only one
        else:
            amainv_elements = self.get_elements(answer,'MAINV')
            if amainv_elements:
                amainv_element = amainv_elements[randint(0, len(elements)-1)]                
                tag_el_count = amainv_element.tag.count()
                if tag_el_count > 0:
                    amainv_tags = amainv_el.tag.filter(Q(personnumber=v_number))
                for tag in amainv_tags:
                    amainv_words.append(self.get_words(None, amainv_tag))

        if not amainv_words:
            amainv_words.append(qwords['MAINV'])

        print "mainverb words.. ", amainv_words
        awords['MAINV'] = amainv_words
            
        return awords

    def generate_syntax(self, answer, question, awords, qwords, qtype, s):

        if not awords.has_key(s):
            awords[s] = []

        print "generating syntax", s
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
                                tag_count = element.tag.filter(personnumber=agr_tag.personnumber).count()
                                if tag_count>0:
                                    tag_elements = element.tag.filter(personnumber=agr_tag.personnumber)

                            if agr_tag.number:
                                tag_count= element.tag.filter(number=agr_tag.number).count()
                                if tag_count>0:
                                    tag_elements = element.tag.filter(number=agr_tag.number)
                                
                # if no agreement, take all tags.
                else:
                    tag_count = element.tag.count()
                    if tag_count > 0:
                        tag_elements = element.tag.all()

                # Take word forms for all tags
                for tag_el in tag_elements:

                    # Special treatment for numerals.
                    if (qtype == "NUM-ATTR" and element.identifier=="NUM-ATTR"):
                        w_count=Word.objects.filter(Q(pos="Num")).count()
                        word_id=Word.objects.filter(Q(pos="Num"))[randint(0,w_count-1)].id
                        if Form.objects.filter(Q(tag=tag_el.id) & Q(word=word_id)).count()>0:
                            fullforms = Form.objects.filter(Q(tag=tag_el.id) & Q(word=word_id))
                            fullf = []
                            for f in fullforms:
                                fullf.append(f.fullform)
                            info = {'word' : word_id, 'tag' : tag_el.id, 'fullform' : fullf[:] }
                            
                        else:
                            info = { 'word': word_id, 'tag' : tag_el.id }

                        swords.append(info)

                    else:
                        swords = self.get_words(element, tag_el)

        # If no tag elements, copy the forms from the question
        if not swords and qwords.has_key(s):
            swords.append(qwords[s])
        if not swords:
            info = {'fullform' : [s] }
            swords.append(info)

        awords[s] = swords
        
        return awords

    def get_db_info(self, db_info):

        anslist=[]
        pos=self.settings.pos

        print self.settings.allcase
        # Select random question type.
        if pos == "N":
            qtype = self.settings.allcase[randint(0, len(self.settings.allcase)-1)]
        else:
            if pos == "V":
                qtype=self.settings.vtype
            else:
                if pos == "Num":
                    qtype = self.numerals[randint(0, len(self.numerals)-1)]

        print "QTYPE: " + qtype

        # If the question id is received from the interface, use that question info
        # Otherwise select random question
        qwords = {}
        if db_info.has_key('question_id'):
            question = Question.objects.get(id=db_info['question_id'])
            qwords=db_info['qwords']
        else:
            q_count=Question.objects.filter(qtype=qtype).count()
            while not qwords:
                #qnum = randint(0, q_count-1)
                # TESTING
                qnum = 5
                print "qnum:", qnum
                question = Question.objects.filter(qtype=qtype)[qnum]
                qwords = None
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
                info = {}
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
        print "awords:", db_info['awords']
        print "awords ...................."
        print "qwords:", db_info['qwords']
        print "qwords ...................."
        form = (QAQuestion(db_info['gametype'], question, answer, \
                           db_info['qwords'], db_info['awords'],\
                           db_info['userans'], db_info['correct'], data, prefix=n))

        self.form_list.append(form)


