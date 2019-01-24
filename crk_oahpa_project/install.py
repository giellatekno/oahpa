# -*- coding: utf-8 -*-
import settings
from os import environ
import os, sys
print " * Correcting paths"
cur_path = os.getcwd()
parent_path = '/' + '/'.join([a for a in cur_path.split('/') if a][0:-1]) + '/'
sys.path.insert(0, parent_path)
environ['DJANGO_SETTINGS_MODULE'] = 'crk_oahpa.settings'

settings.DEBUG = False

from crk_drill.models import *
from optparse import OptionParser, make_option
import sys
from ling import Paradigm
from words_install import Words
from extra_install import Extra
from feedback_install import Feedback_install
from questions_install import Questions
from sahka_install import Sahka  # added by Heli

# TODO: option for oa="yes" only, for crk_
# ota lemma jos on name="oahpa"
# jos on lemma, niin ota käännös jos on oa="yes"

OPTION_LIST = (
	make_option("-a", "--append-words", dest="append",
					  action="store_true", default=False,
					  help="Add wordforms to words without deleting existing wordforms"),
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
	make_option("-g", "--grammarfile", dest="grammarfile",
					  help="XML-file for grammar defaults for questions"),
	make_option("-i", "--links", dest="linkfile",
					  help="Text file for grammarlinks"),
	make_option("-s", "--sem", dest="semtypefile",
					  help="XML-file semantic subclasses"),
	make_option("-t", "--tagfile", dest="tagfile",
					  help="List of tags and tagsets"),
	make_option("-l", "--language", dest="language",
					  help="iso code for language of install"),
	make_option("-m", "--messagefile", dest="messagefile",
                  help="XML-file for feedback messages"),
	make_option("-q", "--questionfile", dest="questionfile",
	              help="XML-file that contains questions"),
	make_option("-k", "--sahka", dest="sahkafile",
                  help="XML-file for Dialogues"),  # added
	make_option("-w", "--wid", dest="wordid",
					  help="delete word using id or lemma"),
	make_option("-p", "--pos", dest="pos",
					  help="pos of the word"),
	make_option("-r", "--paradigmfile", dest="paradigmfile",
					  help="Generate paradigms"))

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

	linginfo = Paradigm()  # class Paradigm in ling.py
	words = Words() # class Words in words_install.py
	extra = Extra()
	sahka = Sahka() # added by Heli
	feedback = Feedback_install()
	questions = Questions()

	if options.tagfile:
		linginfo.handle_tags(options.tagfile, options.add_db)  # install tags

	if options.paradigmfile:
		linginfo.read_paradigms(options.paradigmfile, options.tagfile, options.add_db, pos=options.pos)   # install paradigms

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

	if options.sahkafile:
		sahka.read_dialogue(options.sahkafile)
		sys.exit()

	if options.feedbackfile and options.infile:
	    if options.append:
	        append_only = True
	    else:
	        append_only = False
	    feedback.read_feedback(options.feedbackfile,options.infile, append=append_only)
	    sys.exit()

	if options.linkfile:
		extra.read_address(options.linkfile)
		sys.exit()

	if options.infile:

		if options.append:
			append_only = True
		else:
			append_only = False

		words.install_lexicon(infile=options.infile,
								linginfo=linginfo,
								delete=options.delete,
								paradigmfile=options.paradigmfile,
								append_only=append_only)
		sys.exit()


if __name__ == "__main__":
	main(opts=False)
