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
    semtype = models.CharField(max_length=20)

class Source(models.Model):
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

class Translationnob(models.Model):
    translation = models.CharField(max_length=200, core=True)

class Word(models.Model):
    lemma = models.CharField(max_length=200)
    pos = models.CharField(max_length=5)
    stem = models.CharField(max_length=20)
    dialect = models.CharField(max_length=20)
    valency = models.CharField(max_length=10)
    semtype = models.ManyToManyField(Semtype)
    source = models.ManyToManyField(Source)
    translation = models.ManyToManyField(Translationnob)
 
class Tag(models.Model):
    string = models.CharField(max_length=20)
    pos = models.CharField(max_length=5)
    case = models.CharField(max_length=5)
    number = models.CharField(max_length=5)
    possessive = models.CharField(max_length=5)
    grade = models.CharField(max_length=5)
    infinite = models.CharField(max_length=10)
    personnumber = models.CharField(max_length=6)
    conneg = models.CharField(max_length=5)
    polarity = models.CharField(max_length=5)
    tense = models.CharField(max_length=5)
    mood = models.CharField(max_length=5)
    subclass = models.CharField(max_length=5)
    attributive = models.CharField(max_length=5)
    class Admin:
        pass

class Form(models.Model):
    word = models.ForeignKey(Word)
    tag = models.ForeignKey(Tag)
    fullform = models.CharField(max_length=200, core=True)

class Element(models.Model):
    semtype = models.ForeignKey(Semtype, null=True)
    word = models.ForeignKey(Word, null=True)
    tagspec = models.CharField(max_length=50)
    pos = models.CharField(max_length=5)
    #independent = models.BooleanField()
    #optional = models.BooleanField()

class Question(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)

class QElement(models.Model):
    element=models.ForeignKey(Element)
    question=models.ForeignKey(Question)
    number = models.IntegerField()
    elementtype = models.CharField(max_length=20)

