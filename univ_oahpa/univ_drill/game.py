# -*- coding: utf-8 -*-

from univ_oahpa.univ_drill.models import *
from univ_oahpa.univ_drill.forms import *

from univ_oahpa.conf.tools import switch_language_code

from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from django.core.exceptions import ObjectDoesNotExist
from random import randint

import os
import re
import itertools

import univ_oahpa.settings

# DEBUG = open('/dev/ttys001', 'w')

from random import choice

try:
	L1 = univ_oahpa.settings.L1
except:
	L1 = 'sme'

try:
	LOOKUP_TOOL = univ_oahpa.settings.LOOKUP_TOOL
except:
	LOOKUP_TOOL = 'lookup'


try:
	FST_DIRECTORY = univ_oahpa.settings.FST_DIRECTORY
except:
	FST_DIRECTORY = False

try:
	DEFAULT_DIALECT = univ_oahpa.settings.DEFAULT_DIALECT
except:
	DEFAULT_DIALECT = None


# FST_DIRECTORY = '/opt/smi/sme/bin' #Just testing. Hardcoded here because it looks like looking it up in settings.py failed
# LOOKUP_TOOL = '/usr/local/bin/lookup'

""" moved to forms.py
def relax(strict):
	Returns a list of relaxed possibilities, making changes by relax_pairs.
		
		Many possibilities are generated in the event that users are
		inconsistent in terms of substituting one letter but not substituting 
		another, however, *all* possibilities are not generated.
		
		E.g., *ryøjnesjäjja is accepted for ryöjnesjæjja
				(user types ø instead of ö consistently)
				
				... but ...
			  
			  *töølledh is not accepted for töölledh
				(user mixes the two in one word)
		
		Similarly, directionality is included. <i> is accepted for <ï>, but
		not vice versa.
		
		E.g.:  *ååjmedïdh is not accepted for ååjmedidh, 
				... but ...
				*miele is accepted for mïele.
	
	from django.utils.encoding import force_unicode
	
	relaxed = strict
	sub_str = lambda _string, _target, _sub: _string.replace(_target, _sub)
	
	relax_pairs = {
		# key: value
		# key is accepted for value
		u'ø': u'ö',
		u'ä': u'æ',
		u'i': u'ï'
	}
	
	# Create an iterator. We want to generate as many possibilities as 
	# possible (very fast), so more relaxed options are available.
	searches = relax_pairs.items()
	permutations = itertools.chain(itertools.permutations(searches))
	perms_flat = sum([list(a) for a in permutations], [])
	
	# Individual possibilities
	relaxed_perms = [sub_str(relaxed, R, S) for S, R in perms_flat]
	
	# Possibilities applied one by one
	for S, R in perms_flat:
		relaxed = sub_str(relaxed, R, S)
		relaxed_perms.append(relaxed)
	
	# Return list of unique possibilities
	relaxed_perms = list(set(relaxed_perms))
	relaxed_perms = [force_unicode(item) for item in relaxed_perms]

	return relaxed_perms
"""

class Info:
	pass

