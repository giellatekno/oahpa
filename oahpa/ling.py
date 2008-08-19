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

    def handle_tags(self,tagfile,add_db):
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
                    if add_db and tagclass and string:
                        #print "adding " + tagclass + " " + string
                        tagset, created = Tagset.objects.get_or_create(tagset=tagclass)
                        pos, created = Tagname.objects.get_or_create(tagname=string,tagset=tagset)


    def read_paradigms(self,paradigmfile,tagfile, add_database):
        if not self.tagset:
            self.handle_tags(tagfile)

        fileObj = codecs.open(paradigmfile, "r", "utf-8" )
        posObj=re.compile(r'^(?P<posString>[\w]+)\+.*$', re.U)

        while True:
            line = fileObj.readline()
            if not line: break
            if not line.strip(): continue
            matchObj=posObj.search(line)
            if matchObj:
                pos=matchObj.expand(r'\g<posString>')
            if not self.paradigms.has_key(pos):
                self.paradigms[pos]=[]
            self.paradigms[pos].append(line)
                


    def create_paradigm(self, lemma, pos):
        #print lemma
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
        #gen_norm_lookup = "echo \"" + all.encode('utf-8') + "\" | /usr/local/bin/lookup -flags mbTT -utf8 -d " + gen_norm_fst
        gen_norm_lookup = "echo \"" + all.encode('utf-8') + "\" | /Users/saara/bin/lookup -flags mbTT -utf8 -d " + gen_norm_fst
        lines_tmp = os.popen(gen_norm_lookup).readlines()
        for line in lines_tmp:
            if not line.strip(): continue
            matchObj=genObj.search(line)
            if matchObj:
                g = Entry()
                g.classes={}
                lemma = matchObj.expand(r'\g<lemmaString>')
                g.form = matchObj.expand(r'\g<formString>')
                if re.compile("\?").match(g.form): continue
                g.tags = matchObj.expand(r'\g<tagString>')
                for t in g.tags.split('+'):
                    if self.tagset.has_key(t):
                        tagclass=self.tagset[t]
                        g.classes[tagclass]=t
                self.paradigm.append(g)


class Questions:

