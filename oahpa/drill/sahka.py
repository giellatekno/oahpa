# -*- coding: utf-8 -*-

from oahpa.drill.models import *
from oahpa.drill.forms import *
from django.db.models import Q
from oahpa.drill.game import Game
from random import randint

class SahkaGame(Game):
    
    def update_game(self, counter, prev_form=None):

        print "counter", counter
        print "topicnumber", self.settings['topicnumber']
        new_topic=False
        utterance=None

        if Topic.objects.filter(Q(dialoguetopic__dialogue=self.settings['dialogue_id']) & \
                                Q(dialoguetopic__number=self.settings['topicnumber'])).count()>0:

            topic = Topic.objects.get(Q(dialoguetopic__dialogue=self.settings['dialogue_id']) & \
                                      Q(dialoguetopic__number=self.settings['topicnumber']))
        else:
            return
        
        if prev_form:
            prev_utterance_id = prev_form.utterance_id
            prev_utterance = Utterance.objects.get(id=prev_utterance_id)
            prev_utttype =  prev_utterance.utttype
            
        # If previous utterance was closing, then create a new topic.
        if prev_form and prev_utttype == "closing":
            new_topic=True

        # If previous utterance was opening, then go to next utterance
        if prev_form and prev_utttype == "opening" and topic.utterance_set.count()>1:
            utterance = topic.utterance_set.all().order_by('id')[1]

        # If start of the game or new topic.
        if counter==1 or new_topic:
            dia = Dialogue.objects.get(name="visit")
            self.settings['dialogue_id']=dia.id
            if topic.utterance_set.all().filter(utttype="opening"):
                utterance = topic.utterance_set.all().filter(utttype="opening")[0]
                print "*************00", utterance.utterance
            else:
                utterance = topic.utterance_set.all().order_by('id')[0]
                if utterance.utttype=="closing":
                    self.settings['topicnumber'] = int(self.settings['topicnumber'])+1 
                print "*************0", utterance.utterance
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
        

        # If the last question was correctly answered, proceed to next question/utterance
        # According to the type of the answer
        if prev_form:
            nextlink=None
            if prev_form.pos:
                if prev_utterance.links.filter(linktype="pos"):
                    nextlink = prev_utterance.links.filter(linktype="pos")[0]
            if prev_form.neg:
                if prev_utterance.links.filter(linktype="neg"):
                    nextlink = prev_utterance.links.filter(linktype="neg")[0]
            if prev_form.target:
                if prev_utterance.links.filter(target=prev_form.target):
                    nextlink = prev_utterance.links.filter(target=prev_form.target)[0]
            if not nextlink:
                if prev_utterance.links.filter(linktype="default"):
                    print "GOING TO DEFAULT"
                    nextlink = prev_utterance.links.filter(linktype="default")[0]
                
            if nextlink:                          
                db_info = {}
                db_info['userans'] = ""
                db_info['correct'] = ""
                if nextlink.link:
                    utterance2 = nextlink.link
                    print "*************1", utterance2.utterance
                    db_info['utterance_id'] = utterance2.id                        
                    form, jee  = self.create_form(db_info, counter, 0)
                    self.form_list.append(form)
                    self.num_fields = self.num_fields+1
                    if utterance2.utttype == "question":
                        return
                    else:
                        self.update_game(counter+1, form)
                        return
            else:
                # If next link was not found, go to topic closing.
                if topic.utterance_set.all().filter(utttype="closing"):
                    utterance = topic.utterance_set.all().filter(utttype="closing")[0]
                    print "*************3", utterance.utterance, topic.id
                    self.settings['topicnumber'] = int(self.settings['topicnumber'])+1 
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
                # If there is no topic closing, go to next topic.
                else:
                    self.settings['topicnumber'] = int(self.settings['topicnumber'])+1            
                    topic = Topic.objects.get(Q(dialoguetopic__dialogue=self.settings['dialogue_id']) & \
                                              Q(dialoguetopic__number=self.settings['topicnumber']))
                    utterance = topic.utterance_set.all()[0]
                    print "*************2", utterance.utterance
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
            
        if not self.form_list:
            # No questions found, so the quiz_id must have been bad.
            raise Http404('Invalid quiz id.')



    def create_form(self, db_info, n, data=None):
        
        utterance = Utterance.objects.get(Q(id=db_info['utterance_id']))
        targets = []
        if utterance.links.filter(~Q(target="")):
            target_els = utterance.links.filter(~Q(target=""))
            for t in target_els:
                targets.append(t.target)
        form = (SahkaQuestion(utterance, targets, db_info['userans'], db_info['correct'], data, prefix=n))

        return form, None
