# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from django.db import connection
from django.db import transaction

from django.utils.encoding import smart_unicode

# TODO: abstract from  'sjd' to LLL1

class BulkManager(models.Manager):
	""" This Manager adds additional methods to Feedback.objects. That allows
	for bulk inserting via custom SQL query (calling INSERT INTO on a list of
	dictionaries), this is much faster than using the standard .create() if
	many objects need to be added.

		.create() -> .bulk_insert()
		.messages.add() -> .bulk_add_messages()
		.dialects.add() -> .bulk_add_dialects()


	"""

	@transaction.atomic
	def bulk_insert(self, fields, objs):
		""" Takes a list of fields and a list dictionaries of fields and values,
		iterates and inserts. @transaction.atomic is active, and the
		transaction is committed after insert.
		"""
		qn = connection.ops.quote_name
		cursor = connection.cursor()

		flds = ', '.join([qn(f) for f in fields])
		values_list = [ r[f] for r in objs for f in fields]
		arg_string = ', '.join([u'(' + ', '.join(['%s']*len(fields)) + ')'] * len(objs))
		sql = "INSERT INTO %s (%s) VALUES %s" % (self.model._meta.db_table, flds, arg_string,)
		cursor.execute(sql, values_list)
		transaction.commit()

	@transaction.atomic
	def bulk_add_form_messages(self, objs):
		""" Takes a list of IDs, (feedback_id, feedback_message_id) and inserts
		these to the many-to-many table, committing on complete.  """
		qn = connection.ops.quote_name
		cursor = connection.cursor()

		fields = ['form_id', 'feedbackmsg_id']

		vals = [dict(zip(fields, a)) for a in objs]
		flds = ', '.join([qn(f) for f in fields])
		values_list = [ r[f] for r in vals for f in fields]

		arg_string = ', '.join([u'(' + ', '.join(['%s']*len(fields)) + ')'] * len(vals))

		# postgres seems to automatically ignore, mysql does not
		try:
			postgres = connection.ops._postgres_version
			ignore = ''
		except AttributeError:
			postgres = False
			ignore = 'IGNORE'

		sql = "INSERT %s INTO %s (%s) VALUES %s" % (ignore, "drill_form_feedback", flds, arg_string,)

		cursor.execute(sql, values_list)
		transaction.commit()

	@transaction.atomic
	def bulk_remove_form_messages(self, form_qs):
		""" Takes a form queryset, bulk removes all feedbacks for words with those ids """

		form_ids = form_qs.values_list('id', flat=True)

		qn = connection.ops.quote_name
		cursor = connection.cursor()

		table = "drill_form_feedback"
		fld = qn('form_id')
		args = ', '.join([str(f) for f in form_ids])

		sql = "DELETE FROM %s WHERE %s in (%s)" % (table, fld, args)

		cursor.execute(sql)
		transaction.commit()


	@transaction.atomic
	def bulk_add_messages(self, objs):
		""" Takes a list of IDs, (feedback_id, feedback_message_id) and inserts
		these to the many-to-many table, committing on complete.  """
		qn = connection.ops.quote_name
		cursor = connection.cursor()

		fields = ['feedback_id', 'feedbackmsg_id']

		vals = [dict(zip(fields, a)) for a in objs]
		flds = ', '.join([qn(f) for f in fields])
		values_list = [ r[f] for r in vals for f in fields]

		arg_string = ', '.join([u'(' + ', '.join(['%s']*len(fields)) + ')'] * len(vals))
		sql = "INSERT INTO %s (%s) VALUES %s" % ("drill_feedback_messages", flds, arg_string,)

		cursor.execute(sql, values_list)
		transaction.commit()

	@transaction.atomic
	def bulk_add_dialects(self, objs):
		""" Takes a list of IDs, (feedback_id, dialect_id) and inserts these to
		the many-to-many table, committing on complete.  """
		qn = connection.ops.quote_name
		cursor = connection.cursor()

		fields = ['feedback_id', 'dialect_id']

		vals = [dict(zip(fields, a)) for a in objs]
		flds = ', '.join([qn(f) for f in fields])
		values_list = [ r[f] for r in vals for f in fields]

		arg_string = ', '.join([u'(' + ', '.join(['%s']*len(fields)) + ')'] * len(vals))
		sql = "INSERT INTO %s (%s) VALUES %s" % ("drill_feedback_dialects", flds, arg_string,)

		cursor.execute(sql, values_list)
		transaction.commit()


