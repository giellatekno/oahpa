# -*- coding: utf-8 -*-

from oahpa.drill.models import *
from oahpa.drill.forms import *
from oahpa.drill.game import Game
from django.db.models import Q
from random import randint

class QAGame(Game):

    def init_tags(self):
        """
        Initialize the grammatical information.
        This information should be moved to parameters
        """
        self.num_fields = 6
        self.syntax =('MAINV','SUBJ')
        self.qtype_verbs = set(['V-COND','V-IMPRT','V-POT', 'PRS','PRT'])

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

        dialect = self.settings['dialect']

        word_count = Word.objects.filter(Q(wordqelement__qelement=qelement) & Q(dialects__dialect=dialect) &\
                                         Q(form__tag=tag_el.id)).count()
        word = Word.objects.filter(Q(wordqelement__qelement=qelement) & Q(dialects__dialect=dialect) &\
                                   Q(form__tag=tag_el.id))[randint(0,word_count-1)]
        form = word.form_set.filter(Q(tag=tag_el.id) & Q(dialects__dialect=dialect))[0]
                                         
        if not form: return None

        word_id=word.id
        fullform=form.fullform
            
        info = { 'word' : word_id, 'tag' : tag_el.id, 'fullform' : [ fullform ], 'qelement' : qelement }
        return info
    
    # Select a word matching semtype and return full form.
    def get_words(self, qelement, tag_el=None, lemma=None, word_id=None):
        """
        Select word from possible options in the element.
        """
        words = []
        dialect = self.settings['dialect']
        
        # If there are no information available for these elements, try to use other info.
        word = None
        if lemma and tag_el:
            word = Word.objects.filter(lemma=lemma)[0]
        else:
            if word_id and tag_el:
                word = Word.objects.filter(id=word_id)[0]
        if word:
            form_list = Form.objects.filter(Q(tag=tag_el.id) & Q(word=word.id) & Q(dialects__dialect=dialect))
            if not form_list:
                return []

            fullform = form_list[0].fullform

            info = {'word': word.id, 'tag' : tag_el.id, 'fullform' : [ fullform ] }
            words.append(info)                    

        return words

    def get_elements(self, question_element, identifier):

        if QElement.objects.filter(Q(question=question_element) & \
                                   Q(identifier=identifier)).count()>0:
            return QElement.objects.filter(Q(question=question_element) & \
                                           Q(identifier=identifier))

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

                        if qtype in self.qtype_verbs or self.gametype=="qa":
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

                if not mainv_word: return None
                else:
                    mainv_word['number'] = tag_el.personnumber
                    qwords['MAINV'] = mainv_word

            if not mainv_word: return None
                

        # 2. Other grammatical elements
        # At the moment, agreement is not taken into account
        for s in qwords_list:
            if s in set(self.syntax): continue

            tag_el=None
            word = {}
            
            elements = self.get_elements(question,s)
            if elements:
                element = elements[randint(0, len(elements)-1)]
                copy_id=element.copy_id;
                if copy_id:
                    copy = QElement.objects.filter(id=copy_id)[0]
                    copy_syntax = copy.syntax
                    
                    if qwords.has_key(copy_syntax):
                        word = qwords[copy_syntax]

                else:                
                    tag_el_count = element.tags.count()
                    if tag_el_count > 0:
                        tag_el = element.tags.all()[randint(0, tag_el_count-1)]

                    # Select random word
                    info = self.get_qword(element, tag_el)
                    word = info                    
            else:
                word = {}
                word['fullform'] = []
                word['fullform'].append(s)

            if not word:
                return None
            qwords[s] = word

        # Return the ready qwords list.            
        return qwords


    def generate_answers_subject(self, answer, question, awords, qwords):
        
        words=[]
        word_id=""
        a_number=""
        subj_el=None
        subjword=None

        copy_syntax = ""
        # If there is subject in the question, there is generally agreement.
        subj_elements = self.get_elements(answer,"SUBJ")
        if subj_elements:
            subj_el = subj_elements[0]            
        copy_id=subj_el.copy_id;
        if copy_id:
            subj_copy = QElement.objects.filter(id=copy_id)[0]
            copy_syntax = subj_copy.syntax
        
            if qwords.has_key(copy_syntax):
                qword = qwords[copy_syntax]
                subjtag_id=qword['tag']
                subjtag = Tag.objects.get(id=subjtag_id)
                subjword_id=qword['word']
                
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
                    
                if not words and not len(words)>0:
                    words = self.get_words(None, asubjtag_el, None, subjword_id)
                    words[0]['number'] = a_number

        # Check if there are elements specified for the answer subject.
        else:
            if subj_el:
                tag_el_count = subj_el.tags.count()
                if tag_el_count > 0:
                    tag_el = subj_el.tags.all()[randint(0, tag_el_count-1)]

                if tag_el.pos=="Pron":
                    a_number = tag_el.personnumber 
                else:
                    a_number = tag_el.number 

                info = { 'qelement': subj_el.id, 'word' : subjword, 'tag' : tag_el.id, 'number' : a_number }
                words.append(info)
                
                for word in words:
                    word['number'] = a_number

        awords['SUBJ'] = words[:]

        return awords
    
    def generate_answers_mainv(self, answer, question, awords, qwords):

        mainv_elements = self.get_elements(answer,"MAINV")

        mainv_word=None
        mainv_words = []
        mainv_tag = None
        mainv_tags = []
        va_number = None

        copy_syntax = ""
        # Find content elements.
        if mainv_elements:
            mainv_el = mainv_elements[0]
            if mainv_el.copy_id:
                copy_id = mainv_el.copy_id
                copy_element = QElement.objects.get(id=copy_id)
                copy_syntax = copy_element.identifier
        
        # It is assumed that all subjects cause the same inflection
        # for verb, so it does not matter which subject is selected.
        if awords.has_key('SUBJ') and len(awords['SUBJ'])>0:
            # mainverb number depends on the number of the subject.
            asubj = awords['SUBJ'][0]
            a_number=asubj['number']
            va_number=self.SVPN[a_number]
        else:
            if qwords.has_key(copy_syntax):
                qmainv = qwords[copy_syntax]
                q_number = qmainv['number']
                if q_number:
                    va_number = self.QAPN[q_number]

        # If there is no subject, then the number of the question
        # mainverb determines the number.
        if qwords.has_key(copy_syntax):

            qmainv = qwords[copy_syntax]
            mainv_word = qwords[copy_syntax]['word']

            qmainvtag_id = qmainv['tag']
            qmainvtag = Tag.objects.get(id=qmainvtag_id)
            qmainvtag_string = qmainvtag.string
            v_number = qmainvtag.personnumber
            if va_number:
                amainvtag_string = qmainvtag_string.replace(v_number,va_number)
            else:
                amainvtag_string = qmainvtag_string
                
            mainv_tag = Tag.objects.get(string=amainvtag_string)
            mainv_tags.append(mainv_tag)
            

        # If the main verb is under question, then generate full list.
        if answer.task == "MAINV":
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
                mainv_element = mainv_elements[0]
                tag_el_count = mainv_element.tags.count()
                if tag_el_count > 0:
                    mainv_tags = mainv_el.tags.filter(Q(personnumber=va_number))
                for tag in mainv_tags:
                    info = { 'qelement' : mainv_element.id, 'word' : mainv_word, 'tag' : tag.id }
                    mainv_words.append(info)

            else:
                for tag in mainv_tags:
                    info = { 'tag' : mainv_tag.id, 'word' : mainv_word }
                    mainv_words.append(info)
                    
        if not mainv_words and qwords.has_key("MAINV"):
            mainv_words.append(qwords["MAINV"])

        awords["MAINV"] = mainv_words

        return awords

    def generate_syntax(self, answer, question, awords, qwords, s):

        if s=="SUBJ" or s=="MAINV": return awords

        if not awords.has_key(s):
            awords[s] = []

        word_id=None
        
        tag_elements = []
        swords = []
        elements = self.get_elements(answer,s)

        if not elements:
            info = { 'fullform' : [ s ] }
            swords.append(info)
            awords[s] = swords            
            return awords

        element = elements[0]
        if element.copy_id:
            copy_id = element.copy_id
            copy_element = QElement.objects.get(id=copy_id)
            copy_syntax = copy_element.identifier
            if qwords.has_key(copy_syntax):
                qword = qwords[copy_syntax]
                if qword.has_key('word'):
                    word_id=qword['word']
                        
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
                        anumber = agr_tag.personnumber
                    else:
                        anumber = agr_tag.personnumber
                    tag_count = element.tags.filter(Q(personnumber=anumber) | Q(number=anumber)).count()
                    if tag_count>0:
                        tag_elements = element.tags.filter(Q(personnumber=anumber) | Q(number=anumber))
                                
        # if no agreement, take all tags.
        else:
            tag_count = element.tags.count()
            if tag_count > 0:
                tag_elements = element.tags.all()
                
        # Take word forms for all tags
        for tag_el in tag_elements:                    
            if not word_id:
                info = self.get_qword(element, tag_el)
            else:
                info = { 'qelement' : element.id, 'word' : word_id, 'tag' : tag_el.id  }
            if not info:
                return None
            swords.append(info)

        if not swords:
            return None
        awords[s] = swords

        return awords

    ######### Vasta questions
    def get_question_qa(self,db_info,qtype):

        qwords = {}
        if self.settings.has_key('level'): level=int(self.settings['level'])
        else: level='1'
        
        q_count = Question.objects.filter(gametype="qa", level__lte=level).count()
        question = Question.objects.filter(gametype="qa", level__lte=level)[randint(0,q_count-1)]
        
        qtype = question.qtype
        qwords = None
        qwords= self.generate_question(question, qtype)
        db_info['qwords'] = qwords

        db_info['question_id'] = question.id
        return db_info

    ######## Morfa questions
    def get_question_morfa(self,db_info,qtype):

        qwords = {}
        if self.settings.has_key('pos'):
            pos=self.settings['pos']

        # Get qtype from settings.
        if not qtype:
            if pos == "N":
                qtype = self.settings['case_context']
            if pos == "V":
                qtype=self.settings['vtype_context']
            if pos == "Num":
                qtype=self.settings['num_context']
            if pos == "A":
                qtype=self.settings['adj_context']

        if self.settings.has_key('book'): books=self.settings['book']
        if books:    
            q_count=Question.objects.filter(Q(qtype=qtype) & \
                                            Q(gametype="morfa") & \
                                            (Q(source__name__in=books) | Q(source__name="all" ))).count()
        else:
            q_count=Question.objects.filter(Q(qtype=qtype) & Q(gametype="morfa")).count()

        ### Generate question. If it fails, select another one.
        max = 20
        i=0
        while not qwords and i<max:
            i = i+1
            qnum = randint(0, q_count-1)
            if books:    
                question = Question.objects.filter(Q(qtype=qtype) & \
                                                   Q(gametype="morfa") & \
                                                   (Q(source__name__in=books) | Q(source__name="all" )))[qnum]
            else:
                question = Question.objects.filter(Q(qtype=qtype) & Q(gametype="morfa"))[qnum]
                
            qwords = None
            qwords= self.generate_question(question, qtype)

        db_info['qwords'] = qwords
        db_info['question_id'] = question.id
        return db_info,question


    ########### Morfa answers
    def get_answer_morfa(self,db_info,question):
        
        # Select answer using the id from the interface.
        # Otherwise select answer that is related to the question.
        awords = {}
        if db_info.has_key('answer_id'):
            answer=Question.objects.get(id=db_info['answer_id'])
        else:
            answer_count=question.answer_set.count()
            answer=question.answer_set.all()[randint(0,answer_count-1)]

        # Generate the set of possible answers if they are not coming from the interface
        # Or if the gametype is qa.
        if db_info.has_key('answer_id') and self.settings['gametype'] == 'context':
            awords=db_info['awords']
        else:
            # Generate the set of possible answers
            # Here only the text of the first answer is considered!!
            atext=answer.string
            words_strings = set(atext.split())

            #Initialize each element identifier
            for w in atext.split():
                if w== "": continue
                info = {}
                awords[w] = info

            # Subject and main verb are special cases:
            # There is subject-verb agreement and correspondence with question elements.
            if 'SUBJ' in words_strings:
                awords = self.generate_answers_subject(answer, question, awords, db_info['qwords'])
                
            if 'MAINV' in words_strings:
                awords = self.generate_answers_mainv(answer, question, awords, db_info['qwords'])

            # Rest of the syntax
            for s in words_strings:
                awords = self.generate_syntax(answer, question, awords, db_info['qwords'], s)
                if not awords:
                    return "error"
                    
        db_info['answer_id'] = answer.id
        db_info['awords'] = awords
        return db_info

    def get_db_info(self, db_info,qtype=None,default_qid=None):

        anslist=[]

        # If the question id is received from the interface, use that question info
        # Otherwise select random question
        if db_info.has_key('question_id'):
            question = Question.objects.get(id=db_info['question_id'])
            qwords=db_info['qwords']
        else:
            if default_qid:
                question = Question.objects.get(qid=default_qid)                
                qwords = None
                qwords= self.generate_question(question, qtype)
                db_info['qwords'] = qwords
            # If no default information select question
            else:
                if not self.gametype == "qa":
                    db_info,question = self.get_question_morfa(db_info,qtype)
                else:
                    db_info = self.get_question_qa(db_info,qtype)

        # If Vasta, store and return:
        if not self.gametype == "qa":
            db_info = self.get_answer_morfa(db_info,question)

        return db_info

    def create_form(self, db_info, n, data=None):

        question = Question.objects.get(Q(id=db_info['question_id']))
        answer = None
        if not self.gametype == "qa":
            answer = Question.objects.get(Q(id=db_info['answer_id']))
            form = (ContextMorfaQuestion(question, answer, \
                                         db_info['qwords'], db_info['awords'],\
                                         db_info['userans'], db_info['correct'], data, prefix=n))
        else:
            form = (VastaQuestion(question, \
                                  db_info['qwords'], \
                                  db_info['userans'], db_info['correct'], data, prefix=n))
            
        #print "awords:", db_info['awords']
        #print "awords ...................."
        #print "qwords:", db_info['qwords']
        #print "qwords ...................."

        return form, None

