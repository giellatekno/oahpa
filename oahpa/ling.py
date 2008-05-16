from settings import *
from morph.models import *
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

    def read_paradigms(self, parafile):
        
        fileObj = codecs.open(parafile, "r", "utf-8" )
        genObj=re.compile(r'^(?P<lemmaString>[\w]+)\+(?P<tagString>[\w\+]+)[\t\s]+(?P<formString>[\w]*)$', re.U)

        while True:
            line = fileObj.readline()
            if not line: break
            if not line.strip(): continue
            matchObj=genObj.search(line)
            if matchObj:
                g = Entry()
                g.classes={}
                lemma = matchObj.expand(r'\g<lemmaString>')
                if not self.paradigms.has_key(lemma):
                    self.paradigms[lemma] = []
                g.form = matchObj.expand(r'\g<formString>')
                if re.compile("\?").match(g.form.encode('utf-8')): continue
                g.tags = matchObj.expand(r'\g<tagString>')
                for t in g.tags.split('+'):
                    #print "JEE", t
                    if self.tagset.has_key(t):
                        tagclass=self.tagset[t]
                        #print tagclass
                        g.classes[tagclass]=t
                self.paradigms[lemma].append(g)
                
        fileObj.close()

class Questions:

    def __init__(self):
        self.tagset = {}
        self.questions = {}

    def read_elements(self,head,type, question_element):
        
            i=1
            for el in head.getElementsByTagName("element"):

                pos=el.getAttribute("pos")
                lemmas=el.getElementsByTagName("lemma")
                lemma=""
                tagstring=""
                semclass=""
                if lemmas:
                    lemma = lemmas[0].firstChild.data
                tagstrings = el.getElementsByTagName("grammar")
                if tagstrings:
                    tagstring= tagstrings[0].getAttribute("tag")
                semclasses=el.getElementsByTagName("sem")
                if semclasses:
                    semclass=semclasses[0].getAttribute("class")

                # Search for existing word in the database.
                w=None
                if lemma:
                    word_elements = Word.objects.filter(Q(lemma=lemma) & Q(pos=pos))
                    if word_elements:
                        w=word_elements[0]

                # Search for existing semtype
                s=None
                if semclass:
                    s, created = Semtype.objects.get_or_create(semtype=semclass)
                        
                # Create new element
                # Get does not work properly with NoneType foreign keys.
                try:
                    if w==None:
                        if s==None:
                            element = Element.objects.get(word__isnull=True,semtype__isnull=True,\
                                                          tagspec=tagstring,pos=pos)
                        else:
                            element = Element.objects.get(word__isnull=True,semtype=s,\
                                                          tagspec=tagstring,pos=pos)
                    if not w==None:
                        if s==None:
                            element = Element.objects.get(word=w,semtype__isnull=True,\
                                                          tagspec=tagstring,pos=pos)
                        else:
                            element = Element.objects.get(word=w,semtype=s,\
                                                          tagspec=tagstring,pos=pos)
                except Element.DoesNotExist:
                    element = Element(semtype=s,word=w,\
                                      tagspec=tagstring,pos=pos)
                    element.save()

                qe, created = QElement.objects.get_or_create(element=element, \
                                                             question=question_element,\
                                                             elementtype=type,number=i)
                qe.save()
                
                i=i+1
                
    def read_questions(self, infile):
    
        xmlfile=file(infile)
        tree = _dom.parse(infile)

        print "Created questions:"
        for q in tree.getElementsByTagName("q"):

            # Store question
            question=q.getElementsByTagName("question")[0]
            text=question.getElementsByTagName("text")[0].firstChild.data
            
            question_element, created = Question.objects.get_or_create(question=text)
            print text
            self.read_elements(question,"question",question_element)
