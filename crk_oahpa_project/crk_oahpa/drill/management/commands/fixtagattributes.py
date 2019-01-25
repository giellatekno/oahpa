# -*- encoding: utf-8 -*-
from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')

﻿from django.core.management.base import BaseCommand, CommandError

# from_yaml(cls, loader, node)

from optparse import make_option

import sys


# # #
#
#  Command class
#
# # #

def fixtags():
	Tag = oahpa_module.drill.models.Tag
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