class Comment(models.Model):
	lang = models.CharField(max_length=5)
	comment = models.CharField(max_length=100)
	level = models.CharField(max_length=5)

class Log(models.Model):
	game = models.CharField(max_length=30)
	date = models.DateField(blank=True, null=True)
	userinput = models.CharField(max_length=200)
	iscorrect = models.BooleanField()
	correct = models.TextField()
	example = models.CharField(max_length=200,null=True)
	feedback = models.CharField(max_length=200,null=True)
	comment = models.CharField(max_length=200)
	messageid = models.CharField(max_length=100,null=True)
	lang = models.CharField(max_length=3)

	def outputEntry(self, printattrs=False, delimiter=False):
		""" Renders log information in a one-line string.

			@attr printattrs - Supply a list of attributes to print via printattrs,
						  or specify none for all attributes.

			@attr delimiter - Optionally a delimiter may be specified.

		"""
		import datetime

		if not delimiter:
			delimiter = '|'

		if not printattrs:
			attrs = [
				'game',
				'date',
				'userinput',
				'correct',
				'iscorrect',
				'example',
				'feedback',
				'comment'
			]
		else:
			attrs = printattrs

		vals = []
		for a in attrs:
			ap = self.__getattribute__(a)

			if not type(ap) in [str, unicode]:
				if type(ap) == datetime.date:
					ap = '%d/%d/%d' % (ap.year, ap.month, ap.day)
				else:
					ap = repr(ap)
			else:
				try:
					ap = ap.decode('utf-8')
				except UnicodeEncodeError:
					pass

			if not ap:
				ap = 'None'

			vals.append(ap)


		return unicode(delimiter.join(vals))

	def __str__(self):
		return self.outputEntry()

class Semtype(models.Model):
	semtype = models.CharField(max_length=50)

	def __unicode__(self):
		return smart_unicode(self.semtype)

class Source(models.Model):
	type = models.CharField(max_length=20)
	name = models.CharField(max_length=20)


	def __unicode__(self):
		if self.type and self.name:
			S = "%s: %s" % (self.type, self.name)
		elif self.name:
			S = "%s" % self.name
		return smart_unicode(S)

# First, define the Manager subclass.
class NPosManager(models.Manager):
	def get_query_set(self):
		return super(NPosManager, self).get_query_set().filter(pos='N')

class Dialect(models.Model):
	dialect = models.CharField(max_length=5)
	name = models.CharField(max_length=100)

	def __unicode__(self):
		if self.dialect and self.name:
			S = "%s: %s" % (self.dialect, self.name)
		elif self.name:
			S = "%s" % self.name
		elif self.dialect:
			S = "%s" % self.dialect
		return smart_unicode(S)

def Translations2(target_lang):
	if target_lang in ["nob", "rus", "sme", "eng", "deu", "sjd", "no"]:
		if target_lang == "nob" or "no":	related = 'translations2nob'
		if target_lang == "rus":	related = 'translations2rus'
		if target_lang == "sme":	related = 'translations2sme'
		if target_lang == "eng":	related = 'translations2eng'
		if target_lang == "deu":	related = 'translations2deu'
		if target_lang == "sjd":	related = 'translations2sjd'
		return related
	else:
		return None


# class Nob(models.Manager):
# 	def get_query_set(self):
# 		return super(Nob, self).get_query_set().filter(language='nob')

class MorphPhonTag(models.Model):
	stem		 = models.CharField(max_length=20)
	wordclass	= models.CharField(max_length=20)
	diphthong	= models.CharField(max_length=20)
	gradation	= models.CharField(max_length=20)
	rime		 = models.CharField(max_length=20)
	soggi		= models.CharField(max_length=20)
	# diphthong	= models.CharField(max_length=20)

	def __unicode__(self):
		attrs = [self.stem,
				self.wordclass,
				self.diphthong,
				self.gradation,
				self.rime,
				self.soggi]

		S = smart_unicode('/'.join([a for a in attrs if a.strip()])).encode('utf-8')
		return S

	class Meta:
		unique_together = ("stem",
							"wordclass",
							"diphthong",
							"gradation",
							"rime",
							"soggi",)
