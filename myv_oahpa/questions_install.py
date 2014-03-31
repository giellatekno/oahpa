# -*- coding: utf-8 -*-

from settings import *
from myv_drill.models import *
from xml.dom import minidom as _dom
from optparse import OptionParser
from django import db
import sys
import re
import string
import codecs
from django.utils.encoding import force_unicode
def monitor(function):
	from functools import wraps

	@wraps(function)
	def wrapper(*args, **kwargs):
		print '--\n'
		print ' %s args'
		print '    ' + repr(args)
		print ' %s kwargs'
		print '    ' + repr(kwargs)
		result = function(*args, **kwargs)
		print ' %s args'
		print '    ' + repr(args)
		print ' %s kwargs'
		print '    ' + repr(kwargs)
		print ' %s result'
		print '    ' + repr(result)
		print '--\n'
		return result
	
	return wrapper


class TagError(Exception):
	
	def __init__(self, filename, additional_messages=False):
		self.additional_messages = additional_messages
		self.filename = filename

	def __str__(self):
		msg = ("\n ** Grammars defined in element, but no inflections were found.\n"
				"    Check that tags.txt and paradigms.txt include all tags,\n"
				"    and parts to tags.\n"
				"\n"
				"    Alternatively, ensure that <grammar tag /> is a valid tag,\n"
				"    or that <grammar pos /> is a valid PoS.\n"
				"\n"
				"    If the element specification includes an <id />, ensure that\n"
				"    the <id /> refers to a word in the database that has forms  \n"
				"    with the tags specified.\n"
				"\n"
				"\n"
				"	Error occurred in " + self.filename + "\n")
		if self.additional_messages:
			for k, v in self.additional_messages.iteritems():
				values = "\n".join(["        %s" % i for i in v])
				append = ("\n"
						"    %s:\n" % k)
				append += values
				msg += append
		# if self.id_forms:
			# msg += ("\n"
					# "    Word in <id /> has forms matching:\n")
			
			# for item in self.id_forms:
				# msg += "     %s\n" % item

		return msg

