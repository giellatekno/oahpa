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

        if not self.tagset:
            self.handle_tags()

        self.paradigm = []
							  
        genObj=re.compile(r'^(?P<lemmaString>[\wáŋčžšđŧ]+)\+(?P<tagString>[\w\+]+)[\t\s]+(?P<formString>[\wáŋčžšđŧ]*)$', re.U)
        all=""

        if self.paradigms.has_key(pos):
            for a in self.paradigms[pos]:
                all = all + lemma + "+" + a

        # generator call
        #fstdir="/opt/smi/sme/bin"
        #lookup = /usr/local/bin/lookup

        fstdir="/Users/saara/gt/sme/bin"
        lookup = "/Users/saara/bin/lookup"

        gen_norm_fst = fstdir + "/isme-norm.fst"

        gen_norm_lookup = "echo \"" + all.encode('utf-8') + "\" | " + lookup + " -flags mbTT -utf8 -d " + gen_norm_fst
        lines_tmp = os.popen(gen_norm_lookup).readlines()
        for line in lines_tmp:
            print line.decode('utf-8')
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


    def generate_numerals(self):
        """
        Generate all the cardinal numbers
        Create paradigms and store to db
        """

        language = "sme"
        #fstdir="/opt/smi/" + language + "/bin"
        #lookup = /usr/local/bin/lookup
        
        fstdir="/Users/saara/gt/" + language + "/bin"        
        lookup = "/Users/saara/bin/lookup"

        numfst = fstdir + "/" + language + "-num.fst"

        for num in range(1,20):

            num_lookup = "echo \"" + str(num) + "\" | " + lookup + " -flags mbTT -utf8 -d " + numfst
            numerals = os.popen(num_lookup).readlines()

            # Take only first one.
            # Change this if needed!
            num_list=[]
            for num in numerals:
                line = num.strip()
                if line:
                    nums = line.split('\t')
                    num_list.append(nums[1].decode('utf-8'))
            numstring = num_list[0]

            w, created = Word.objects.get_or_create(wordid=num, lemma=numstring, pos="Num")
            w.save()

            self.create_paradigm(numstring, "Num")
            for form in self.paradigm:
                form.form = form.form.replace("#","")
                g=form.classes
                t,created=Tag.objects.get_or_create(string=form.tags,pos=g.get('Wordclass', ""),\
                                                    number=g.get('Number',""),case=g.get('Case',""),\
                                                    possessive=g.get('Possessive',""),grade=g.get('Grade',""),\
                                                    infinite=g.get('Infinite',""), \
                                                    personnumber=g.get('Person-Number',""),\
                                                    polarity=g.get('Polarity',""),\
                                                    tense=g.get('Tense',""),mood=g.get('Mood',""), \
                                                    subclass=g.get('Subclass',""), \
                                                    attributive=g.get('Attributive',""))
                
                t.save()
                form, created = Form.objects.get_or_create(fullform=form.form,tag=t,word=w)
                form.save()


