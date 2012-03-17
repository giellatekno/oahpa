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

from settings import *
from univ_drill.models import Feedback,Feedbackmsg,Feedbacktext,Dialect,Comment,Tag
from xml.dom import minidom as _dom
from django.db.models import Q
import sys
import re
import string
import codecs

from django.db import transaction
from itertools import product

class Entry:
	pass

stem_convert = {
	'2syll': '2syll',
	'3syll': '3syll',
	'bisyllabic': '2syll',
	'trisyllabic': '3syll',
	'contracted': 'Csyll',
	'Csyll': 'Csyll',
	'': '', # contracted : Csyll ?
}

class Feedback_install:


	def __init__(self):
		self.tagset = {}
		self.paradigms = {}
		self.obj_count = 0
		self.duplicate_count = 0
		self.dialects = ["KJ","GG"]
		self.created_objects_cache = {}

	def read_messages(self,infile):

		xmlfile=file(infile)
		tree = _dom.parse(infile)
		lex = tree.getElementsByTagName("messages")[0]
		lang = lex.getAttribute("xml:lang")		

		for el in tree.getElementsByTagName("message"):
			mid=el.getAttribute("id")
			order = ""
			order = el.getAttribute("order")
			message = el.firstChild.data
			print >> sys.stdout, message
			fm, created = Feedbackmsg.objects.get_or_create(msgid=mid)
			fm.save()

			fmtext, created=Feedbacktext.objects.get_or_create(language=lang,feedbackmsg=fm,order=order)
			fmtext.message=message
			fmtext.save()

	# NOTE: this silences some exceptions, so if something goes wrong, comment it out
	# @transaction.commit_manually
	def read_feedback(self, infile, wordfile):
		"""
			There are some longer comments below on how to alter this code.
			CTRL+F #NEW_ATTRIBUTES.
			
			General notes: changed 'empty' values to '', because this is completely
			fine in the database. The part of the code that reset 'empty' to ''
			was deleting some data, so it seems best to just set null from the beginning
			and keep in mind that filtering with val='' is different than filtering without
			val=''.
			
		"""

		# from django.db import connection
		print >> sys.stdout, infile
		print >> sys.stdout, wordfile

		wordfile=file(wordfile)
		wordtree = _dom.parse(wordfile)

		# Find out different values for variables.
		# Others can be listed, but soggi is searched at the moment.
		rimes={}
		gradations={}
		attrsuffixs={}
		compsuffixs={}
		soggis={}
		for el in wordtree.getElementsByTagName("l"):
			if el.getAttribute("rime"):
				rime = el.getAttribute("rime")
				if rime=="0": rime = ""
				rimes[rime] = 1
			if el.getAttribute("gradation"):
				gradation = el.getAttribute("gradation")
				gradations[gradation] = 1
			if el.getAttribute("attrsuffix"):
				attrsuffix = el.getAttribute("attrsuffix")
				if attrsuffix=="0": attrsuffix = "noattr"
				attrsuffixs[attrsuffix] = 1
			if el.getAttribute("compsuffix"):
				compsuffix = el.getAttribute("compsuffix")
				if compsuffix=="0": compsuffix = "nocomp"
				compsuffixs[compsuffix] = 1
			if el.getAttribute("soggi"):
				soggi = el.getAttribute("soggi")
				soggis[soggi] = 1
		
		soggis[''] = 1
		attrsuffixs["noattr"] = 1
		compsuffixs[""] = 1
		rimes[""] = 1
		
		#NEW_ATTRIBUTES
		# More with this search tag below.
		# New attributes should go here, with a list of all possible values.
		# Later in the code, these will all be iterated through in a factorial style, 
		# so note that adding things to these lists and the forloops further down
		# may result in big changes.
		
		# TODO: fetch these from the database
		# list(set(Tag.objects.filter(pos=pos).values_list('tense', flat=True)))

		diphthongs = ["yes","no"]
		stems = ["3syll", "2syll", "Csyll"]
		wordclasses = ['I', 'II', 'III', 'IV', 'V', 'VI']
		grades = ["Comp","Superl","Pos"]
		# Sma requires different cases
		cases = ["Nom", "Acc", "Gen", "Ill", "Loc", "Com", "Ess"]
		numbers = ["Sg","Pl"]
		tenses = ["Prs","Prt"]
		moods = ["Ind","Cond","Pot","Imprt"]
		personnumbers = ["Sg1","Sg2","Sg3","Du1","Du2","Du3","Pl1","Pl2","Pl3"]
		
		messages = []
		print >> sys.stdout, rimes.keys()
		print >> sys.stdout, soggis.keys()
		print >> sys.stdout, gradations.keys()
		print >> sys.stdout, compsuffixs.keys()
		print >> sys.stdout, attrsuffixs.keys()
		print >> sys.stdout, wordclasses
		print >> sys.stdout, grades
		print >> sys.stdout, cases
		print >> sys.stdout, numbers
		print >> sys.stdout, personnumbers
		
		print >> sys.stdout, diphthongs

		
		# Read the feedback file
		xmlfile=file(infile)
		tree = _dom.parse(infile)

		fb = tree.getElementsByTagName("feedback")[0]
		pos = fb.getAttribute("pos").capitalize()
		if pos:
			print  >> sys.stdout,"Deleting old feedbacks for pos", pos
			oldfs = Feedback.objects.filter(pos=pos).delete()			
		stem_messages = {}
		gradation_messages = {}

		if pos=="V":
			rimes[""] = 1
			diphthongs.append("")
		if pos=="Num":
			rimes[""] = 1
			diphthongs.append("")

		# cursor = connection.cursor()						

		wordforms = tree.getElementsByTagName("stems")[0]
		for el in wordforms.getElementsByTagName("l"):
			feedback = None
			stem =""
			diphthong =""
			rime =""
			gradation=""
			soggi =""
			attrsuffix =""
			wordclass = ""

			ftempl = Entry()

			ftempl.pos = pos
			ftempl.wordclass = ""

			if el.getAttribute("stem"):
				stem=el.getAttribute("stem")
				print >> sys.stdout, 'stem found: %s' % repr(stem)
				try:
					stem = stem_convert[stem]
				except:
					print >> sys.stderr, "Unknown value: %s" % stem
					sys.exit(2)
				
				if stem: ftempl.stem = [ stem ]
			if not stem:  ftempl.stem = stems
			
			if el.getAttribute("class"):
				wordclass=el.getAttribute("class")
				print >> sys.stdout, 'class found: %s' % repr(wordclass)
				if wordclass: ftempl.wordclass = [ wordclass ]
			if not wordclass:  ftempl.wordclass = wordclasses
			
			# Complementary distribution of stem and wordclass
			if pos == 'V':  # NB! HERE ARE SOME CHANGES NEEDED FOR sme
				if stem == '3syll':
					ftempl.wordclass = ['']
				elif wordclass:
					ftempl.stem = [ '2syll' ]
			# print 'wc: ' + repr(ftempl.wordclass)
			# print 'st: ' + repr(ftempl.stem)
			if el.getAttribute("gradation"):
				gradation=el.getAttribute("gradation")
				if gradation: ftempl.gradation = [ gradation ]
			if not gradation: ftempl.gradation = gradations.keys()
				
			if el.getAttribute("diphthong"):
				diphthong=el.getAttribute("diphthong")
				if diphthong: ftempl.diphthong = [ diphthong ]
			if not diphthong: ftempl.diphthong = diphthongs

			if el.getAttribute("soggi"):
				soggi=el.getAttribute("soggi")
				if soggi: ftempl.soggi = [ soggi ]
			if not soggi: ftempl.soggi = soggis.keys()

			if el.getAttribute("attrsuffix"):
				attrsuffix=el.getAttribute("attrsuffix")
				if attrsuffix: ftempl.attrsuffix = [ attrsuffix ]
			if not attrsuffix: ftempl.attrsuffix = attrsuffixs.keys()

			if el.getAttribute("rime"):
				rime=el.getAttribute("rime")
				if rime:
					if rime=="0": rime = ""
					ftempl.rime = [ rime ]
			if not rime: ftempl.rime = rimes.keys()

			# Compile a message object, figuring out which morphosyntactic
			# selections are relevant
			# 
			msgs = el.getElementsByTagName("msg")
			for mel in msgs:

				f = Entry()

				# TODO: are all of the default options that need to be here
				# here?

				# TODO: subclasses?

				case = ""
				number = ""
				personnumber = ""
				tense = ""
				mood = ""
				grade = ""
				attributive = ""

				#NEW_ATTRIBUTES
				# (Leave comment for documentation)
				f.pos = ftempl.pos[:]
				f.stem = ftempl.stem[:]
				f.wordclass = ftempl.wordclass[:]
				f.gradation = ftempl.gradation[:]
				f.diphthong = ftempl.diphthong[:]
				f.soggi = ftempl.soggi[:]
				f.rime = ftempl.rime[:]
				f.attrsuffix = ftempl.attrsuffix[:]
				f.attributes = el.attributes
				f.dialects = self.dialects[:]
				
				msgid = mel.firstChild.data
				#print "Message id", msgid
				f.msgid = msgid

				if el.getAttribute("attribute"):
					attributive=el.getAttribute("attribute")
					if attributive: f.attributive = [ 'Attr' ]
				else: f.attributive = ['Attr', 'NoAttr']
				
				if mel.getAttribute("case"):
					case=mel.getAttribute("case")
					if case: f.case = [ case ]
					# Since noattr is not marked, case entails noattr.
					f.attributive = [ 'NoAttr' ]
				if not case: f.case = cases

				if mel.getAttribute("number"):
					number=mel.getAttribute("number")
					if number: f.number = [ number ]
				if not number: f.number = numbers

				if mel.getAttribute("personnumber"):
					personnumber=mel.getAttribute("personnumber")
					if personnumber: f.personnumber = [ personnumber ]
				if not personnumber: f.personnumber = personnumbers

				if mel.getAttribute("tense"):
					tense=mel.getAttribute("tense")
					if tense: f.tense = [ tense ]
				if not tense: f.tense = tenses

				if mel.getAttribute("mood"):
					mood=mel.getAttribute("mood")
					if mood: f.mood = [ mood ]
				if not mood: f.mood = moods

				if mel.getAttribute("grade"):
					grade=mel.getAttribute("grade")
					if grade: f.grade = [ grade ]
				if not grade: f.grade = grades

				if mel.getAttribute("dialect"):
					dialect=mel.getAttribute("dialect")
					if dialect:
						invd=dialect.lstrip("NOT-")
						f.dialects.remove(invd)

				messages.append(f)

		# Here we run through all permutations of all of the cases, stem types,
		# rimes, soggis, etc., and compile a dictionary of each unique
		# permutation and the messages it is associated with:

		# 	{
		#		("stemtype", "strong", "uo-o", "etc..."): [<Feedback obj: g_and_as>, <Feedback obj: t_g>, etc...],
		#		("stemtype", "weak", "x", "etc..."): [<Feedback obj: weak_grade>, <Feedback obj: t_g>, <Feedback obj: -iin-ending>, etc...],
		#	}

		prep_for_insert = set()
		inverse_kwargs_to_message = {}

		poses = ["N", "Num", "V", "A"]
		for f in messages:
			if f.pos not in poses:
				print "No POS match."
				sys.exit()
			print >> sys.stdout, 'Calculating permutations for ' + f.msgid + ': ' + u', '.join([a.value for a in f.attributes.values()])
			
			# For each message and pos, we get all of the permutations for the
			# relevant morphosyntactic categories run through them and see if
			# there are relevante feedback messages, then collect these in the
			# big dictionary object.
			# 
			# Permutations are first appended to a set to remove any potential
			# duplicates.
			# 
			# If you are adding new attributes, there are several places
			# immediately below to do so (#NEW_ATTRIBUTES)
			if f.pos == "A":
				def gen_prod():
					products = product(
						list(set(f.stem)),
						list(set(f.gradation)),
						list(set(f.diphthong)),
						list(set(f.rime)),
						list(set(f.soggi)),
						list(set(f.grade)),
						list(set(f.case)),
						list(set(f.number)),
						list(set(f.attributive)),
						list(set(f.attrsuffix)),
					)

					return products

				total_iteration_count = len([a for a in gen_prod()])

				products = gen_prod()
				
				# Create set of all arguments to insert, iteration will
				# remove all of the redundant ones.
				prep_for_insert = set()
				for iteration in products:
					stem, gradation, diphthong, rime, soggi, grade, \
					case, number, attributive, attrsuffix = iteration

					if attributive == 'Attr':
				 		# Attributive forms: no case inflection.
						case = ""
						number = ""												
					else:
						attributive = 'NoAttr'
						if case == "Ess":
							number = ""

					prep_for_insert.add((
									pos,
									stem,
									gradation,
									diphthong,
									rime,
									soggi,
									grade,
									case,
									number,
									attributive,
									attrsuffix,
									))

				# Assign to the big dictionary
				for item in prep_for_insert:
					if item in inverse_kwargs_to_message:
						inverse_kwargs_to_message[item].append(f)
					else:
						inverse_kwargs_to_message[item] = [f]
				
			
			if f.pos in ["N", "Num"]:				
				# TODO: check what the actual contents of f.stem, etc are,
				# make sure that there are null options for all of these 
				# (except for probably case and number are not possibly null)

				def gen_prod():
					products = product(
						f.stem, 
						f.diphthong, 
						f.gradation, 
						f.soggi, 
						f.rime, 
						f.case, 
						f.number,
						)

					return products
					# include gradation, diphthong, rime also ?
				total_iteration_count = len([a for a in gen_prod()])
				# print 'Product: %d' % total_iteration_count

				products = gen_prod()
				
				
				prep_for_insert = set()
				count = 0
				for iteration in products:
					stem, diphthong, gradation, soggi, rime, \
					case, number = iteration # Here
					
					if case == "Ess":
						number = ""
					
					prep_for_insert.add((
								pos,
								stem,
								diphthong,
								gradation,
								soggi,
								rime,
								case,
								number,
								))


				for item in prep_for_insert:
					if item in inverse_kwargs_to_message:
						inverse_kwargs_to_message[item].append(f)
					else:
						inverse_kwargs_to_message[item] = [f]
			
			if f.pos == "V":				
				def gen_prod():
					products = product( f.stem, 
										f.diphthong,
										f.gradation, # added 
										f.soggi, 
										f.rime, 
										f.personnumber, 
										f.tense, 
										f.mood)
					
					return products

				total_iteration_count = len([a for a in gen_prod()])
				# print 'Product: %d' % total_iteration_count

				products = gen_prod()
				
				
				prep_for_insert = set()
				count = 0
				for iteration in products:
					stem, diphthong, gradation, soggi, \
					rime, personnumber, tense, mood = iteration

					# Wordclass and stem are basically the same thing, 
					# if one is set, the other is not. Complementary distribution.
					# Leaving '2syll' in because it makes filtering later easier.
					if stem == '3syll':
						wordclass = ''
						
					insert_kwargs = (
						pos,
						stem,
						soggi,
						diphthong,  # added for sme
						gradation,  # added for sme
						rime,
						personnumber,
						tense,
						mood,
					)
				
					prep_for_insert.add(insert_kwargs)


				for item in prep_for_insert:
					if item in inverse_kwargs_to_message:
						inverse_kwargs_to_message[item].append(f)
					else:
						inverse_kwargs_to_message[item] = [f]

		# These are the field names for Feedback 
		#
		# If you are adding new morphosyntactic attributes, this is one of the
		# places to do it (#NEW_ATTRIBUTES). There should be no need to edit
		# the code following this dictionary for processing bulk inserts, only
		# unless you are adding a new related model, or removing them.

		insert_keys = {
			"A": ('pos',
					'stem',
					'gradation',
					'diphthong',
					'rime',
					'soggi',
					'grade',
					'case2',
					'number',
					'attributive',
					'attrsuffix',),

			"Num": ('pos',
 					'stem',
 					'diphthong',
 					'gradation',
 					'soggi',
 					'rime',
					'case2',
 					'number'),

			"N": ('pos',
 					'stem',
 					'diphthong',
 					'gradation',
 					'soggi',
 					'rime',
					'case2',
 					'number'),

			"V": ('pos',
					'stem',
					'soggi',
					'diphthong',  # added for sme
					'gradation',  # added for sme
					'rime',
					'personnumber',
					'tense',
					'mood',
					),
		}

		# Here we collect all of the dialect and message objects in a cache, to
		# prevent the need for many successive database queries, the less, the
		# better!
		# 
		dialects_cache = {}
		messages_cache = {}

		count = 0
		for kwargs, fs in inverse_kwargs_to_message.iteritems():
			count += 1
			# print kwargs
			for f in fs:
				if f.msgid in dialects_cache:
					messages = dialects_cache[f.msgid]
				else:
					messages = Feedbackmsg.objects.filter(msgid=f.msgid)
					for msg in messages:
						if f.msgid in messages_cache:
							messages_cache[f.msgid].append(msg.id)
						else:
							messages_cache[f.msgid] = [msg.id]

				if f.msgid in dialects_cache:
					dialects = dialects_cache[f.msgid]
				else:
					dialects = Dialect.objects.filter(dialect__in=f.dialects)
					for dial in dialects:
						if f.msgid in dialects_cache:
							dialects_cache[f.msgid].append(dial.id)
						else:
							dialects_cache[f.msgid] = [dial.id]

		print 'Done preselecting messages and dialects.'
		
		# Now that all of the arguments, dialects and messages are prepared,
		# create all of the Feedback objects and add message and dialects
		#
		iteration_count = 0
		total_iteration_count = len(inverse_kwargs_to_message.keys())
		
		def chunks(l, n):
			""" Yield successive n-sized chunks from l.
			"""
			for i in xrange(0, len(l), n):
				yield l[i:i+n]
		
		if len(inverse_kwargs_to_message.keys()) == 0:
			print "No messages were compiled."
			sys.exit()
		else:
			kwarg_chunks = chunks(inverse_kwargs_to_message.keys(), 1000)
			keys = insert_keys.get(inverse_kwargs_to_message.values()[0][0].pos)

		# All of the Feedback objects are inserted, 1000 per commit
		print >> sys.stdout, " * Bulk inserting... "
		for chunk in kwarg_chunks:
			feedback_kwargs_for_insert = [dict(zip(keys, values)) for values in chunk]
			Feedback.objects.bulk_insert(keys, feedback_kwargs_for_insert)

		def get_key_values(obj, ks):
			" Fetch a list of keys from an object, return those keys "
			vs = []
			for k in ks:
				vs.append(obj.__getattribute__(k))
			return vs

		total_feedbacks = Feedback.objects.count()
		print 'Feedback object count: %d' % total_feedbacks

		# Create a unique set of feedback IDs and message or dialect IDS
		# for bulk insert, based on using inverse_kwargs_to_message, 
		# and the object caches compiled above
		# 
		# First step, collect all the IDs.
		# 
		feedback_messages_mtm = set()
		feedback_dialects_mtm = set()

		print 'Collecting Messages and Dialects for Feedback'
		for feedback in Feedback.objects.only(*keys).iterator():
			vals = tuple(get_key_values(feedback, keys))
			fs = inverse_kwargs_to_message.get(vals, False)
			if not fs:
				# print 'skipped %s' % repr(vals)
				continue
			for f in fs:
				messages = messages_cache.get(f.msgid, False)
				dialects = dialects_cache.get(f.msgid, False)
				if messages:
					msgs = [(feedback.id, m) for m in messages]
					for m in msgs:
						feedback_messages_mtm.add(m)
				if dialects:
					dials = [(feedback.id, d) for d in dialects]
					for d in dials:
						feedback_dialects_mtm.add(d)

		_pos = inverse_kwargs_to_message.values()[0][0].pos
		if _pos == 'A':
			chunk_size = 10000
		else:
			chunk_size = 1000

		# Chunk message and feedback IDs and bulk-insert them.
		# 
		message_chunks = chunks(list(feedback_messages_mtm), chunk_size)
		total_objs = len(list(feedback_messages_mtm))
		prog = 0
		print ' * Bulk inserting messages'
		for chunk in message_chunks:
			zipped = [dict(zip(keys, a)) for a in chunk]
			Feedback.objects.bulk_add_messages(chunk)
			prog += chunk_size
			if prog%10000 == 0:
				print '%d/%d Feedback-Message relations' % (prog, total_objs)


		# Chunk dialect and feedback IDs and bulk-insert them.
		# 
		dialect_chunks = chunks(list(feedback_dialects_mtm), chunk_size)
		total_objs = len(list(feedback_dialects_mtm))
		prog = 0
		print ' * Bulk inserting dialects'
		for chunk in dialect_chunks:
			zipped = [dict(zip(keys, a)) for a in chunk]
			Feedback.objects.bulk_add_dialects(chunk)
			prog += chunk_size
			if prog%10000 == 0:
				print '%d/%d Feedback-Dialect relations' % (prog, total_objs)

		# Done!

