from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from settings import *
from drill.models import *
from xml.dom import minidom as _dom
from optparse import OptionParser
from django.db.models import Q
import sys
import re
import codecs
from ling import Paradigm, Questions

parser = OptionParser()

parser.add_option("-f", "--file", dest="infile",
                  help="lexicon file name")
parser.add_option("-p", "--pos", dest="pos",
                  help="Pos info")
parser.add_option("-t", "--tagfile", dest="tagfile",
                  help="List of tags and tagsets")
parser.add_option("-r", "--paradigmfile", dest="paradigmfile",
                  help="Generate paradigms")
parser.add_option("-q", "--questionfile", dest="questionfile",
                  help="XML-file that contains questions")
parser.add_option("-g", "--grammarfile", dest="grammarfile",
                  help="XML-file for grammar defaults for questions")
parser.add_option("-s", "--sem", dest="semtypefile",
                  help="XML-file semantic subclasses")
parser.add_option("-u", "--update", dest="update",
                  action="store_true", default=False,
                  help="If update data")

(options, args) = parser.parse_args()

linginfo = Paradigm()
questions = Questions()

if options.tagfile:
    linginfo.handle_tags(options.tagfile)

if options.paradigmfile:
    linginfo.read_paradigms(options.paradigmfile)

if options.grammarfile:
    questions.read_grammar(options.grammarfile)
    exit()
    
if options.questionfile:
    questions.read_questions(options.questionfile)
    exit()

if options.semtypefile:
    questions.read_semtypes(options.semtypefile)
    exit()

    
xmlfile=file(options.infile)
tree = _dom.parse(options.infile)

for e in tree.getElementsByTagName("entry"):

    # Store first unique fields
    lemma=e.getElementsByTagName("lemma")[0].firstChild.data
    stem=""
    dialect=""
    if e.getElementsByTagName("stem"):
        stem=e.getElementsByTagName("stem")[0].getAttribute("class")
    if e.getElementsByTagName("dialect"):
        dialect=e.getElementsByTagName("dialect")[0].getAttribute("class")

    # Part of speech information
    # Is it in lexicon file or not..
    if options.pos:
        pos=options.pos
    else:
        pos=e.getElementsByTagName("pos")[0].getAttribute("class")       
        if not pos:
            print "Part of speech information not found for ", lemma, ". give it command line: --pos=N"
            sys.exit()

    # Search for existing word in the database.
    word_elements = Word.objects.filter(Q(lemma=lemma) & Q(pos=pos))

    # Update old one if the word was found
    if word_elements:
        if not options.update:
            print "Entry exists for ", lemma;
        w=word_elements[0]
        w.stem=stem
        w.dialect=dialect
    else:
        if options.update:
            print "Adding entry for ", lemma , ".";
        # Otherwise create new word
        w=Word(lemma=lemma,pos=pos,stem=stem,dialect=dialect);
    w.save()
    
    # Add forms and tags
    if options.paradigmfile:
        linginfo.create_paradigm(lemma,pos)		
        for form in linginfo.paradigm:
            g=form.classes
            t,created=Tag.objects.get_or_create(string=form.tags,pos=g.get('Wordclass', ""),\
                                                number=g.get('Number',""),case=g.get('Case',""),\
                                                possessive=g.get('Possessive',""),grade=g.get('Grade',""),\
                                                infinite=g.get('Infinite',""), \
                                                personnumber=g.get('Person-Number',""),\
                                                polarity=g.get('Polarity',""),\
                                                tense=g.get('Tense',""),mood=g.get('Mood',""), \
                                                subclass=g.get('Subclass',""),attributive=g.get('Attributive',""))

            t.save()
            form, created = Form.objects.get_or_create(fullform=form.form,tag=t,word=w)
            form.save()
                
    # Create many-to-many fields
    translations = e.getElementsByTagName("translations")[0]
    elements=translations.getElementsByTagName("tr")
    for el in elements:
        if el.firstChild:
            translation=el.firstChild.data
            lang=el.getAttribute("xml:lang")
            if translation and lang == "nob":
                tr_entry, created = Translationnob.objects.get_or_create(translation=translation)
                w.translation.add(tr_entry)
                w.save()

    
    if e.getElementsByTagName("sources"):
        sources = e.getElementsByTagName("sources")[0]
        elements=sources.getElementsByTagName("book")
        for el in elements:
            book=el.getAttribute("name")
            if book:
                # Add book to the database
                # Leave this if DTD is used
                book_entry, created = Source.objects.get_or_create(name=book)
                if created:
                    print "Created book entry with name ", book
                w.source.add(book_entry)
                w.save()

    if e.getElementsByTagName("semantics"):
        semantics = e.getElementsByTagName("semantics")[0]
        elements=semantics.getElementsByTagName("sem")
        for el in elements:
            sem=el.getAttribute("class")
            if sem:
                # Add semantics entry if not found.
                # Leave this if DTD is used.
                sem_entry, created = Semtype.objects.get_or_create(semtype=sem)
                if created:
                    print "Created semtype entry with name ", sem
                w.semtype.add(sem_entry)
                w.save()

        elements=semantics.getElementsByTagName("valency")
        for el in elements:
            val=el.getAttribute("class")
            if val:
                w.valency = val
                w.save()


"""
semtypes = ['ABSTRACTS','ACTIONS','AMOUNTS','ANIMALS','BODYPART','CHRISTMAS','CLOTHES','CONTAINERS','CONVERSATION','EDUCATION','FAMILY','FEELINGS','GROUPS','HUMANS','HANDICRAFTS','ILLNESS','JOB','NATURE','OTHERS','PLACES','PLANTS','PROFESSION','SCHOOL','SOUNDS','SOUP','SUBJECTS','THINGS','TIME','TRAVELLING','WEATHER']

for type in semtypes:
    st=Semtype(semtype=type)
    st.save()

"""
