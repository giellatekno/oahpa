from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

import sys

# # #
#
#  Command class
#
# # #

word_attrs = [
	"id",
	"lemma",
	"pos",
	"wordclass",
	"language",
	"presentationform",
	"stem",
	"valency",
	"hid",
	"diphthong",
	"gradation",
	"rime",
	"attrsuffix",
	"compsuffix",
	"soggi",
	"compare",
	"frequency",
	"geography",
	"tcomm",
]

###	"semtype",
###	"dialects",
###	"source",
### TODO: translations

def printword(word_key):
	Word = oahpa_module.drill.models.Word
	ws = Word.objects.filter(lemma=word_key)

	if ws.count() == 0:
		print >> sys.stderr, "No words found for '%s'." % word_key

	for w in ws:
		forms = w.form_set.all()

		for attr in word_attrs:
			v = w.__getattribute__(attr)
			if v:
				print "%s:\t%s" % (attr, v)

		print 'semtypes: %s' % ', '.join(w.semtype.all().values_list('semtype', flat=True))
		print 'dialects: %s' % ', '.join(w.dialects.all().values_list('dialect', flat=True))
		print 'sources: %s' % ', '.join(w.source.all().values_list('name', flat=True))
		print 'Wordforms: %d forms generated\n' % forms.count()
		for form in w.form_set.all():
			dialects = form.dialects.all().values_list('dialect', flat=True)
			if len(dialects) > 0:
				dialects = ', '.join(dialects)
			else:
				dialects = ""
			print "\t%s\t\t%s\t\t%s" % (form.tag.string, form.fullform, dialects)

		print
		for translation in w.wordtranslation_set.all():
			print "\t%s - %s" % (translation.language, translation.definition)

		print '\nQuestion membership:'
		question_memberships = w.wordqelement_set.all().values_list(
			'qelement__question__qid',
			'qelement__question__question__qid',
			'qelement__question__qatype')

		ordered_qms = []
		for q_m in question_memberships:
			q_ms = ' - '.join([q for q in q_m[::-1] if q])
			ordered_qms.append(q_ms)

		ordered_qms.sort()
		ordered_qms.reverse()
		for q_ms in ordered_qms:
			print '\t' + q_ms

		print "--"


class Command(BaseCommand):
	args = '--word'
	help = """
	Print all of the relations for a word by the word's lemma (-w)
	"""
	option_list = BaseCommand.option_list + (
		make_option("-w", "--word", dest="word_key", default=False,
						  help="Tag element to search for"),
	)

	def handle(self, *args, **options):
		import sys, os

		printword(options['word_key'])
