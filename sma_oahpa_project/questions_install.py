# -*- coding: utf-8 -*-
from local_conf import LLL1
import importlib
settings = importlib.import_module(LLL1+'_oahpa.settings')
sdm = importlib.import_module(LLL1+'_oahpa.drill.models')

from xml.dom import minidom as _dom
from optparse import OptionParser
from django import db
import sys
import re
import string
import codecs

#sys.stdout = codecs.getwriter('utf8')(sys.stdout)

from kitchen.text.converters import getwriter
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

class Questions:

	def read_element(self,qaelement,el,el_id,qtype):

		semclass = False

		print
		#Chiara's note, this throws unicode error without kitchen module
		print "Creating element", el_id

		# Syntactic function of the element
		if self.values.has_key(el_id) and self.values[el_id].has_key('syntax'):
			syntax = self.values[el_id]['syntax']
		else:
			syntax = el_id

		if not el:
			#Chiara's note, this throws unicode error without kitchen module
			print syntax, "No element given."

		# Some of the answer elements share content of question elements.
		content_id=""
		if el:
			content_id = el.getAttribute("content")
		if not content_id: content_id=el_id
		# Search for the same element in question side
		# If there is no element given in the answer, the element
		# is a copy of the question.
		question_qelements = None

		if (not el or el.getAttribute("content")) and \
			sdm.QElement.objects.filter(question__id=qaelement.question_id,
									identifier=content_id).count() > 0:
			question_qelements = sdm.QElement.objects.filter(question__id=qaelement.question_id,
														 identifier=content_id)
		else:
			if el and el.getAttribute("content"):
				if sdm.QElement.objects.filter(question__id=qaelement.id,
										   identifier=content_id).count() > 0:
					question_qelements = sdm.QElement.objects.filter(question__id=qaelement.id,
																 identifier=content_id)

		if not el and question_qelements:
			for q in question_qelements:
				qe = sdm.QElement.objects.create(question=qaelement,
											 identifier=el_id,
											 syntax=q.syntax)
				# mark as a copy
				q.copy_set.add(qe)
				qe.save()
				q.save()
				return

		############### AGREEMENT
		# Search for elementes that agree
		agr_elements=None
		if syntax=="MAINV":
			agr_id="SUBJ"
			print "TRYING verb agreement " + agr_id + " " + qaelement.qatype
			if sdm.QElement.objects.filter(question=qaelement, syntax=agr_id,
									   question__qatype=qaelement.qatype).count() > 0:
				agr_elements = sdm.QElement.objects.filter(question=qaelement,
													   syntax=agr_id,
													   question__qatype=qaelement.qatype)


		agreement = ""
		if el: agreement = el.getElementsByTagName("agreement")
		if agreement: print "Agreement:", agreement[0].getAttribute("id")

		# Agreement from xml-files
		# Try first inside question or answer
		# Then in answer-question level
		if agreement:
			agr_id=agreement[0].getAttribute("id")
			if sdm.QElement.objects.filter(question=qaelement, syntax=agr_id,
									   question__qatype=qaelement.qatype).count() > 0:
				agr_elements = sdm.QElement.objects.filter(question=qaelement,
													   syntax=agr_id,
													   question__qatype=qaelement.qatype)

			else:
				if sdm.Question.objects.filter(id=qaelement.question_id).count() > 0:
					q=sdm.Question.objects.filter(id=qaelement.question_id)[0]
					if sdm.QElement.objects.filter(question__id=qaelement.question_id,
											   syntax=agr_id).count() > 0:
						agr_elements = sdm.QElement.objects.filter(question__id=qaelement.question_id,
															   syntax=agr_id)

			if not agr_elements:
				print "ERROR: no agreement elements found"

		############ WORDS
		# Search for existing word in the database.
		ids = []
		if el: ids=el.getElementsByTagName("id")
		words = {}
		word_elements = None
		for i in ids:
			word_id = i.firstChild.data
			word_id_hid = i.getAttribute("hid").strip()
			if word_id:
				if word_id_hid:
					#Chiara's note, this throws unicode error without kitchen module
					print "found word %s/%s" % (word_id, word_id_hid)
					word_elements = sdm.Word.objects.filter(wordid=word_id, hid=int(word_id_hid))
				else:
					#Chiara's note, this throws unicode error without kitchen module
					print "found word %s" % word_id
					word_elements = sdm.Word.objects.filter(wordid=word_id)
				# Add pos information here!
				if not word_elements:
					#Chiara's note, this throws unicode error without kitchen module
					print "Word not found! " + word_id

		# Search for existing semtype
		# Semtype overrides the word id selection
		if not word_elements:
			semclasses= []
			if el: semclasses=el.getElementsByTagName("sem")
			if semclasses:
				semclass=semclasses[0].getAttribute("class")
				word_elements = sdm.Word.objects.filter(semtype__semtype=semclass)
			valclasses= []
			if el: valclasses=el.getElementsByTagName("val")
			if valclasses:
				valclass=valclasses[0].getAttribute("class")
				word_elements = sdm.Word.objects.filter(valency=valclass)

		# If still no words, get the default words for this element:
		if not word_elements:
			if self.values.has_key(el_id) and self.values[el_id].has_key('words'):
				word_elements = self.values[el_id]['words']

		if word_elements:
			for w in word_elements:
				if not words.has_key(w.pos): words[w.pos] = []
				words[w.pos].append(w)

		############# GRAMAMR
		tagelements = None
		grammars = []
		if el: grammars = el.getElementsByTagName("grammar")
		if not el or not grammars:
			# If there is no grammatical specification, the element is created solely
			# on the basis of grammar.
			if self.values.has_key(el_id):
				if self.values[el_id].has_key('tags'):
					tagelements = self.values[el_id]['tags']
		# An element for each different grammatical specification.
		else:
			poses = []
			tags = []
			for gr in grammars:
				tags.append(gr.getAttribute("tag"))
				poses.append(gr.getAttribute("pos"))
			tagstrings = []
			if poses:
				if self.values.has_key(el_id):
					if self.values[el_id].has_key('tags'):
						tagelements = self.values[el_id]['tags'].filter(pos__in=poses)
			if tags:
				for tag in tags:
					tagvalues = []
					self.get_tagvalues(tag,"",tagvalues)
					tagstrings.extend(tagvalues)
				if tagelements:
					tagelements = tagelements or sdm.Tag.objects.filter(string__in=tagstrings)
				else:
					tagelements = sdm.Tag.objects.filter(string__in=tagstrings)


			# Extra check for pronouns
			# If pronoun id is given, only the tags related to that pronoun are preserved.
			for t in tagelements:
				if t.pos == 'Pron':
					if not words.has_key('Pron'): break
					found = False
					for w in words['Pron']:
						if sdm.Form.objects.filter(tag=t,word=w).count()>0:
							found = True
							break
					if not found:
						tagelements = tagelements.exclude(id=t.id)

			# Remove those words which do not have any forms with the tags.
			if words.has_key('N'):
				for w in words['N']:
					found = False
					for t in tagelements:
						if t.pos == 'N':
							if sdm.Form.objects.filter(tag=t, word=w).count()>0:
								found = True
					if not found:
						words['N'].remove(w)

		# Find different pos-values in tagelements
		posvalues = {}
		# Elements that do not inflection information are not created.
		if not tagelements and not agr_elements:
			#Chiara's note, this throws unicode error without kitchen module
			print "no inflection for", el_id
			if len(grammars) > 0:
				print >> sys.stderr, " ** Grammars defined in element, but no inflections were found."
				print >> sys.stderr, "    Check that tags.txt and paradigms.txt include all tags."
				print >> sys.stderr, ""
				print >> sys.stderr, "    Alternatively, ensure that <grammar tag /> is a valid tag,"
				print >> sys.stderr, "    or that <grammar pos /> is a valid PoS."
				sys.exit(2)
			return
		if not tagelements: posvalues[""] = 1
		else:
			for t in tagelements:
				posvalues[t.pos] = 1
		attempt = False
		if el:
			task = el.getAttribute("task")
			if task:
				print "setting", el_id, "as task"
				qaelement.task = syntax
				qaelement.save()
		else:
			if el_id == qtype:
				qaelement.task = syntax
				qaelement.save()
		# if el:
			# task = el.getAttribute("task")
			# if task:
				# # print task
				# # print syntax
				# # print 'TEST'
				# # raw_input()
				# print "setting", el_id, "as task"
				# qaelement.task = syntax
				# qaelement.save()
				# attempt = True
				# if qaelement.task != syntax:
					# print 'Task not saved!'
					# sys.exit(2)
				# # print qaelement.task
				# # raw_input()
		# else:
			# if el_id == qtype:
				# qaelement.task = syntax
				# qaelement.save()
				# attempt = True

		# if task:
			# if qaelement.task != syntax:
				# print 'TASK NOT SAVED'
				# print qaelement.task
				# print syntax
				# print 'attempt: '
				# print attempt
				# sys.exit(2)

		############# CREATE ELEMENTS
		print 'CREATING ELEMENTS'
		print 'Elements for the following keys...'
		print posvalues.keys()
		# Add an element for each pos:
		for p in posvalues.keys():
			qe = sdm.QElement.objects.create(question=qaelement,\
										 identifier=el_id,\
										 syntax=syntax)
			if semclass:
				semty, _ = sdm.Semtype.objects.get_or_create(semtype=semclass)
				qe.semtype = semty
				qe.save()

			print '\tsemtype: ', semclass
			# Add links to corresponding question elements.
			if question_qelements:
				for q in question_qelements:
					q.copy_set.add(qe)
					qe.save()
					q.save()

			if tagelements:
				for t in tagelements:
					print '\ttag: ', t.string
					if t.pos == p:
						qe.tags.add(t)

			# Create links to words.
			if not words.has_key(p):
				word_pks = None
				print "looking for words..", el_id, p
				# word_elements = Word.objects.filter(form__tag__in=qe.tags.all()) # pos=p)

				# Just filtering isn't enough; .filter() doesn't return a list of unique items with this kind of query.

				if semclass:
					word_pks = sdm.Word.objects.filter(form__tag__in=qe.tags.all()).filter(semtype=qe.semtype).values_list('pk', flat=True)
				else:
					word_pks = sdm.Word.objects.filter(form__tag__in=qe.tags.all()).values_list('pk', flat=True)
				word_pks = list(set(word_pks))
				if len(word_pks) == 0:
					print 'Error: Elements with zero possibilities not permitted.'
					print ' > ', qe.question
					print ' > Word tags: %s' % repr(qe.tags.all())
					print ' > semtypes: %s' % repr(qe.semtype)
					sys.exit(2)
				print '%d elements available. ' % len(word_pks)

				word_elements_gen = (sdm.Word.objects.get(pk=int(b)) for b in word_pks)

				if not word_elements:
					word_elements = []
				else:
					word_elements = list(word_elements)

				if word_elements_gen:
					for w in word_elements_gen:
						if not words.has_key(p):
							words[w.pos] = []
						if not words.has_key(w.pos):
							words[w.pos] = []
						words[w.pos].append(w)
						word_elements.append(w)

			# print 'Creating elements for %d words' % word_elements.count()
			for w in word_elements:
				qe.wordqelement_set.create(word=w)
				# we = WordQElement.objects.create(qelement=qe,\
												 # word=w)

			# add agreement info.
			if agr_elements:
				for a in agr_elements:
					a.agreement_set.add(qe)
				a.save()
			qe.save()


	# Read elements attached to particular question or answer.
	def read_elements(self, head, qaelement, qtype):

		els = head.getElementsByTagName("element")
		qastrings =  qaelement.string.split()

		# Read first subject for agreement
		element=None
		if "SUBJ" in set(qastrings):
			for e in els:
				if e.getAttribute("id")=="SUBJ":
					element = e
					break

			self.read_element(qaelement, element, "SUBJ", qtype)


		# Process rest of the elements in the string.
		subj=False
		for s in qastrings:
			if s=="SUBJ" and not subj:
				subj=True
				continue

			syntax = s.lstrip("(")
			syntax = syntax.rstrip(")")

			element=None
			found = False
			for e in els:
				el_id = e.getAttribute("id")
				if el_id==s and not s=="SUBJ":
					self.read_element(qaelement,e,syntax,qtype)
					found = True
			if not found:
				self.read_element(qaelement,None,syntax,qtype)

	def read_questions(self, infile, grammarfile):

		xmlfile=file(infile)
		tree = _dom.parse(infile)

		self.read_grammar(grammarfile)

		qs = tree.getElementsByTagName("questions")[0]
		gametype = qs.getAttribute("game")
		if not gametype: gametype="morfa"

		print "Created questions:"
		for q in tree.getElementsByTagName("q"):
			qid = q.getAttribute('id')
			if not qid:
				print "ERROR Missing question id, stopping."
				exit()
			print qid.encode('utf-8')
			level = q.getAttribute('level')
			if not level: level="1"

			# Store question
			qtype=""
			qtype_els = q.getElementsByTagName("qtype")
			# MIX
			if qtype_els:
				qtype = ','.join([qtype.firstChild.data for qtype in qtype_els])
				# qtype = q.getElementsByTagName("qtype")[0].firstChild.data
			question=q.getElementsByTagName("question")[0]
			text=question.getElementsByTagName("text")[0].firstChild.data

			#If there exists already a question with that name, delete all the references to it.
			if qid:
				questions = sdm.Question.objects.filter(qid=qid)
				if questions:
					questions[0].delete()

			question_element,created = sdm.Question.objects.get_or_create(qid=qid, \
																	  level=int(level), \
																	  string=text, \
																	  qtype=qtype, \
																	  gametype=gametype,\
																	  qatype="question")

			# Add source information if present
			if q.getElementsByTagName("sources"):
				sources = q.getElementsByTagName("sources")[0]
				elements=sources.getElementsByTagName("book")
				for el in elements:
					book=el.getAttribute("name")
					if book:
						# Add book to the database
						# Leave this if DTD is used
						book_entry, created = sdm.Source.objects.get_or_create(name=book)
						if created:
							print "Created book entry with name ", book
					question_element.source.add(book_entry)
					question_element.save()

			else:
				book = "all"
				# Add book to the database
				book_entry, created = sdm.Source.objects.get_or_create(name=book)
				if created:
					print "Created book entry with name ", book
				question_element.source.add(book_entry)
				question_element.save()

			# Read the elements
			self.read_elements(question, question_element,qtype)

			# There can be more than one answer for each question,
			# Store them separately.
			answers=q.getElementsByTagName("answer")
			for ans in answers:
				text=ans.getElementsByTagName("text")[0].firstChild.data
				answer_element = sdm.Question.objects.create(string=text,qatype="answer",question=question_element,level=1)

				answer_element.save()
				self.read_elements(ans, answer_element, qtype)
			db.reset_queries()


	def read_grammar(self, infile):

		xmlfile=file(infile)
		tree = _dom.parse(infile)

		self.values = {}

		tags=tree.getElementsByTagName("tags")[0]
		for el in tags.getElementsByTagName("element"):

			identifier=el.getAttribute("id")

			info2 = {}

			elements = []
			word_id=""
			word = None

			syntax =""
			syntaxes = el.getElementsByTagName("syntax")
			if syntaxes:
				syntax = syntaxes[0].firstChild.data
				info2['syntax'] = syntax

			word_ids = el.getElementsByTagName("id")
			if word_ids:
				word_id = word_ids[0].firstChild.data
				word_id_hid = word_ids[0].getAttribute("hid").strip()
				if word_id:
					words = sdm.Word.objects.filter(wordid=word_id)
					if word_id_hid:
						words = words.filter(hid=int(word_id_hid))
					info2['words'] = words

			info2['pos'] = []
			tagstrings = []

			grammars = el.getElementsByTagName("grammar")
			for gr in grammars:
				pos=gr.getAttribute("pos")
				if pos:
					info2['pos'].append(pos)

				tag=gr.getAttribute("tag")
				tagvalues = []
				self.get_tagvalues(tag,"",tagvalues)
				tagstrings.extend(tagvalues)

			if len(tagstrings) > 0:
				tags = sdm.Tag.objects.filter(string__in=tagstrings)
				info2['tags'] = tags

			self.values[identifier] = info2

	def get_tagvalues(self,rest,tagstring,tagvalues):

		if not rest:
			tagvalues.append(tagstring)
			return
		if rest.count("+") > 0:
			t, rest = rest.split('+',1)
		else:
			t=rest
			rest=""
		if sdm.Tagname.objects.filter(tagname=t).count() > 0:
			if tagstring:
				tagstring = tagstring + "+" + t
			else:
				tagstring = t
			self.get_tagvalues(rest,tagstring,tagvalues)
		else:
			if sdm.Tagset.objects.filter(tagset=t).count() > 0:
				tagnames=sdm.Tagname.objects.filter(tagset__tagset=t)
				for t in tagnames:
					if tagstring:
						tagstring2 = tagstring + "+" + t.tagname
					else:
						tagstring2 = t.tagname
					self.get_tagvalues(rest,tagstring2,tagvalues)


	def delete_question(self, qid=None):

		if qid:
			questions = sdm.Question.objects.filter(qid=qid)
			if questions:
				for q in questions:
					q.delete()

			questions = sdm.Question.objects.filter(string=qid)
			if questions:
				for q in questions:
					q.delete()
