# -*- coding: utf-8 -*-
from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import *
from drill.models import *
from xml.dom import minidom as _dom
from optparse import OptionParser
from django.db.models import Q
import sys
import re
import codecs
from ling import Paradigm
from feedback_install import Feedback
from sahka_install import Sahka
from extra_install import Extra
from questions_install import Questions
from words_install import Words

parser = OptionParser()

parser.add_option("-b", "--db", dest="add_db",
                  action="store_true", default=False,
                  help="Used for adding tag infoformation to database")
parser.add_option("-c", "--comments", dest="commentfile",
                  help="XML-file for comments")
parser.add_option("-d", "--dialect", dest="dialect",
                  help="Dialect used in feedback messages")
parser.add_option("-e", "--feedbackfile", dest="feedbackfile",
                  help="XML-file for feedback")
parser.add_option("-f", "--file", dest="infile",
                  help="lexicon file name")
parser.add_option("-g", "--grammarfile", dest="grammarfile",
                  help="XML-file for grammar defaults for questions")
parser.add_option("-i", "--links", dest="linkfile",
                  help="Text file for grammarlinks")
parser.add_option("-k", "--sahka", dest="sahkafile",
                  help="XML-file for Dialogues")
parser.add_option("-l", "--places", dest="placenamefile",
                  action="store_true", default=False,
                  help="If placenames")
parser.add_option("-m", "--messagefile", dest="messagefile",
                  help="XML-file for feedback messages")
parser.add_option("-n", "--num", dest="numerals",
                  action="store_true", default=False,
                  help="Generate numerals")
parser.add_option("-p", "--pos", dest="pos",
                  help="Pos info")
parser.add_option("-q", "--questionfile", dest="questionfile",
                  help="XML-file that contains questions")
parser.add_option("-r", "--paradigmfile", dest="paradigmfile",
                  help="Generate paradigms")
parser.add_option("-s", "--sem", dest="semtypefile",
                  help="XML-file semantic subclasses")
parser.add_option("-t", "--tagfile", dest="tagfile",
                  help="List of tags and tagsets")
parser.add_option("-u", "--qid", dest="questionid",
                  help="delete question using id or text")
parser.add_option("-v", "--delete", dest="delete",
                  action="store_true", default=False,
                  help="delete words that do not appear in the lexicon file of certain pos")


(options, args) = parser.parse_args()

linginfo = Paradigm()
feedback = Feedback()
sahka = Sahka()
questions = Questions()
extra = Extra()
words = Words()

if options.tagfile:
    linginfo.handle_tags(options.tagfile, options.add_db)

if options.paradigmfile:
    linginfo.read_paradigms(options.paradigmfile, options.tagfile, options.add_db)

if options.questionid:
    questions.delete_question(options.questionid)
    sys.exit()
    
if options.questionfile and options.grammarfile:
    questions.read_questions(options.questionfile,options.grammarfile)
    sys.exit()

if options.grammarfile:
    questions.read_grammar(options.grammarfile)
    sys.exit()
    
if options.semtypefile:
    extra.read_semtypes(options.semtypefile)
    sys.exit()

if options.feedbackfile:
    if options.pos and options.dialect:
        feedback.read_feedback(options.feedbackfile, options.pos, options.dialect, options.messagefile)
        sys.exit()

if options.numerals:
    linginfo.generate_numerals()
    sys.exit()

if options.messagefile:
    questions.read_messages(options.messagefile)
    sys.exit()

if options.commentfile:
    extra.read_comments(options.commentfile)
    sys.exit()

if options.sahkafile:
    sahka.read_dialogue(options.sahkafile)
    sys.exit()

if options.linkfile:
    extra.read_address(options.linkfile)
    sys.exit()

if options.infile:
    words.install_lexicon(options.infile,options.delete,options.paradigmfile,options.placenamefile)
    sys.exit()

