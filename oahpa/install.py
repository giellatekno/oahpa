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
parser.add_option("-d", "--db", dest="add_db",
                  action="store_true", default=False,
                  help="Used for adding tag infoformation to database")
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
parser.add_option("-l", "--place", dest="placenamefile",
                  action="store_true", default=False,
                  help="If placenames")
parser.add_option("-u", "--update", dest="update",
                  action="store_true", default=False,
                  help="If update data")

(options, args) = parser.parse_args()

linginfo = Paradigm()
questions = Questions()

if options.tagfile:
    linginfo.handle_tags(options.tagfile, options.add_db)

if options.paradigmfile:
    linginfo.read_paradigms(options.paradigmfile, options.tagfile, options.add_db)

if options.grammarfile:
    questions.read_grammar(options.grammarfile)
    exit()
    
if options.questionfile:
    questions.read_questions(options.questionfile)
    exit()

if options.semtypefile:
    questions.read_semtypes(options.semtypefile)
    exit()

if not options.infile:
    exit()


xmlfile=file(options.infile)
tree = _dom.parse(options.infile)

lex = tree.getElementsByTagName("lexicon")[0]
mainlang = lex.getAttribute("xml:lang")
if not mainlang:
    mainlang="sme"

for e in tree.getElementsByTagName("entry"):

    # Store first unique fields
    id=e.getAttribute("id")
    lemma=e.getElementsByTagName("lemma")[0].firstChild.data
    if not id:
        id=lemma
    stem=""
    dialect=""
    diphthong=0
    gradation=0
    rime=""
    if e.getElementsByTagName("stem"):
        stem=e.getElementsByTagName("stem")[0].getAttribute("class")
        diphthong_text=e.getElementsByTagName("stem")[0].getAttribute("diphthong")
        if diphthong_text == "no": diphthong = 0
        else: diphthong = 1
        gradation_text=e.getElementsByTagName("stem")[0].getAttribute("gradation")
        if gradation_text == "no": gradation = 0
        else: gradation = 1
        rime=e.getElementsByTagName("stem")[0].getAttribute("rime")

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
    if mainlang == "nob":
        word_elements = Wordnob.objects.filter(Q(wordid=id))
    else:
        word_elements = Word.objects.filter(Q(wordid=id) & Q(pos=pos))

    # Update old one if the word was found
    if word_elements:
        # If adding placenames, do not update already existing entries.
        if options.placenamefile: continue            

        if not options.update:
            print "Entry exists for ", lemma;
        w=word_elements[0]
        w.pos=pos
        w.lemma=lemma
        w.stem=stem
        w.dialect=dialect
        w.save()
    else:
        if options.update:
            print "Adding entry for ", lemma , ".";
        # Otherwise create new word
        if mainlang=="nob":
            w=Wordnob(wordid=id,lemma=id,pos=pos);
        else:   
            w=Word(wordid=id,lemma=lemma,pos=pos,stem=stem,diphthong=diphthong,rime=rime,gradation=gradation,dialect=dialect);
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

        # Give placenames special semantic tag
        # This is temporary solution.
        if options.placenamefile:
            sem_entry, created = Semtype.objects.get_or_create(semtype="PLACE-NAME-LEKSA")
            if created:
                print "Created semtype entry with name PLACE-NAME-LEKSA"
            w.semtype.add(sem_entry)
            w.save()

        else:
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
        

    if e.getElementsByTagName("valency"):
        elements=e.getElementsByTagName("valency")
        for el in elements:
            val=el.getAttribute("class")
            if val:
                w.valency = val
                w.save()

    # Add translations
    translations = e.getElementsByTagName("translations")[0]
    elements=translations.getElementsByTagName("tr")
    for el in elements:        
        if el.firstChild:
            translation=el.firstChild.data
            lang=el.getAttribute("xml:lang")
            if lang == "sme":
                transl, created = Word.objects.get_or_create(wordid=translation)
                if created:
                    transl.lemma=translation
                    transl.save()
            else:
                if lang == "nob":
                    transl, created = Wordnob.objects.get_or_create(wordid=translation)
                    if created:
                        transl.lemma=translation
                        transl.save()

                    # If placenames
                    # Give norwegian words same semantic classes as sami words.
                    # Temporary solution.
                    if options.placenamefile:
                        sem_entry, created = Semtype.objects.get_or_create(semtype="PLACE-NAME-LEKSA")
                        if created:
                            print "Created semtype entry with name PLACE-NAME-LEKSA"
                        transl.semtype.add(sem_entry)
                        transl.save()

                else: continue

            # Add reference to the new word object as translation.
            w.translations.add(transl)
            w.save()                   


"""
semtypes = ['ABSTRACTS','ACTIONS','AMOUNTS','ANIMALS','BODYPART','CHRISTMAS','CLOTHES','CONTAINERS','CONVERSATION','EDUCATION','FAMILY','FEELINGS','GROUPS','HUMANS','HANDICRAFTS','ILLNESS','JOB','NATURE','OTHERS','PLACES','PLANTS','PROFESSION','SCHOOL','SOUNDS','SOUP','SUBJECTS','THINGS','TIME','TRAVELLING','WEATHER']

for type in semtypes:
    st=Semtype(semtype=type)
    st.save()

"""