class Questions:

	def read_element(self,qaelement,el,el_id,qtype):
		
		semclass = False
		
		elemt_id_msg = "\tCreating element %s (%s)" % (el_id, qaelement.qatype)
		print >> sys.stdout, elemt_id_msg.encode('utf-8')

		# Syntactic function of the element
		if self.grammar_defaults.has_key(el_id) and self.grammar_defaults[el_id].syntax:
			syntax = self.grammar_defaults[el_id].syntax
		else:
			syntax = el_id
		
		if not el:
			_msg = '\t%s - %s' % (syntax, "No element given.")
			print _msg.encode('utf-8')

		# Some of the answer elements share content of question elements.
		content_id = ""
		if el:
			content_id = el.getAttribute("content")
		if not content_id: content_id=el_id
		# Search for the same element in question side
		# If there is no element given in the answer, the element
		# is a copy of the question.
		question_qelements = None
		
		qelems = QElement.objects.filter(question__id=qaelement.question_id,
								identifier=content_id)

		if (not el or el.getAttribute("content")) and \
			QElement.objects.filter(question__id=qaelement.question_id,
									identifier=content_id).count() > 0:
			question_qelements = QElement.objects.filter(question__id=qaelement.question_id,
														 identifier=content_id)
		else:
			if el and el.getAttribute("content"):
				if QElement.objects.filter(question__id=qaelement.id,
										   identifier=content_id).count() > 0:
					question_qelements = QElement.objects.filter(question__id=qaelement.id,
																 identifier=content_id)
		
		# Hmm, maybe not detecting copy correctly
		if not el and question_qelements:
			for q in question_qelements:
				qe = QElement.objects.create(question=qaelement,
											 identifier=el_id,
											 syntax=q.syntax,
											 gametype=qaelement.gametype)  # added by Heli
				# copy = QElement.objects.get(question=qaelement.question,
				#									identifier=el_id,
				#									syntax=q.syntax)
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
			print "\tTRYING verb agreement " + agr_id + " " + qaelement.qatype
			if QElement.objects.filter(question=qaelement, syntax=agr_id,
									   question__qatype=qaelement.qatype).count() > 0:
				agr_elements = QElement.objects.filter(question=qaelement,
													   syntax=agr_id,
													   question__qatype=qaelement.qatype)
		

		agreement = ""
		if el: agreement = el.getElementsByTagName("agreement")
		if agreement: print "\tAgreement:", agreement[0].getAttribute("id")
		
		# Agreement from xml-files
		# Try first inside question or answer
		# Then in answer-question level
		if agreement:
			agr_id=agreement[0].getAttribute("id")
			if QElement.objects.filter(question=qaelement, syntax=agr_id,
									   question__qatype=qaelement.qatype).count() > 0:
				agr_elements = QElement.objects.filter(question=qaelement,
													   syntax=agr_id,
													   question__qatype=qaelement.qatype)
				
			else:
				if Question.objects.filter(id=qaelement.question_id).count() > 0:
					q=Question.objects.filter(id=qaelement.question_id)[0]
					if QElement.objects.filter(question__id=qaelement.question_id,
											   syntax=agr_id).count() > 0:
						agr_elements = QElement.objects.filter(question__id=qaelement.question_id,
															   syntax=agr_id)

			if not agr_elements:
				print "* ERROR: no agreement elements found"
				
		############ WORDS
		# Search for existing word in the database.
		if el: 
			ids = el.getElementsByTagName("id")
		else:
			ids = list()

		words = {}
		word_elements = None
		for i in ids:
			word_id = i.firstChild.data
			word_id_hid = i.getAttribute("hid").strip()
			if word_id:
				if word_id_hid:
					print "\tfound word %s/%s" % (word_id, word_id_hid)
					word_elements = Word.objects.filter(wordid=word_id, hid=int(word_id_hid))
				else:
					print "\tfound word %s" % word_id
					word_elements = Word.objects.filter(wordid=word_id)
				# Add pos information here!
				if not word_elements:
					print "\tWord not found! " + word_id
					
		# Search for existing semtype
		# Semtype overrides the word id selection
		if not word_elements:
			semclasses = []
			if el:
				semclasses = el.getElementsByTagName("sem")
				if semclasses:
					semclass = semclasses[0].getAttribute("class")
					word_elements = Word.objects.filter(semtype__semtype=semclass)
			elif qaelement.question:
				# check question for copy, grab semclasses
				has_copies = QElement.objects.filter(question=qaelement.question,
								identifier=el_id)
				if has_copies:
					semclasses = has_copies.values_list('semtype__semtype', flat=True)
					semclass = semclasses[0]
					word_elements = Word.objects.filter(semtype__semtype=semclass)

			if el: 
				valclasses = el.getElementsByTagName("val")

				if valclasses:
					valclass = valclasses[0].getAttribute("class")
					word_elements = Word.objects.filter(valency=valclass)

		# If still no words, get the default words for this element:
		if not word_elements:
			grammar_def = self.grammar_defaults.get(el_id, False)
			if grammar_def:
				if grammar_def.words:
					word_elements = self.grammar_defaults[el_id].words

		if word_elements:
			for w in word_elements:
				if not words.has_key(w.pos): words[w.pos] = []
				words[w.pos].append(w)

		############# GRAMMAR
		tagelements = None
		grammars = list()
		not_found = []

		if el: 
			grammars = el.getElementsByTagName("grammar")

		if not el or not grammars:
			# If there is no grammatical specification, the element is created
			# solely on the basis of grammar.

			# However, if the element is already defined previously in the
			# sentence, there is no need to create another element. In fact,
			# this could result in weirdness if the element is also defined in
			# the grammar, because otherwise the install process would recreate
			# it with the wrong default tags.

			# If the element is declared in the question, and we are now
			# processing the answer, tags need to be grabbed from the question
			# elements so that the normal copy process can procede, otherwise
			# they are copied from the grammar, which is not what should
			# happen.

			preceding = QElement.objects.filter(question=qaelement, 
												identifier=el_id,)
			
			if qaelement.question:
				has_copies = QElement.objects.filter(question=qaelement.question,
												 identifier=el_id,)
			else:
				has_copies = False

			if preceding:
				print " * Element already declared in the question"
				return
			if has_copies:
				tagelements = sum([list(p.tags.all()) for p in has_copies], [])
			elif self.grammar_defaults.has_key(el_id):
				if self.grammar_defaults[el_id].tags:
					tagelements = self.grammar_defaults[el_id].tags

			if tagelements:
				tagelements = list(set(tagelements))

		# An element for each different grammatical specification.
		else:
			poses = []
			tags = []
			for gr in grammars:
				tags.append(gr.getAttribute("tag"))
				poses.append(gr.getAttribute("pos"))
			tagstrings = []
			if poses:
				if self.grammar_defaults.has_key(el_id):
					if self.grammar_defaults[el_id].tags:
						tagelements = self.grammar_defaults[el_id].tags.filter(pos__in=poses)
			if tags:
				tagstrings = self.get_tagvalues(tags)
				if tagelements:
					tagelements = tagelements or Tag.objects.filter(string__in=tagstrings)
				else:
					tagelements = Tag.objects.filter(string__in=tagstrings)
				
				# print tagelements
				# raw_input()


			# Extra check for pronouns
			# If pronoun id is given, only the tags related to that pronoun are preserved.
			for t in tagelements:
				if t.pos == 'Pron':
					if not words.has_key('Pron'): break
					found = False
					for w in words['Pron'][:]:
						corresponding_forms = Form.objects.filter(tag__in=tagelements,
																	word=w)
						if corresponding_forms.count() > 0:
							found = True
						else:
							# Should pop those that don't match, or else
							# problems may arise
							# TODO: this for other POS
							fenc = lambda x: force_unicode(x).encode('utf-8')
							possible_forms = [repr(w.lemma) + '+' + form.tag.string
												for form in w.form_set.all()]
							not_found.append(
								(list(set(possible_forms)), 
								t.string)
							)
							words['Pron'].pop(words['Pron'].index(w))
					if not found:
						tagelements = tagelements.exclude(id=t.id)

			# Remove those words which do not have any forms with the tags.
			if words.has_key('N'): 
				for w in words['N']:
					found = False
					for t in tagelements:
						if t.pos == 'N':
							if Form.objects.filter(tag=t, word=w).count()>0:
								found = True
					if not found:
						words['N'].remove(w)
			
		# Find different pos-values in tagelements
		posvalues = {}
		task = ""
		# Elements that do not inflection information are not created.
		if not tagelements and not agr_elements:
			print "\tno inflection for", el_id
			if len(grammars) > 0:
				additional_messages = {
					'Grammar tags available for word id':
						sum([a[0] for a in not_found], []),
					'<grammar /> specified':
						[a[1] for a in not_found],
					'question id': [qaelement.qid],
				}
				raise TagError(self.infile_name, additional_messages)
			return

		if not tagelements: 
			posvalues[""] = 1
		else:
			for t in tagelements:
				posvalues[t.pos] = 1

		attempt = False

		if el:
			task = el.getAttribute("task")
			if task:
				print "\tsetting", el_id, "as task"
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
		print '\tCREATING ELEMENTS'
		print '\tElements for the following keys...'
		print '\t' + repr(posvalues.keys())
		# Add an element for each pos:
		for p in posvalues.keys():
			qe = QElement.objects.create(question=qaelement,\
										 identifier=el_id,\
										 syntax=syntax)  
			if semclass:
				semty, _ = Semtype.objects.get_or_create(semtype=semclass)
				qe.semtype = semty
				qe.save()
			else:
				semty = False
			if task:
				qe.task=task
				qe.save()
			
			print '\t\tsemtype: ', semclass
			# Add links to corresponding question elements.
			if question_qelements:
				for q in question_qelements:
					q.copy_set.add(qe)
					qe.save()
					q.save()

			if tagelements:
				for t in tagelements:
					if semty:
						ws_ = Word.objects.filter(semtype=semty)
					elif word_elements:
						ws_ = word_elements
					else:
						ws_ = Word.objects.all()

					if ws_.filter(form__tag=t).count() == 0:
						err_ = "tag:  %s" % t.string
						if semty:
							err_ += u"\t(no matching forms with semtype %s)" % semty
						elif word_elements:
							_msg = force_unicode(','.join(ws_.values_list('lemma', flat=True)))
							err_ += u"\t(no matching forms with words: %s)" % _msg
						print '\t\t%s' % err_
						continue
					if t.pos == p:
						print '\t\ttag: ', t.string
						qe.tags.add(t)

			# Create links to words.
			if not words.has_key(p):
				word_pks = None
				print "\tlooking for words..", el_id, p
				# word_elements = Word.objects.filter(form__tag__in=qe.tags.all()) # pos=p)
				
				# Just filtering isn't enough; .filter() doesn't return a list of unique items with this kind of query. 
				
				if semclass:
					word_pks = Word.objects.filter(form__tag__in=qe.tags.all()).filter(semtype=qe.semtype).values_list('pk', flat=True)
				else:
					word_pks = Word.objects.filter(form__tag__in=qe.tags.all()).values_list('pk', flat=True)

				word_pks = list(set(word_pks))
				if len(word_pks) == 0:
					print 'Error: Elements with zero possibilities not permitted.'
					print ' > ', qe.qid
					print ' > ', qe.question
					print ' > Word tags: %s' % repr(qe.tags.all())
					print ' > semtypes: %s' % repr(qe.semtype)
					sys.exit(2)
				print '\t%d elements available. ' % len(word_pks)
				
				word_elements_gen = (Word.objects.get(pk=int(b)) for b in word_pks)
				
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

		self.infile_name = infile
		self.grammarfile_name = grammarfile
		xmlfile=file(infile)
		tree = _dom.parse(infile)

		self.read_grammar_defaults(grammarfile)

		qs = tree.getElementsByTagName("questions")[0]
		gametype = qs.getAttribute("game")
		if not gametype: gametype="morfa"

		print "Created questions:"
		for q in tree.getElementsByTagName("q"):
			qid = q.getAttribute('id')
			if not qid:
				print "ERROR Missing question id, stopping."
				exit()

			print "\n##"
			print "### INSTALLING QUESTION: %s" % qid.encode('utf-8')
			print "##\n"
				
			level = q.getAttribute('level')
			if not level: level="1"
			lemmacount = q.getAttribute('lemmacount')  # added by Heli
			if not lemmacount: lemmacount="0"
			
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
				questions = Question.objects.filter(qid=qid)
				if questions:
					questions[0].delete()

			question_element,created = Question.objects.get_or_create(qid=qid, \
																	  level=int(level),lemmacount=int(lemmacount), \
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
						book_entry, created = Source.objects.get_or_create(name=book)
						if created:
							print "\tCreated book entry with name ", book
					question_element.source.add(book_entry)
					question_element.save()					

			else:
				book = "all"
				# Add book to the database
				book_entry, created = Source.objects.get_or_create(name=book)
				if created:
					print "\tCreated book entry with name ", book
				question_element.source.add(book_entry)
				question_element.save()

			# Read the elements
			self.read_elements(question, question_element,qtype)	

			# There can be more than one answer for each question,
			# Store them separately.
			answers=q.getElementsByTagName("answer")
			for ans in answers:				
				text=ans.getElementsByTagName("text")[0].firstChild.data
				answer_element = Question.objects.create(string=text,qatype="answer",question=question_element,level=1,lemmacount=0)

				answer_element.save()
				self.read_elements(ans, answer_element, qtype)
			db.reset_queries() 


	def read_grammar_defaults(self, infile):
		""" Read a grammar file and make the results accessible in 
		self.grammar_defaults

		This has the structure:
			{
				'SUBJ': {
					'pos': [u'N', u'Pron'],
					'tags': [<Tag: N+Sg+Nom>, <Tag: N+Pl+Nom>, etc...]
				},
				'N-LOC': {
					'pos': [u'N'],
					'tags': [<Tag N+Sg+Loc>, <Tag: N+Pl+Nom>, etc...]
				},
			}

			<element id="SUBJ">
				<grammar pos="Pron" tag="Pron+Pers+Person-Number+Nom"/>
				<grammar pos="N" tag="N+NumberN+Nom"/>
			</element>

			{
				'SUBJ': 
			}
		"""

		class GrammarDefaultError(Exception):
			def __init__(self, element=False, tagstrings=False):
				self.element = element
				self.tagstrings = tagstrings

			def __str__(self):
				msg = (
				"\n ** No tags were present in the database matching\n"
				)
				if self.element:
					msg += "    grammar element: %s\n" % self.element
				else:
					msg += "    an unknown grammar element\n"

				if self.tagstrings:
					msg += "    with the following expanded tag strings:\n"
					msg += "      " + "      ".join(self.tagstrings)
				
				msg += "\n    Check that these words/forms are installed"
				return msg

		class GrammarDefault(object):

			Error = GrammarDefaultError

			def __init__(self, 
						poses=False, 
						tags=False, 
						words=False, 
						syntax=False):

				self.tags = tags or list()
				self.poses = poses or list()
				self.words = words or list()
				self.syntax = syntax or list()

			def __str__(self):
				returns = []

				if self.poses:
					returns.append('|'.join(self.poses) + ' - ')

				if self.tags:
					returns.append(', '.join([t.string for t in self.tags]))
				else:
					if self.poses:
						returns.append('None')
				if self.words:
					returns.append(', '.join([w.lemma for w in self.words]))

				if self.syntax:
					returns.append(', '.join(self.syntax))

				return ' '.join(returns)

			def __repr__(self):
				return '<GrammarDefault: %s>' % str(self)
	
		xmlfile = file(infile)
		tree = _dom.parse(infile)

		self.grammar_defaults = {}
		
		tags = tree.getElementsByTagName("tags")[0]
		elements = tags.getElementsByTagName("element")

		for el in elements:
			identifier = el.getAttribute("id")
			
			grammar_default = GrammarDefault()
			
			word_id = None
			word = None
			
			syntax = ""
			syntaxes = el.getElementsByTagName("syntax")
			if syntaxes:
				syntax = syntaxes[0].firstChild.data
				grammar_default.syntax = syntax
				
			word_ids = el.getElementsByTagName("id")
			if word_ids:
				word_id = word_ids[0].firstChild.data
				word_id_hid = word_ids[0].getAttribute("hid").strip()
				if word_id:
					words = Word.objects.filter(wordid=word_id)
					if word_id_hid:
						words = words.filter(hid=int(word_id_hid))
					grammar_default.words = words

			tagstrings = []

			grammars = el.getElementsByTagName("grammar")
			for gr in grammars:
				pos = gr.getAttribute("pos")
				if pos:
					grammar_default.poses.append(pos)

				tag = gr.getAttribute("tag")
				tagstrings.extend(self.get_tagvalues([tag]))

			if len(tagstrings) > 0:
				tags = Tag.objects.filter(string__in=tagstrings)
				if tags.count() == 0:
					tag_elements = ', '.join([e.toprettyxml() for e in grammars])
					raise GrammarDefault.Error(element=tag_elements,
												tagstrings=tagstrings)
				else:
					grammar_default.tags = tags
				
			self.grammar_defaults[identifier] = grammar_default

	def get_tagvalues(self, tags):
		""" This alters state of things without returning objects 

			Recurses through set of supplied tags to ensure that each element
			is represented in tags.txt and paradigms.txt. """

		def fill_out(tags):
			from itertools import product

			def make_list(item):
				if type(item) == list:
					return item
				else:
					return [item]

			return list(product(*map(make_list, tags)))

		def parse_tag(tag):
			""" Iterate through a tag string by chunks, and check for tag sets
			and tag names. Return the reassembled tag on success. """

			tag_string = []
			for item in tag.split('+'):
				if Tagname.objects.filter(tagname=item).count() > 0:
					tag_string.append(item)
				elif Tagset.objects.filter(tagset=item).count() > 0:
					tagnames = Tagname.objects.filter(tagset__tagset=item)
					tag_string.append([t.tagname for t in tagnames])
				else:
					tag_string.append(item)

			if len(tag_string) > 0:
				# ++ -> + in order to support % as null in tags.txt
				return ['+'.join(item).replace('++', '+') for item in fill_out(tag_string)]
			else:
				return False

		if type(tags) == list:
			tags = [a for a in tags if a]
			parsed = sum(map(parse_tag, tags), [])
			return parsed
		else:
			return False

	def delete_question(self, qid=None):
		
		if qid:
			questions = Question.objects.filter(qid=qid)
			if questions:
				for q in questions:
					q.delete()

			questions = Question.objects.filter(string=qid)
			if questions:
				for q in questions:
					q.delete()
