# -*- coding: utf-8 -*-

from settings import *
from drill.models import *
from xml.dom import minidom as _dom
from optparse import OptionParser
from django.db.models import Q
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

        topicnum=0
        for topic in tree.getElementsByTagName("topic"):
            utts = []
            topicname = topic.getAttribute("name")

            t, created = Topic.objects.get_or_create(topicname=topicname)
            t.save()

            dt, created = DialogueTopic.objects.get_or_create(topic=t,dialogue=d)
            dt.number=topicnum
            dt.save()
            topicnum=topicnum+1
            
            i=0

            for utt in topic.getElementsByTagName("utt"):
                utt_name = utt.getAttribute("name")
                utttype = utt.getAttribute("type")

                utterance = {}
                utt_text=""
                if utt.getElementsByTagName("text"):
                    utt_text = utt.getElementsByTagName("text")[0].firstChild.data
                utterance['text'] = utt_text
                utterance['name'] = utt_name
                utterance['type'] = utttype
                utterance['number'] = i
                i=i+1
                utterance['alts'] = []
                for alt in utt.getElementsByTagName("alt"):
                    alter = {}
                    alter['type'] = alt.getAttribute("type")
                    alter['target'] = alt.getAttribute("target")
                    alter['link'] = alt.getAttribute("link")
                    alttext =""
                    if alt.getElementsByTagName("text"):
                        alttext = alt.getElementsByTagName("text")[0].firstChild.data
                    alter['text'] = alttext
                    utterance['alts'].append(alter)
                utts.append(utterance)
                
            for u in utts:
                utt, created = Utterance.objects.get_or_create(utterance=u['text'],\
                                                               utttype=u['type'],\
                                                               topic=t,\
                                                               name=u['name'])
                utt.save()
                
            for u in utts:
                utterance = Utterance.objects.get(name=u['name'])
                for a in u['alts']:
                    if a['link']:
                        uttlink = Utterance.objects.get(name=a['link'])

                    if a['text']:
                        print "creating utterance2"
                        utterance2, created = Utterance.objects.get_or_create(utterance=a['text'],\
                                                                              utttype='text',\
                                                                              topic=t)
                        utterance2.save()
                        if a['link']:
                            linkutt2, created = LinkUtterance.objects.get_or_create(link=uttlink)
                            linkutt2.save()
                            utterance2.links.add(linkutt)
                            utterance2.save()

                        # If the alternative contains text, create a new utterance out of it:
                        linkutt, created = LinkUtterance.objects.get_or_create(link=utterance2,\
                                                                               linktype=a['type'],\
                                                                               target=a['target'])
                        linkutt.save()                                                

                        utterance.links.add(linkutt)
                        utterance.save()

                    else:
                        if a ['link']:
                            linkutt, created = LinkUtterance.objects.get_or_create(link=uttlink,\
                                                                                   linktype=a['type'],\
                                                                                   target=a['target'])
                            linkutt.save()                        
                            
                            utterance.links.add(linkutt)
                            utterance.save()
                        