def leksa_filter(Model,
					lang=False,
					tx_lang=False,
					semtype_incl=False,
					semtype_excl=False,
					source=False,
					geography=False,
					frequency=False,
					ids=False):
	EXCL = {}
	QUERY = {}

	if semtype_excl:
		EXCL['semtype__semtype__in'] = semtype_excl

	QUERY['language'] = lang
	QUERY['wordtranslation__language'] = tx_lang

	# Heli: I think that the next if-clause is relevant only for leksa-place ?

	if geography:
		QUERY['geography'] = geography
	else:
		a = 'semtype__semtype__in'
		if a in EXCL:
			EXCL[a].append('PLACES')
		else:
			EXCL[a] = ['PLACES']

	if semtype_incl:
		QUERY['semtype__semtype__in'] = list(semtype_incl)

	if frequency:
		QUERY['frequency__in'] = frequency

	if source and source not in ['all', 'All']:
		QUERY['source__name__in'] = [source]

	query_set = Model.objects.exclude(**EXCL).filter(**QUERY).order_by('?')[:10]
	query_ids = query_set.values_list('id', 'lemma')

	return query_ids



class Word(models.Model):
	"""
		>>> a = Word.objects.create(lemma='omg')
		>>> a.wordnob_set.create(lemma='bbq')
	"""
	wordid = models.CharField(max_length=200, db_index=True)
	language = models.CharField(max_length=5, default='sme', db_index=True)
	lemma = models.CharField(max_length=200, db_index=True)
	presentationform = models.CharField(max_length=5)
	pos = models.CharField(max_length=12) # Accomodate larger PoS
	stem = models.CharField(max_length=20)
	wordclass = models.CharField(max_length=8)
	valency = models.CharField(max_length=10)
	hid = models.IntegerField(null=True, default=None)
	semtype = models.ManyToManyField(Semtype)
	source = models.ManyToManyField(Source)
	diphthong = models.CharField(max_length=5)
	gradation = models.CharField(max_length=20)
	rime = models.CharField(max_length=20)
	attrsuffix = models.CharField(max_length=20)
	compsuffix = models.CharField(max_length=20)
	soggi = models.CharField(max_length=10)
	compare = models.CharField(max_length=5)
	# translations2nob = models.ManyToManyField('Wordnob')
	# translations2swe = models.ManyToManyField('Wordswe')
	# translations2sme = models.ManyToManyField('Wordsme')
	# translations2eng = models.ManyToManyField('Wordeng')
	# translations2deu = models.ManyToManyField('Worddeu')
	frequency = models.CharField(max_length=10)
	geography = models.CharField(max_length=10)
	objects = models.Manager() # The default manager.
	N_objects = NPosManager() # The Noun-specific manager
	tcomm = models.BooleanField(default=False)
	# nob = Nob()
	morphophon = models.ForeignKey(MorphPhonTag, null=True)
	dialects = models.ManyToManyField(Dialect)



	def morphTag(self, nosave=True):
		try:
			mphon = self.morphophon
		except MorphPhonTag.DoesNotExist:
			mphon = False
		if not mphon:
			kwargs = {
				'stem':		 self.stem,
				'wordclass':	self.wordclass,
				'diphthong':	self.diphthong,
				'gradation':	self.gradation,
				'rime':		 self.rime,
				'soggi':		self.soggi,
			}
			morphtag, create = MorphPhonTag.objects.get_or_create(**kwargs)
			if nosave:
				return morphtag
			else:
				self.morphophon = morphtag
				self.save()


	def __init__(self, *args, **kwargs):
		super(Word, self).__init__(*args, **kwargs)
		self.definition = self.lemma
		if self.stem in ['3syll', 'trisyllabic']:
			self.wordclass = 'Odd'

		from functools import partial

		self.translations2nob = partial(self.translations2, target_lang='nob')()
		self.translations2eng = partial(self.translations2, target_lang='eng')()
		self.translations2deu = partial(self.translations2, target_lang='deu')()
		self.translations2rus = partial(self.translations2, target_lang='rus')()
		self.translations2sme = partial(self.translations2, target_lang='sme')()
		self.translations2sjd = partial(self.translations2, target_lang='sjd')()

	def create(self, *args, **kwargs):
		morphtag = self.morphTag()
		self.morphophon = morphtag
		self.pos = self.pos.lower().capitalize()
		super(Word, self).create(*args, **kwargs)

	def save(self, *args, **kwargs):
		""" Words model has an override to uppercase pos attribute on save,
			in case data isn't saved properly.
			"""
		morphtag = self.morphTag()
		self.pos = self.pos.lower().capitalize()
		self.morphophon = morphtag

		super(Word, self).save(*args, **kwargs)

	def __unicode__(self):
		return smart_unicode(self.lemma)

	def sem_types_admin(self):
		return ', '.join([item.semtype for item in self.semtype.order_by('semtype').all()])

	def source_admin(self):
		return ', '.join([item.name for item in self.source.order_by('name').all()])

	def translations2(self, target_lang):
		"""
			Returns obj.translations2XXX for string
		"""
		target_lang = target_lang[-3::]
		# related = Translations2(target_lang)
		# return self.__getattribute__(related)
		return self.wordtranslation_set.filter(language__startswith=target_lang)

	def baseform(self):
		"""
			Returns the infinitive/recitation Form for the Word.

			V - Inf
			N - Nom
			A - Attr

			Take a look at code in game.BareGame.get_baseform and move that here.
		"""

		pos_base = {
			'V': 'Inf',
			'N': 'Nom',
			'A': 'Attr',
			'Pron': 'Nom',
		}
		if self.pos == 'A':
			if self.tag.string.find('Attr') > -1:
				form_filter = 'A+Sg+Nom'
			else:
				form_filter = 'A+Attr'
			try:
				return self.form_set.filter(tag__string=form_filter)[0]
			except:
				return None
		else:
			try:
				return self.form_set.filter(tag__string__icontains=pos_base[self.pos])[0]
			except:
				return None

