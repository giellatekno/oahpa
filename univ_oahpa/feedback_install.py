# -*- coding: utf-8 -*-

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
		# self.dialects = ["KJ","GG"]

	def read_messages(self,infile):

		xmlfile=file(infile)
		tree = _dom.parse(infile)
		lex = tree.getElementsByTagName("messages")[0]
		lang = lex.getAttribute("xml:lang")		

		for el in tree.getElementsByTagName("message"):
			mid=el.getAttribute("id")
			message = el.firstChild.data
			print >> sys.stdout, message
			fm, created = Feedbackmsg.objects.get_or_create(msgid=mid)
			fm.save()

			fmtext, created=Feedbacktext.objects.get_or_create(language=lang,feedbackmsg=fm)
			fmtext.message=message
			fmtext.save()

	def insert_feedback(self,
							pos,
							stem,
							rime,
							soggi,
							case,
							number,
							gradation="",
							diphthong="",
							personnumber="",
							tense="",
							mood="",
							attributive="",
							grade="",
							attrsuffix="",
							wordclass=""):
		try:
			stem = stem_convert[stem]
		except KeyError:
			print >> sys.stderr, "Non-existent stem: %s" % stem
			sys.exit(2)
		
		attrs = {
			'pos': pos,
			'stem': stem,
			'diphthong': diphthong,
			'gradation': gradation,
			'rime': rime,
			'soggi': soggi,
			'case2': case,
			'number': number,
			'personnumber': personnumber,
			'tense': tense,
			'mood': mood,
			'grade': grade,
			'attrsuffix': attrsuffix,
			'wordclass': wordclass,
		}
		
		try:
			feed, created = Feedback.objects.get_or_create(**attrs)
		except Exception, e:
			print >> sys.stderr, Exception, e
			print >> sys.stderr, attrs
			sys.exit()

		if created:
			self.obj_count += 1
		
		return feed

	# NOTE: this silences some exceptions, so if something goes wrong, comment it out
	@transaction.commit_manually
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
		
		messages=[]
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
		pos = fb.getAttribute("pos").upper()
		if pos:
			print  >> sys.stdout,"Deleting old feedbacks for pos", pos
			oldfs = Feedback.objects.filter(pos=pos)			
			for f in oldfs:
				f.delete()				
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

			msgs = el.getElementsByTagName("msg")
			for mel in msgs:

				f = Entry()

				case = ""
				number = ""
				personnumber = ""
				tense = ""
				mood = ""
				grade = ""
				attributive = ""

				f.pos = ftempl.pos[:]
				f.stem = ftempl.stem[:]
				f.wordclass = ftempl.wordclass[:]
				f.gradation = ftempl.gradation[:]
				f.diphthong = ftempl.diphthong[:]
				f.soggi = ftempl.soggi[:]
				f.rime = ftempl.rime[:]
				f.attrsuffix = ftempl.attrsuffix[:]
				f.attributes = el.attributes
				# f.dialects = self.dialects[:]
				
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

				# if mel.getAttribute("dialect"):
					# dialect=mel.getAttribute("dialect")
					# if dialect:
						# invd=dialect.lstrip("NOT-")
						# f.dialects.remove(invd)

				messages.append(f)

		
		for f in messages:
			print >> sys.stdout, f.msgid + ': ' + u', '.join([a.value for a in f.attributes.values()])
			messages = Feedbackmsg.objects.filter(msgid=f.msgid)
			# dialects = Dialect.objects.filter(dialect__in=f.dialects)
			
			# Beginning to refactor this code in a simpler way below
			# Adjectives is untouched, but nominals and verbs are simplified.
			# Once we begin importing adjectives, this will probably need tob e
			# changed, as there are things being iterated here which are not a part
			# of sma.
			
			# TODO: test the adjective part
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
				# print 'Product: %d' % total_iteration_count

				products = gen_prod()
				
				messages = Feedbackmsg.objects.filter(msgid=f.msgid)

				# Create set of all arguments to insert, iteration will
				# remove all of the redundant ones.
				prep_for_insert = set()
				for iteration in products:
					stem, gradation, diphthong, rime, soggi, grade, case, \
					number, attributive, attrsuffix = iteration

					if attributive == 'Attr':
				 		# Attributive forms: no case inflection.
						case = ""
						number = ""												
					else:
						attributive = 'NoAttr'
						if case == "Ess":
							number = ""

					prep_for_insert.add((pos,
									stem,
									rime,
									soggi,
									case,
									number,
									'',
									'',
									'',
									attributive,
									grade,
									attrsuffix,
									''))
				
				keys = ('pos', 'stem', 'rime', 'soggi', 'case', 'number',
					'personnumber', 'tense', 'mood', 'attributive', 'grade',
					'attrsuffix', 'wordclass')

				# Iterate and insert 
				count = 0
				prep_for_insert = list(prep_for_insert)
				total_iteration_count = len(prep_for_insert)
				for aset in prep_for_insert:
					kwargs = dict(zip(keys, aset))

					f2 = self.insert_feedback(**kwargs)
					
					if messages:
						for msg in messages:
				   	   		f2.messages.add(msg)
				   	else:
						print >> sys.stderr, "No messages found:", f.msgid
					# for d in dialects:
				   	   # f2.dialects.add(d)
					f2.save()
					count += 1
					if count%100 == 0:
						print >> sys.stdout, 'created %d feedbacks' % self.obj_count
						print >> sys.stdout, '%s  %d/%d' % (f.msgid, count, total_iteration_count)

					if count%2500 == 0:
						print 'commit'
						transaction.commit()
					
				print >> sys.stdout, '%s  %d/%d' % (f.msgid, count, total_iteration_count)
				transaction.commit()
			
			#NEW_ATTRIBUTES
			# The above was too complex and made troubleshooting difficult, so I simplified it. 
			# Adjectives will take more work, but are possible-- just mind all of the if statements
			# splitting things up between Attr and NoAttr and so on.
			
			# Eventually this code can be combined with verbs.
			
			# Here we iterate through all possible values of the items in product()
			# and create Feedback items for each of them. Then, if messages match
			# these attributes, they are added to the Feedback.
			
			# If new attributes need to be added, be sure to include them in products
			# as well as pop them out of the iteration variable below ('here').
			
			# New attributes will also need to be added above.
			
			if f.pos in ["N", "Num"]:				
				def gen_prod():
					products = product(
						f.stem, 
						f.soggi, 
						f.case, 
						f.number)

					return products
					# include gradation, diphthong, rime also ?
				total_iteration_count = len([a for a in gen_prod()])
				# print 'Product: %d' % total_iteration_count

				products = gen_prod()
				
				messages = Feedbackmsg.objects.filter(msgid=f.msgid)
				
				prep_for_insert = set()
				count = 0
				for iteration in products:
					stem, soggi, case, number = iteration # Here
					
					if case == "Ess":
						number = ""
					
					prep_for_insert.add((pos,
								stem,
								soggi,
								case,
								number,
								# empties
								'', 
								'', # added for sme
								'', # added for sme
								'',
								'',
								'',
								'',
								'',
								'',
								'',
								))

				keys = ('pos', 'stem', 'rime', 'soggi', 'case', 'number',
					'personnumber', 'tense', 'mood', 'attributive', 'grade',
					'attrsuffix', 'wordclass')

				# Iterate and insert 
				count = 0
				prep_for_insert = list(prep_for_insert)
				total_iteration_count = len(prep_for_insert)
				for aset in prep_for_insert:
					kwargs = dict(zip(keys, aset))

					f2 = self.insert_feedback(**kwargs)
					
					if messages:
						for msg in messages:
							f2.messages.add(msg)
					else: 
						print >> sys.stderr, "No messages found:", f.msgid
					# for d in dialects:
						# f2.dialects.add(d)
					f2.save()
					count += 1
					if count%100 == 0:
						print >> sys.stdout,'created %d feedbacks' % self.obj_count
						print >> sys.stdout, '%s  %d/%d' % (f.msgid, count, total_iteration_count)

					if count%2500 == 0:
						print 'commit'
						transaction.commit()
					
				print >> sys.stdout, '%s  %d/%d' % (f.msgid, count, total_iteration_count)
				transaction.commit()
				
			
			if f.pos == "V":				
				def gen_prod():
					products = product(f.wordclass, 
										f.stem, 
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
				
				messages = Feedbackmsg.objects.filter(msgid=f.msgid)
				
				prep_for_insert = set()
				count = 0
				for iteration in products:
					wordclass, stem, diphthong, gradation, soggi, \
					rime, personnumber, tense, mood = iteration

					# Wordclass and stem are basically the same thing, 
					# if one is set, the other is not. Complementary distribution.
					# Leaving '2syll' in because it makes filtering later easier.
					if stem == '3syll':
						wordclass = ''
						
					insert_kwargs = (
						pos,
						stem,
						wordclass,
						soggi,
						personnumber,
						tense,
						mood,
						'',
						'',
						diphthong,  # added for sme
						gradation,  # added for sme
						'',
						'',
						'',
						'',
					)
				
					prep_for_insert.add(insert_kwargs)
					
				keys = ['pos',
						'stem',
						'wordclass',
						'soggi',
						'personnumber',
						'tense',
						'mood',
						'attributive',
						'rime',
						'diphthong',  # added for sme
						'gradation',  # added for sme
						'case',
						'number',
						'grade',
						'attrsuffix']

				# Iterate and insert 
				count = 0
				prep_for_insert = list(prep_for_insert)
				total_iteration_count = len(prep_for_insert)
				for aset in prep_for_insert:

					kwargs = dict(zip(keys, aset))
					f2 = self.insert_feedback(**kwargs)

					if messages:
						for msg in messages:
							f2.messages.add(msg)
					else: 
						print >> sys.stdout, "No messages found:", f.msgid
					# for d in dialects:
						# f2.dialects.add(d)
					f2.save()
					count += 1
					if count%100 == 0:
						print >> sys.stdout, 'created %d feedbacks' % self.obj_count
						print >> sys.stdout, '%s  %d/%d' % (f.msgid, count, total_iteration_count)

					if count%2500 == 0:
						print 'commit'
						transaction.commit()
					
				print >> sys.stdout, '%s  %d/%d' % (f.msgid, count, total_iteration_count)
				transaction.commit()

			transaction.commit()
		transaction.commit()

