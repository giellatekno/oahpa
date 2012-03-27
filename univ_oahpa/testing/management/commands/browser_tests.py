from django.core.management.base import BaseCommand, CommandError

# from_yaml(cls, loader, node)

from optparse import make_option

import sys

from univ_drill.models import Tag

import requests

HOST = 'http://oahpa.uit.no/univ_oahpa'

def test_morfas():
	""" Tests here make sure that we at least get a question set for all
	possible options in Leksa, Morfa-S, Morfa-C and Numra. """
	from univ_drill.forms import CASE_CHOICES
	from itertools import product
	from operator import itemgetter

	test_keys = {
		'/univ_oahpa/morfas/s/': { 	
				# form value, values to iterate
				'case': map(itemgetter(0), CASE_CHOICES),
				'bisyllabic': [True],
				'trisyllabic': [False],
				'contracted': [False],
				'book': ['all'],
		},
		'/univ_oahpa/morfas/v/': {
				'vtype': '',
				'bisyllabic': [True],
				'trisyllabic': [False],
				'contracted': [False],
				'book': ['all'],
		},
		'/univ_oahpa/morfas/a/': {
				'adjcase': '',
				'grade': '',
				'bisyllabic': [True],
				'trisyllabic': [False],
				'contracted': [False],
				'book': ['all'],
		},
		'/univ_oahpa/morfas/p/': {
				'pron_type': '',
				'pron_case': '',
				'bisyllabic': [True],
				'trisyllabic': [False],
				'contracted': [False],
				'book': ['all'],
		},
		'/univ_oahpa/morfas/l/': {
				'num_bare': '',
				'num_level': '',
				'num_type': '',
				'bisyllabic': [True],
				'trisyllabic': [False],
				'contracted': [False],
				'book': ['all'],
		},
	}

	for url, parameter_set in test_keys.iteritems():
		path = {
			'host': HOST,
			'path': url,
		}
		print path
		# r = requests.get('%(host)s%(path)' % path)
		# assert r.status_code == '200'

		parameters = [(key, vals) for key, vals in parameter_set.items()]
		keys, values = [a[0] for a in parameters], [a[1] for a in parameters]

		value_iterations = product(*values)

		for iter_ in value_iterations:
			print zip(keys, iter_)


	return True


# # # 
# 
#  Command class
#
# # #

class Command(BaseCommand):
	args = '--tagelement'
	help = """
	Strips tags of an element and then merges them all.
	"""
	option_list = BaseCommand.option_list + (
		make_option("-t", "--tagelement", dest="tagelement", default=False,
						  help="Tag element to search for"),
		make_option("-d", "--dryrun", dest="dryrun", default="True",
						  help="List tags matching element instead of merging"),
		
		# TODO: question iterations count
	)

	def handle(self, *args, **options):
		import sys, os

		test_morfas()