# TODO: Wordxxx need to be one object
# TODO: admin interface is going to have problems loading tons of words, should use search field instead


class WordTranslation(models.Model):
	""" Abstract parent class for all translations.
		Meta.abstract = True

		TODO: null=True necessary?
	"""
	word = models.ForeignKey(Word, db_index=True)
	language = models.CharField(max_length=5, db_index=True)
	wordid = models.CharField(max_length=200, db_index=True)
	lemma = models.CharField(max_length=200, blank=True)
	# definition = models.CharField(max_length=200, db_index=True)
	phrase = models.TextField(blank=True)
	explanation = models.TextField(blank=True)
	# TODO: pos = models.CharField(max_length=12)
	pos = models.CharField(max_length=12)
	semtype = models.ManyToManyField(Semtype)
	source = models.ManyToManyField(Source)
	# translations = models.ManyToManyField(Word)
	frequency = models.CharField(max_length=10)
	geography = models.CharField(max_length=10)
	tcomm = models.BooleanField(default=False)
	tcomm_pref = models.BooleanField(default=False)
	# TODO:
	# Need a method here which returns the correct translation string

	# lemma
	# lemma (phrase)
	# lemma (phrase) – explanation
	def _getTrans(self):
		if self.lemma:
			return self.lemma
		elif self.phrase:
			return self.phrase
		elif self.explanation:
			return self.explanation
		else:
			return ''

	def _getAnswer(self):
		word_answers = []
		if self.lemma:
			word_answers.append(self.lemma)
		elif self.phrase:
			word_answers.append(self.phrase)
		return word_answers

	def __unicode__(self):
		return smart_unicode(self._getTrans())

	def save(self, *args, **kwargs):
		self.definition = self._getTrans()
		super(WordTranslation, self).save(*args, **kwargs)


	def __init__(self, *args, **kwargs):
		super(WordTranslation, self).__init__(*args, **kwargs)
		self.definition = self._getTrans()
		self.word_answers = self._getAnswer()


	# class Meta:
	# 	abstract = True

