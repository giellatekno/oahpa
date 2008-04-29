#! /usr/bin/env python -w
# -*- coding: utf-8 -*- 

import sys
import re
import os, subprocess as su
from xml.dom import minidom as _dom
import getopt
from optparse import OptionParser


parser = OptionParser()

parser.add_option("-f", "--file", dest="infile",
                  help="lexicon file name")
parser.add_option("-b", "--book", dest="book",
                  help="book name")
parser.add_option("-l", "--lemma", dest="lemma",
                  help="Lemma string")
parser.add_option("-v", "--valency", dest="valency",
                  help="Valency class")
parser.add_option("-s", "--semantics", dest="semclass",
                  help="Semantic class")
parser.add_option("-t", "--stem", dest="stemclass",
                  help="Stem class")
parser.add_option("-d", "--dialect", dest="dialect",
                  help="Dialect class")
parser.add_option("-a", "--all", dest="print_all",
                  action="store_true", default=False,
                  help="print the whole entry, not just lemma")

(options, args) = parser.parse_args()

 
infile = "/Users/saara/ped/sme/xml/verbs.xml"
xmlfile=file(infile)
tree = _dom.parse(infile)
#print tree.toprettyxml(' ')
for e in tree.getElementsByTagName("entry"):

    if options.book:
        s=e.getElementsByTagName("sources")[0]
        for b in  s.getElementsByTagName("book"):
            if b.getAttribute("name").encode('utf8') == options.book:                
                if options.print_all:
                    print e.toxml()
                    #raw_input()
                    #break
                else:
                    ltext=e.getElementsByTagName("lemma")[0].firstChild.data
                    print ltext

    if options.lemma:
        ltext=e.getElementsByTagName("lemma")[0].firstChild.data
        if ltext and ltext == options.lemma:
            if options.print_all:
                print e.toxml()
            else:
                print ltext
                    
    if options.valency:
        v=e.getElementsByTagName("valency")[0]
        for b in v.getElementsByTagName("val"):
            if b.getAttribute("class").encode('utf8') == options.valency:
                if options.print_all:
                    print e.toxml()
                else:
                    ltext=e.getElementsByTagName("lemma")[0].firstChild.data
                    print ltext

    if options.semclass:
        s=e.getElementsByTagName("semantics")[0]
        for b in  s.getElementsByTagName("sem"):
            if b.getAttribute("class").encode('utf8') == options.semclass:
                if options.print_all:
                    print e.toxml()
                else:
                    ltext=e.getElementsByTagName("lemma")[0].firstChild.data
                    print ltext
    if options.stemclass:
        s=e.getElementsByTagName("stem")[0]
        if s.getAttribute("class").encode('utf8') == options.stemclass:
            if options.print_all:
                print e.toxml()
            else:
                ltext=e.getElementsByTagName("lemma")[0].firstChild.data
                print ltext

    if options.dialect:
        s=e.getElementsByTagName("dialect")[0]
        if s.getAttribute("class").encode('utf8') == options.dialect:
            if options.print_all:
                print e.toxml()
            else:
                ltext=e.getElementsByTagName("lemma")[0].firstChild.data
                print ltext
                    
  

"""
p=ParserCreate('utf-8')

def start_element(name, attrs):
    if name=="entry"

p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data


p.ParseFile(xmlfile)
"""

