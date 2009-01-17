# -*- coding: utf-8 -*-
from settings import *
from drill.models import *
from django.db.models import Q
from xml.dom import minidom as _dom
import sys
import re
import string
import codecs


class Extra:

    # Installs links to the grammatical information under giellatekno.
    # The link list appears to the upper right corner of the oahpa-pages.
    # File sme/src/grammarlinks.txt
    def read_address(self,linkfile):

        addressObj=re.compile(r'^(?P<linkString>[^\s]+)\s*(?P<addressString>[^\s]+)\s*$', re.U)
        linkfileObj = codecs.open(linkfile, "r", "utf-8" )
        links = []
        while True:
            line = linkfileObj.readline()
            if not line: break
            if not line.strip(): continue
            matchObj=addressObj.search(line) 
            if matchObj:
                address = matchObj.expand(r'\g<addressString>')
                link = matchObj.expand(r'\g<linkString>')
                if link and address:
                    lang="sme"
                    if address.count(".nno.") > 0:
                        lang = "no"
                    t, created = Grammarlinks.objects.get_or_create(name=link,language=lang)
                    t.address=address
                    t.save()
                    links.append(link)
        linkobjects = Grammarlinks.objects.all()
        for l in linkobjects:
            if l.name not in set(links):
                print l.name
                l.delete()

    #The comments presented to the user after completing the game.
    def read_comments(self, commentfile):
        xmlfile=file(commentfile)
        tree = _dom.parse(commentfile)        

        comments_el = tree.getElementsByTagName("comments")[0]
        lang = comments_el.getAttribute("xml:lang")

        comments = Comment.objects.filter(lang=lang)
        for c in comments:
            c.delete()
        for el in comments_el.getElementsByTagName("comment"):
            level = el.getAttribute("level")
            for com in el.getElementsByTagName("text"):
                text = com.firstChild.data
                print text
                comment, created = Comment.objects.get_or_create(lang=lang, comment=text, level=level)
                comment.save()

    # Installs the semantic superclasses
    # defined in sme/xml/semantic_sets.xml
    def read_semtypes(self, infile):

        xmlfile=file(infile)
        tree = _dom.parse(infile)

        for el in tree.getElementsByTagName("subclasses"):
            semclass=el.getAttribute("class")
            print semclass
            s, created = Semtype.objects.get_or_create(semtype=semclass)
            for el2 in el.getElementsByTagName('sem'):
               subclass  = el2.getAttribute("class")
               print "\t" + subclass
               for w in Word.objects.filter(Q(semtype__semtype=subclass) & ~Q(semtype__semtype=semclass)):
                   w.semtype.add(s)
                   w.save()
               for w in Wordnob.objects.filter(Q(semtype__semtype=subclass) & ~Q(semtype__semtype=semclass)):
                   w.semtype.add(s)
                   w.save()