# Following are subclassed from above, no need to add anything special.
#
# class Wordnob(WordTranslation):
# 	class Meta: abstract = True
# class Wordswe(WordTranslation):
# 	class Meta: abstract = True
# class Wordsme(WordTranslation):
# 	class Meta: abstract = True
# class Wordeng(WordTranslation):
# 	class Meta: abstract = True
# class Worddeu(WordTranslation):
# 	class Meta: abstract = True

class Tagset(models.Model):
	tagset = models.CharField(max_length=25)

	def __unicode__(self):
		return smart_unicode(self.tagset)

class Tagname(models.Model):
	tagname = models.CharField(max_length=25)
	tagset = models.ForeignKey(Tagset)

	def __unicode__(self):
		return smart_unicode(self.tagname)

class Tag(models.Model):
	string = models.CharField(max_length=40, unique=True)
	# TODO: pos = models.CharField(max_length=12)
	attributive = models.CharField(max_length=5)
	case = models.CharField(max_length=5)
	conneg = models.CharField(max_length=5)
	grade = models.CharField(max_length=10)
	infinite = models.CharField(max_length=10)
	mood = models.CharField(max_length=5)
	number = models.CharField(max_length=5)
	personnumber = models.CharField(max_length=8)
	polarity = models.CharField(max_length=5)
	pos = models.CharField(max_length=12)
	possessive = models.CharField(max_length=5)
	subclass = models.CharField(max_length=10)
	tense = models.CharField(max_length=5)

	class Admin:
		pass

	def __unicode__(self):
		return smart_unicode(self.string)

	def fix_attributes(self):

		# TODO: check that all tagsets are in here
		tagset_names = {
			# object attribute: tagset name
			'attributive': 'attributive',
			'case': 'Case',
			'conneg': 'ConNeg',
			'grade': 'Grade',
			'infinite': 'Infinite',
			'mood': 'Mood',
			'number': 'Number',
			'personnumber': 'Person-Number',
			'polarity': 'Polarity',
			'pos': 'Wordclass',
			'possessive': 'Possessive',
			'subclass': 'Subclass',
			'tense': 'Tense',
		}

		tagname_to_set = {}
		for attr, tsetname in tagset_names.items():
			tagnames = Tagname.objects.filter(tagset__tagset=tsetname)\
							.values_list('tagname', flat=True)

			for t in tagnames:
					tagname_to_set[t] = attr


		for piece in self.string.split('+'):
			attrname = tagname_to_set.get(piece, False)

			if attrname:
				self.__setattr__(attrname, piece)

	def create(self, *args, **kwargs):
		self.fix_attributes()
		super(Tag, self).create(*args, **kwargs)

	# def save(self, *args, **kwargs):
	# 	self.fix_attributes()
	# 	super(Tag, self).save(*args, **kwargs)

