# -*- coding: utf-8 -*-

from oahpa.drill.models import *
from oahpa.drill.forms import *
from django.db.models import Q
from oahpa.drill.game import Game
from random import randint

class SahkaGame(Game):
    
    def update_game(self, counter, prev_form=None):

        #print "counter", counter
        print "topicnumber", self.settings['topicnumber']
        new_topic=False
        utterance=None

        print self.settings
        if Topic.objects.filter(Q(dialogue__name=self.settings['dialogue']) & \
                                Q(number=self.settings['topicnumber'])).count()>0:

            topic = Topic.objects.get(Q(dialogue__name=self.settings['dialogue']) & \
                                      Q(number=self.settings['topicnumber']))
        else:
            return

        if prev_form:
            prev_utterance_id = prev_form.utterance_id
            prev_utterance = Utterance.objects.get(id=prev_utterance_id)
            prev_utttype =  prev_utterance.utttype

        ####### 1. part: Start or end a new conversation
            
        # If previous utterance was opening, then go to next utterance
        if prev_form and prev_utttype == "opening" and topic.utterance_set.filter(utttype="question").count()>0:
            utterance = topic.utterance_set.filter(utttype="question").order_by('id')[0]

        print "NAME", topic.topicname
        # If previous utterance was closing, then create a new topic.
        if prev_form and prev_utttype == "closing":
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
            if prev_form.target:
                if prev_utterance.links.filter(target=prev_form.target):
                    nextlink = prev_utterance.links.filter(target=prev_form.target)[0]
            if not nextlink:
                if prev_utterance.links.filter(linktype="default"):
                    nextlink = prev_utterance.links.filter(linktype="default")[0]
                    
            if nextlink:
                utterance = nextlink.link
                db_info = {}
                db_info['userans'] = ""
                db_info['correct'] = ""
                db_info['utterance_id'] = utterance.id
                form, jee  = self.create_form(db_info, counter, 0)
                self.form_list.append(form)
                self.num_fields = self.num_fields+1
                if utterance.utttype == "closing":
                    self.settings['topicnumber'] = int(self.settings['topicnumber'])+1
                if not utterance.utttype == "question":
                    self.update_game(counter+1, form)               
                return

            else:
                # If next link was not found, go to topic closing.
                utterance = topic.utterance_set.all().filter(utttype="closing")[0]
                db_info = {}
                db_info['userans'] = ""
                db_info['correct'] = ""
                db_info['utterance_id'] = utterance.id
                form, jee  = self.create_form(db_info, counter, 0)
                self.form_list.append(form)
                self.num_fields = self.num_fields+1
                self.settings['topicnumber'] = int(self.settings['topicnumber'])+1 
                self.update_game(counter+1, form)
                return
            
        if not self.form_list:
            # No questions found, so the quiz_id must have been bad.
            raise Http404('Invalid quiz id.')



    def create_form(self, db_info, n, data=None):
        
        utterance = Utterance.objects.get(Q(id=db_info['utterance_id']))
        targets = []
        if utterance.links.filter(~Q(target="")):
            target_els = utterance.links.filter(~Q(target=""))
            for t in target_els:
                targets.append(force_unicode(t.target))
        form = (SahkaQuestion(utterance, targets, db_info['userans'], db_info['correct'], data, prefix=n))

        return form, None
