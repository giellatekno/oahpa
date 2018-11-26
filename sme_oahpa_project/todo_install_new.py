#!/usr/bin/env python
# -*- coding: utf-8 -*-
import settings
from os import environ
import os, sys
print " * Correcting paths"	
cur_path = os.getcwd()
parent_path = '/' + '/'.join([a for a in cur_path.split('/') if a][0:-1]) + '/'
sys.path.insert(0, parent_path)
# why use the smaoahpa settings?
environ['DJANGO_SETTINGS_MODULE'] = 'smaoahpa.settings'

settings.DEBUG = False

from smadrill.models import *
from optparse import OptionParser, make_option
import sys
from ling_new import Paradigm
# there is no words_install_new class, yet a words_install_test
from words_install_new import Words
from extra_install import Extra
from feedback_install import Feedback_install
from pronouns_install import Pronouns
from questions_install import Questions

# TODO: option for oa="yes" only, for sma
# ota lemma jos on name="oahpa"
# jos on lemma, niin ota käännös jos on oa="yes"

OPTION_LIST = (
	make_option("-b", "--db", dest="add_db",
					  action="store_true", default=False,
					  help="Used for adding tag infoformation to database"),
	make_option("-c", "--comments", dest="commentfile",
					  help="XML-file for comments"),
	make_option("-d", "--delete", dest="delete",
					  action="store_true", default=False,
					  help="delete words that do not appear in the lexicon file of certain pos"),
	make_option("-e", "--feedbackfile", dest="feedbackfile",
					  help="XML-file for feedback"),
	make_option("-f", "--file", dest="infile",
					  help="lexicon file name"),
	make_option("-P", "--pronouns", dest="pronounfile",
					  help="lexicon file name"),
	make_option("-g", "--grammarfile", dest="grammarfile",
					  help="XML-file for grammar defaults for questions"),
	make_option("-s", "--sem", dest="semtypefile",
					  help="XML-file semantic subclasses"),
	make_option("-t", "--tagfile", dest="tagfile",
					  help="List of tags and tagsets", default=False),
	make_option("-m", "--messagefile", dest="messagefile",
                  help="XML-file for feedback messages"),
	make_option("-q", "--questionfile", dest="questionfile",
	              help="XML-file that contains questions"),
	make_option("-w", "--wid", dest="wordid",
					  help="delete word using id or lemma"),
	make_option("-p", "--pos", dest="pos",
					  help="pos of the deleted word"),
	make_option("-r", "--paradigmfile", dest="paradigmfile",
					  help="Generate paradigms", default=False))

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	option_list = BaseCommand.option_list + OPTION_LIST
	help = 'Help text goes here'
		
	def handle(self, **options):
		main(opts=option_list)

def main(opts):
	if opts:
		parser = OptionParser(option_list=opts)
	else:
		parser = OptionParser(option_list=OPTION_LIST)
	
	(options, args) = parser.parse_args()

	linginfo = Paradigm()
	words = Words()
	extra = Extra()
	feedback = Feedback_install()
	pronouns = Pronouns()
	questions = Questions()
	
	if options.tagfile:
		linginfo.handle_tags(options.tagfile, options.add_db)

	if options.paradigmfile:
		linginfo.read_paradigms(options.paradigmfile, options.tagfile, options.add_db)

	if options.wordid:
		words.delete_word(options.wordid,options.pos)
		sys.exit()

	if options.questionfile and options.grammarfile:
	    questions.read_questions(options.questionfile,options.grammarfile)
	    sys.exit()
	
	if options.semtypefile:
		extra.read_semtypes(options.semtypefile)
		sys.exit()
	
	if options.messagefile:
	    feedback.read_messages(options.messagefile)
	    sys.exit()

	if options.feedbackfile and options.infile:
	    feedback.read_feedback(options.feedbackfile,options.infile)
	    sys.exit()
	
	if options.pronounfile:
		pronouns.install_lexicon(infile=options.pronounfile,
							linginfo=linginfo,
							delete=options.delete,
							paradigmfile=options.paradigmfile)
		sys.exit()

	if options.infile:
		words.install_lexicon(infile=options.infile,linginfo=linginfo,delete=options.delete,paradigmfile=options.paradigmfile)
		sys.exit()


if __name__ == "__main__":
	main(opts=False)
