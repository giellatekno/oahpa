from django.core.management.base import BaseCommand, CommandError

# from_yaml(cls, loader, node)

from optparse import make_option
from django.utils.encoding import force_unicode

import sys


# # # 
# 
#  Command class
#
# # #

def testbaseforms(tfilter=False, tag_string=False):
	from drill.models import Form
	from django.db.models import Count

	if tag_string:
		missing = Form.objects.filter(tag__string=tag_string)
	else:
		missing = Form.objects.all()
	
	missing = missing.only('word__lemma', 'fullform', 'tag__string')
	
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

		print >> sys.stdout, s
		print >> sys.stdout, b + '\n'

class Command(BaseCommand):
	args = '--tagelement'
	help = """
	Search through the lexicon and test .getBaseform() on each form.
	Alternatively specify a tag (-t/--tagstring) to filter forms by.

	View all baseforms:
		python manage.py testbaseforms
	
	View only A+Attr baseforms:
		python manage.py testbaseforms -t A+Attr | grep Baseform | grep A+Attr 

	View only A+Attr, find baseforms returning A+Attr instead of A+Sg+Nom
		python manage.py testbaseforms -t A+Attr | grep Baseform | grep A+Attr 
	
	Also, search for MISSING, which will reveal places where .getBaseform can't
	actually return anything.
	"""
	option_list = BaseCommand.option_list + (
		make_option("-t", "--tagstring", dest="tag_string", default=False,
						  help="Tag element to search for"),
	)

	def handle(self, *args, **options):
		import sys, os

		tag_string = options['tag_string']
		
		testbaseforms(tag_string=tag_string)



