# -*- coding: utf-8 -*-

from settings import *
from drill.models import *
from xml.dom import minidom as _dom
from optparse import OptionParser
from django.db.models import Q
import sys
import re
import codecs


class Entry:
    pass

class Paradigm:

    def __init__(self):
        self.tagset = {}
        self.paradigms = {}

    def handle_tags(self,tagfile):
        tags =[]
        fileObj = codecs.open(tagfile, "r", "utf-8" )
        tags = fileObj.readlines()
        fileObj.close()
        
        classObj=re.compile(r'^#\s*(?P<typeString>[\w\-]*)\s*$', re.U)
        stringObj=re.compile(r'^(?P<tagString>[\w]*)\s*$', re.U)

        tagclass=""
        for line in tags:
            line.strip()
            matchObj=classObj.search(line) 
            if matchObj:
                tagclass = matchObj.expand(r'\g<typeString>')
            else:
                matchObj=stringObj.search(line)
                if matchObj:
                    string = matchObj.expand(r'\g<tagString>')
                    self.tagset[string]=tagclass

    def read_paradigms(self,paradigmfile):
        if not self.tagset:
            self.handle_tags()

        fileObj = codecs.open(paradigmfile, "r", "utf-8" )
        genObj=re.compile(r'^(?P<posString>[\w]+)\+.*$', re.U)

        while True:
            line = fileObj.readline()
            if not line: break
            if not line.strip(): continue
            matchObj=genObj.search(line)
            if matchObj:
                pos=matchObj.expand(r'\g<posString>')
            if not self.paradigms.has_key(pos):
                self.paradigms[pos]=[]
            self.paradigms[pos].append(line)

    def create_paradigm(self, lemma, pos):
        print lemma
        if not self.tagset:
            self.handle_tags()

        self.paradigm = []
							  
        genObj=re.compile(r'^(?P<lemmaString>[\wá]+)\+(?P<tagString>[\w\+]+)[\t\s]+(?P<formString>[\wá]*)$', re.U)
        all=""
        for a in self.paradigms[pos]:
            all = all + lemma + "+" + a
        # generator call
        #fstdir="/opt/smi/sme/bin"
        fstdir="/Users/saara/gt/sme/bin"
        gen_norm_fst = fstdir + "/isme-norm.fst"
#        gen_norm_lookup = "echo \"" + all.encode('utf-8') + "\" | /usr/local/bin/lookup -flags mbTT -utf8 -d " + gen_norm_fst
        gen_norm_lookup = "echo \"" + all.encode('utf-8') + "\" | /Users/saara/bin/lookup -flags mbTT -utf8 -d " + gen_norm_fst
        lines_tmp = os.popen(gen_norm_lookup).readlines()
        for line in lines_tmp:
            if not line.strip(): continue
            matchObj=genObj.search(line)
            if matchObj:
                #print line
                g = Entry()
                g.classes={}
                lemma = matchObj.expand(r'\g<lemmaString>')
                g.form = matchObj.expand(r'\g<formString>')
                if re.compile("\?").match(g.form): continue
                g.tags = matchObj.expand(r'\g<tagString>')
                for t in g.tags.split('+'):
                    #print "JEE" + t
                    if self.tagset.has_key(t):
                        tagclass=self.tagset[t]
                        g.classes[tagclass]=t
                self.paradigm.append(g)


class Questions:

    def __init__(self):
        self.tagset = {}
        self.questions = {}

    # Read elements attached to particular question or answer.
    def read_elements(self,head,elementtype, question_element):

        for el in head.getElementsByTagName("element"):

            syntax=el.getAttribute("type")
            
            lemma=""
            tag=""
            semclass=""
            pos=""
            tagstrings = el.getElementsByTagName("grammar")
            if tagstrings:
                tag= tagstrings[0].getAttribute("tag")
                pos= tagstrings[0].getAttribute("pos")
                
            semclasses=el.getElementsByTagName("sem")
            if semclasses:
                semclass=semclasses[0].getAttribute("class")

            # Search for existing word in the database.
            w=None
            lemmas=el.getElementsByTagName("lemma")
            for l in lemmas:
                lemma = l.firstChild.data
                if lemma:
                    print lemma
                    # Add pos information here!
                    word_elements = Word.objects.filter(Q(lemma=lemma))
                    if word_elements:
                        w=word_elements[0]
                    else:
                        print "Word not found! " + lemma
                        
            # Search for existing semtype
            # If not found, create a new one
            s=None
            if semclass:
                s, created = Semtype.objects.get_or_create(semtype=semclass)
                        
            # Try to find an element matching the specification.
            # Attach an element to a manytomany-table qelement.
            # If element was not found, create a new one.
            elements=None
            if not tag:
                if not pos:
                    elements=Element.objects.filter(syntax=syntax)
                else:
                    elements=Element.objects.filter(pos=pos, syntax=syntax)
            else:
                elements=Element.objects.filter(tagspec=tag)

            # create qelement object that connects element and question
            if elements:
                for element in elements:
                    qe, created = QElement.objects.get_or_create(element=element, \
                                                                 question=question_element,\
                                                                 elementtype=elementtype, \
                                                                 word=w,semtype=s)
                    qe.save()
            else:
                if tag: pos = tag.split('+')[0]                    
                element, created = Element.objects.get_or_create(tagspec=tag, pos=pos, syntax=syntax)
                print tag + " " + " " + pos + " " + syntax
                qe, created = QElement.objects.get_or_create(element=element, \
                                                             question=question_element,\
                                                             elementtype=elementtype, \
                                                             word=w,semtype=s)
                qe.save()
                
                
    def read_questions(self, infile):
    
        xmlfile=file(infile)
        tree = _dom.parse(infile)

        print "Created questions:"
        for q in tree.getElementsByTagName("q"):

            # Store question
            qtype = q.getElementsByTagName("qtype")[0].firstChild.data
            question=q.getElementsByTagName("question")[0]
            text=question.getElementsByTagName("text")[0].firstChild.data
            
            question_element = Question.objects.create(question=text, qtype=qtype)
            print text
            self.read_elements(question,"question",question_element)
            
            answer=q.getElementsByTagName("answer")[0]
            text=answer.getElementsByTagName("text")[0].firstChild.data
            question_element.answer=text
            question_element.save()
            print text
            self.read_elements(answer, "answer", question_element)


    def read_grammar(self, infile):
    
        xmlfile=file(infile)
        tree = _dom.parse(infile)

        print "Created elements:"
        for el in tree.getElementsByTagName("element"):

            syntax=el.getAttribute("type")
            for gr in el.getElementsByTagName("grammar"):
                pos=gr.getAttribute("pos")
                tag=gr.getAttribute("tag")
                print syntax + " " + pos + " " + tag
                element, created = Element.objects.get_or_create(tagspec=tag, pos=pos, syntax=syntax)
                element.save()
