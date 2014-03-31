# -*- coding: utf-8 -*-
import settings
from django.db.models import Q
from xml.dom import minidom as _dom
from django.utils.encoding import force_unicode
import sys

from myv_drill.models import * 
from collections import OrderedDict


# For easier debugging.
# _D = open('/dev/ttys005', 'w')
_D = open('/dev/null', 'w')

COUNT_ONLY = False

supported_langs = ['myv', 'nob', 'sme', 'swe', 'deu', 'eng', 'fin', 'rus']

# # # 
# 
#  Settings variables 
# 
# # # 

_STDERR = sys.stderr
_STDIN = sys.stdin
_STDOUT = sys.stdout

try:
	DIALECTS = settings.DIALECTS
	NG_DIALECT = settings.NONGEN_DIALECT
except:
	print """Dialects not defined in settings.py... 
		DIALECTS = {
			'main': ('isma-norm.fst', 'Unrestricted'),
			'SH': ('isma-SH.restr.fst', 'Short forms'),
			'L': ('isma-L.restr.fst', 'Long forms'),
			'NG': (None, 'Non-Presented forms'),
		}

		DEFAULT_DIALECT = 'SH'
		NONGEN_DIALECT = 'NG'
	"""
	sys.exit(2)

try:
	INFINITIVE_SUBTRACT = settings.INFINITIVE_SUBTRACT
	INFINITIVE_ADD = settings.INFINITIVE_ADD
except:
	print """Infinitives not defined in settings.py...
		 	INFINITIVE_SUBTRACT = {
		 		'nob': ur'^(?P<inf>å )?(?P<lemma>.*)$',
		 		'swe': ur'^(?P<inf>att )?(?P<lemma>.*)$',
		 		'eng': ur'^(?P<inf>to )?(?P<lemma>.*)$',
		 		'deu': ur'^(?P<inf>zu )?(?P<lemma>.*)$',
		 	}
		 	
		 	INFINITIVE_ADD = {
		 		'nob': ur'å \g<lemma>',
		 		'swe': ur'att \g<lemma>',
		 		'eng': ur'to \g<lemma>',
		 		'deu': ur'zu \g<lemma>',
		 	}

	"""
	sys.exit(2)

from django.db import transaction

# # # 
# 
#  Some XML shortcuts
# 
# # # 

_elements = lambda e, x: e.getElementsByTagName(x)
_attribute = lambda e, x: e.getAttribute(x)
def _data(e):
	try: 
		return e.firstChild.data
	except AttributeError:
		return False

def _firstelement(e, x):
	e = _elements(e, x)
	try:
		return e[0]
	except IndexError:
		return None

# # # 
# 
#  Handy objects
# 
# # # 

class Analysis(object):

	def getTag(self):
		
		tag_kwargs = {
			'string': self.tags,
			'pos': self.classes.get('Wordclass', ""),
			'number': self.classes.get('Number',""),
			'case': self.classes.get('Case',""),
			'possessive': self.classes.get('Possessive',""),
			'grade': self.classes.get('Grade',""),
			'infinite': self.classes.get('Infinite',""), 
			'personnumber': self.classes.get('Person-Number',""),
			'polarity': self.classes.get('Polarity',""),
			'tense': self.classes.get('Tense',""),
			'mood': self.classes.get('Mood',""), 
			'subclass': self.classes.get('Subclass',""),
			'attributive': self.classes.get('Attributive',"")
		}

		t, created = Tag.objects.get_or_create(**tag_kwargs)
		t.save()

		return t

	def __init__(self, linginfo, analysis):
		# TODO: update_only setting
		self.classes = {}

		self.form, self.tags = analysis
		
		for t in self.tags.split('+'):
			if linginfo.tagset.has_key(t):
				tagclass = linginfo.tagset[t]
				self.classes[tagclass] = t

