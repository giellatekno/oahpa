# -*- coding: utf-8 -*-

from settings import *
import sys
from mhr_drill.models import *
from xml.dom import minidom as _dom
from django.db.models import Q
from django.utils.encoding import force_unicode

import re
import string
import codecs


class Sahka:

    def add_wordlist(self,word,t):
        cgfile="/opt/smi/mhr/bin/mhr-ped.cg3"  # on victorio
        #cgfile="../mhr/src/mhr-ped.cg3" # relative path, for local use

        wordclass = word.getAttribute("class")
        print wordclass
        listObj=re.compile(r'^\#LIST\s*' + wordclass + '\s*=\s?(?P<listString>.*).*;.*$', re.U)
        cgfileObj = codecs.open(cgfile, "r", "utf-8" )
        while True:
            line = cgfileObj.readline()
            if not line: break
            if not line.strip(): continue
            matchObj=listObj.search(line) 
            if matchObj:
                list = matchObj.expand(r'\g<listString>')
                for w in list.split():
                    w = w.strip("\"")
                    w = w.replace('#','')
                    print w
                    if Form.objects.filter(fullform=w).count()>0:
                        word = Form.objects.filter(fullform=w)[0]
                        t.formlist.add(word)
                        t.save()
                    else:
                        print "***ERROR: no word found from database:", w 
        if t.formlist.all().count()==0:
            print "***ERROR: no words found for", wordclass
        cgfileObj.close()                        

    def read_dialogue(self,infile):

        print infile

        xmlfile=file(infile)
        tree = _dom.parse(infile)

        dialogue_name = tree.getElementsByTagName("dialogue")[0].getAttribute("name")
        d, created = Dialogue.objects.get_or_create(name=dialogue_name)
        
        #If there exists already a dialogue with that name, delete all the references to it.
        if not created:
            d.delete()
        d.save()        
        topicutts={}
        topicnum=0
        image=""
        for topic in tree.getElementsByTagName("topic"):
            utts = []
            topicname = topic.getAttribute("name")
            image = topic.getAttribute("image")

            t, created = Topic.objects.get_or_create(topicname=topicname,dialogue=d)
            t.number=topicnum
            t.image=image
            t.save()

            if topic.childNodes[0].localName == "word":
                word = topic.getElementsByTagName("word")[0]
                self.add_wordlist(word,t)
            topicnum=topicnum+1

            # createn opening and closing if they do not exist in xml-file.
            opening = False
            closing = False
            i=0

            for utt in topic.getElementsByTagName("utt"):
                utt_name = utt.getAttribute("name")
                utttype = utt.getAttribute("type")
                uttlink = utt.getAttribute("link")
                if utttype:
                    if utttype == "opening": opening = True
                    if utttype == "closing": closing = True
                utterance = {}
                utt_text=""
                utt_word=None
                if utt.getElementsByTagName("text"):
                    if utt.getElementsByTagName("text")[0].firstChild.data:
                        utt_text = utt.getElementsByTagName("text")[0].firstChild.data

                if utt.getElementsByTagName("word"):
                    utt_word = utt.getElementsByTagName("word")[0]
                
                if utt.getElementsByTagName("element"):
                    uttelement = utt.getElementsByTagName("element")[0]
                    el_id = uttelement.getAttribute("id")
                    tag = ""
                    if  uttelement.getElementsByTagName("grammar"):
                        grammar = uttelement.getElementsByTagName("grammar")[0] 
                        tag = grammar.getAttribute("tag")
                    utterance['elements'] = { 'id' : el_id, 'tag' : tag }

                utterance['text'] = utt_text
                utterance['name'] = utt_name
                utterance['type'] = utttype
                utterance['word'] = utt_word
                utterance['link'] = uttlink
                utterance['number'] = i
                i=i+1
                utterance['alts'] = []
                
                for alt in utt.getElementsByTagName("alt"):
                    alter = {}
                    alter['target'] = alt.getAttribute("target")
                    alter['link'] = alt.getAttribute("link")
                    alter['variable'] = alt.getAttribute("variable")
                    alter['constant'] = alt.getAttribute("constant")
                    alttext =""
                    if alt.getElementsByTagName("text"):
                        alttext = alt.getElementsByTagName("text")[0].firstChild.data
                    alter['text'] = alttext

                    if alt.getElementsByTagName("element"):
                        altelement = alt.getElementsByTagName("element")[0]
                        el_id = altelement.getAttribute("id")
                        tag = ""
                        if  altelement.getElementsByTagName("grammar"):
                            grammar = altelement.getElementsByTagName("grammar")[0] 
                            tag = grammar.getAttribute("tag")
                        alter['elements'] = { 'id' : el_id, 'tag' : tag }

                    utterance['alts'].append(alter)

                utts.append(utterance)
                
            for u in utts:
                utt, created = Utterance.objects.get_or_create(utterance=u['text'],\
                                                               utttype=u['type'],\
                                                               topic=t,\
                                                               name=u['name'])
                if u['word']:
                    print "Adding wordlist", u['text']
                    self.add_wordlist(u['word'],utt)
                utt.save()

                # Create syntactic specifictation for variables
                if u.has_key('elements'):
                    tag=None
                    if u['elements']['tag']:
                        if Tag.objects.filter(string=u['elements']['tag']).count()>0:
                            tag = Tag.objects.filter(string=u['elements']['tag'])[0]
                        else:
                            print "*******ERRROR: tag not found", u['elements']['tag'] 
                    uelement, created = UElement.objects.get_or_create(syntax=u['elements']['id'],\
                                                                       tag=tag,\
                                                                       utterance=utt)

                    uelement.save()

            # create an opening or closing if not exist:
            if not opening: 
                utt, created = Utterance.objects.get_or_create(utterance="",\
                                                               utttype="opening",\
                                                               topic=t,)
                utt.save()
            if not closing: 
                utt, created = Utterance.objects.get_or_create(utterance="",\
                                                               utttype="closing",\
                                                               topic=t,)
                utt.save()

            topicutts[topicname] = utts

        for tname in topicutts:
            t = Topic.objects.get(topicname=tname,dialogue=d)
            for u in topicutts[tname]:
                utterance2=None
                next_utterance=None
                linkutt0=None
                linkutt=None
                linkutt2=None
                utterance = Utterance.objects.get(name=u['name'],topic=t)
                print utterance.utterance
                if u['link']:
                    next_utterance = Utterance.objects.get(Q(name=u['link']) & Q(topic__dialogue=t.dialogue))
                    print "..linking to", next_utterance.utterance
                    linkutt0, created = LinkUtterance.objects.get_or_create(link=next_utterance,target="default")
                    linkutt0.save()
                    utterance.links.add(linkutt0)
                    utterance.save()
                for a in u['alts']:

                    if a['link']:
                        #print a['link']
                        #print t.dialogue.name
                        #print t.dialogue.id
                        #print utterance.id
                        next_utterance = Utterance.objects.get(Q(name=a['link']) & Q(topic__dialogue=t.dialogue))
                        #print next_utterance.topic.dialogue.id

                    if a['text']:
                        utterance2, created = Utterance.objects.get_or_create(utterance=a['text'],\
                                                                              utttype='text',\
                                                                              topic=t)
                        utterance2.save()

                        # Create syntactic specifictation for variables
                        if a.has_key('elements'):
                            tag=None
                            if a['elements']['tag']:
                                if Tag.objects.filter(string=a['elements']['tag']).count()>0:
                                    tag = Tag.objects.filter(string=a['elements']['tag'])[0]
                                else:
                                    print "*******ERRROR: tag not found", a['elements']['tag'] 
                            uelement, created = UElement.objects.get_or_create(syntax=a['elements']['id'],\
                                                                               tag=tag,\
                                                                               utterance=utterance2)
                            uelement.save()

                            
                        if a['link']:
                            linkutt2, created = LinkUtterance.objects.get_or_create(link=next_utterance,\
                                                                                    target="default")
                            linkutt2.save()
                            utterance2.links.add(linkutt2)
                            utterance2.save()
                        
                        # If the alternative contains text, create a new utterance out of it:
                        linkutt, created = LinkUtterance.objects.get_or_create(link=utterance2,\
                                                                               target=a['target'], \
                                                                               variable=a['variable'],\
                                                                               constant=a['constant'])
                        linkutt.save()                                                
                    
                        utterance.links.add(linkutt)
                        utterance.save()

                    else:
                        if a ['link']:
                            linkutt, created = LinkUtterance.objects.get_or_create(link=next_utterance,\
                                                                                   target=a['target'], \
                                                                                   variable=a['variable'], \
                                                                                   constant=a['constant'])
                            linkutt.save()                        
                            
                            utterance.links.add(linkutt)
                            utterance.save()
                        