class Questions:

    def read_element(self,qaelement,el,el_id,qtype):

        print "Creating element", el_id

        # Syntactic function of the element
        if self.values.has_key(el_id) and self.values[el_id].has_key('syntax'):
            syntax = self.values[el_id]['syntax']
        else:
            syntax = el_id

        if not el: print "No element given."

        # Some of the answer elements share content of question elements.
        content_id=""
        if el: content_id = el.getAttribute("content")
        if not content_id: content_id=el_id
            
        # Search for the same element in question side
        # If there is no element given in the answer, the element
        # is a copy of the question.
        question_qelements = None
        
        if QElement.objects.filter(Q(question__id=qaelement.question_id) & \
                                   Q(identifier=content_id)).count() > 0:
            question_qelements = QElement.objects.filter(Q(question__id=qaelement.question_id) & \
                                                         Q(identifier=content_id))

            if not el:
                print "LUOMASSA", syntax
                for q in question_qelements:
                    qe = QElement.objects.create(question=qaelement,\
                                                 identifier=el_id,\
                                                 syntax=q.syntax)
                    
                    # mark as a copy
                    q.copy_set.add(qe)
                    qe.save()
                    q.save()
                    return
            
        ############### AGREEMENT
        # Search for elementes that agree
        agr_elements=None
        if syntax=="MAINV":
            agr_id="SUBJ"
            print "TRYING verb agreement " + agr_id + " " + qaelement.qatype
            if QElement.objects.filter(Q(question=qaelement) & Q(syntax=agr_id) &\
                                       Q(question__qatype=qaelement.qatype)).count() > 0:
                agr_elements = QElement.objects.filter(Q(question=qaelement) & \
                                                       Q(syntax=agr_id) &\
                                                       Q(question__qatype=qaelement.qatype))
                print "*** found agreement elements 0"
        

        agreement = ""
        if el: agreement = el.getElementsByTagName("agreement")
        if agreement: print "Agreement:", agreement[0].getAttribute("id")
        
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
                if Question.objects.filter(id=qaelement.question_id).count() > 0:
                    q=Question.objects.filter(id=qaelement.question_id)[0]
                    if QElement.objects.filter(Q(question__id=qaelement.question_id) & \
                                               Q(syntax=agr_id)).count() > 0:
                        agr_elements = QElement.objects.filter(Q(question__id=qaelement.question_id) & \
                                                               Q(syntax=agr_id))
                        print "*** found agreement elementes 2"


        ############ WORDS
        # Search for existing word in the database.
        ids = []
        if el: ids=el.getElementsByTagName("id")
        words = {}
        word_elements = None
        for i in ids:
            word_id = i.firstChild.data
            if word_id:
                # Add pos information here!
                word_elements = Word.objects.filter(Q(wordid=word_id))
                if not word_elements:
                    print "Word not found! " + word_id            
                    
        # Search for existing semtype
        # Semtype overrides the word id selection
        if not word_elements:
            semclasses= []
            if el: semclasses=el.getElementsByTagName("sem")
            if semclasses:
                semclass=semclasses[0].getAttribute("class")
                word_elements = Word.objects.filter(Q(semtype__semtype=semclass))
            valclasses= []
            if el: valclasses=el.getElementsByTagName("val")
            if valclasses:
                valclass=valclasses[0].getAttribute("class")
                word_elements = Word.objects.filter(Q(valency=valclass))
                print "Valency class", valclass, word_elements.count()


        # If still no words, get the default words for this element:
        if not word_elements:
            if self.values.has_key(el_id) and self.values[el_id].has_key('words'):
                word_elements = self.values[el_id]['words']

        if word_elements:
            for w in word_elements:
                if not words.has_key(w.pos): words[w.pos] = []
                words[w.pos].append(w)


        ############# GRAMAMR
        tagelements = None
        grammars = []
        if el: grammars = el.getElementsByTagName("grammar")
        if not el or not grammars:
            # If there is no grammatical specification, the element is created solely
            # on the basis of grammar.
            if self.values.has_key(el_id):
                if self.values[el_id].has_key('tags'):
                    tagelements = self.values[el_id]['tags']

        # An element for each different grammatical specification.
        else:
            poses = []
            tags = []
            for gr in grammars:
                tags.append(gr.getAttribute("tag"))
                poses.append(gr.getAttribute("pos"))

            tagstrings = []
            if poses:
                if self.values.has_key(el_id):
                    if self.values[el_id].has_key('tags'):
                        tagelements = self.values[el_id]['tags'].filter(pos__in=poses)

            if tags:
                for tag in tags:
                    tagvalues = []
                    self.get_tagvalues(tag,"",tagvalues)
                    tagstrings.extend(tagvalues)
                print tagstrings
                if tagelements:
                    tagelements = tagelements | Tag.objects.filter(Q(string__in=tagstrings))
                else:
                    tagelements = Tag.objects.filter(Q(string__in=tagstrings))

            # Extra check for pronouns
            # If pronoun id is given, only the tags related to that pronoun are preserved.
            for t in tagelements:
                if t.pos == 'Pron':
                    print "kaikki", t.string
                    if not words.has_key('Pron'): break
                    found = False
                    print "going through"
                    for w in words['Pron']:
                        print w.lemma
                        if Form.objects.filter(Q(tag=t) & Q(word=w)).count()>0:
                            found = True
                            break
                    if not found:
                        print "removing an element.."
                        print t.string
                        tagelements = tagelements.filter(~Q(id=t.id))
            
        # Find different pos-values in tagelements
        posvalues = {}
        # Elements that do not inflection information are not created.
        if not tagelements and not agr_elements:
            print "no inflection for", el_id
            return
        if not tagelements: posvalues[""] = 1
        else:
            for t in tagelements:
                posvalues[t.pos] = 1

        if el:
            task = el.getAttribute("task")
            print "setting", el_id, "as task"
            if task:
                qaelement.task = syntax
                qaelement.save()
        else:
            if el_id == qtype:
                qaelement.task = syntax
                qaelement.save()
                
        ############# CREATE ELEMENTS

        # Add an element for each pos:
        for p in posvalues.keys():
            qe = QElement.objects.create(question=qaelement,\
                                         identifier=el_id,\
                                         syntax=syntax)
            
            # Add links to corresponding question elements.
            if question_qelements:
                for q in question_qelements:
                    q.copy_set.add(qe)
                    qe.save()
                    q.save()

            if tagelements:
                for t in tagelements:
                    if t.pos == p:
                        qe.tags.add(t)

            # Create links to words.
            if not words.has_key(p):
                print "looking for words..", el_id, p
                word_elements = Word.objects.filter(pos=p)
                if word_elements:
                    for w in word_elements:
                        if not words.has_key(p): words[w.pos] = []
                        words[w.pos].append(w)

            for w in words[p]:
                we = WordQElement.objects.create(qelement=qe,\
                                                 word=w)

            # add agreement info.
            if agr_elements:
                for a in agr_elements:
                    a.agreement_set.add(qe)
                a.save()
            qe.save()

    # Read elements attached to particular question or answer.
    def read_elements(self, head, qaelement, qtype):

        els = head.getElementsByTagName("element")
        qastrings =  qaelement.string.split()

        # Read first subject for agreement
        element=None
        if "SUBJ" in set(qastrings):
            for e in els:
                if e.getAttribute("id")=="SUBJ":
                    element = e
                    break

            self.read_element(qaelement, element, "SUBJ", qtype)


        # Process rest of the elements in the string.
        for s in qastrings:
            if s=="SUBJ": continue

            syntax = s.lstrip("(")
            syntax = syntax.rstrip(")")

            element=None
            found = False
            for e in els:
                el_id = e.getAttribute("id")
                if el_id==s:
                    self.read_element(qaelement,e,syntax,qtype)
                    found = True
            if not found:
                self.read_element(qaelement,None,syntax,qtype)

    def read_questions(self, infile, grammarfile):
    
        xmlfile=file(infile)
        tree = _dom.parse(infile)

        self.read_grammar(grammarfile)

        print "Created questions:"
        for q in tree.getElementsByTagName("q"):

            gametype = q.getAttribute('game')
            # Store question
            qtype=""
            qtype_el = q.getElementsByTagName("qtype")
            if qtype_el:
                qtype = q.getElementsByTagName("qtype")[0].firstChild.data
            question=q.getElementsByTagName("question")[0]
            text=question.getElementsByTagName("text")[0].firstChild.data
            
            question_element = Question.objects.create(string=text, \
                                                       qtype=qtype, \
                                                       gametype=gametype,\
                                                       qatype="question")
            question_element.save()

            self.read_elements(question, question_element,qtype)    

            # There can be more than one answer for each question,
            # Store them separately.
            answers=q.getElementsByTagName("answer")
            for ans in answers:                
                text=ans.getElementsByTagName("text")[0].firstChild.data
                answer_element = Question.objects.create(string=text,qatype="answer",question=question_element)
                answer_element.save()                
                print text
                self.read_elements(ans, answer_element,qtype)


    def read_grammar(self, infile):
    
        xmlfile=file(infile)
        tree = _dom.parse(infile)

        self.values = {}
        
        print "Created elements:"
        tags=tree.getElementsByTagName("tags")[0]
        for el in tags.getElementsByTagName("element"):

            identifier=el.getAttribute("id")
            print "Reading default values for", identifier
            
            info2 = {}
            
            elements = []
            word_id=""
            word = None
            
            syntax =""
            syntaxes = el.getElementsByTagName("syntax")
            if syntaxes:
                syntax = syntaxes[0].firstChild.data
                info2['syntax'] = syntax
                
            word_ids = el.getElementsByTagName("id")
            if word_ids:
                word_id = word_ids[0].firstChild.data
                if word_id:
                    words = Word.objects.filter(wordid=word_id)
                    info2['words'] = words

            info2['pos'] = []
            tagstrings = []

            grammars = el.getElementsByTagName("grammar")
            for gr in grammars:
                optional=0
                
                pos=gr.getAttribute("pos")
                if pos:
                    info2['pos'].append(pos)

                tag=gr.getAttribute("tag")
                optional=gr.getAttribute("optional")
                print optional
                
                tagvalues = []
                self.get_tagvalues(tag,"",tagvalues)
                tagstrings.extend(tagvalues)

            if len(tagstrings) > 0:
                tags = Tag.objects.filter(string__in=tagstrings)
                info2['tags'] = tags
                
            self.values[identifier] = info2


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
               for w in Wordnob.objects.filter(Q(semtype__semtype=subclass) & ~Q(semtype__semtype=semclass)):
                   print w.lemma + ": adding semtype " + semclass
                   w.semtype.add(s)
                   w.save()

    def read_messages(self,infile):

        xmlfile=file(infile)
        tree = _dom.parse(infile)

        for el in tree.getElementsByTagName("message"):
            mid=el.getAttribute("id")
            message = el.firstChild.data
            
            fm, created = Feedbackmsg.objects.get_or_create(msgid=mid, message=message)
            fm.save()

    def set_null(self):

        feedbacks=Feedback.objects.filter(stem='empty')
        for f in feedbacks:
            f.stem=""
            f.save()
        feedbacks=Feedback.objects.filter(gradation='empty')
        for f in feedbacks:
            f.gradation=""
            f.save()
        feedbacks=Feedback.objects.filter(diphthong='empty')
        for f in feedbacks:
            f.diphthong=""
            f.save()
        feedbacks=Feedback.objects.filter(rime='empty')
        for f in feedbacks:
            f.rime=""
            f.save()
        feedbacks=Feedback.objects.filter(soggi='empty')
        for f in feedbacks:
            f.soggi=""
            f.save()
        feedbacks=Feedback.objects.filter(case2='empty')
        for f in feedbacks:
            f.case2=""
            f.save()
        feedbacks=Feedback.objects.filter(number='empty')
        for f in feedbacks:
            f.number=""
            f.save()
        feedbacks=Feedback.objects.filter(personnumber='empty')
        for f in feedbacks:
            f.personnumber=""
            f.save()
        feedbacks=Feedback.objects.filter(tense='empty')
        for f in feedbacks:
            f.tense=""
            f.save()
        feedbacks=Feedback.objects.filter(mood='empty')
        for f in feedbacks:
            f.mood=""
            f.save()
        feedbacks=Feedback.objects.filter(grade='empty')
        for f in feedbacks:
            f.grade=""
            f.save()
        feedbacks=Feedback.objects.filter(attrsuffix='empty')
        for f in feedbacks:
            f.attrsuffix=""
            f.save()
    
    def insert_feedback(self,cursor,pos,stem,diphthong,gradation,rime,soggi,case,number,personnumber="empty",tense="empty",mood="empty",attributive="empty",grade="empty",attrsuffix="empty"):
        #print pos, stem, diphthong, gradation, rime, soggi,case,number,personnumber,tense,mood,grade
        
        cursor.execute("INSERT INTO oahpa.drill_feedback (pos,stem,diphthong,gradation,rime,soggi,case2,number,personnumber,tense,mood,attributive,grade,attrsuffix) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE pos=%s", (pos,stem,diphthong,gradation,rime,soggi,case,number,personnumber,tense,mood,attributive,grade,attrsuffix,pos))

    def read_feedback(self, infile, pos, msgfile=None):

        from django.db import connection
        print infile
        if not pos: return None

        if msgfile:
            self.read_messages(msgfile)

        xmlfile=file(infile)
        tree = _dom.parse(infile)

        stem_messages = {}
        gradation_messages = {}

        # Find out different values for variables.
        # Others can be listed, but soggi is searched at the moment.
        rimes={}
        attrsuffixs={}
        compsuffixs={}
        #soggis={}
        wordforms = tree.getElementsByTagName("stems")[0]
        for el in wordforms.getElementsByTagName("stem"):
            if el.getAttribute("rime"):
                rime = el.getAttribute("rime")
                if rime=="0": rime = "norime"
                rimes[rime] = 1
            if el.getAttribute("attrsuffix"):
                attrsuffix = el.getAttribute("attrsuffix")
                if attrsuffix=="0": rime = "noattr"
                attrsuffixs[attrsuffix] = 1
            if el.getAttribute("compsuffix"):
                compsuffix = el.getAttribute("compsuffix")
                if compsuffix=="0": rime = "nocomp"
                compsuffixs[compsuffix] = 1

        #    if el.getAttribute("soggi"):
        #        soggi = el.getAttribute("soggi")
        #        soggis[soggi] = 1

        #soggis[""] = 1
        #soggis = {}
        #attrsuffixs = ['noattr','a','s','es','os','is','i>e','u>o']

        soggis = ['i', 'a', 'u', 'e', 'o','empty']
        attrsuffixs["noattr"] = 1
        compsuffixs["empty"] = 1
        rimes["norime"] = 1
        diphthongs = ["yes","no"]
        stems = ["bisyllabic","trisyllabic","contracted"]
        gradations = ["inv","no","yes"]
        grades = ["Comp","Superl","Pos"]
        cases = ["Acc", "Gen", "Ill","Loc","Com","Ess","Nom"]
        numbers = ["Sg","Pl"]
        tenses = ["Prs","Prt"]
        moods = ["Ind","Cond","Pot","Imprt"]
        personnumbers = ["Sg1","Sg2","Sg3","Du1","Du2","Du3","Pl1","Pl2","Pl3"]
                                
        messages=[]
        print rimes.keys()
        print soggis
        print gradations
        print grades
        print cases
        print numbers 

        cursor = connection.cursor()                        

        wordforms = tree.getElementsByTagName("stems")[0]
        for el in wordforms.getElementsByTagName("stem"):
            feedback = None
            stem =""
            diphthong =""
            rime =""
            gradation=""
            soggi =""
            attrsuffix =""

            ftempl = Entry()

            ftempl.pos = pos

            if el.getAttribute("class"):
                stem=el.getAttribute("class")
                if stem: ftempl.stem = [ stem ]
            if not stem:  ftempl.stem = stems

            if el.getAttribute("gradation"):
                gradation=el.getAttribute("gradation")
                if gradation: ftempl.gradation = [ gradation ]
            if not gradation: ftempl.gradation = gradations
                
            if el.getAttribute("diphthong"):
                diphthong=el.getAttribute("diphthong")
                if diphthong: ftempl.diphthong = [ diphthong ]
            if not diphthong: ftempl.diphthong = diphthongs

            if el.getAttribute("soggi"):
                soggi=el.getAttribute("soggi")
                if soggi: ftempl.soggi = [ soggi ]
            if not soggi: ftempl.soggi = soggis

            if el.getAttribute("attrsuffix"):
                attrsuffix=el.getAttribute("attrsuffix")
                if attrsuffix: ftempl.attrsuffix = [ attrsuffix ]
            if not attrsuffix: ftempl.attrsuffix = attrsuffixs.keys()

            if el.getAttribute("rime"):
                rime=el.getAttribute("rime")
                if rime:
                    if rime=="0": rime = "norime"
                    ftempl.rime = [ rime ]
            if not rime: ftempl.rime = rimes.keys()

            msgs = el.getElementsByTagName("msg")
            for mel in msgs:

                f = Entry()

                case = ""
                number = ""
                personnumber = ""
                tense = ""
                mood = ""
                grade = ""
                attributive = ""

                f.pos = ftempl.pos[:]
                f.stem = ftempl.stem[:]
                f.gradation = ftempl.gradation[:]
                f.diphthong = ftempl.diphthong[:]
                f.soggi = ftempl.soggi[:]
                f.rime = ftempl.rime[:]
                f.attrsuffix = ftempl.attrsuffix[:]
                
                msgid = mel.firstChild.data
                #print "Message id", msgid
                f.msgid = msgid

                if el.getAttribute("attribute"):
                    attributive=el.getAttribute("attribute")
                    if attributive: f.attributive = [ 'Attr' ]
                else: f.attributive = ['Attr', 'NoAttr']
                
                if mel.getAttribute("case"):
                    case=mel.getAttribute("case")
                    if case: f.case = [ case ]
                    # Since noattr is not marked, case entails noattr.
                    f.attributive = [ 'NoAttr' ]
                if not case: f.case = cases

                if mel.getAttribute("number"):
                    number=mel.getAttribute("number")
                    if number: f.number = [ number ]
                if not number: f.number = numbers

                if mel.getAttribute("personnumber"):
                    personnumber=mel.getAttribute("personnumber")
                    if personnumber: f.personnumber = [ personnumber ]
                if not personnumber: f.personnumber = personnumbers

                if mel.getAttribute("tense"):
                    tense=mel.getAttribute("tense")
                    if tense: f.tense = [ tense ]
                if not tense: f.tense = tenses

                if mel.getAttribute("mood"):
                    mood=mel.getAttribute("mood")
                    if mood: f.mood = [ mood ]
                if not mood: f.mood = moods

                if mel.getAttribute("grade"):
                    grade=mel.getAttribute("grade")
                    if grade: f.grade = [ grade ]
                if not grade: f.grade = grades


                messages.append(f)


        for f in messages:
            print f.msgid
            if f.pos == "N" or pos=="A":
                for stem in f.stem:
                    for gradation in f.gradation:
                        for diphthong in f.diphthong:
                            for rime in f.rime:
                                for soggi in f.soggi:
                                    if f.pos == "A":
                                        for grade in f.grade:
                                            for attributive in f.attributive:
                                                if attributive == 'Attr':
                                                    # Attributive forms: no case inflection.
                                                    for attrsuffix in f.attrsuffix:
                                                        case="empty"
                                                        number="empty"
                                                        self.insert_feedback(cursor,pos,stem,diphthong,gradation,rime,soggi,case,number,'empty','empty','empty','Attr',grade,attrsuffix)
                                                        f2, created=Feedback.objects.get_or_create(stem=stem,\
                                                                                                   diphthong=diphthong,\
                                                                                                   gradation=gradation,\
                                                                                                   rime=rime,\
                                                                                                   attributive='Attr',\
                                                                                                   attrsuffix=attrsuffix,\
                                                                                                   pos=pos,\
                                                                                                   number=number,\
                                                                                                   grade=grade,\
                                                                                                   soggi=soggi)
                                                        msgs = Feedbackmsg.objects.filter(msgid=f.msgid)
                                                        if msgs:
                                                            f2.messages.add(msgs[0])
                                                        else : print "No messages found:", f.msgid
                                                        f2.save()
                                    
                                                else:
                                                    for case in f.case:
                                                        #essive without number inflection
                                                        if case == "Ess":
                                                            number="empty"
                                                            self.insert_feedback(cursor,pos,stem,diphthong,gradation,rime,soggi,case,number,'empty','empty','empty','NoAttr',grade)
                                                            f2, created=Feedback.objects.get_or_create(stem=stem,\
                                                                                                       diphthong=diphthong,\
                                                                                                       gradation=gradation,\
                                                                                                       rime=rime,\
                                                                                                       attributive='NoAttr',\
                                                                                                       pos=pos,\
                                                                                                       number=number,\
                                                                                                       case2=case,\
                                                                                                       grade=grade,\
                                                                                                       soggi=soggi)
                                                            msgs = Feedbackmsg.objects.filter(msgid=f.msgid)
                                                            if msgs:
                                                                f2.messages.add(msgs[0])
                                                            else : print "No messages found:", f.msgid														
                                                            f2.save()
                                                            
                                                        else:
                                                            for number in f.number:
                                                                self.insert_feedback(cursor,pos,stem,diphthong,gradation,rime,soggi,case,number,'empty','empty','empty','NoAttr',grade)
                                                                f2, created=Feedback.objects.get_or_create(stem=stem,\
                                                                                                           diphthong=diphthong,\
                                                                                                           gradation=gradation,\
                                                                                                           rime=rime,\
                                                                                                           attributive='NoAttr',\
                                                                                                           pos=pos,\
                                                                                                           case2=case,\
                                                                                                           number=number, \
                                                                                                           grade=grade,\
                                                                                                           soggi=soggi)
                                                                msgs = Feedbackmsg.objects.filter(msgid=f.msgid)
                                                                if msgs:
                                                                    f2.messages.add(msgs[0])
                                                                else : print "No messages found:", f.msgid														
                                                                f2.save()
                                    if f.pos == "N":
                                        for case in f.case:
                                            # Essive: no number inflection
                                            if case == "Ess":
                                                number="empty"
                                                self.insert_feedback(cursor,pos,stem,diphthong,gradation,rime,soggi,'Ess',number)
                                                
                                                f2=Feedback.objects.get(stem=stem,\
                                                                        diphthong=diphthong,\
                                                                        gradation=gradation,\
                                                                        rime=rime,\
                                                                        case2='Ess',\
                                                                        number=number,\
                                                                        pos=pos,\
                                                                        soggi=soggi)
                                                msgs = Feedbackmsg.objects.filter(msgid=f.msgid)
                                                if msgs:
                                                    f2.messages.add(msgs[0])
                                                else : print "No messages found:", f.msgid
                                                f2.save()
                                                continue
                                            else:
                                                for number in f.number:
                                                    self.insert_feedback(cursor,pos,stem,diphthong,gradation,rime,soggi,case,number)
                                                    
                                                    f2=Feedback.objects.get(stem=stem,\
                                                                            diphthong=diphthong,\
                                                                            gradation=gradation,\
                                                                            rime=rime,\
                                                                            pos=pos,\
                                                                            case2=case,\
                                                                            number=number, \
                                                                            soggi=soggi)
                                                    
                                                    msgs = Feedbackmsg.objects.filter(msgid=f.msgid)
                                                    if msgs:
                                                        f2.messages.add(msgs[0])
                                                    else : print "No messages found:", f.msgid
                                                    f2.save()

                                                    


            if f.pos == "V":
                for stem in f.stem:
                    for diphthong in f.diphthong:
                        for soggi in f.soggi:                                                           
                            for personnumber in f.personnumber:
                                for tense in f.tense:
                                    for mood in f.mood:
                                        
                                        self.insert_feedback(cursor,pos,stem,diphthong,gradation,'empty',soggi,'empty','empty',personnumber,tense,mood)
                                        f2, created = Feedback.objects.get_or_create(stem=stem,\
                                                                                     diphthong=diphthong,\
                                                                                     gradation=gradation,\
                                                                                     soggi=soggi,\
                                                                                     tense=tense,\
                                                                                     pos=pos,\
                                                                                     mood=mood,\
                                                                                     personnumber=personnumber)
                                        messages = Feedbackmsg.objects.filter(msgid=f.msgid)
                                        if messages:										
                                            f2.messages.add(messages[0])
                                        else : print "No messages found:", f.msgid
                                        f2.save()
        cursor.close()
        connection.close()
        self.set_null()
