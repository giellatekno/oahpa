from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

SUBTYPE_CHOICES = (
    ('bisyllabic', _('bisyllabic')),
    ('trisyllabic', _('trisyllabic')),
    ('contracted', _('contracted')),
)

POS_CHOICES = (
    ('N', _('noun')),
    ('V', _('verb')),
    ('Adj', _('adjective')),
)

class Semtype(models.Model):
    semtype = models.CharField(max_length=50)

class Source(models.Model):
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

class Word(models.Model):
    wordid = models.CharField(max_length=200)
    lemma = models.CharField(max_length=200)
    pos = models.CharField(max_length=5)
    stem = models.CharField(max_length=20)
    dialect = models.CharField(max_length=20)
    valency = models.CharField(max_length=10)
    semtype = models.ManyToManyField(Semtype)
    source = models.ManyToManyField(Source)
    diphthong=models.BooleanField(null=True)
    gradation=models.CharField(max_length=5)
    rime = models.CharField(max_length=20)
    soggi = models.CharField(max_length=10)
    compare = models.CharField(max_length=5)
    translations = models.ManyToManyField('Wordnob')
    frequency = models.CharField(max_length=10)
    geography = models.CharField(max_length=10)
    
class Wordnob(models.Model):
    wordid = models.CharField(max_length=200)
    lemma = models.CharField(max_length=200)
    pos = models.CharField(max_length=5)
    semtype = models.ManyToManyField(Semtype)
    source = models.ManyToManyField(Source)
    translations = models.ManyToManyField(Word)
    frequency = models.CharField(max_length=10)
    geography = models.CharField(max_length=10)

class Tagset(models.Model):
    tagset = models.CharField(max_length=25)

class Tagname(models.Model):
    tagname=models.CharField(max_length=25)
    tagset=models.ForeignKey(Tagset)    

class Tag(models.Model):
    string = models.CharField(max_length=25)
    pos = models.CharField(max_length=5)
    case = models.CharField(max_length=5)
    number = models.CharField(max_length=5)
    possessive = models.CharField(max_length=5)
    grade = models.CharField(max_length=10)
    infinite = models.CharField(max_length=10)
    personnumber = models.CharField(max_length=6)
    conneg = models.CharField(max_length=5)
    polarity = models.CharField(max_length=5)
    tense = models.CharField(max_length=5)
    mood = models.CharField(max_length=5)
    subclass = models.CharField(max_length=10)
    attributive = models.CharField(max_length=5)
    class Admin:
        pass

class Form(models.Model):
    word = models.ForeignKey(Word)
    tag = models.ForeignKey(Tag)
    fullform = models.CharField(max_length=200, core=True)

class Question(models.Model):
    string = models.CharField(max_length=200)
    qtype = models.CharField(max_length=20)
    qatype = models.CharField(max_length=20)
    answer = models.ForeignKey('self', blank=True, null=True, related_name='answer_set')
    gametype = models.CharField(max_length=5)
    
class QElement(models.Model):
    question=models.ForeignKey(Question, null=True)
#    semtype = models.ForeignKey(Semtype, null=True)
#    word = models.ForeignKey(Word, null=True)
    optional = models.BooleanField(null=True)
    syntax = models.CharField(max_length=50)
    identifier = models.CharField(max_length=20)
    gametype = models.CharField(max_length=5)
    agreement = models.ForeignKey('self', blank=True, null=True, related_name='agreement_set')
    tags = models.ManyToManyField(Tag)
    game = models.CharField(max_length=20)
    copy = models.ForeignKey('self', blank=True, null=True, related_name='copy_set')

class WordQElement(models.Model):
    word = models.ForeignKey(Word, null=True)
    qelement = models.ForeignKey(QElement, null=True)
    semtype = models.ForeignKey(Semtype, null=True)

class Feedbackmsg(models.Model):
    msgid = models.CharField(max_length=50)
    message = models.CharField(max_length=200)

class Feedback(models.Model):
    messages = models.ManyToManyField(Feedbackmsg)
    pos = models.CharField(max_length=5)
    stem = models.CharField(max_length=20)
    diphthong=models.NullBooleanField(blank=True)
    gradation=models.CharField(max_length=5)
    rime = models.CharField(max_length=20)
    soggi = models.CharField(max_length=10)
    case = models.CharField(max_length=5)
    number = models.CharField(max_length=5)
    personnumber = models.CharField(max_length=5)
    tense = models.CharField(max_length=5)
    mood = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)

