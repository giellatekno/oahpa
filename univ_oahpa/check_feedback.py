#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
USAGE
-----

Specify each file name as a separate argument


	python2.7 check_feedback.py ../sme/meta/messages_vasta.xml \
   						   	   ../sme/meta/messages_vasta.fin.xml \
   						   	   ../sme/meta/messages_vasta.sme.xml \
   						   	   ../sme/meta/messages_vasta.eng.xml \
   						   	   ../sme/meta/messages_vasta.swe.xml

Script will check all permutations of these files to figure out which msgids
are missing from one or many, missing items are printed to stderr (for
inclusion in error log), and calculation in progress is printed to stdout.

"""

from xml.dom import minidom as _dom
import sys
import re
import string
import codecs
import operator
from itertools import product

from django.utils.encoding import force_unicode

def fix_encoding(s):
	try:
		s = s.decode('utf-8')
	except:
		pass
	
	return force_unicode(s)

try:
	from collections import OrderedDict
except ImportError:
	from conf.ordereddict import OrderedDict

def chunks(l, n):
	""" Yield successive n-sized chunks from l.
	"""
	for i in xrange(0, len(l), n):
		yield l[i:i+n]

def get_attrs(item, attr_names):
	""" For an object, get attributes from a list of attributes.
	"""
	vals = []
	for attr in attr_names:
		val = item.__getattribute__(attr)
		if val:
			vals.append(fix_encoding(val))
		else:
			vals.append('')
	return vals

def render_kwargs(D):
	lines = []
	for k, vs in D.iteritems():
		line = ' %s = %s ' % (k, ', '.join(vs))
		lines.append(line)
	
	return '\n'.join(lines)

def read_messages(infiles):

	file_sets = {}
	for infile in infiles:
		xmlfile = file(infile)
		tree = _dom.parse(infile)
		lex = tree.getElementsByTagName("messages")[0]
		lang = lex.getAttribute("xml:lang")		

		msg_ids = set()
		for el in tree.getElementsByTagName("message"):
			msg_ids.add(el.getAttribute("id"))

		file_sets[infile] = msg_ids
	
	from itertools import permutations
	total_differences = set()
	for set1, set2 in permutations(file_sets.items(), 2):
		diff = set1[1] ^ set2[1]
		print >> sys.stdout, 'Symmetric distance in:'
		print >> sys.stdout, '  %s' % set1[0] 
		print >> sys.stdout, '  %s' % set2[0]
		print >> sys.stdout, ''
		print >> sys.stdout, '  %s' % ', '.join(diff)
		print >> sys.stdout, ''
		print >> sys.stdout, ''
		for a in diff:
			total_differences.add(a)

	if len(list(total_differences)) > 0:
		print >> sys.stderr, ' ! Missing feedback messages in one or many files:'
		for a in list(total_differences):
			print >> sys.stderr, '    ' + a
			missing_files = [f for f, _is in file_sets.items() if a not in _is]
			print >> sys.stderr, '    ' + ', '.join(missing_files)
		print >> sys.stderr, ''
	else:
		print >> sys.stdout, " * No asymmetricalities between feedback files"
	


	
	# print reduce(lambda _s, __s: _s ^ __s, file_sets.values())
	
if __name__ == "__main__":
	filenames = sys.argv[1::]
	read_messages(filenames)

