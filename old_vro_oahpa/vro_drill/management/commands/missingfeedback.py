from django.core.management.base import BaseCommand, CommandError

# from_yaml(cls, loader, node)

from optparse import make_option

import sys


# # # 
# 
#  Command class
#
# # #

def findmissing(tfilter=False, count=0):
	from univ_drill.models import Form
	from django.db.models import Count

	missing = Form.objects.filter()\
							.annotate(fc=Count('feedback'))\
							.filter(fc=0)\
							.values('word__lemma', 'fullform', 'tag__string')
	
	for m in missing.iterator():
		s = "%(word__lemma)s\t%(fullform)s\t%(tag__string)s" % m
		try:
			s = s.encode('utf-8')
		except:
			pass
		print >> sys.stdout, s

class Command(BaseCommand):
	args = '--tagelement'
	help = """
	Search for word forms with missing feedback messages
	"""
	option_list = BaseCommand.option_list + (
		make_option("-t", "--tagelement", dest="tagelement", default=False,
						  help="Tag element to search for"),
	)

	def handle(self, *args, **options):
		import sys, os

		tag_element = options['tagelement']
		dry_run = options['dryrun']
		
		findmissing()


