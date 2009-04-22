# -*- coding: utf-8 -*-
from settings import *
from drill.models import *
from django.db.models import Q
from xml.dom import minidom as _dom
from django.utils.encoding import force_unicode
import sys
import re
import string
import codecs


# Lexicons: words

class Words:

    def install_lexicon(self,infile,linginfo,delete=None,paradigmfile=None,placenamefile=None):

        xmlfile=file(infile)
        tree = _dom.parse(infile)
        
        lex = tree.getElementsByTagName("lexicon")[0]
        mainlang = lex.getAttribute("xml:lang")
        if not mainlang and not placenamefile:
            print "Attribute mainlang not defined in", infile, "stop."
            sys.exit()

        self.all_wordids=[]

        for e in tree.getElementsByTagName("entry"):
            pos=e.getElementsByTagName("pos")[0].getAttribute("class")
            self.store_word(e,linginfo,mainlang,paradigmfile,placenamefile,delete)

        if delete and pos and not placenamefile:
            allids = Word.objects.filter(Q(pos=pos) & ~Q(semtype__semtype="PLACE-NAME-LEKSA")).values_list('wordid',flat=True)
            for a in allids:
                if force_unicode(a) not in set(self.all_wordids):
                    print "Word id not found from xml. Deleting:", a
                    word = Word.objects.get(pos=pos,wordid=a)
                    word.delete()

        if delete and placenamefile:
            allids = Word.objects.filter(Q(pos="N") & Q(semtype__semtype="PLACE-NAME-LEKSA")).values_list('wordid',flat=True)
            for a in allids:
                if force_unicode(a) not in set(self.all_wordids):
                    print "Word id not found from xml. Deleting:", a
                    word = Word.objects.get(pos=pos,wordid=a)
                    word.delete()

    def add_translation(self,el,w,pos,placenamefile):
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

    def add_semantics(self,e,w,placenamefile):
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
                    print sem					
                    # Add semantics entry if not found.
                    # Leave this if DTD is used.
                    sem_entry, created = Semtype.objects.get_or_create(semtype=sem)
                    if created:
                        print "Created semtype entry with name ", sem
                    w.semtype.add(sem_entry)
                    w.save()        

    def add_sources(self,e,w):
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

    def store_word(self,e,linginfo,mainlang,paradigmfile,placenamefile,delete):

        # Store first unique fields
        id=e.getAttribute("id")
        lemma=e.getElementsByTagName("lemma")[0].firstChild.data
        if not id:
            id=lemma
        self.all_wordids.append(id)
        stem=""
        forms=""
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
        presentationform = ""
        only_sg = 0
        only_pl = 0
        noleksa = 0
        print lemma
        if e.getElementsByTagName("forms"):
            forms=e.getElementsByTagName("forms")[0]
			
        if e.getElementsByTagName("presentationform"):
            presentationform=e.getElementsByTagName("presentationform")[0].firstChild.data

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
        if e.getElementsByTagName("noleksa"):
            noleksa = 1

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
        w=None
        if mainlang == "nob":
            w,created = Wordnob.objects.get_or_create(wordid=id)
        else:
            w,created = Word.objects.get_or_create(wordid=id,pos=pos)

        w.pos=pos
        w.lemma=lemma
        w.presentationform=presentationform
        print presentationform
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

        if mainlang=="sme":
            for d in dialects:
                dia, created = Dialect.objects.get_or_create(dialect=d)
                w.dialects.add(dia)
                w.save()
            
        # Add forms and tags
        if paradigmfile:
            linginfo.create_paradigm(lemma,pos,forms)
            # Remove old forms.
            forms = Form.objects.filter(word=w)
            for f in forms:
                f.delete()
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
                
                form = Form(fullform=f.form,tag=t,word=w)				
                print f.form
                form.save()
                if len(f.dialects)==1: dialects2 = f.dialects[:]
                else: dialects2 = dialects[:]
                for d in dialects2:
                    dia, created = Dialect.objects.get_or_create(dialect=d)
                    form.dialects.add(dia)
                    form.save()
                form.save()

        if only_sg:
            print "deleting plural forms for", w.lemma
            Form.objects.filter(Q(word=w.id) & Q(tag__number="Pl")).delete()
        if only_pl:
            print "deleting singular forms for", w.lemma
            Form.objects.filter(Q(word=w.id) & Q(tag__number="Sg")).delete
        if noleksa:
            print "word not in leksa", w.lemma
            w.leksa=0
        else:
            w.leksa=1

        if e.getElementsByTagName("sources"):
            self.add_sources(e,w)
        
        if e.getElementsByTagName("semantics"):
            self.add_semantics(e,w,placenamefile)
        
        # Add translations
        translations = e.getElementsByTagName("translations")[0]
        elements=translations.getElementsByTagName("tr")
        for el in elements:
            self.add_translation(el,w,pos,placenamefile)


    def delete_word(self, wid=None,pos=None):

        if not pos:
            print "specify the part of speech with option -p"
        if wid and pos:
            words = Word.objects.filter(wordid=wid,pos=pos)
            for w in words:
                print "Removing", w.wordid
                w.delete()
        if not words:
            print wid, "not found"