class Game(object):
	def __init__(self, settings):
		self.query_set = False
		self.lemmas_selected = []
		self.form_list = []
		self.count = ""
		self.score = ""
		self.comment = ""
		self.settings = settings
		self.all_correct = ""
		self.show_correct = 0
		self.num_fields = 6
		self.global_targets = {}
		# .has_key deprecated, is there a way to use in with this?
		if not self.settings.has_key('gametype'):
			self.settings['gametype'] = "bare"
		
		if self.settings.has_key('semtype'):
			if self.settings['semtype'] in ('all','All'):  # upper- or lowercase
				# self.settings['semtype'] = self.settings['allsem']
				self.settings['semtype'] = 'all'
			else:
				semtype = self.settings['semtype'][:]
				self.settings['semtype'] = []
				self.settings['semtype'].append(semtype)

	def new_game(self):
		self.form_list = []
		word_ids = []
		i = 1
		num = 0
		# if self.settings['pos'] == 'Pron':
			# print 'omg'
			# for i in range(self.num_fields):
				# db_info = {}
				# db_info['userans'] = ""
				# db_info['correct'] = ""
				
				# errormsg = self.get_db_info(db_info)

				# form, word_id = self.create_form(db_info, i, 0)
				# print form
		# else:

		# Use this to make sure that pronouns don't have repeated
		# pronouns
		existing_tags = []
		
		# Can this be changed? Self.create_form should go without fail.
		tries = 0
		maxtries = 40
		
		while i < self.num_fields and len(self.form_list) < 5 and tries < maxtries:
			tries += 1
			db_info = {}
			db_info['userans'] = ""
			db_info['correct'] = ""
			
			errormsg = self.get_db_info(db_info)
			
			if errormsg and errormsg == "error":
				# i = i+1
				continue
				# raise Http404(errormsg)
			
			form = None
			
			try:
				form, word_id = self.create_form(db_info, i, 0)
			except Http404, e:
				raise e
			except ObjectDoesNotExist:
				continue
						
			# Do not generate same question twice
			if word_id:
				num = num + 1
				if word_id in set(word_ids):
					continue
				else: word_ids.append(word_id)
		
			self.form_list.append(form)
			i = i+1
		
		# print len(self.form_list)
		if tries == maxtries:
			raise Http404('No questions were able to be generated.')
		if not self.form_list:
			# No questions found, so the quiz_id must have been bad.
			raise Http404('Invalid quiz id.')
		
	def search_info(self, reObj, string, value, words, t_type):
		matchObj = reObj.search(string)
		if matchObj:
			syntax = matchObj.expand(r'\g<syntaxString>')
			if not words.has_key(syntax):
				words[syntax] = {}
			
			words[syntax][t_type] = value
		return words
	
				
	def check_game(self, data=None):
		db_info = {}
		
		question_tagObj = re.compile(r'^question_tag_(?P<syntaxString>[\w\-]*)$', re.U)
		question_wordObj = re.compile(r'^question_word_(?P<syntaxString>[\w\-]*)$', re.U)
		question_fullformObj = re.compile(r'^question_fullform_(?P<syntaxString>[\w\-]*)$', re.U)
		answer_tagObj = re.compile(r'^answer_tag_(?P<syntaxString>[\w\-]*)$', re.U)
		answer_wordObj = re.compile(r'^answer_word_(?P<syntaxString>[\w\-]*)$', re.U)
		answer_fullformObj = re.compile(r'^answer_fullform_(?P<syntaxString>[\w\-]*)$', re.U)
		targetObj = re.compile(r'^target_(?P<syntaxString>[\w\-]*)$', re.U)
		
		# Collect all the game targets as global variables
		self.global_targets = {}
		
		# If POST data was data check, regenerate the form using ids.
		# This iterates through forms in list of forms
		for n in range (1, self.num_fields):
			db_info = {}
			qwords = {}
			awords = {}
			tmpawords = {}
			
			# This compiles a dictionary from all of the form fields
				# {u'answer': u'', 
				# u'userans': u'empty', 
				# u'correct': u'empty', 
				# u'tag_id': u'66', 
				# u'word_id': u'628'}
			
			for fieldname, value in data.items():
				# print >> DEBUG, d, value
				if fieldname.count(str(n) + '-') > 0:
					fieldname = fieldname.lstrip(str(n) + '-')
					qwords = self.search_info(question_tagObj, fieldname, value, qwords, 'tag')
					qwords = self.search_info(question_wordObj, fieldname, value, qwords, 'word')
					qwords = self.search_info(question_fullformObj, fieldname, value, qwords, 'fullform')
					
					tmpawords = self.search_info(answer_tagObj, fieldname, value, tmpawords, 'tag')
					tmpawords = self.search_info(answer_wordObj, fieldname, value, tmpawords, 'word')
					tmpawords = self.search_info(answer_fullformObj, fieldname, value, tmpawords, 'fullform')
					
					self.global_targets = self.search_info(targetObj, fieldname, value, self.global_targets, 'target')
					
					db_info[fieldname] = value
					
			
			
			# This appears to not be used for leksa and morfa
			# Or if it is to be used with morfa, last stanza has problem.
			# Furthermore, qwords has no keys, and thus doesn't iterate.
			for syntax in qwords.keys():
				if qwords[syntax].has_key('fullform'):
					qwords[syntax]['fullform'] = [qwords[syntax]['fullform']]
			
			# This also appears to not be used for leksa and morfa
			# Or else there's a problem in the initial forloop.
			# Dictionary here comes out empty.
			# tmpawords doesn't iterate here; no keys
			for syntax in tmpawords.keys():
				awords[syntax] = []
				info = {}
				if tmpawords[syntax].has_key('word'):
					info['word'] = tmpawords[syntax]['word']
					if tmpawords[syntax].has_key('tag'):
						info['tag'] = tmpawords[syntax]['tag']
					if tmpawords[syntax].has_key('fullform'):
						info['fullform'] = [ tmpawords[syntax]['fullform']]
					
					awords[syntax].append(info)
				# print info
			
			
			db_info['awords'] = awords
			db_info['qwords'] = qwords
			db_info['global_targets'] = self.global_targets
			
			new_db_info = {}
			
			# Generate possible answers for contextual Morfa.
			if self.settings.has_key('gametype') and self.settings['gametype'] == 'context':
				new_db_info = self.get_db_info(db_info)
			if not new_db_info:
				new_db_info = db_info
			form, word_id = self.create_form(new_db_info, n, data)
			if form:
				self.form_list.append(form)
	
	def get_score(self, data):
		
		# Add correct forms for words to the page
		if "show_correct" in data:
			self.show_correct = 1
			
			for form in self.form_list:
				form.set_correct()
				
				self.count = 2
		
		# Count correct answers:
		self.all_correct = 0
		self.score = ""
		self.comment = ""
		i = 0
		
		points = sum([1 for form in self.form_list if form.error == "correct"])
		
		if points == len(self.form_list):
			self.all_correct = 1
		
		if self.show_correct or self.all_correct:
			self.score = self.score.join([repr(i), "/", repr(len(self.form_list))])
		
		if (self.show_correct or self.all_correct) and not self.settings['gametype'] == 'qa' :
			if i == 2:
				i = 3
			if i == 1:
				i = 2
			if self.settings.has_key('language'):
				language = switch_language_code(self.settings['language'])
				
				com_count = Comment.objects.filter(Q(level=i) & Q(lang=language)).count()
				if com_count > 0:
					self.comment = Comment.objects.filter(Q(level=i) & Q(lang=language))[randint(0,com_count-1)].comment
		
		self.score = '%d/%d' % (points, len(self.form_list))


