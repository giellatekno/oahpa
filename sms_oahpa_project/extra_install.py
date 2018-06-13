# -*- coding: utf-8 -*-

from local_conf import LLL_OAHPA
import importlib
sdm = importlib.import_module(LLL_OAHPA+'.drill.models')

from django.db.models import Q
from xml.dom import minidom as _dom
from django.utils.encoding import force_unicode
import sys
import re
import string
import codecs

# TODO: get these from settings

languages = [
    'sms',
    'rus',
	'sme',
	'nob', # was: 'nob' But in the documentation url-s the abbreviation nno is used to mark the Norwegian version of a help page. 
	'eng',
	'fin', 
	'deu',
]

class Link(object):
	def get_lang(self):
		""" Assumes that the file language is stored as part of the
			file name in the link, e.g., 

			substantiv.nob.html
					   ^

		"""
		file_name = self.url.split('/')[-1]
		file_name, _, _ = file_name.partition('#')
		try:
			title, language, suffix = file_name.split('.')
		except ValueError:
			language = 'sme'
		if language == 'nno':
			language = 'nob' # added this
		
		self.language = language

	def __init__(self, S):
		S = S.strip()
		self.S = S
		
		keyword, _, link = S.partition('\t')
		self.keyword = keyword
		self.url = link

		self.get_lang()
	
	def create_obj(self):
		kwargs = {'name': self.keyword,
					'address': self.url,
					'language': self.language}

		self.obj, _  = Grammarlinks.objects.get_or_create(**kwargs)


	


class Extra:

	# Installs links to the grammatical information under giellatekno.
	# The link list appears to the upper right corner of the oahpa-pages.
	# The links are in the file sme/meta/grammarlinks.txt 
	def read_address(self,linkfile):

		
		linkfileObj = open(linkfile, "r")
		data = [l for l in linkfileObj.readlines() if l.strip()]
		
		links = [Link(l) for l in data]
		languages = list(set([link.language for link in links]))

		linkobjects = Grammarlinks.objects.filter(language__in=languages).delete()

		for link in links:
			try:
				link.create_obj()

				print >> sys.stdout, 'Created link for %s/%s' % (link.obj.language, link.obj.name)
			except Exception:
				print >> sys.stderr, 'Check the source file and reinstall.'




				
	#The comments presented to the user after completing the game.
	def read_comments(self, commentfile):
		xmlfile=file(commentfile)
		tree = _dom.parse(commentfile)		

		comments_el = tree.getElementsByTagName("comments")[0]
		lang = comments_el.getAttribute("xml:lang")

		comments = Comment.objects.filter(lang=lang)
		for c in comments:
			c.delete()
		for el in comments_el.getElementsByTagName("comment"):
			level = el.getAttribute("level")
			for com in el.getElementsByTagName("text"):
				text = com.firstChild.data
				print text
				comment, created = Comment.objects.get_or_create(lang=lang, comment=text, level=level)
				comment.save()

	# Installs the semantic superclasses
	# defined in sme/xml/semantic_sets.xml
	def read_semtypes(self, infile):

		xmlfile=file(infile)
		tree = _dom.parse(infile)

		for el in tree.getElementsByTagName("subclasses"):
			semclass=el.getAttribute("class")
			print semclass
			s, created = sdm.Semtype.objects.get_or_create(semtype=semclass)
			for el2 in el.getElementsByTagName('sem'):
			   subclass  = el2.getAttribute("class")
			   print "\t" + subclass
			   for w in sdm.Word.objects.filter(Q(semtype__semtype=subclass) & ~Q(semtype__semtype=semclass)):
				   w.semtype.add(s)
				   print u"\t%s added to word id: %d" % (s, w.id)
				   w.save()
			   for w in sdm.WordTranslation.objects.filter(Q(semtype__semtype=subclass) & ~Q(semtype__semtype=semclass)):
				   w.semtype.add(s)
				   print u"\t%s added to %d" % (s, w.id)
				   w.save()