class Form(models.Model):
	word = models.ForeignKey(Word)
	tag = models.ForeignKey(Tag)
	fullform = models.CharField(max_length=200)
	dialects = models.ManyToManyField(Dialect)
	feedback = models.ManyToManyField('Feedbackmsg')
 	objects = BulkManager()

 	@property
 	def dialect(self):
 		return [d.dialect for d in self.dialects.all() if len(d.dialect) == 2]

	def __unicode__(self):
		return smart_unicode(self.fullform)
		# Testing-- related lookups seem to be quite slow in MySQL...?
		# return '%s; %s+%s' % (self.fullform, self.word.lemma, self.tag)

	def getBaseform(self, match_num=False, return_all=False):
		""" Gets the base form (e.g., citation/dictionary form) for
			the wordform. Nouns -> Nom+Sg, Verbs -> Inf

			@param match_num:
				True - If the form supplied is a noun and plural
					   the baseform will be Nominative Plural

			TODO: baseforms for
			Pron+Refl+Sg+Nom
			 ** no form

			Pron+Refl+Pl+Nom
			  ** no form

			All Recipr+Pl forms are not returning baseforms
				Pron+Recipr+Pl+Acc+PxDu2
				Pron+Recipr+Pl+Ill+PxDu2
				Pron+Recipr+Pl+Loc+PxDu2
				Pron+Recipr+Pl+Com+PxDu2
				 ... etc
		"""

		# Exceptional behavior for Der/AV, and other possibilities, f. ex., Der/AN
		if self.tag.subclass.find('Der/') > -1:
			# Der  /  AV
			_, _, poses = self.tag.subclass.partition('/')

			if poses in ['PassL', 'PassS']:
				# Chop off V+Der/PassL bit, and search for forms with tag that
				# is the rest.
				rest = self.tag.string.replace('+Der/PassS+V', '')\
										.replace('+Der/PassL+V', '')
				return self.word.form_set.filter(tag__string=rest)[0].getBaseform(
					match_num=match_num,
					return_all=False)
			if len(poses) == 2:
				_from, _to = poses[0], poses[1]
				# Return the base form of a tag from the word's form set that
				# matches the _from part of the derivation tag, this will be
				# the underived wordform's base form
				return self.word.form_set.filter(tag__pos=_from)[0].getBaseform(
					match_num=match_num,
					return_all=False)

		if self.tag.pos in ['N', 'n', 'Num']:
			if match_num:
				number = self.tag.number
			else:
				number = 'Sg'
			baseform_num = self.word.form_set.filter(tag__case='Nom')

			baseform = baseform_num.filter(tag__number=number)
			if baseform.count() == 0 and number == 'Sg' and baseform_num.count() > 0:
				baseform = baseform_num
		elif self.tag.pos == 'Pron':

			person_match_attr = False
			if self.tag.personnumber:
				person_match_attr = 'personnumber'
			elif self.tag.possessive:
				person_match_attr = 'possessive'

			number_match = False
			if self.tag.number:
				number_match = self.tag.number
			else:
				number_match = 'Sg'

			kwargs = {}

			if person_match_attr:
				try:
					person_value = self.tag__getattribute(person_match_attr)
				except AttributeError:
					# TODO: handle error?
					person_value = ''
				kwargs['tag__' + person_match_attr] = person_value

			base_case = 'Nom'
			if self.tag.subclass in ['Recipr', 'Refl']:
				base_case = 'Gen'

			if self.tag.subclass in ['Recipr', 'Dem', 'Rel']: # Rel added by Heli
				kwargs['tag__number'] = number_match

			#if self.tag.subclass:
			 #    kwargs['tag__subclass'] = self.tag.subclass # added by Heli
			# print kwargs
			baseform_num = self.word.form_set.filter(tag__case=base_case)
			#print baseform_num
			baseform = baseform_num.filter(**kwargs)

			if baseform.count() == 0 and number_match == 'Sg' and baseform_num.count() > 0:
				baseform = baseform_num

		elif self.tag.pos in ['V', 'v']:
			if self.word.lemma in [u'lea', u'ii']:
				kwarg = {'tag__personnumber': 'Sg3'}
			else:
				kwarg = {'tag__infinite': 'Inf'}

			# Non-derived verbs need to exclude Der
			baseform = self.word.form_set.exclude(tag__string__contains='Der')\
											.filter(**kwarg)
			if baseform.count() == 0:
				baseform = self.word.form_set.filter(tag__personnumber='Sg3')
			if baseform.count() == 0:
				raise Form.DoesNotExist

		elif self.tag.pos in ['A', 'a']:
			# TODO: veljer systemet Coll og Ord grunnformen?
			if match_num:  # added by Heli, by example of N
				number = self.tag.number
			else:
				number = 'Sg'

			if self.tag.subclass:
				subclass = self.tag.subclass
			else:
				subclass = ''

			print subclass
			baseform = self.word.form_set.filter(tag__case='Nom',
													tag__number=number,
													tag__grade='',
													tag__subclass=subclass,
													tag__attributive='')
			# print baseform
			if baseform.count() == 0:
				baseform = self.word.form_set.all()
			if not baseform:
				raise Form.DoesNotExist
		else:
			raise Form.DoesNotExist

		try:
			if return_all:
				return baseform
			else:
				return baseform[0]
		except IndexError:
			raise Form.DoesNotExist


# akte, snjaltje, brorredh, gaavnedidh, tjuatsajidh

## missing = []
## for w in Word.objects.all():
##  fs = w.form_set.all()
##  if fs.count() > 0:
##   try:print fs[0].getBaseform().fullform
##   except:print '*** ' + w.lemma; missing.append(w)