class BareGame(Game):
	
	casetable = {
		'NOMPL': 'Nom', 
		'ATTR': 'Attr',
		'PRED': 'Pred', 
		#'N-NOM': 'Nom',
		'N-ILL': 'Ill', 
		'N-ESS': 'Ess', 
		'N-GEN': 'Gen',
		'N-LOC': 'Loc',
		'N-ACC': 'Acc', 
		'N-COM': 'Com',
		'A-ATTR': 'Attr',
		'COMP': 'Comp', # was: A-COMP
		'SUPERL': 'Superl', # was: A-SUPERL
		'POS':'',
		'CARD': 'Num', # these 3 added for implementing num_type choice
		'ORD': 'A+Ord',
		'COLL': 'N+Coll',
		'': ''
	}
	
	def get_baseform(self, word_id, tag):
		
		basetag = None
		
		if tag.pos in ["N", "A", "Num", "Pron"]:
			if tag.number and tag.case != "Nom":
				tagstring = tag.pos + "+" + tag.number + "+Nom"
			else:
				tagstring = tag.pos + "+Sg" + "+Nom"
			if Form.objects.filter(word__pk=word_id, tag__string=tagstring).count() > 0:
				basetag = Tag.objects.filter(string=tagstring)[0]
		
		if tag.pos=="V":
			tagstring = "V+Inf"
			if Form.objects.filter(word__pk=word_id,tag__string=tagstring).count() > 0:
				basetag = Tag.objects.filter(string=tagstring)[0]
		
		return basetag
	
	def get_db_info(self, db_info):
		
		if self.settings.has_key('pos'):
			pos = self.settings['pos']

		
		syll = True and	self.settings.get('syll')	or   "All"
		case = True and	self.settings.get('case')	or   ""
		levels = True and  self.settings.get('level')   or   []
		adjcase = True and self.settings.get('adjcase') or   ""
		pron_type = True and self.settings.get('pron_type') or   ""
		proncase = True and self.settings.get('proncase') or   ""
		grade = True and self.settings.get('grade')   or   ""
		source = ""
		
		mood, tense, infinite, attributive = "", "", "", ""

		num_bare = ""
		# if self.settings.has_key('syll'):
		# 	syll = self.settings['syll']
		# if self.settings.has_key('case'):
		# 	case = self.settings['case']
		# if self.settings.has_key('level'):
		# 	levels = self.settings['level']
		# if self.settings.has_key('adjcase'):
		# 	adjcase = self.settings['adjcase']
		if self.settings.has_key('source'):  # was: book, but in forms.py it is called source
			source = self.settings['source']
			if source.lower() != 'all':
				try:
					S = Source.objects.filter(name=source)
					source = S
				except Source.DoesNotExist:
					source = False
			else:
				source = False
		if self.settings.has_key('num_bare'):
			num_bare = self.settings['num_bare']
		if self.settings.has_key('num_level'):
			num_level = self.settings['num_level']
		if self.settings.has_key('num_type'):  # added by Heli
			num_type = self.settings['num_type']	
		if self.settings.has_key('grade'):
			grade = self.settings['grade']

		pos_tables = {
			"N":	case,
			"A":	adjcase,
			"Num":  num_bare,
			"V":	"",
			"Pron": proncase,
		}
		
		sylls = []
		bisyl = ['2syll', 'bisyllabic']
		trisyl = ['3syll', 'trisyllabic']
		Csyl = ['Csyll', 'contracted'] # added for sme

		for item in syll:
			if item in bisyl:
				sylls.append('2syll')
			if item in trisyl:
				sylls.append('3syll')
			if item in Csyl:
				sylls.append('Csyll')
		
		if pos == 'Pron':
			syll = ['']
		
		case = self.casetable[pos_tables[pos]]
		grade = self.casetable[grade]
		num_type = self.casetable[num_type] # added by Heli
		
		pos_mood_tense = {
			"PRS":	("Ind", "Prs", ""),
			"PRT":	("Ind", "Prt", ""),
			"PRF":	("", "", "PrfPrc"),
			"GER":	("", "", "Ger"),
			"COND":   ("Cond", "Prs", ""),
			"IMPRT":  ("Imprt", "", ""),
			"POT":	("Pot", "Prs", "")
		}
		
		if pos == "V" and self.settings.has_key('vtype'):
			mood, tense, infinite = pos_mood_tense[self.settings['vtype']]
		
		
		number = ["Sg","Pl",""]
		
		if case == "Ess":
			number = [""] 
		elif case == "Nom" and pos != "Pron":
			number = ["Pl"]
		else:
			number = ["Sg","Pl"]  # added by Heli

		# A+Sg+Nom
		
		# following values are in grade
		# A+Comp+Sg+Nom
		# A+Superl+Sg+Nom

		# following value is in case
		# A+Attr
		if pos == 'A':
			if "Attr" in [attributive, case]: 
				attributive = "Attr"
				case = ""  
				number = [""]
			else:			
				attributive = ""  		
		
		maxnum, i = 20, 0
		
		TAG_QUERY = Q(pos=pos)
		
		TAG_EXCLUDES = False
		
		FORM_FILTER = False

		# Query filtering on words
		# SUB_QUERY = Q(word__stem__in=sylls)
		SUB_QUERY = False

		if pos in ['Pron', 'N', 'Num']:
			TAG_QUERY = TAG_QUERY & \
						Q(case=case)
						# regardless of whether it's Actor, Coll, etc.

			if pos == 'N':
				TAG_QUERY = TAG_QUERY & \
							Q(possessive="") & \
							Q(number__in=number)

			# 'Pers' subclass for pronouns, otherwise none.
			# TODO: combine all subclasses so forms can be fetched
			if pos == 'Pron':
				sylls = False
				TAG_QUERY = TAG_QUERY & Q(subclass=pron_type)
			else:
				TAG_QUERY = TAG_QUERY & Q(subclass='')

			if pos == 'Num':
				TAG_QUERY = TAG_QUERY & Q(subclass='')
				if num_level == '1':  # Numerals in Sg on level 1
				    TAG_QUERY = TAG_QUERY & Q(number='Sg')
				else:  # Numerals in both Sg and Pl on level 1-2
					TAG_QUERY = TAG_QUERY & Q(number__in=['Sg','Pl'])
				if num_type == 'ORD':  # Card / Ord / Coll
					TAG_QUERY = TAG_QUERY & Q(tag__string__contains="A+Ord")
				elif num_type == 'COLL':
					TAG_QUERY = TAG_QUERY & Q(tag__string__contains="N+Coll")
                    
		if pos == 'V':
			TAG_QUERY =  TAG_QUERY & \
							Q(tense=tense) & \
							Q(mood=mood) & \
							Q(infinite=infinite)

			if tense != 'Prs':
				TAG_EXCLUDES = Q(string__contains='ConNeg')
			
		if pos == 'A':
			base_set = Form.objects.filter(Q(tag__string__contains="A+") & (Q(tag__string='A+Attr') | Q(tag__string__contains='Nom')))
			TAG_QUERY = Q(pos="A") & \
						Q(attributive=attributive) & \
						Q(grade=grade) & \
						Q(case=case) & \
						Q(number__in=number)
		# case -> adjcase ?
		
		# filter can include several queries, exclude must have only one
		# to work successfully
		tags = Tag.objects.filter(TAG_QUERY)\
							.exclude(subclass='Prop')\
							.exclude(polarity='Neg')
			
		if TAG_EXCLUDES:
			tags = tags.exclude(TAG_EXCLUDES)

		if tags.count() == 0:
			keys = ['pos', 'case', 'tense', 'mood', 'attributive', 'grade', 'number']
			values = [pos, case, tense, mood, attributive, grade, number]
			error = "Morfa.get_db_info: Database is improperly loaded.\
					 No tags for the query were found.\n\n\
					 %s\n\n\
					 %s" % (TAG_QUERY, SUB_QUERY)

			if TAG_EXCLUDES:
				error += "\nexcludes: %" % TAG_EXCLUDES

			raise Http404(error)
		
		if self.settings['pos'] == "Num":
			if self.settings.has_key('num_level') and str(self.settings['num_level']) == "1":
				smallnum = ["1","2","3","4","5","6","7","8","9","10"]
				QUERY = Q(pos__iexact=pos) & Q(presentationform__in=smallnum)
			else:
				QUERY = Q(pos__iexact=pos)
		else:
			# levels is not what we're looking for
			QUERY = Q(pos__iexact=pos) & Q(stem__in=syll)
			if source and source not in ['all', 'All']:
				QUERY = QUERY & Q(source__name=source)
				
		error = "Morfa.get_db_info: Database is improperly loaded.\
				 There are no Words, Tags or Forms, or the query\
				 is not returning any."
		NoWordsFound = Http404(error)
		
		# settings dialect?
		if self.settings.has_key('dialect'):
			UI_Dialect = self.settings['dialect']
		else:
			UI_Dialect = DEFAULT_DIALECT

		try:
			tag = tags.order_by('?')[0]
			
			no_form = True
			count = 0
			while no_form and count < 10:

				# Pronouns are a bit different, so we need to resort the tags
				if tag.pos == 'Pron':
					tag = tags.order_by('?')[0]

				random_word = tag.form_set.filter(word__language=L1)

				if sylls:
					random_word = random_word.filter(word__stem__in=sylls)
				if source:
					random_word = random_word.filter(word__source__in=source)
				if random_word.count() > 0:
					random_form = random_word.order_by('?')[0]
					random_word = random_form.word
					no_form = False
					break
				elif random_word.count () == 1:
					random_form = random_word[0]
					random_word = random_form.word
					break
				else:
					count += 1
					continue

			db_info['word_id'] = random_word.id
			db_info['tag_id'] = tag.id

		except IndexError:
			wc = Word.objects.count()
			tc = Tag.objects.count()
			fc = Form.objects.count()
			wfc = Word.objects.filter(QUERY).count()
			tfc = Tag.objects.filter(TAG_QUERY).count()
			if 0 in [tc, wc, fc, wfc, tfc]:
				# print error
				error += "Word count (%d), Tag count (%d), Form count (%d), Words matching query (%d), Tags matching query (%d)." % (wc, tc, fc, wfc, tfc)
				error += "\n  Query: %s" % repr(QUERY)
				error += "\n  Tag Query: %s" % repr(TAG_QUERY)
				raise Http404(error)
		return
	
	
	def create_form(self, db_info, n, data=None):
		language = self.settings['language']
		pos = self.settings['pos']
		
		if self.settings.has_key('dialect'):
			UI_Dialect = self.settings['dialect']
		else:
			UI_Dialect = DEFAULT_DIALECT

		Q_DIALECT = Dialect.objects.get(dialect=UI_Dialect)
		
		if not db_info.has_key('word_id'):
			return None, None
		
		word_id = db_info['word_id']
		
		tag_id = db_info['tag_id']
		
		tag = Tag.objects.get(id=tag_id)
		
		if pos == 'Pron':
			# Need to filter by lemma for pronouns
			pronoun_lemma = Word.objects.get(id=word_id).lemma
			form_list = Form.objects.filter(tag=tag, word__lemma=pronoun_lemma)
		else:
			form_list = Form.objects.filter(word__id=word_id, tag=tag)
		
		if not form_list:
			raise Form.DoesNotExist
		# print ', '.join([a.fullform for a in form_list])
		correct = form_list[0]
		
		if pos in ['N', 'V', 'A', 'Num']: # added Num
			word = Word.objects.get(Q(id=word_id))
			# Preserve number in nouns: Sg-Sg, Pl-Pl
		elif pos == 'Pron':
			word = correct.word
		
		# Get baseform, matching number; except for in essive where
		# there is no number, and with Nominative, where the test is
		# about turning nominative singular into nominative plural, 
		# thus all baseforms should be singular.

		if tag.case in ['Ess', 'Nom']:
			match_number = False
		else:
			match_number = True
		
		
		def baseformFilter(form):
			#   Get baseforms, and filter based on dialects.
				
			#	NOTE: Need to use getBaseform on Form object, not Word, 
			#	because Word.getBaseform doesn't pay attention to number.

			if self.settings.has_key('dialect'):
				UI_Dialect = self.settings['dialect']
			else:
				UI_Dialect = DEFAULT_DIALECT
			
			bfs = form.getBaseform(match_num=match_number, return_all=True)

			excluded = bfs.exclude(dialects__dialect='NG')
			filtered = excluded.filter(dialects__dialect=UI_Dialect)

			# If no non-NG forms are found, then we have to display those.
			if filtered.count() == 0 and excluded.count() > 0:
				return list(excluded)
			else:
				return list(filtered)

		
		base_forms = [baseformFilter(form) for form in form_list]

		# Flatten
		base_forms = sum(base_forms, [])
		
		# Just in case multiple are returned, get the first.
		try:
			baseform = list(set(base_forms))[0]
		except IndexError:
			if len(base_forms) == 0:
				baseform = form.getBaseform(match_num=match_number)
		
		target_key = switch_language_code(self.settings['language'][-3::])
		
		translations = sum([w.word_answers for w in word.translations2(target_key).all()],[])
		
		# All possible forms
		fullforms = form_list.values_list('fullform',flat=True)
		
		# Just the ones we want to present for just one dialect
		present = form_list.filter(dialects=Q_DIALECT)
		
		# Unless there aren't any ... 
		if present.count() == 0:
			present = form_list
		
		# Exclude those that shouldn't be displayed, but should be accepted
		present_ng = present.exclude(dialects__dialect='NG')
		
		# Unless this results in none... 

		if present_ng.count() == 0:
			present_ng = present
		
		present_ng = present_ng.values_list('fullform',flat=True)
		
		# print tag.string, repr(correct)
		morph = (MorfaQuestion(
					word=word,
					tag=tag,
					baseform=baseform, 
					correct=correct,
					fullforms=fullforms,
					present=present_ng,
					translations=translations,
					question="",
					dialect=Q_DIALECT,
					language=language,
					userans_val=db_info['userans'],  # TODO: userans not in use?
					correct_val=db_info['correct'],
					data=data,
					prefix=n)
				)
		return morph, word_id
		
	


