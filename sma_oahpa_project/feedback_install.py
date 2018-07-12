# -*- coding: utf-8 -*-
from local_conf import LLL1
import importlib
settings = importlib.import_module(LLL1+'_oahpa.settings')
sdm = importlib.import_module(LLL1+'_oahpa.drill.models')

from xml.dom import minidom as _dom
from django.db.models import Q
import sys
import re
import string
import codecs

from itertools import product

#sys.stdout = codecs.getwriter('utf8')(sys.stdout)
from kitchen.text.converters import getwriter
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

class Entry:
	pass

stem_convert = {
	'2syll': '2syll',
	'3syll': '3syll',
	'bisyllabic': '2syll',
	'trisyllabic': '3syll',
	'': '',
}


class Feedback_install:

	def __init__(self):
		self.tagset = {}
		self.paradigms = {}
		# self.dialects = ["KJ","GG"]

	def read_messages(self,infile):

		xmlfile=file(infile)
		tree = _dom.parse(infile)
		lex = tree.getElementsByTagName("messages")[0]
		lang = lex.getAttribute("xml:lang")

		for el in tree.getElementsByTagName("message"):
			mid=el.getAttribute("id")
			message = el.firstChild.data
		    #Chiara's note, this throws unicode error without kitchen module
			print message
			fm, created = sdm.Feedbackmsg.objects.get_or_create(msgid=mid)
			fm.save()

			fmtext, created = sdm.Feedbacktext.objects.get_or_create(language=lang,feedbackmsg=fm)
			fmtext.message=message
			fmtext.save()

	def insert_feedback(self,pos,stem,rime,soggi,case,number,personnumber="",tense="",mood="",attributive="",grade="",attrsuffix="", wordclass=""):
		try:
			stem = stem_convert[stem]
		except KeyError:
			print "Non-existent stem: %s" % stem
			sys.exit(2)

		attrs = {
			'pos': pos,
			'stem': stem,
			# 'diphthong': diphthong,
			# 'gradation': gradation,
			# 'rime': rime,
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

		feed, created = sdm.Feedback.objects.get_or_create(**attrs)

		return feed

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
		print infile
		print wordfile

		wordfile=file(wordfile)
		wordtree = _dom.parse(wordfile)

		# Find out different values for variables.
		# Others can be listed, but soggi is searched at the moment.
		rimes={}
		# gradations={}
		attrsuffixs={}
		compsuffixs={}
		soggis={}
		for el in wordtree.getElementsByTagName("l"):
			if el.getAttribute("rime"):
				rime = el.getAttribute("rime")
				if rime=="0": rime = ""
				rimes[rime] = 1
			# if el.getAttribute("gradation"):
				# gradation = el.getAttribute("gradation")
				# gradations[gradation] = 1
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

		# diphthongs = ["yes","no"]
		stems = ["3syll", "2syll"]
		wordclasses = ['I', 'II', 'III', 'IV', 'V', 'VI']
		grades = ["Comp","Superl","Pos"]
		# Sma requires different cases
		cases = ["Nom", "Acc", "Gen", "Ill", "Ine", "Ela", "Com", "Ess"]
		numbers = ["Sg","Pl"]
		tenses = ["Prs","Prt"]
		moods = ["Ind","Cond","Pot","Imprt"]
		personnumbers = ["Sg1","Sg2","Sg3","Du1","Du2","Du3","Pl1","Pl2","Pl3"]

		messages=[]
		# print rimes.keys()
		print soggis.keys()
		# print gradations.keys()
		print compsuffixs.keys()
		print attrsuffixs.keys()
		print wordclasses
		print grades
		print cases
		print numbers
		print personnumbers

		# print diphthongs


		# Read the feedback file
		xmlfile=file(infile)
		tree = _dom.parse(infile)

		fb = tree.getElementsByTagName("feedback")[0]
		pos = fb.getAttribute("pos").upper()
		if pos:
			print "Deleting old feedbacks for pos", pos
			oldfs = sdm.Feedback.objects.filter(pos=pos)
			for f in oldfs:
				f.delete()
		stem_messages = {}
		# gradation_messages = {}

		if pos=="V":
			rimes[""] = 1
			# diphthongs.append("")
		if pos=="Num":
			rimes[""] = 1
			# diphthongs.append("")

		# cursor = connection.cursor()

		wordforms = tree.getElementsByTagName("stems")[0]
		for el in wordforms.getElementsByTagName("l"):
			feedback = None
			stem =""
			diphthong =""
			rime =""
			# gradation=""
			soggi =""
			attrsuffix =""
			wordclass = ""

			ftempl = Entry()

			ftempl.pos = pos
			ftempl.wordclass = ""

			if el.getAttribute("stem"):
				stem=el.getAttribute("stem")
				print 'stem found: %s' % repr(stem)
				try:
					stem = stem_convert[stem]
				except:
					print "Unknown value: %s" % stem
					sys.exit(2)

				if stem: ftempl.stem = [ stem ]
			if not stem:  ftempl.stem = stems

			if el.getAttribute("class"):
				wordclass=el.getAttribute("class")
				print 'class found: %s' % repr(wordclass)
				if wordclass: ftempl.wordclass = [ wordclass ]
			if not wordclass:  ftempl.wordclass = wordclasses

			# Complementary distribution of stem and wordclass
			if pos == 'V':
				if stem == '3syll':
					ftempl.wordclass = ['']
				elif wordclass:
					ftempl.stem = [ '2syll' ]
			# print 'wc: ' + repr(ftempl.wordclass)
			# print 'st: ' + repr(ftempl.stem)
			# if el.getAttribute("gradation"):
				# gradation=el.getAttribute("gradation")
				# if gradation: ftempl.gradation = [ gradation ]
			# if not gradation: ftempl.gradation = gradations.keys()

			# if el.getAttribute("diphthong"):
				# diphthong=el.getAttribute("diphthong")
				# if diphthong: ftempl.diphthong = [ diphthong ]
			# if not diphthong: ftempl.diphthong = diphthongs

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
				# f.gradation = ftempl.gradation[:]
				# f.diphthong = ftempl.diphthong[:]
				f.soggi = ftempl.soggi[:]
				f.rime = ftempl.rime[:]
				f.attrsuffix = ftempl.attrsuffix[:]
				# f.dialects = self.dialects[:]

				msgid = mel.firstChild.data
			    #Chiara's note, this throws unicode error without kitchen module
				print "Message id", msgid
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
		    #Chiara's note, this throws unicode error without kitchen module
			print f.msgid
			messages = sdm.Feedbackmsg.objects.filter(msgid=f.msgid)
			# dialects = Dialect.objects.filter(dialect__in=f.dialects)

			# Beginning to refactor this code in a simpler way below
			# Adjectives is untouched, but nominals and verbs are simplified.
			# Once we begin importing adjectives, this will probably need tob e
			# changed, as there are things being iterated here which are not a part
			# of sma.

			if f.pos == "A": # or pos=="A" or pos=="Num":
				for stem in f.stem:
					# for gradation in f.gradation:
					# for diphthong in f.diphthong:
					for rime in f.rime:
						for soggi in f.soggi:
							if f.pos == "A":
								for grade in f.grade:
									for attributive in f.attributive:
										if attributive == 'Attr':
											# Attributive forms: no case inflection.
											for attrsuffix in f.attrsuffix:
												case=""
												number=""
												self.insert_feedback(
													pos=pos,
													stem=stem,
													rime=rime,
													soggi=soggi,
													case=case,
													number=number,
													personnumber='',
													tense='',
													mood='',
													attributive='Attr',
													grade=grade,
													attrsuffix=attrsuffix,
													wordclass='')

												f2, created = sdm.Feedback.objects.get_or_create(stem=stem,\
																						   # diphthong=diphthong,\
																						   # gradation=gradation,\
																						   # rime=rime,\
																						   attributive='Attr',\
																						   attrsuffix=attrsuffix,\
																						   pos=pos,\
																						   number=number,\
																						   grade=grade,\
																						   soggi=soggi)
												if messages:
													f2.messages.add(msgs[0])
												else : print "No messages found:", f.msgid
												# for d in dialects:
													# f2.dialects.add(d)
												f2.save()

										else:
											for case in f.case:
												#essive without number inflection
												if case == "Ess":
													number=""

													self.insert_feedback(pos=pos,
																		stem=stem,
																		rime=rime,
																		soggi=soggi,
																		case=case,
																		number=number,
																		personnumber='',
																		tense='',
																		mood='',
																		attributive='NoAttr',
																		grade=grade,
																		attrsuffix='',
																		wordclass='')

													f2, created = sdm.Feedback.objects.get_or_create(stem=stem,\
																							   # diphthong=diphthong,\
																							   # gradation=gradation,\
																							   # rime=rime,\
																							   attributive='NoAttr',\
																							   pos=pos,\
																							   number=number,\
																							   case2=case,\
																							   grade=grade,\
																							   soggi=soggi)
													if messages:
														f2.messages.add(msgs[0])
													else : print "No messages found:", f.msgid
													# for d in dialects:
														# f2.dialects.add(d)

													f2.save()

												else:
													for number in f.number:
														self.insert_feedback(pos=pos,
																			stem=stem,
																			rime=rime,
																			soggi=soggi,
																			case=case,
																			number=number,
																			personnumber='',
																			tense='',
																			mood='',
																			attributive='NoAttr',
																			grade=grade,
																			# attrsuffix='',
																			wordclass='')

														f2, created = sdm.Feedback.objects.get_or_create(stem=stem,\
																								   # diphthong=diphthong,\
																								   # gradation=gradation,\
																								   # rime=rime,\
																								   attributive='NoAttr',\
																								   pos=pos,\
																								   case2=case,\
																								   number=number, \
																								   grade=grade,\
																								   soggi=soggi)
														if messages:
															f2.messages.add(msgs[0])
														else : print "No messages found:", f.msgid
														# for d in dialects:
															# f2.dialects.add(d)

														f2.save()

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
				products = product(
					f.stem,
					f.soggi,
					f.case,
					f.number)
				messages = sdm.Feedbackmsg.objects.filter(msgid=f.msgid)

				for iteration in products:
					stem, soggi, case, number = iteration # Here

					if case == "Ess":
						number = ""

					f2 = self.insert_feedback(
								pos=pos,
								stem=stem,
								soggi=soggi,
								case=case,
								number=number,
								# empties
								rime='',
								personnumber='',
								tense='',
								mood='',
								attributive='',
								grade='',
								attrsuffix='',
								wordclass='',
								)

					if messages:
						for msg in messages:
							f2.messages.add(msg)
					else:
						print "No messages found:", f.msgid
					# for d in dialects:
						# f2.dialects.add(d)
					f2.save()


			if f.pos == "V":
				products = product(f.wordclass,
									f.stem,
#									f.diphthong,
									f.soggi,
#									f.rime,
									f.personnumber,
									f.tense,
									f.mood)
				messages = sdm.Feedbackmsg.objects.filter(msgid=f.msgid)

				for iteration in products:
					wordclass, stem, soggi, personnumber, tense, mood = iteration
					# Wordclass and stem are basically the same thing,
					# if one is set, the other is not. Complementary distribution.
					# Leaving '2syll' in because it makes filtering later easier.
					if stem == '3syll':
						wordclass = ''

					insert_kwargs = {
						'pos': pos,
						'stem': stem,
						'wordclass': wordclass,
						'soggi': soggi,
						'personnumber': personnumber,
						'tense': tense,
						'mood': mood,
						'attributive': '',
						'rime': '',
						'case': '',
						'number': '',
						'grade': '',
						'attrsuffix': '',
					}

					f2 = self.insert_feedback(**insert_kwargs)

					if messages:
						for msg in messages:
							f2.messages.add(msg)
					else:
						print "No messages found:", f.msgid
					# for d in dialects:
						# f2.dialects.add(d)
					f2.save()
