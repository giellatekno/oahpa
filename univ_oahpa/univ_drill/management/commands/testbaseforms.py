from django.core.management.base import BaseCommand, CommandError

# from_yaml(cls, loader, node)

from optparse import make_option

import sys


# # # 
# 
#  Command class
#
# # #

def testbaseforms(tfilter=False, tag_string=False):
	from univ_drill.models import Form
	from django.db.models import Count

	if tag_string:
		missing = Form.objects.filter(tag__string=tag_string)
	else:
		missing = Form.objects.all()
	
	def fmtform(f):
		fs = {
			'word__lemma': f.word.lemma,
			'fullform': f.fullform,
			'tag__string': f.tag.string,
		}

		return "%(word__lemma)s\t%(fullform)s\t%(tag__string)s" % fs
	
	for m in missing.iterator():
		s = "Form:     " + fmtform(m)
		try:
			bf = m.getBaseform()
		except Exception, e:
			bf = False
			print e

		if bf:
			b = "Baseform: " + fmtform(bf)
		else:
			b = "Baseform: MISSING."

		print >> sys.stdout, s.encode('utf-8')
		print >> sys.stdout, b.encode('utf-8') + '\n'

class Command(BaseCommand):
	args = '--tagelement'
	help = """
	Strips tags of an element and then merges them all.
	"""
	option_list = BaseCommand.option_list + (
		make_option("-t", "--tagstring", dest="tag_string", default=False,
						  help="Tag element to search for"),
		
		# TODO: question iterations count
	)

	def handle(self, *args, **options):
		import sys, os

		tag_string = options['tag_string']
		
		testbaseforms(tag_string=tag_string)