class NumGame(Game):
	generate_fst = 'sme-num.fst'
	answers_fst = 'sme-inum.fst'
	
	def get_db_info(self, db_info):
		""" Options supplied by views
			ord, card - obvious
			kl1 - easy clock (half hours only)
			kl2 - medium clock (quarter hours)
			TODO: kl3 - difficult clock (all numbers??)
		"""
		numeral=""
		num_list = []
		
		random_num = randint(1, int(self.settings['maxnum']))
		
		db_info['numeral_id'] = str(random_num)
		
		if self.settings['gametype'] == 'ord':
			db_info['numeral_id'] += "."
		
		return db_info
		
	def generate_forms(self, forms, fstfile):
		import subprocess
		from threading import Timer
		
		lookup = LOOKUP_TOOL
		gen_norm_fst = FST_DIRECTORY + "/" + fstfile
		try:
			open(gen_norm_fst)
		except IOError:
			raise Http404("File %s does not exist." % gen_norm_fst)
		
		gen_norm_command = [lookup, "-flags", "mbTT", "-utf8", "-d", gen_norm_fst]
		
		try:
			forms.encode('utf-8')
		except UnicodeDecodeError:
			pass
	
		num_proc = subprocess.Popen(gen_norm_command, 
									stdin=subprocess.PIPE, 
									stdout=subprocess.PIPE, 
									stderr=subprocess.PIPE)
		
		def kill_proc(proc=num_proc):
			try:
				proc.kill()
				raise Http404("Process for %s took too long." % ' '.join(gen_norm_command))
			except OSError:
				pass
			return
		
		t = Timer(5, kill_proc)
		t.start()
		output, err = num_proc.communicate(forms)

		return output, err
	
	def clean_fst_output(self, output):
		num_tmp = output.decode('utf-8').splitlines()
		cleaned = []
		for num in num_tmp:
			line = num.strip()
			# line = line.replace(' ','')
			if line:
				nums = line.split('\t')
				if len(nums) == 3:
					nums = (nums[0], '?')
				else:
					nums = tuple(nums)
			cleaned.append(nums)
		return cleaned
	
	def strip_unknown(self, analyses):
		return [a for a in analyses if a[1] != '?']
	
	def check_answer(self, question, useranswer, formanswer):
		gametype = self.settings['numgame']
		# print gametype
		if useranswer.strip():
			forms = useranswer.encode('utf-8')
			
			if gametype == 'string':
				fstfile = self.generate_fst
			elif gametype == 'numeral':
				fstfile = self.answers_fst
			
			output, err = self.generate_forms(forms, fstfile)
			
			num_list = self.clean_fst_output(output)
			num_list = self.strip_unknown(num_list)
			# print repr([question, useranswer, num_list])
			
			# 'string' refers to the question here, not the answer
			if gametype == 'string':
				# user answer must match with numeral generated from
				# the question
				
				if useranswer in [a[0] for a in num_list] and \
					question in [a[1] for a in num_list]:
					return True
				else:
					return False

			elif gametype == 'numeral':
				# Numbers generated from user answer must match up
				# with numeral in the question
				num_list = num_list + formanswer
				try:
					_ = int(useranswer)
					return False
				except ValueError:
					pass
				if question in [a[1] for a in num_list] or \
					useranswer in num_list:
					return True
				else:
					return False

			

	def create_form(self, db_info, n, data=None):
		
		if self.settings['gametype'] in ["ord", "card"]:
			language = L1
		else:
			language = L1

		numstring = ""
		
		fstfile = self.generate_fst
		q, a = 0, 1

		# production paths
		lookup = "%s\n" % db_info['numeral_id']
		output, err = self.generate_forms(lookup, fstfile)
		
		num_tmp = output.splitlines()
		num_list = []
		for num in num_tmp:
			line = num.strip()
			line = line.replace(' ','')
			if line:
				nums = line.split('\t')
				num_list.append(nums[a].decode('utf-8'))
		try:
			numstring = num_list[0]
		except IndexError:
			error = "Morfa.NumGame.create_form: Database is improperly loaded, \
					 or Numra is unable to look up words."
			raise Http404(error)
		
		form = (NumQuestion(
					numeral=db_info['numeral_id'],
					num_string=numstring,
					num_list=num_list,
					gametype=self.settings['numgame'],
					userans_val=db_info['userans'],
					correct_val=db_info['correct'],
					data=data,
					prefix=n,
					game=self)
				)
		
		return form, numstring

