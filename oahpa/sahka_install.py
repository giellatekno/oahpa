# -*- coding: utf-8 -*-

from settings import *
from drill.models import *
from xml.dom import minidom as _dom
from optparse import OptionParser
from django.db.models import Q
from django.utils.encoding import force_unicode
import sys
import re
import string
import codecs


class Sahka:

    def read_dialogue(self,infile):
        
        xmlfile=file(infile)
        tree = _dom.parse(infile)

        dialogue_name = tree.getElementsByTagName("dialogue")[0].getAttribute("name")
        d, created = Dialogue.objects.get_or_create(name=dialogue_name)
        d.save()

        topicutts={}
        topicnum=0
        for topic in tree.getElementsByTagName("topic"):
            utts = []
            topicname = topic.getAttribute("name")

            t, created = Topic.objects.get_or_create(topicname=topicname,dialogue=d)
            t.number=topicnum
            t.save()
            topicnum=topicnum+1

            # createn opening and closing if they do not exist in xml-file.
            opening = False
            closing = False
            i=0

            for utt in topic.getElementsByTagName("utt"):
                utt_name = utt.getAttribute("name")
                utttype = utt.getAttribute("type")
                if utttype:
                    if utttype == "opening": opening = True
                    if utttype == "closing": closing = True
                utterance = {}
                utt_text=""
                if utt.getElementsByTagName("text"):
                    if utt.getElementsByTagName("text")[0].firstChild.data:
                        utt_text = utt.getElementsByTagName("text")[0].firstChild.data
                utterance['text'] = utt_text
                utterance['name'] = utt_name
                utterance['type'] = utttype
                utterance['number'] = i
                i=i+1
                utterance['alts'] = []
                print utt_text
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
                    utterance['alts'].append(alter)

                utts.append(utterance)
                
            for u in utts:
                print u['text']
                utt, created = Utterance.objects.get_or_create(utterance=u['text'],\
                                                               utttype=u['type'],\
                                                               topic=t,\
                                                               name=u['name'])
                utt.save()

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
                linkutt=None
                linkutt2=None
                utterance = Utterance.objects.get(name=u['name'],topic=t)
                print utterance.utterance
                for a in u['alts']:
                    if a['link']:
                        print "link0:", a['link']
                        next_utterance = Utterance.objects.get(name=a['link'])

                    if a['text']:
                        print a['text']
                        utterance2, created = Utterance.objects.get_or_create(utterance=a['text'],\
                                                                              utttype='text',\
                                                                              topic=t)
                        utterance2.save()
                        if a['link']:
                            print "link1:", a['link']
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
                            print "link:", a['link']
                            linkutt, created = LinkUtterance.objects.get_or_create(link=next_utterance,\
                                                                                   target=a['target'], \
                                                                                   variable=a['variable'], \
                                                                                   constant=a['constant'])
                            linkutt.save()                        
                            
                            utterance.links.add(linkutt)
                            utterance.save()
                        
