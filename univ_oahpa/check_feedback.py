# -*- coding: utf-8 -*-
"""

 * XML Structure
 * Install script structure
 * Future?

FEEDBACK AND XML-SOURCE
-------- --- ----------

Feedback message files have the following structure:

	<?xml version="1.0" encoding="utf-8"?>
	<messages xml:lang="fin"> 
		<message order="A" id="case1">WORDFORM has ... </message>  
		<message order="A" id="case2">WORDFORM has ... </message>  
		<message order="A" id="case3">WORDFORM has ... </message>  
		<message order="A" id="case4">WORDFORM has ... </message>  
		<message order="B" id="number1"> and is in singular.</message>  
		<message order="B" id="number2"> and is in plural.</message>  
	</messages>

In this case the id attribute corresponds to the message id, and the
order attribute corresponds to the order that the message will appear
in in the user interface. Orders are specified with the letters A-Z,
and if an order is not specified, it is assumed that this message will
come first, before A.

Nouns: attributes required: pos, soggi, stem, case/case2, number

	<l> nodes in messages.xml and n_smanob must match for
		pos, soggi, stem
	
	Remaining inflectional items, case and number, come from the tag.
				
	feedback_nouns.xml: 
	
	<feedback pos="N">
	  <stems>
		<l stem="2syll">
		  <msg pos="n">bisyllabic_stem</msg>
		</l>
		<l stem="3syll">
		  <msg pos="n">trisyllabic_stem</msg>
		</l>

		<l stem="3syll" soggi="a">
		  <msg case="Ill">soggi_a</msg>
		  <msg case="Ine">soggi_a</msg>
		  <msg case="Ela">soggi_a</msg>
		  <msg case="Com" number="Sg">soggi_a</msg>
		  <msg case="Ess">soggi_a</msg>
		  <note>daktarasse, vuanavasse, e/o > a</note>
		</l>
	 </stems>
	</feedback>
	
	
	n_smanob.xml:
	
	<e>
	  <lg>
		 <l margo="e" pos="n" soggi="e" stem="3syll">aagkele</l>
	  </lg>
	  { ... SNIP ... }
	</e>
	
Verbs: Mostly the same. <l/>s match for class, stem, pos
inflectional information from Tag object pertaining to mood, tense, personnumber.

FEEDBACK DATA STRUCTURE

Remember that this code runs once per word, and not on a huge set of words,
so it should ideally be returning only one Feedback object.

Feedback objects are then linked to Feedbackmsg objects, which contain
message IDs, such as soggi_o, class_1, which then link to Feedbacktext objects
which contain the corresponding messages in other languages.

Feedback objects should be linked to multiple Feedbackmsg items (typically, 3)
which individually contain class, syllable and umlaut information.

Feedback.messages.all()

INSTALL PROCESS
------- -------

The install process is invoked with a lexicon file and a feedback file: 

    python feedback_install.py -f word_file.xml --feedbackfile feedback_file.xml

The outcome of the install process is currently such that there is a Feedback
object in the database for each possible permutation of morphosyntactic
features, which correspond to both Word object attributes (morphophonology
mostly, rime, stem type, inflectional class, etc.) and Tag object attributes
(morphosyntactic mostly, person tense, number, etc.)

This results in many objects being generated, and as such the process may take
a long time depending on the kind of data being installed. There are several
optimizations in place, however: inserts are run in batch, not by the typical
Model.objects.create() method, and before this, all objects and database
relationships that need to be represented in these batch inserts are fetched,
with every query cached in python objects. At best, the script will run in 2
minutes, at worst, 30 minutes.

EDITING
-------

In order to add new morphosyntactic classes, there are several places that may
need to be checked. Usually it's a good idea to pick a feature that is similar
to the one being implemented, and search through the file. 

Some comments are marked with #NEW_ATTRIBUTES, so search through the file for
these for a hint at where to start.


FUTURE
------

Enterprising individuals who are willing to optimize more may consider altering
the model structure, such that Feedbackmsg objects are associated directly with
Form objects, saving the need to create tons of Feedback objects with all the
various permutations of morphosyntactic features.


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
		print >> sys.stderr, ''
	else:
		print >> sys.stdout, " * No asymmetricalities between feedback files"
	


	
	# print reduce(lambda _s, __s: _s ^ __s, file_sets.values())
	
if __name__ == "__main__":
	filenames = sys.argv[1::]
	read_messages(filenames)

