from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Comment(models.Model):
    lang = models.CharField(max_length=5)	
    comment = models.CharField(max_length=100)	
    level = models.CharField(max_length=5)

class Log(models.Model):
    game = models.CharField(max_length=30)
    date = models.DateField(blank=True, null=True)
    userinput = models.CharField(max_length=200)
    iscorrect = models.BooleanField()
    correct = models.CharField(max_length=200)
    example = models.CharField(max_length=200,null=True)
    comment = models.CharField(max_length=200)

class Semtype(models.Model):
    semtype = models.CharField(max_length=50)

class Source(models.Model):
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

# First, define the Manager subclass.
class NPosManager(models.Manager):
    def get_query_set(self):
        return super(NPosManager, self).get_query_set().filter(pos='N')

class Dialect(models.Model):
    dialect = models.CharField(max_length=5)
    name = models.CharField(max_length=100)

class Word(models.Model):
    wordid = models.CharField(max_length=200)
    lemma = models.CharField(max_length=200)
    pos = models.CharField(max_length=5)
    stem = models.CharField(max_length=20)
    valency = models.CharField(max_length=10)
    semtype = models.ManyToManyField(Semtype)
    source = models.ManyToManyField(Source)
    diphthong=models.CharField(max_length=5)
    gradation=models.CharField(max_length=20)
    rime = models.CharField(max_length=20)
    attrsuffix = models.CharField(max_length=20)
    soggi = models.CharField(max_length=10)
    compare = models.CharField(max_length=5)
    translations = models.ManyToManyField('Wordnob')
    frequency = models.CharField(max_length=10)
    geography = models.CharField(max_length=10)
    dialects = models.ManyToManyField(Dialect,null=True)
    objects = models.Manager() # The default manager.
    N_objects = NPosManager() # The Noun-specific manager
    
    
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
    fullform = models.CharField(max_length=200)
    dialects = models.ManyToManyField(Dialect)

########### CONTEXT-MORFA, VASTA

class Question(models.Model):
    qid = models.CharField(max_length=200)
    level = models.IntegerField(max_length=3)
    task = models.CharField(max_length=20)
    string = models.CharField(max_length=200)
    qtype = models.CharField(max_length=20)
    qatype = models.CharField(max_length=20)
    question = models.ForeignKey('self', blank=True, null=True, related_name='answer_set')
    gametype = models.CharField(max_length=5)
    source = models.ManyToManyField(Source)
    
class QElement(models.Model):
    question=models.ForeignKey(Question, null=True)
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

############# MORFA FEEDBACK

class Feedbackmsg(models.Model):
    msgid = models.CharField(max_length=50)
    message = models.CharField(max_length=200)

class Feedback(models.Model):
    messages = models.ManyToManyField(Feedbackmsg)
    pos = models.CharField(max_length=5,blank=True,null=True)
    stem = models.CharField(max_length=20,blank=True,null=True)
    diphthong=models.CharField(max_length=5,blank=True,null=True)
    gradation=models.CharField(max_length=15,null=True,blank=True)
    rime = models.CharField(max_length=20,null=True,blank=True)
    soggi = models.CharField(max_length=10,null=True,blank=True)
    case2 = models.CharField(max_length=5,null=True,blank=True)
    number = models.CharField(max_length=5,null=True,blank=True)
    personnumber = models.CharField(max_length=5,null=True,blank=True)
    tense = models.CharField(max_length=5,null=True,blank=True)
    mood = models.CharField(max_length=10,null=True,blank=True)
    grade = models.CharField(max_length=10,null=True,blank=True)
    attrsuffix = models.CharField(max_length=10,null=True,blank=True)
    attributive = models.CharField(max_length=10,null=True,blank=True)
    dialects = models.ManyToManyField(Dialect)
    
    class Meta:
        unique_together = ("pos","stem","diphthong","gradation","rime","soggi","case2","number","personnumber","tense","mood","grade","attrsuffix","attributive")

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
    number = models.IntegerField(max_length=3,null=True)
    image = models.CharField(max_length=50,null=True,blank=True)
    formlist = models.ManyToManyField(Form)


######### EXTRA
class Grammarlinks(models.Model):
    name = models.CharField(max_length=200,blank=True,null=True)
    address = models.CharField(max_length=800,blank=True,null=True)
    language = models.CharField(max_length=5,blank=True,null=True)
