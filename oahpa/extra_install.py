# -*- coding: utf-8 -*-
from settings import *
from drill.models import *
from django.db.models import Q
import sys
import re
import string
import codecs


class Extra:

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