class Entry(object):
	""" The beginning of a class for parsing entry nodes. 
		This makes it much easier to read the code below, so well worth it. Potential
		gotchas are with indexes.

		Next step is to add some methods that create the django Word or WordTranslation objects...
	""" 
	
	def processMiniParadigm(self, mini_paradigm):
		""" Processes a mini_paradigm
         
            <mini_paradigm>
				<analysis ms="Pron_Pers_Sg2_Acc">
            	   <wordform>datnem</wordform>
            	</analysis>
            	<analysis ms="Pron_Pers_Sg2_Gen">
            	   <wordform>dov</wordform>
            	</analysis>
            </mini_paradigm>

			# TODO:	<analysis ms="Pron_Pers_Pl1_Ill" dial="NG">
		"""
		try:
			analyses = _elements(mini_paradigm, 'analysis')
		except IndexError:
			return None
		paradigm_forms = []
		for analysis in analyses:
			ms = _attribute(analysis, 'ms')
			ms = ms.split('_')
			dial = _attribute(analysis, 'dial')
			wordforms = [_data(an) for an in _elements(analysis, 'wordform')]
			
			paradigm_forms += [(word, ms, dial) for word in wordforms]

		return paradigm_forms

	def processLG(self):
		""" Handles nodes such as...
			
			<lg>
      		   <l pos="n" soggi="oe" stem="2syll">aajroe</l>
      		</lg>

      		Including those containing lemma_ref and miniparadigms:

			<lg>
				<l pos="pron" type="pers">mijjen</l>
         		<lemma_ref lemmaID="mijjieh_pron_pers">mijjieh</lemma_ref>
         		<analysis>Pron_Pers_Pl1_Gen</analysis>
			</lg>

		"""
		
		n = self.node
		lg = _elements(n, "lg")[0]
		l = _elements(lg, "l")[0]
		
		# first item is xml attribute, second is what to set it to on
		# the python object, if None, then it is the same
		l_attrs = [
			("attr", None),
			("class", "wordclass"),
			("dial", None),
			("diph", None),
			("gen_only", None),
			("hid", None),
			("margo", None),
			("nr", None),
			("p3p", None),
			("pos", None),
			("gradation", None),
			("diphthong", None),
			("rime", None),
			("soggi", None),
			("stem", None),
			("type", "wordtype"),
			("umlaut", None),
			("vow", None),
			("xml:lang", None),

		]
		
		analysis = _firstelement(lg, "analysis")
		miniparadigm = _firstelement(lg, "mini_paradigm")
		lemma_ref = _firstelement(lg, "lemma_ref")

		if analysis:
			self.analysis = _data(analysis).replace('_', '+')
		else:
			self.analysis = False

		if miniparadigm:
			self.lemma_analyses = self.processMiniParadigm(miniparadigm)
		else:
			self.lemma_analyses = False
		
		if lemma_ref:
			self.lemma_ref = _data(lemma_ref)
		else:
			self.lemma_ref = False

		for xmlattr, objattr in l_attrs:
			if not objattr:
				objattr = xmlattr
			self.__setattr__(objattr, _attribute(l, xmlattr))

		self.lemma = _data(l)
	
	def processSources(self):
		""" Handles nodes such as...
            <sources>
               <book name=""/>
               <frequency class="common"/>
               <geography class="mid"/>
            </sources>
		"""

		n = self.node

		self.frequency = False
		self.geography = False
		self.sources = False

		try:
			sources = _elements(n, "sources")[0]
		except IndexError:
			self.sources = False
			return
		books = _elements(sources, "book")
		
		book_names = [_attribute(b, "name") for b in books]
		
		self.sources = book_names

		frequency = _elements(sources, "frequency")
		geography = _elements(sources, "geography")

		self.frequency = [_attribute(b, "class") for b in frequency]
		self.geography = [_attribute(b, "class") for b in geography]


	def _handleSemantics(self, node):
		"""  Handles nodes such as...
			<semantics>
        	   <sem class="FISHING" />
        	   <sem class="mLONG_SHORT" />
        	</semantics>
        """ 
		
		try:
			semantics = _elements(node, "semantics")[0]
		except IndexError:
			return False
		sems = _elements(semantics, "sem")

		semclasses = [_attribute(b, 'class') for b in sems]

		return semclasses 

	def _handleTranslations(self, node):
		""" Handles nodes such as...
			<tg xml:lang="nob">
        	   <tf pos="phrase_n" stat="pref" tcomm="no">spor etter reinflokk</tf>
        	   <t pos="n" stat="notpref" tcomm="no">reinspor</t>
        	   <t pos="n" stat="notpref" tcomm="no">spor</t>
        	</tg>

		"""

		__tcomm = lambda v: True and v in ['yes', 'YES', 'true', 'True'] or False
		__stat = lambda v: True and v.lower() == 'pref' or False

		tgs = _elements(node, "tg")
		translations = {}

		for tg in tgs:
			lang = _attribute(tg, "xml:lang")
			
			trans_list = []
			Ts = _elements(tg, "t")
			# tf = phrase, te = explanation, t = lemma
			for T in Ts:
				trans = {
					'pos': _attribute(T, 'pos'),
					'stat': __stat(_attribute(T, 'stat')),
					'tcomm': __tcomm(_attribute(T, 'tcomm')),
					'lemma': _data(T),
					'phrase': False,
					'explanation': False,
				}
				trans_list.append(trans)

			TFs = _elements(tg, "tf")
			for T in TFs:
				trans = {
					'pos': _attribute(T, 'pos'),
					'stat': __stat(_attribute(T, 'stat')),
					'tcomm': __tcomm(_attribute(T, 'tcomm')),
					'lemma': False,
					'phrase': _data(T),
					'explanation': False,
				}
				trans_list.append(trans)

			TEs = _elements(tg, "te")
			for T in TEs:
				trans = {
					'pos': _attribute(T, 'pos'),
					'stat': __stat(_attribute(T, 'stat')),
					'tcomm': __tcomm(_attribute(T, 'tcomm')),
					'lemma': False,
					'phrase': False,
					'explanation': _data(T),
				}
				trans_list.append(trans)


			translations[lang] = trans_list

		return translations

	def processMeaningGroups(self):
		""" Handles nodes such as...
			<mg>
				<semantics>
					<sem class="FAMILY" />
				</semantics>
				<tg xml:lang="nob">
         		   <tf pos="phrase_n" stat="pref" tcomm="no">bestefars barnebarn</tf>
         		   <tf tcomm="no">bestefar sitt barnebarn</tf>
         		</tg>
         		<tg xml:lang="swe">
         		   <tf pos="phrase_n" stat="pref" tcomm="no">bestefars barnebarn_SWE</tf>
         		</tg>
         	</mg>
         	<mg>
				etc...
			</mg>
			
		"""
		self.meanings = []

		mgs = _elements(self.node, "mg")


		for mg in mgs:
			meaning = {}
			meaning['semantics'] = self._handleSemantics(mg)
			meaning['translations'] = self._handleTranslations(mg)

			self.meanings.append(meaning)


	def make_checksum(self):
		import hashlib
	 	self.checksum = hashlib.md5(self.node.toxml().encode('utf-8')).hexdigest()

	def __init__(self, e_node):
		""" Takes a parsed e_node and begins the process. Returns traceback upon fail.

		"""

		self.node = e_node
		
		try:
			self.exclude = _attribute(e_node, 'exclude')
			self.processLG()
			self.processSources()
			self.processMeaningGroups()
			self.make_checksum()
		except Exception, e:
			import traceback
			message = 'Traceback:\n%s' % (
							'\n'.join(traceback.format_exception(*sys.exc_info())),)
			
			print >> _STDERR, e_node.toxml().encode('utf-8')
			print >> _STDERR, "Error while handling XML:"
			print >> _STDERR, Exception, e
			print >> _STDERR, message
			print >> _STDERR, "Exiting." 
			sys.exit(2)