from forms import KlokkaQuestion

class Klokka(NumGame):

	QuestionForm = KlokkaQuestion
	
	generate_fst = 'iclock-sme.fst'
	answers_fst = 'clock-sme.fst'

	error_msg = "Morfa.Klokka.create_form: Database is improperly loaded, \
					 or Numra is unable to look up words."

	def get_db_info(self, db_info):
		
		hour = str(randint(0, 23))
		
		if len(hour) == 1:
			hour = '0' + hour
		else:
			hour = str(hour)
		if self.settings['gametype'] == "kl1":
			min_options = ['00', '30']
			minutes = choice(min_options)
		elif self.settings['gametype'] == "kl2":
			min_options = ['00', '15', '30', '45']
			minutes = choice(min_options)
		elif self.settings['gametype'] == "kl3":
			mins = str(randint(0, 59))
			if len(mins) == 1:
				mins = '0' + mins
			minutes = mins

		random_num = '%s:%s' % (hour, minutes)

		db_info['numeral_id'] = str(random_num)

		return db_info
	
	
	def check_answer(self, question, useranswer, formanswer):
		# TODO: in string->num, need to display the corresponding numeral if
		# it is one that can be 14 hour time
		gametype = self.settings['numgame']
		if useranswer.strip():
			forms = useranswer.encode('utf-8')
			
			if gametype == 'string':
				fstfile = self.generate_fst
			elif gametype == 'numeral':
				fstfile = self.answers_fst
			
			output, err = self.generate_forms(forms, fstfile)
			
			num_list = self.clean_fst_output(output)
			num_list = self.strip_unknown(num_list)
			# print repr([question, useranswer, num_list])
			
			# 'string' refers to the question here, not the answer
			if gametype == 'string':
				# user answer must match with numeral generated from
				# the question
				
				if useranswer in [a[0] for a in num_list] and \
					question in [a[1] for a in num_list]:
					return True
				else:
					return False

			elif gametype == 'numeral':
				# Numbers generated from user answer must match up
				# with numeral in the question

				# Bug in numeral game seems to be presenting wrong set of numerals, 
				# so if answerset contains 13+, need to remove and take the lower.
				# Or 'militaryrelax' the answer

				num_list = num_list + formanswer
				try:
					_ = int(useranswer)
					return False
				except ValueError:
					pass
				if question in [a[1] for a in num_list] or \
					useranswer in num_list:
					return True
				else:
					return False

	def create_form(self, db_info, n, data=None):
		if self.settings['gametype'] in ["kl1", "kl2", "kl3"]:
			language = L1

		numstring = ""

		fstfile = self.generate_fst
		q, a = 0, 1
	
		lookup = "%s\n" % db_info['numeral_id']

		# lookup = "%s\n" % db_info['numeral_id']
		output, err = self.generate_forms(lookup, fstfile)
		
		# norm, allnum = output.split('\n\n')[0:2]
		
		norm_list = []
		for num in output.decode('utf-8').splitlines():
			line = num.strip()
			if line:
				nums = line.split('\t')
				norm_list.append(nums[a])

		try:
			numstring = norm_list[0]
		except IndexError:
			raise Http404(self.error_msg)
		
		form = (self.QuestionForm(
					numeral=db_info['numeral_id'],
					num_string=numstring,
					present_list=norm_list,
					accept_list=norm_list,
					gametype=self.settings['numgame'],
					userans_val=db_info['userans'],
					correct_val=db_info['correct'],
					data=data,
					prefix=n,
					game=self)
				)
		
		return form, numstring

