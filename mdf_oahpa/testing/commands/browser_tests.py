from django.core.management.base import BaseCommand, CommandError

# from_yaml(cls, loader, node)

from optparse import make_option

import sys

from mdf_drill.models import Tag

import requests

HOST = 'http://oahpa.uit.no'

def test_morfas():
	""" Tests here make sure that we at least get a question set for all
	possible options in Leksa, Morfa-S, Morfa-C and Numra. """
	from mdf_drill.forms import (CASE_CHOICES, 
									VTYPE_CHOICES, 
									ADJCASE_CHOICES, 
									ADJEX_CHOICES)
	
	from itertools import product
	from operator import itemgetter

	pass_count = 0
	fail_count = 0

	test_keys = {
		'/mdf_oahpa/morfas/': { 	
				# form value, values to iterate
				'case': map(itemgetter(0), CASE_CHOICES),
				'bisyllabic': [True],
				'trisyllabic': [False],
				'contracted': [False],
				'book': ['all'],
		},
		'/mdf_oahpa/morfas/v/': {
				'vtype': map(itemgetter(0), VTYPE_CHOICES),
				'bisyllabic': [True],
				'trisyllabic': [False],
				'contracted': [False],
				'book': ['all'],
		},
		'/mdf_oahpa/morfas/a/': {
				'adjcase': map(itemgetter(0), ADJCASE_CHOICES),
				'grade': map(itemgetter(0), ADJEX_CHOICES),
				'bisyllabic': [True],
				'trisyllabic': [False],
				'contracted': [False],
				'book': ['all'],
		},
		# '/mdf_oahpa/morfas/p/': {
				# 'pron_type': '',
				# 'pron_case': '',
				# 'bisyllabic': [True],
				# 'trisyllabic': [False],
				# 'contracted': [False],
				# 'book': ['all'],
		# },
		# '/mdf_oahpa/morfas/l/': {
				# 'num_bare': '',
				# 'num_level': '',
				# 'num_type': '',
				# 'bisyllabic': [True],
				# 'trisyllabic': [False],
				# 'contracted': [False],
				# 'book': ['all'],
		# },
	}

	count = 0
	failed_url_params = []

	for url, parameter_set in test_keys.iteritems():
		path = {
			'host': HOST,
			'path': url,
		}
		uri = '%(host)s%(path)s' % path
		print 'trying: %s' % uri
		count += 1
		r = requests.get(uri)
		try:
			assert r.status_code == 200
			print 'status: %d' % r.status_code
			print 'testing form values ... '
			pass_count += 1
			clear_for_subtest = True
		except AssertionError:
			print 'Error %d on %s' % (r.status_code, uri)
			fail_count += 1
			clear_for_subtest = False
			failed_url_params.append((uri,))
			continue

		parameters = [(key, vals) for key, vals in parameter_set.items()]
		keys, values = [a[0] for a in parameters], [a[1] for a in parameters]

		value_iterations = product(*values)

		for iter_ in value_iterations:
			post_data = zip(keys, iter_)
			print '  trying:'
			for k, v in post_data:
				print '    %s - %s' % (k, v)

			if clear_for_subtest:
				count += 1
				u = requests.post(uri, data=dict(post_data))
			else:
				print '    SKIP'
				fail_count += 1
				continue

			try:
				assert u.status_code == 200
				print '    pass: %d' % u.status_code
				pass_count += 1
			except AssertionError:
				print '    FAIL: %d' % u.status_code
				fail_count += 1
				failed_url_params.append((uri,dict(post_data)))
				continue



	print 'Successful: %d/%d' % (pass_count, count)
	print 'FAILED: %d/%d' % (fail_count, count)
	
	print 'Tests failed:'
	for k in failed_url_params:
		print k
		# print '  %s: %s' % (k, repr(v))

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



