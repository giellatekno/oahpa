# -*- coding: utf-8 -*-
from settings import *
from drill.models import *
from django.db.models import Q
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
                    t, created = Links.objects.get_or_create(name=link,language=lang)
                    t.address=address
                    t.save()
                    links.append(link)
        linkobjects = Links.objects.all()
        for l in linkobjects:
            if l.name not in set(links):
                print l.name
                l.delete()

    # Installs the semantic superclasses
    # defined in sme/xml/semantic_sets.xml
    def read_semtypes(self, infile):

        xmlfile=file(infile)
        tree = _dom.parse(infile)

        for el in tree.getElementsByTagName("subclasses"):
            semclass=el.getAttribute("class")
            s, created = Semtype.objects.get_or_create(semtype=semclass)
            for el2 in el.getElementsByTagName('sem'):
               subclass  = el2.getAttribute("class")
               for w in Word.objects.filter(Q(semtype__semtype=subclass) & ~Q(semtype__semtype=semclass)):
                   w.semtype.add(s)
                   w.save()
               for w in Wordnob.objects.filter(Q(semtype__semtype=subclass) & ~Q(semtype__semtype=semclass)):
                   w.semtype.add(s)
                   w.save()