############# MORFA FEEDBACK

class Feedbackmsg(models.Model):
	"""
		XML code for messages in messages.xml
	"""
	msgid = models.CharField(max_length=100)

	def __unicode__(self):
		return self.msgid


class Feedbacktext(models.Model):
	"""
		Message text in messages.xml
	"""
	message = models.CharField(max_length=200)
	language = models.CharField(max_length=6)
	feedbackmsg = models.ForeignKey(Feedbackmsg)
	order = models.CharField(max_length=3, blank=True)

	def __unicode__(self):
		attrs = [
				self.language,
				self.order,
				self.message,
			]
		S = unicode('/'.join([a for a in attrs if a.strip()])).encode('utf-8')
		return smart_unicode(self.language + u':' + self.message)




########### CONTEXT-MORFA, VASTA

class Question(models.Model):
	qid = models.CharField(max_length=200)
	level = models.IntegerField()
	task = models.CharField(max_length=20)
	string = models.CharField(max_length=200)
	qtype = models.CharField(max_length=20)
	qatype = models.CharField(max_length=20)
	question = models.ForeignKey('self',
								 blank=True,
								 null=True,
								 related_name='answer_set')
	gametype = models.CharField(max_length=7)
	lemmacount = models.IntegerField()
	source = models.ManyToManyField(Source)
	def __unicode__(self):
		return self.qid + ': ' + self.string

class QElement(models.Model):
	"""
		QElements are individual elements of a question, such as a pronoun, subject, N-ACC, etc.
		They contain a set of WordQElements which represent each possible Word item in the database
		which could be filled in for a given slot in a question.

		WordQElements are filtered when installed by the database, as such there should be no need
		to filter in qagame (???)


	"""
	question = models.ForeignKey(Question, null=True)
	syntax = models.CharField(max_length=50)
	identifier = models.CharField(max_length=20)
	task = models.CharField(max_length=20)  # added for VastaS
	gametype = models.CharField(max_length=7)
	agreement = models.ForeignKey('self',
								  blank=True,
								  null=True,
								  related_name='agreement_set')

	semtype = models.ForeignKey(Semtype, null=True) # ManyToMany instead?
	tags = models.ManyToManyField(Tag)
	game = models.CharField(max_length=20)
	copy = models.ForeignKey('self',
							 blank=True,
							 null=True,
							 related_name='copy_set')
	def __unicode__(self):
		return smart_unicode(self.question.string + ': ' + self.identifier)

class WordQElement(models.Model):
	"""

	"""
	word = models.ForeignKey(Word, null=True)
	qelement = models.ForeignKey(QElement, null=True)
	# semtype = models.ForeignKey(Semtype, null=True)


############ SAHKA

class Dialogue(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)

class Utterance(models.Model):
    utterance = models.CharField(max_length=500,blank=True,null=True)
    utttype = models.CharField(max_length=20,blank=True,null=True)
    links = models.ManyToManyField('LinkUtterance')
    name = models.CharField(max_length=200,blank=True,null=True)
    topic = models.ForeignKey('Topic')
    formlist = models.ManyToManyField(Form)

class UElement(models.Model):
    utterance=models.ForeignKey(Utterance, null=True)
    syntax = models.CharField(max_length=50)
    tag = models.ForeignKey(Tag,null=True,blank=True)

class LinkUtterance(models.Model):
    link = models.ForeignKey(Utterance,null=True,blank=True)
    target = models.CharField(max_length=20,null=True,blank=True)
    variable = models.CharField(max_length=20,null=True,blank=True)
    constant = models.CharField(max_length=20,null=True,blank=True)

class Topic(models.Model):
    topicname = models.CharField(max_length=50,blank=True,null=True)
    dialogue = models.ForeignKey(Dialogue)
    number = models.IntegerField(null=True)
    image = models.CharField(max_length=50,null=True,blank=True)
    formlist = models.ManyToManyField(Form)

######### EXTRA
class Grammarlinks(models.Model):
	name = models.CharField(max_length=200,blank=True,null=True)
	address = models.CharField(max_length=800,blank=True,null=True)
	language = models.CharField(max_length=5,blank=True,null=True)