#    def __init__(self):


    def read_element(self,head,qaelement,el,syntax,optional):

        lemma=""
        tag=""
        semclass=""
        pos=""
        gametype=""
        w=None
        s=None
        agr_elements=None
        elements=None
        agreement=None
        print "ELEMENT " + syntax

        # Add subject-mainverb agreement by default.
        if syntax=="MAINV":
            agr_id="SUBJ"
            print "TRYING verb agreement " + agr_id + " " + qaelement.qatype
            if QElement.objects.filter(Q(question=qaelement) & Q(syntax=agr_id) &\
                                       Q(question__qatype=qaelement.qatype)).count() > 0:
                agr_elements = QElement.objects.filter(Q(question=qaelement) & \
                                                       Q(syntax=agr_id) &\
                                                       Q(question__qatype=qaelement.qatype))
                print "*** found agreement elements 0"

        # If there is an xml-element, collect information from there.
        if el:
            gametype= el.getAttribute("game")
            
            grammar = el.getElementsByTagName("grammar")
            if grammar:
                tag= grammar[0].getAttribute("tag")
                pos= grammar[0].getAttribute("pos")

            # Search for existing semtype
            # If not found, create a new one                
            semclasses=el.getElementsByTagName("sem")
            semgame=[]
            if semclasses:
                semclass=semclasses[0].getAttribute("class")
                semgame_str = semclasses[0].getAttribute("game")
                if semgame_str:
                    semgame.append(semgame_str)
            if semclass:
                s, created = Semtype.objects.get_or_create(semtype=semclass)

            # if the game was not given, using both
            if not semgame and s:
                semgame= ["morfa", "qa"]
                
            # Search for agreement, only one allowed at the moment
            agreement = el.getElementsByTagName("agreement")

            # Search for existing word in the database.
            ids=el.getElementsByTagName("id")
            for i in ids:
                word_id = i.firstChild.data
                if word_id:
                    #print "Searching lemma: " + lemma
                    # Add pos information here!
                    word_elements = Word.objects.filter(Q(wordid=word_id))
                    if word_elements:
                        w=word_elements[0]
                    else:
                        print "Word not found! " + word_id
                                            
            # Try to find an element matching the specification.
            # Attach an element to a manytomany-table qelement.
            # If element was not found, create a new one.
            if tag:
                print "SEARCHING TAGS " + tag
                tagvalues = []
                self.get_tagvalues(tag,"",tagvalues)
                elements=Tag.objects.filter(Q(string__in=tagvalues))
            else:
                if pos:
                    print "POS " + pos
                    if QElement.objects.filter(Q(question__isnull=True) & \
                                               Q(identifier=syntax) & \
                                               Q(tag__pos=pos)).count()>0:
                        qel = QElement.objects.filter(Q(question__isnull=True) & \
                                                      Q(identifier=syntax) & \
                                                      Q(tag__pos=pos))[0]
                        elements = qel.tag.filter(pos=pos)
                else:
                    if QElement.objects.filter(Q(question__isnull=True) & \
                                               Q(identifier=syntax)).count()>0:
                        qel = QElement.objects.filter(Q(question__isnull=True) & \
                                                      Q(identifier=syntax))[0]
                        elements = qel.tag.all()

            # Agreement from xml-files
            # Try first inside question or answer
            # Then in answer-question level
            if agreement:
                agr_id=agreement[0].getAttribute("id")
                if QElement.objects.filter(Q(question=qaelement) & Q(syntax=agr_id) & \
                                           Q(question__qatype=qaelement.qatype)).count() > 0:
                    agr_elements = QElement.objects.filter(Q(question=qaelement) & \
                                                           Q(syntax=agr_id) &\
                                                           Q(question__qatype=qaelement.qatype))
                    print "*** found agreement elementes 1"
                        
                else:
                    if Question.objects.filter(id=qaelement.answer_id).count() > 0:
                        q=Question.objects.filter(id=qaelement.answer_id)[0]
                        if QElement.objects.filter(Q(question__id=qaelement.answer_id) & \
                                                   Q(syntax=agr_id)).count() > 0:
                            agr_elements = QElement.objects.filter(Q(question__id=qaelement.answer_id) & \
                                                                   Q(syntax=agr_id))
                            print "*** found agreement elementes 2"

                            
            # create qelement object that connects element and question
            # If there are elements created for the specification, create links to them.
            qe = QElement.objects.create(question=qaelement,\
                                         identifier = syntax, \
                                         syntax = syntax, \
                                         word=w,\
                                         optional=optional, \
                                         gametype=gametype)

            if s:
                for sem in semgame:
                    q_sem = SemtypeElement.objects.create(qelement=qe, \
                                                          semtype=s, \
                                                          game=sem)
            if agr_elements:
                for a in agr_elements:
                    a.agreement_set.add(qe)
                    #qe.agreement_set.add(a)
                    a.save()
                qe.save()
                
            if elements:
                for element in elements:
                    qe.tag.add(element)
                qe.save()
            return

        # If there is a dummy element for this use it
        if QElement.objects.filter(Q(identifier=syntax) & Q(question__isnull=True)).count()>0:
            qelements = QElement.objects.filter(Q(identifier=syntax) & Q(question__isnull=True))
            for qel in qelements:
                semelements = SemtypeElement.objects.filter(Q(qelement=qel))
                #print "COPYING.. " + str(qel.id)
                element_count = qel.tag.count()
                elements = list(qel.tag.all())

                qe = QElement.objects.create(question=qaelement,\
                                             word=w,\
                                             optional=qel.optional,\
                                             identifier=syntax,\
                                             gametype=gametype, \
                                             syntax=qel.syntax)
                if s:
                    for sem in semelements:
                         q_sem = SemtypeElement.objects.create(qelement=qe, \
                                                              semtype=sem.semtype, \
                                                              game=sem.game)

                for element in elements:
                    #print "adding element " + syntax
                    qe.tag.add(element)
                qe.save()
                if agr_elements:
                    for a in agr_elements:
                        a.agreement_set.add(qe)
                        #qe.agreement_set.add(a)
                        a.save()
                    qe.save()
            return

        # If there is no information, create qelement object that connects element and question
        qe = QElement.objects.create(question=qaelement,\
                                     identifier = syntax, \
                                     syntax = syntax, \
                                     word=w,\
                                     gametype=gametype, \
                                     optional=optional)

        if elements:
            for element in elements:
                qe.tag.add(element)
            qe.save()

    # Read elements attached to particular question or answer.
    def read_elements(self,head,qaelement):

        els = head.getElementsByTagName("element")
        qastrings =  qaelement.string.split()

        #Read first subject and answersubject for agreement
        element=None
        if "SUBJ" in set(qastrings):
            for e in els:
                if e.getAttribute("id")=="SUBJ":
                    element = e
                    break
                
            self.read_element(head,qaelement,element,"SUBJ",0)

        element=None
        if "ANSWERSUBJECT" in set(qastrings):
            for e in els:
                if e.getAttribute("id")=="ANSWERSUBJECT":
                    element = e
                    break
                
            self.read_element(head,qaelement,element,"ANSWERSUBJECT",0)

        # Process rest of the elements in the string.
        for s in qastrings:
            if s=="SUBJ": continue
            if s=="ANSWERSUBJECT": continue

            if s.find('('): optional=0
            else: optional=1
            syntax = s.lstrip("(")
            syntax = syntax.rstrip(")")

            element=None            
            for e in els:
                el_id = e.getAttribute("id")
                if el_id==s:
                    self.read_element(head,qaelement,e,syntax,optional)


    def read_questions(self, infile):
    
        xmlfile=file(infile)
        tree = _dom.parse(infile)

        print "Created questions:"
        for q in tree.getElementsByTagName("q"):

            # Store question
            qtype=""
            qtype_el = q.getElementsByTagName("qtype")
            if qtype_el:
                qtype = q.getElementsByTagName("qtype")[0].firstChild.data
            question=q.getElementsByTagName("question")[0]
            text=question.getElementsByTagName("text")[0].firstChild.data
            
            question_element = Question.objects.create(string=text, qtype=qtype, qatype="question")
            question_element.save()
            print text
            self.read_elements(question, question_element)            

            # There can be more than one answer for each question,
            # Store them separately.
            answers=q.getElementsByTagName("answer")
            for ans in answers:                
                text=ans.getElementsByTagName("text")[0].firstChild.data
                answer_element = Question.objects.create(string=text,qatype="answer",answer=question_element)
                answer_element.save()                
                print text
                self.read_elements(ans, answer_element)


    def read_grammar(self, infile):
    
        xmlfile=file(infile)
        tree = _dom.parse(infile)

        print "Created elements:"
        tags=tree.getElementsByTagName("tags")[0]
        for el in tags.getElementsByTagName("element"):

            syntax=el.getAttribute("id")
            elements = []
            for gr in el.getElementsByTagName("grammar"):
                pos=gr.getAttribute("pos")
                tag=gr.getAttribute("tag")
                print syntax + " " + pos + " " + tag
                tagvalues = []
                self.get_tagvalues(tag,"",tagvalues)
                for t in tagvalues:
                    if Tag.objects.filter(string=t).count() > 0:
                        element = Tag.objects.get(string=t)
                        element.save()
                        elements.append(element)
                        
                # create a dummy question element for the tag
                qe = QElement.objects.create(optional=0, identifier=syntax, syntax=syntax)
                for element in elements:
                    qe.tag.add(element)
                qe.save()

        partitions=tree.getElementsByTagName("partitions")[0]        
        for el in partitions.getElementsByTagName("part"):
            name=el.getAttribute("name")
            syntax=el.getAttribute("id")
            for select in el.getElementsByTagName("select"):
                element = select.getElementsByTagName("element")[0]
                el_id = element.getAttribute("id")
                optional = element.getAttribute("optional")
                if not optional:
                    optional=0
                elements = []
                for gr in element.getElementsByTagName("grammar"):
                    pos=gr.getAttribute("pos")
                    tag=gr.getAttribute("tag")
                    #print syntax + " " + pos + " " + tag
                    tagvalues = []
                    self.get_tagvalues(tag,"",tagvalues)
                    for t in tagvalues:
                        if Tag.objects.filter(string=t).count() > 0:
                            element = Tag.objects.get(string=t)
                            element.save()
                            elements.append(element)
                            
                # create a dummy question element for ANSWERSUBJECT
                qe = QElement.objects.create(optional=optional, identifier=name, syntax=el_id)
                for element in elements:
                    qe.tag.add(element)
                qe.save()


    def get_tagvalues(self,rest,tagstring,tagvalues):

        if not rest:
            tagvalues.append(tagstring)
            return
        if rest.count("+") > 0:
            t, rest = rest.split('+',1)
        else:
            t=rest
            rest=""
        if Tagname.objects.filter(tagname=t).count() > 0:
            if tagstring:
                tagstring = tagstring + "+" + t
            else:
                tagstring = t
            self.get_tagvalues(rest,tagstring,tagvalues)
        else:
            if Tagset.objects.filter(Q(tagset=t)).count() > 0:
                tagnames=Tagname.objects.filter(tagset__tagset=t)
                for t in tagnames:
                    if tagstring:
                        tagstring2 = tagstring + "+" + t.tagname
                    else:
                        tagstring2 = t.tagname
                    self.get_tagvalues(rest,tagstring2,tagvalues)
    
    def read_semtypes(self, infile):

        xmlfile=file(infile)
        tree = _dom.parse(infile)

        for el in tree.getElementsByTagName("subclasses"):
            semclass=el.getAttribute("class")
            s, created = Semtype.objects.get_or_create(semtype=semclass)
            for el2 in el.getElementsByTagName('sem'):
               subclass  = el2.getAttribute("class")
               for w in Word.objects.filter(Q(semtype__semtype=subclass) & ~Q(semtype__semtype=semclass)):
                   print w.lemma + ": adding semtype " + semclass
                   w.semtype.add(s)
                   w.save()