class Words(object):

	def paradigm_is_changed(self, key, paradigm):
		# TODO: only run this when update setting is present 
		return True
		from diff.models import ParadigmDiff
		import hashlib

		hashable = '|'.join(paradigm.keys())
		checksum = hashlib.md5(hashable.encode('utf-8')).hexdigest()

		try:
			diff = ParadigmDiff.objects.get(key=key)
		except ParadigmDiff.DoesNotExist:
			diff = ParadigmDiff.objects.create(key=key, checksum=checksum)
			diff.save()
			return True
		
		if checksum == diff.checksum:
			return False
		else:
			diff.checksum = checksum
			diff.save()
			return True

	
	@transaction.commit_on_success
	def install_lexicon(self,infile,linginfo,delete=None,paradigmfile=False, verbose=True):
		global VERBOSE
		VERBOSE = verbose

		# xmlfile = file(infile) # never used
		tree = _dom.parse(infile)
		
		lex = tree.getElementsByTagName("r")[0]
		mainlang = lex.getAttribute("xml:lang")
		print >> _STDOUT, "Mainlang defined ", mainlang.encode('utf-8')
		if not mainlang:
			print >> _STDERR, "Attribute mainlang not defined in", infile, "stop."
			sys.exit()

		self.all_wordids = []
		
		es = tree.getElementsByTagName("e")
		total = len(es)
		count = 0
		
		# Collect data to generate words, or skip if they are already
		# provided
		
		entries = []
		for e in es:
			entry = Entry(e)

			if entry.lemma_analyses or entry.analysis:
				pass
			else:
				if paradigmfile:
					paradigm_args = [
						entry.lemma,
						entry.pos,
						entry.hid,
						entry.wordtype,		# TV, IV, TODO: Neg
						entry.gen_only,
						[],
					]

					try:
						linginfo.collect_gen_data(*paradigm_args)
					except TypeError:
						print e.toxml()
						print >> sys.stderr, "XML file contains an empty <l /> element."
						print >> sys.stderr, "... Exiting."
						
						sys.exit(2)

			entries.append(entry)
		

		if paradigmfile:
			linginfo.generate_all(dialects=DIALECTS)
		
		for entry in entries:

			# Uppercase POS.
			pos = entry.pos.upper()
			if pos.startswith('PHRASE'):
				pos = pos.replace('PHRASE', '') # Just incase we have longer POS.
				pos = pos.replace('_', '')

			if pos:
				if not COUNT_ONLY:
					if VERBOSE:
						print >> _STDOUT, "pos defined ", pos.encode('utf-8')

				self.store_word(entry=entry,
								linginfo=linginfo,
								mainlang=mainlang,
								delete=delete,
								paradigmfile=paradigmfile)
				
			else:
				try:
					__data = e.getElementsByTagName("lg")[0]\
								.getElementsByTagName("l")[0]\
								.firstChild.data
				except AttributeError:
					__data = 'None'

				if not COUNT_ONLY:
					if VERBOSE:
						print >> _STDOUT, "undefined pos for ", __data.encode('utf-8')
			
			count += 1
			print >> _STDOUT, '--- %d/%d entries processed' % (count, total)
			
			
		if delete and pos:
			allids = Word.objects.filter(pos=pos)\
									.exclude(semtype__semtype="PLACE-NAME-LEKSA")\
									.values_list('wordid',flat=True)

			for a in allids:
				if force_unicode(a) not in set(self.all_wordids):
					print >> _STDOUT, "Word id not found from xml. Deleting:", a.encode('utf-8')
					word = Word.objects.get(pos=pos,wordid=a)
					word.delete()
		
		# transaction.commit()


	def add_translation(self, language, txdata, w, entry, semantics):
		translation = lemma = phrase = explanation = False
		
		if txdata['lemma']:
			translation = lemma = txdata['lemma']
		
		if txdata['phrase']:
			translation = phrase = txdata['phrase']
		
		if txdata['explanation']:
			translation = explanation = txdata['explanation']
		
		if not translation:
			print >> _STDERR, " *** No translation lemma given in word translation elements for <%s>. Skipping this translation." % entry.lemma.encode('utf-8')
			return
		
		pos = entry.pos.upper()
		if pos == 'PROP':
			pos = 'N'

		wt_kwargs = {
			'language': language,
			'word': w,
			'wordid': translation,
			'pos': pos,
			'tcomm': txdata['tcomm'],
			'tcomm_pref': txdata['stat']
		}
		
		if lemma:
			wt_kwargs['lemma'] = lemma
		elif phrase:
			wt_kwargs['phrase'] = phrase
		elif explanation:
			wt_kwargs['explanation'] = explanation

		try:
			transl, created = WordTranslation.objects.get_or_create(**wt_kwargs)
			if semantics:
				for item in semantics:
					transl.semtype.add(item)
		except WordTranslation.MultipleObjectsReturned:
			print >> _STDERR, "Extra similar translation objects found, deleting extras..."
			transls = list(WordTranslation.objects.filter(**wt_kwargs))
			for t in transls[1::]:
				t.delete()

		# Add reference to the new word object as translation.
		w.save()				   

		if VERBOSE:
			print >> _STDOUT, "Translation for <%s> added: %s" % (language.encode('utf-8'), translation.encode('utf-8'))

	def add_semantics(self, semantics, w, entry):
		if entry.exclude:
			excl = entry.exclude
			exclusions = [a.strip() for a in excl.split(',') if a.strip()]
			for exclusion in exclusions:
				exclude_type, _ = Semtype.objects.get_or_create(semtype='exclude_' + exclusion)
				w.semtype.add(exclude_type)
				direction = (exclusion[0:3], exclusion[3:6])
				if VERBOSE:
					print >> _STDOUT, ' *** This word will be excluded in %s->%s' % direction
		
		mg_semtypes = []
		
		if semantics:
			for semclass in semantics:
				if not COUNT_ONLY:
					if VERBOSE:
						print >> _STDOUT, "Semantic cls: ", semclass.encode('utf-8')
				# Add semantics entry if not found.
				# Leave this if DTD is used.
				sem_entry, created = Semtype.objects.get_or_create(semtype=semclass)
				if created:
					if VERBOSE:
						print >> _STDOUT, "Created semtype entry with name ", semclass.encode('utf-8')
				w.semtype.add(sem_entry)

				mg_semtypes.append(sem_entry)
				w.save()		
		return mg_semtypes

	def add_sources(self,entry,w):
		for bookname in entry.sources:
			book_entry, created = Source.objects.get_or_create(name=bookname)
			if created:
				if VERBOSE:
					print >> _STDOUT, "Created book entry with name ", bookname.encode('utf-8')

			w.source.add(book_entry)
			w.save()

	def store_word(self,entry,linginfo,mainlang,paradigmfile,delete):
		OUT_STRS = []
		ERR_STRS = []

		# TODO: sometimes translations are added despite no changes
		changes_to_xml = True
		changes_to_paradigm = True
		# Intialize null variables
		stem, forms, gradation, rime						=	[""]*4
		wordclass, attrsuffix, soggi, valency				= 	[""]*4
		compare, frequency, geography, presentationform 	= 	[""]*4

		diphthong = "no"
		
		exist_kwargs = {}

		# Store first unique fields
		wid = entry.lemma

		if not entry.lemma:
			print >> _STDERR, "No lemma defined"
			sys.exit(2)
		else:
			lemma = entry.lemma

		if not wid:
			wid = lemma
		
		exist_kwargs['language'] = mainlang

		self.all_wordids.append(wid)
		
		
		if entry.wordclass:
			wordclass = entry.wordclass
			if not COUNT_ONLY:
				OUT_STRS.append(wordclass)
		
		
		if entry.frequency:
			frequency = entry.frequency[0]

		if entry.geography:
			geography = entry.geography[0]

		# Part of speech information
		pos = entry.pos
		hid = entry.hid
		
		if entry.hid:
			hid = int(entry.hid)
			exist_kwargs['hid'] = hid
		else:
			hid = None

		pos = pos.upper()
		if pos.startswith('PHRASE'):
			pos = pos.replace('PHRASE', '') # Just incase we have longer POS.
			pos = pos.replace('_', '')
		
		if pos == 'PROP':
			pos = 'N'

		exist_kwargs['pos'] = pos
		
		soggi = entry.soggi
		diphthong = entry.diphthong
		gradation = entry.gradation
		stem = entry.stem
		rime = entry.rime


		trisyllabic = ['3syll', '3', 'trisyllabic']
		bisyllabic = ['2syll', '2', 'bisyllabic']

		if stem in trisyllabic:			stem = '3syll'
		if stem in bisyllabic:			stem = '2syll'

		# Search for existing word in the database.
		w = None
		
		if entry.lemma_ref:
			# For entries with lemma ref, we need to
			# actually fetch an existing word entry,
			# and add the lemma here as fullform to Form models
			exist_kwargs['lemma'] = entry.lemma_ref
			exist_kwargs['wordid'] = entry.lemma_ref
		else:
			exist_kwargs['lemma'] = lemma
			exist_kwargs['wordid'] = lemma

		
		try:
			w, created = Word.objects.get_or_create(**exist_kwargs)
		except Word.MultipleObjectsReturned:
			w = Word.objects.filter(**exist_kwargs)
			w.delete()
			w = Word.objects.create(**exist_kwargs)

		# Check if there are changes to the word's XML element, and if not, skip
		changes_to_xml = True
		# try:
			# diff = w.worddiff_set.all()[0]
			# if entry.checksum != diff.checksum:
				# changes_to_xml = True
		# except:
			# diff = w.worddiff_set.create(checksum=entry.checksum)
			# diff.save()
			# changes_to_xml = True
		
		# if not changes_to_xml:
		# 	print >> sys.stdout, ' * No changes detected to word XML, skipping... '
		# 	return

		w.wordclass = wordclass
		w.pos = pos
		w.wordid = w.lemma = lemma
		# w.presentationform = presentationform
		w.stem = stem
		w.rime = rime
		w.compare = compare
		w.attrsuffix = attrsuffix
		w.soggi = soggi
		w.gradation = gradation
		w.diphthong = diphthong

		w.valency = valency
		w.frequency = frequency
		OUT_STRS.append(frequency)
		OUT_STRS.append(geography)
		w.geography = geography
		w.hid = hid
		w.save()

		dialect_objects = []
		
		# Create dialect forms
		for dialect, dial_data in DIALECTS.items():
			dial, created = Dialect.objects.get_or_create(dialect=dialect)
			if created:
				dial.name = dial_data[1]
				dial.save()
			if dialect != NG_DIALECT:
				dialect_objects.append(dial)
		
		# additional dialect mappings
		# NG - main, NG; but not L and SH

		main_dialect = Dialect.objects.get(dialect='main')
		ng_dialect = Dialect.objects.get(dialect=NG_DIALECT)

		if entry.dial:
			dialect, created = Dialect.objects.get_or_create(dialect=entry.dial)
			if created:
				dialect.name = DIALECTS[entry.dial][1]
				dialect.save()
			if entry.dial != NG_DIALECT:
				dialect_objects.append(dial)
		else:
			dialect = False

		if entry.lemma_analyses:
			pregenerated = True
		else:
			pregenerated = False

		if pregenerated:
			analyses = []
			if entry.lemma_analyses:
				analyses = entry.lemma_analyses
				# Join tags
				analyses = [(form, '+'.join(tags), dial) for form, tags, dial in analyses]
			
			for analysis in analyses:
				analysis, dialect = (analysis[0], analysis[1]), analysis[2]
				g = Analysis(linginfo, analysis)
				tag = g.getTag()					
				
				form, _ = Form.objects.get_or_create(fullform=g.form, tag=tag, word=w)
				form.save()

				if dialect:
					if type(dialect) != Dialect:
						dialect = Dialect.objects.get(dialect=dialect)
					form.dialects.add(dialect)
				
				# form.dialects.add(main_dialect)
				del form
				if not COUNT_ONLY:
					if dialect:
						if VERBOSE:
							OUT_STRS.append(force_unicode("Created form: %s\t%s\t\t%s" % (tag.string, g.form, dialect.dialect)))
					else:
						if VERBOSE:
							OUT_STRS.append(force_unicode("Created form: %s\t%s" % (tag.string, g.form)))
		elif paradigmfile:

			# Create a dictionary that with keys for the tag and wordform, and
			# set as key the word class and dialects, thus there is no need to
			# reiterate through already created wordforms just to add dialects.
			# Time-saving, because we iterate through wordforms and add
			# dialects, rather than iterating through dialects and going
			# through wordforms once for each dialect.

			paradigms_to_create = dict() # OrderedDict()
			# TODO: sorted by tag
			for dialect in dialect_objects:
				if VERBOSE:
					OUT_STRS.append('Forms for dialect %s' % dialect.dialect)

				generated_forms = linginfo.get_paradigm(lemma=lemma,
										pos=pos,
										forms=forms, 
										dialect=dialect.dialect)

				if not generated_forms:
					continue

				for form in generated_forms: 
					tag = form.tags
					wform = form.form
					key = '%s|%s' % (tag, wform)

					if key in paradigms_to_create:
						form_info = paradigms_to_create[key]
					else:
						form_info = {'class': form}

					if 'dialects' in form_info:
						form_info['dialects'].append(dialect)
					else:
						form_info['dialects'] = [dialect]

					paradigms_to_create[key] = form_info
						
			paradigms_to_create = OrderedDict(sorted(paradigms_to_create.items(), key=lambda t: t[0]))

			changes_to_paradigm = False
			paradigm_key = '%s|%s|%s' % (lemma, pos, dialect.dialect)
			changes_to_paradigm = self.paradigm_is_changed(paradigm_key, paradigms_to_create)

			if changes_to_paradigm:

				existing = Form.objects.filter(word=w)

				if existing.count() > 0:
					existing.delete()

				for key, item in paradigms_to_create.iteritems():
					f_dialects = item.get('dialects', False)
					f = item.get('class', False)

					g = f.classes

					if w.pos == "A" and w.compare == "no" and \
					   	   (g.get('Grade')=="Comp" or g.get('Grade')=="Superl"):
						continue

					tag_kwargs = {
						'string': 			f.tags,
						'pos': 				g.get('Wordclass', ""),
						'number': 			g.get('Number',""),
						'case': 			g.get('Case',""),
						'possessive': 		g.get('Possessive',""),
						'grade': 			g.get('Grade',""),
						'infinite': 		g.get('Infinite',""), 
						'personnumber': 	g.get('Person-Number',""),
						'polarity': 		g.get('Polarity',""),
						'tense': 			g.get('Tense',""),
						'mood': 			g.get('Mood',""), 
						'subclass': 		g.get('Subclass',""),
						'attributive': 		g.get('Attributive',""),
					}

					t,created=Tag.objects.get_or_create(**tag_kwargs)

					t.save()

					# form = Form(fullform=f.form,tag=t,word=w)	

					form, _ = Form.objects.get_or_create(fullform=f.form, tag=t, word=w)
					form.save()

					names = set()
					for dialect in f_dialects:
						names.add(dialect.dialect)
						form.dialects.add(dialect)

					if not COUNT_ONLY:
						if VERBOSE:
							fmt = (t.string, 
									f.form, 
									', '.join(list(names)))
							
							_outstr = u"Created form: %s\t%s\t\t%s" % fmt
							OUT_STRS.append(_outstr)

					del form

		# Figure out NG forms, main dial forms that are not in any of
		# the other dialects.

		if changes_to_paradigm:
			non_main = Dialect.objects.exclude(dialect='main').exclude(dialect='NG')

			for form in w.form_set.filter(dialects=main_dialect):
				ng = False
				for nm in non_main:
					if nm in form.dialects.all():
						ng = True
				
				if ng:
					continue
				else:
					form.dialects.add(ng_dialect)


		
		if changes_to_xml:
			if entry.sources:
				self.add_sources(entry, w)
		
		if changes_to_xml:
			for mgroup in entry.meanings:
				# Semantics goes first, might copy to WordTranslation objects
				mg_semantics = self.add_semantics(mgroup['semantics'], w, entry)
				
				for language, translations in mgroup['translations'].items():
					for translation in translations:
						self.add_translation(language=language, 
												txdata=translation, 
												w=w, 
												entry=entry, 
												semantics=mg_semantics)

		if not changes_to_xml:
			OUT_STRS.append(' * No changes to XML detected, skipping Word objects.')

		if not changes_to_paradigm:
			OUT_STRS.append(' * No changes in generation detected, skipping Form objects.')

		print >> _STDOUT, '\n'.join(OUT_STRS).encode('utf-8')
		print >> _STDERR, '\n'.join(ERR_STRS).encode('utf-8')
		OUT_STRS = list()
		ERR_STRS = list()


	def delete_word(self, wid=None,pos=None):

		if not pos:
			print "specify the part of speech with option -p"
			# to debug and fix: delete word routine
			# wordruss = Wordrus.objects.filter(wordid=wid)
			# for w in wordruss:
			# 		print "Removing", w.wordid
			#		w.delete()
		if wid and pos:
			words = Word.objects.filter(wordid=wid,pos=pos)
			for w in words:
				if not COUNT_ONLY:
					print >> _STDOUT, "Removing", w.wordid.encode('utf-8')
				w.delete()
		if not words:
			print wid, "not found"