##
#
#  Dato
#
##

class Dato(Klokka):
	from forms import DatoQuestion as QuestionForm

	# QuestionForm = DatoQuestion
	
	generate_fst = 'idate-sme.fst'
	answers_fst = 'date-sme.fst'

	error_msg = "Dato.create_form: Database is improperly loaded, \
					 or Dato is unable to look up forms."

	def get_db_info(self, db_info):
		""" Going to need to subclass this because klokka generates the wrong thing.

			Lookup format is DD.M.

			Dato has no difficulty options.
		"""
		from random import choice

		def dayrange(x):
			return range(1,x+1)
		
		# List of tuples with all possible days
		# built from (month, maxdays)

		months = [(x, dayrange(y)) for x, y in [(1, 31),
												(2, 29),
												(3, 31),
												(4, 30),
												(5, 31),
												(6, 30),
												(7, 31),
												(8, 31),
												(9, 30),
												(10, 31),
												(11, 30),
												(12, 31)]]

		month, days = choice(months)

		date = '%d.%d.' % (choice(days), month)
		
		db_info['numeral_id'] = str(date)



class QuizzGame(Game):

	def get_db_info(self, db_info):

		# levels = self.settings['level']
		semtypes = self.settings['semtype']
		geography = self.settings['geography']
		frequency = True and self.settings['frequency'] or False # frequency value or False
		source = self.settings['source']
		
		source_language = self.settings['transtype'][0:3]
		target_language = self.settings['transtype'][-3::]
		QueryModel = Word
		 	
		# Excludes
		excl = ['exclude_' + self.settings['transtype']]
		
		error = "QuizzGame.get_db_info: Database may be improperly loaded. \
		Query for semantic type %s and book %s returned zero results." % ((semtypes, source))
		
		# This query is fairly expensive, and must be run once per game-form generation. Thus,
		# on the first generation it is run, and the results are stored to a list.
		# Each successive time this is run after the first query, a word is selected from the list
		# and popped off.
		
		if not self.query_set:
			leksa_kwargs = {'lang': source_language, 
							'tx_lang': target_language}
			
			excl.append('mPERSNAME')

			if semtypes and semtypes not in ['all', 'All']:
				leksa_kwargs['semtype_incl'] = semtypes

			if source and source not in ['all', 'All']:
				leksa_kwargs['source'] = source
				leksa_kwargs['semtype_incl'] = False 
			
			if geography:
				leksa_kwargs['geography'] = geography

			if excl:
				leksa_kwargs['semtype_excl'] = excl

			# The following is written by the example of sylls in MorfaS: this
			# can probably be simplified-- with sylls in MorfaS there was a
			# time when there were several possible values (3syll,
			# trisyllabic), but this should be no longer the case...

			kw_frequency = []
			common = ['common', 'common']
			rare = ['rare', 'rare']

			if frequency:
				for item in frequency:
					if item in common:
					    kw_frequency.extend(common)
					if item in rare:
					    kw_frequency.extend(rare)
				
				leksa_kwargs['frequency'] = list(set(kw_frequency))

			word_set = leksa_filter(QueryModel, **leksa_kwargs)

			self.query_set = word_set
		
		try:
			while True:
				random_word = choice(self.query_set)
				if random_word[1] not in self.lemmas_selected:
					break
				else:
					continue
			self.lemmas_selected.append(random_word[1])
			# self.query_set.pop(self.query_set.index(random_word))
		except IndexError:
			if len(self.query_set) == 0:
				raise Http404(error)
		
		db_info['word_id'] = random_word[0]
		db_info['question_id'] = ""
		
		return db_info
			
	def create_form(self, db_info, n, data=None):
		tr_lemmas = []
		# This is producing an unnecessary query, but it takes a lot of work to switch this
		# to just passing a word model instead of the ID.
		# Ideally should pass the model, so there's no need to query it again.
		word_id = db_info['word_id']
		
		target_language = self.settings['transtype'][-3::]
		source_language = self.settings['transtype'][0:3]
				
		word = Word.objects.get(Q(id=word_id))
		
		translations = word.wordtranslation_set.filter(language=target_language)
		tr_lemmas.extend([w.definition for w in translations])
		

		# Get correct answers; pick the first (oho!)
		# Need to not pick the first one.
		correct = ""
		preferred = False
		possible = False
		stat_pref = False
		tcomms = False
		if type(word) == Word:
			trans_obj = word.translations2(self.settings['transtype']).all()
			possible = [t.definition for t in trans_obj.filter(tcomm=False)]
			trans = [t.definition for t in trans_obj]
			
			tcomms = [t.definition for t in trans_obj.filter(tcomm=True)]
			stat_pref = [t.definition for t in trans_obj.filter(tcomm_pref=True)]
			
			if len(tcomms) > 0:
				preferred = [t.definition for t in trans_obj.filter(tcomm=False)]
			if not correct:
				if len(stat_pref) > 0:
					correct = stat_pref[:]
		elif type(word) == WordTranslation:
			trans_obj = word.word
			trans = [trans_obj.lemma]
			if not correct:
				correct = trans
		
		question_list = []
		
		userans_val = ''
		try:
			userans_val = db_info['answer'].strip()
		except KeyError:
			userans_val = db_info['userans']
		
		form = (LeksaQuestion(
					tcomms,
					stat_pref,
					preferred,
					possible, 
					self.settings['transtype'],
					word,
					correct,
					tr_lemmas,
					question_list,
					userans_val,
					db_info['correct'],
					data,
					prefix=n,))
		return form, word.id


