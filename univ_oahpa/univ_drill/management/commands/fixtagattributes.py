from django.core.management.base import BaseCommand, CommandError

# from_yaml(cls, loader, node)

from optparse import make_option

import sys


# # # 
# 
#  Command class
#
# # #

def fixtags():
	from univ_drill.models import Tag
	tags = Tag.objects.all()

	print 'Fixing attributes...'
	for tag in tags:
		print tag.string
		tag.fix_attributes()
		tag.save()
	
	print 'Done'

class Command(BaseCommand):
	help = """
	Sometimes during the install process attributes on tag objects are not
	properly set. This corrects that issue.
	"""
	option_list = BaseCommand.option_list

	def handle(self, *args, **options):
		fixtags()

