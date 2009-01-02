# -*- coding: utf-8 -*-
from settings import *
from drill.models import *
from django.db.models import Q
from xml.dom import minidom as _dom
import sys
import re
import string
import codecs


# Lexicons: words

class Words:

    def install_lexicon(self,infile,paradigmfile=None,placenamefile=None):

        xmlfile=file(infile)
        tree = _dom.parse(infile)
        
        lex = tree.getElementsByTagName("lexicon")[0]
        mainlang = lex.getAttribute("xml:lang")
        if not mainlang and not placenamefile:
            print "Attribute mainlang not defined in", infile, "stop."
            sys.exit()

        for e in tree.getElementsByTagName("entry"):
            
            # Store first unique fields
            id=e.getAttribute("id")
            lemma=e.getElementsByTagName("lemma")[0].firstChild.data
            if not id:
                id=lemma
            stem=""
            dialects=["GG","KJ"]
            diphthong="no"
            gradation=""
            rime=""
            attrsuffix=""
            soggi=""
            valency=""
            compare=""
            frequency=""
            geography=""
            only_sg = 0
            only_pl = 0

            if e.getElementsByTagName("stem"):
                stem=e.getElementsByTagName("stem")[0].getAttribute("class")
                diphthong=e.getElementsByTagName("stem")[0].getAttribute("diphthong")
                gradation=e.getElementsByTagName("stem")[0].getAttribute("gradation")
                rime=e.getElementsByTagName("stem")[0].getAttribute("rime")
                if rime=="0": rime="norime"
                soggi=e.getElementsByTagName("stem")[0].getAttribute("soggi")
                compare=e.getElementsByTagName("stem")[0].getAttribute("compare")
                attrsuffix=e.getElementsByTagName("stem")[0].getAttribute("attrsuff")
                if attrsuffix == "0": attrsuffix="noattr"
        
            for d in e.getElementsByTagName("dialect"):
                dialect=d.getAttribute("class")
                if dialect:
                    invd=dialect.lstrip("NOT-")
                    dialects.remove(invd)
    
            if e.getElementsByTagName("frequency"):
                frequency=e.getElementsByTagName("frequency")[0].getAttribute("class")

            if e.getElementsByTagName("geography"):
                geography=e.getElementsByTagName("geography")[0].getAttribute("class")

            if e.getElementsByTagName("only-sg"):
                only_sg = 1
            if e.getElementsByTagName("only-pl"):
                only_pl = 1

            if e.getElementsByTagName("valency"):
                valencies = e.getElementsByTagName("valency")[0]
                for val in valencies.getElementsByTagName("val"):
                    valency = val.getAttribute("class")
                    if valency: break

            # Part of speech information
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
                
                w=word_elements[0]
                w.pos=pos
                w.lemma=lemma
                w.stem=stem
                w.rime=rime
                w.compare = compare
                w.attrsuffix = attrsuffix
                w.soggi=soggi
                w.gradation=gradation
                w.diphthong=diphthong
                if not mainlang == "nob":
                    for d in dialects:
                        dia, created = Dialect.objects.get_or_create(dialect=d)
                        w.dialects.add(dia)
                        w.save()

                w.valency = valency
                w.frequency = frequency
                w.geography = geography
                w.save()

            # If adding placenames, do not update anymore
            #if placenamefile: continue  

            else:
                # Otherwise create new word
                if mainlang=="nob":
                    w=Wordnob(wordid=id,lemma=id,pos=pos);
                else:   
                    w=Word(wordid=id,lemma=lemma,pos=pos,stem=stem,diphthong=diphthong,\
                           rime=rime,soggi=soggi,gradation=gradation,attrsuffix=attrsuffix);
                    w.save()

                for d in dialects:
                    dia, created = Dialect.objects.get_or_create(dialect=d)
                    w.dialects.add(dia)
                    w.save()
            w.save()
            
            # Add forms and tags
            if paradigmfile:
                linginfo.create_paradigm(lemma,pos)
                for f in linginfo.paradigm:

                    g=f.classes
                    if w.pos == "A" and w.compare == "no" and \
                           (g.get('Grade')=="Comp" or g.get('Grade')=="Superl"):
                        continue
                    
                    t,created=Tag.objects.get_or_create(string=f.tags,pos=g.get('Wordclass', ""),\
                                                        number=g.get('Number',""),case=g.get('Case',""),\
                                                        possessive=g.get('Possessive',""),\
                                                        grade=g.get('Grade',""),\
                                                        infinite=g.get('Infinite',""), \
                                                        personnumber=g.get('Person-Number',""),\
                                                        polarity=g.get('Polarity',""),\
                                                        tense=g.get('Tense',""),mood=g.get('Mood',""), \
                                                        subclass=g.get('Subclass',""),\
                                                        attributive=g.get('Attributive',""))

                    t.save()

                    form, created = Form.objects.get_or_create(fullform=f.form,tag=t,word=w)
                    if len(f.dialects)==1: dialects2 = f.dialects[:]
                    else: dialects2 = dialects[:]
                    for d in dialects2:
                        dia, created = Dialect.objects.get_or_create(dialect=d)
                        form.dialects.add(dia)
                        form.save()
                    form.save()

            if only_sg:
                print "deleting forms for", w.lemma
                Form.objects.filter(Q(word=w.id) & Q(tag__number="Pl")).delete()
            if only_pl:
                print "deleting forms for", w.lemma
                Form.objects.filter(Q(word=w.id) & Q(tag__number="Sg")).delete
 				

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
                if placenamefile:
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
        

            # Add translations
            translations = e.getElementsByTagName("translations")[0]
            elements=translations.getElementsByTagName("tr")
            for el in elements:        
                if el.firstChild:
                    translation=el.firstChild.data
                    lang=el.getAttribute("xml:lang")
                    if lang == "sme":
                        if Word.objects.filter(wordid=translation,pos=pos).count()>0:
                            transl = Word.objects.filter(wordid=translation,pos=pos)[0]
                        else:
                            transl, created = Word.objects.get_or_create(wordid=translation,pos=pos)
                            if created:
                                transl.lemma=translation
                                transl.save()
                                # Add reference to the new word object as translation.
                        w.translations.add(transl)
                        w.save()                   

                    else:
                        if lang == "nob":
                            transl, created = Wordnob.objects.get_or_create(wordid=translation)
                            if created:
                                transl.lemma=translation
                                transl.save()
                            w.translations.add(transl)
                            w.save()
								
                            # special treatment for å-verbs.
                            if pos=="V":
                                oo = "å".decode('utf8')
                                wordform = translation.lstrip(oo + " ")
                                transl, created = Wordnob.objects.get_or_create(wordid=wordform)
                                if created:
                                    transl.lemma=wordform
                                    transl.save()
                                # Add reference to the new word object as translation.
                                w.translations.add(transl)
                                w.save()                   



                            # If placenames
                            # Give norwegian words same semantic classes as sami words.
                            # Temporary solution.
                            if placenamefile:
                                sem_entry, created = Semtype.objects.get_or_create(semtype="PLACE-NAME-LEKSA")
                                if created:
                                    print "Created semtype entry with name PLACE-NAME-LEKSA"
                                    transl.semtype.add(sem_entry)
                                    transl.frequency=w.frequency
                                    transl.geography=w.geography
                                    transl.save()

                                transl.save()

