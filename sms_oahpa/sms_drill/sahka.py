# -*- coding: utf-8 -*-

from sms_oahpa.sms_drill.models import *
from sms_oahpa.sms_drill.forms import *
from django.db.models import Q
from sms_oahpa.sms_drill.game import Game
from random import randint

class SahkaGame(Game):

    def update_formlist(self,t):
        #print "updating formlist"
        #print t.id
        if t.formlist.all().count()>0:
            self.settings['wordlist'] = ""
            wlist=[]
            for w in t.formlist.all():
                word = w.fullform
                wlist.append(word)
            self.settings['wordlist'] = ", ".join(wlist)
            #print wlist
            
    def update_topic(self, topic):
        if topic.image:
            self.settings['image'] = topic.image			
        self.update_formlist(topic)


    def form_utterance(self, utterance):
        u = utterance.utterance
        self.update_formlist(utterance)
        #print u
        qwords={}
        for w in u.split():
            if w== "": continue
            word = {'fullform' : [] }
            if self.global_targets.has_key(w):
                fullform=""
                wstring = self.global_targets[w]['target']
                if UElement.objects.filter(utterance=utterance, syntax=w).count()>0:
                    tag = UElement.objects.filter(utterance=utterance, syntax=w)[0].tag
                    if Form.objects.filter(word__lemma=wstring, tag=tag).count()>0:
                        fullform = Form.objects.filter(word__lemma=wstring, tag=tag)[0]
                        word['fullform'].append(fullform.fullform)
                        #print fullform.fullform
                if not fullform:
                    word['fullform'].append(wstring)
            else:
                word['fullform'].append(w)
                
            qwords[w] = word
        return qwords
    
    def update_game(self, counter, prev_form=None):

        new_topic=False
        utterance=None

        if Topic.objects.filter(Q(dialogue__name=self.settings['dialogue']) & \
                                Q(number=self.settings['topicnumber'])).count()>0:

            topic = Topic.objects.get(Q(dialogue__name=self.settings['dialogue']) & \
                                      Q(number=self.settings['topicnumber']))
        else:
            return

        self.update_topic(topic)

        if prev_form:
            prev_utterance_id = prev_form.utterance_id
            prev_utterance = Utterance.objects.get(id=prev_utterance_id)
            prev_utttype =  prev_utterance.utttype
            self.global_targets = prev_form.global_targets
            
        ####### 1. part: Start or end a new topic
            
        # If previous utterance was opening, then go to next utterance
        if prev_form and prev_utttype == "opening" and topic.utterance_set.filter(utttype="question").count()>0:
            utterance = topic.utterance_set.filter(utttype="question").order_by('id')[0]

        # If previous utterance was closing, then create a new topic.
        if prev_form and prev_utttype == "closing":
            if prev_utterance.links.filter(target="default"):
                nextlink = prev_utterance.links.filter(target="default")[0]
                utterance = nextlink.link
                topic=utterance.topic
                self.settings['topicnumber'] = int(topic.number)
                self.update_topic(topic)
            new_topic=True

        # If start of the game or new topic, pick the opening:
        if counter==1 or new_topic:
            dia = Dialogue.objects.get(name=self.settings['dialogue'])
            self.settings['dialogue']=dia.name
            utterance = topic.utterance_set.all().filter(utttype="opening")[0]
            
        # If the utterance was found create it and return
        if utterance:
            db_info = {}
            db_info['userans'] = ""
            db_info['correct'] = ""
            db_info['utterance_id'] = utterance.id
            qwords = self.form_utterance(utterance)
            db_info['qwords'] = qwords

            db_info['global_targets'] = self.global_targets
                
            form, jee  = self.create_form(db_info, counter, 0)
            self.form_list.append(form)

            self.num_fields = self.num_fields+1
            if not utterance.utttype == "question":
                self.update_game(counter+1, form)               
            return
        
        #### 2. part Follow the link from previous question
        
        # If the last question was correctly answered, proceed to next question/utterance
        # According to the type of the answer
        if prev_form:
            nextlink=None
            #print prev_form.target
            #print prev_utterance.id
            #print prev_form.dia_messages
            for msg in prev_form.dia_messages:
                msg = msg.lstrip("dia-")
                if prev_utterance.links.filter(target=msg):
                    nextlink = prev_utterance.links.filter(target=msg)[0]
                    #print "OK"
                    break
            if not nextlink:
                if prev_utterance.links.filter(target="default"):
                    nextlink = prev_utterance.links.filter(target="default")[0]
            if nextlink:

                utterance = nextlink.link
                topic=utterance.topic
                self.settings['topicnumber'] = topic.number
                self.update_topic(topic)
				
                db_info = {}
                db_info['userans'] = ""
                db_info['correct'] = ""
                db_info['utterance_id'] = utterance.id
                qwords = self.form_utterance(utterance)
                db_info['qwords'] = qwords

                db_info['global_targets'] = self.global_targets
                
                form, jee  = self.create_form(db_info, counter, 0)
                self.form_list.append(form)
                self.num_fields = self.num_fields+1
                if utterance.utttype == "closing":
                    self.settings['topicnumber'] = int(utterance.topic.number) + 1
                if not utterance.utttype == "question":
                    self.update_game(counter+1, form)               
                return

            else:
                # If next link was not found, go to topic closing.
                utterance = topic.utterance_set.all().filter(utttype="closing")[0]
                topic=utterance.topic
                self.update_topic(topic)

                db_info = {}
                db_info['userans'] = ""
                db_info['correct'] = ""
                db_info['utterance_id'] = utterance.id
                qwords = self.form_utterance(utterance)
                db_info['qwords'] = qwords

                db_info['global_targets'] = self.global_targets

                form, jee  = self.create_form(db_info, counter, 0)
                self.form_list.append(form)
                self.num_fields = self.num_fields+1
                self.settings['topicnumber'] = int(utterance.topic.number) + 1
                self.update_game(counter+1, form)
                return
            
        if not self.form_list:
            # No questions found, so the quiz_id must have been bad.
            raise Http404('Invalid quiz id.')



    def create_form(self, db_info, n, data=None):

        utterance = Utterance.objects.get(Q(id=db_info['utterance_id']))
        targets = []
        language="nob"
        if self.settings.has_key('language'):
            language = self.settings['language']

        if utterance.links.filter(~Q(target="")):
            target_els = utterance.links.filter(~Q(target=""))
            for t in target_els:
                targets.append(force_unicode(t.target))
        qwords = db_info['qwords']
        global_targets = db_info['global_targets']

        form = (SahkaQuestion(utterance, qwords, targets, global_targets, language, db_info['userans'], db_info['correct'], data, prefix=n))

        return form, None
