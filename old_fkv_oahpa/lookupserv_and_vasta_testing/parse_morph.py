#! /usr/bin/env python -w
# -*- coding: utf-8 -*- 

import sys
import re
import os, subprocess as sub
import codecs
import MySQLdb

try:
    conn = MySQLdb.connect (host = "localhost",
                            user = "saara",
                            passwd = "vesiLasi",
                            db = "oahpa")
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit (1)

cursor = conn.cursor ()

file = sys.argv[1]
pos = sys.argv[2]

insert_to_db=1
read_gen=0
translations=0
forms=1
words=0

class Entry:
    pass

## Populate table word.
def add_word_db(e):

    cursor.execute ("""
        SELECT lemma FROM morph_word WHERE lemma=%s
    """, e.lemma.encode('utf8'))
    row = cursor.fetchone ()
    if not row == None:
        return

    cursor.execute ("""
        INSERT INTO morph_word (lemma, type, pos, semtype, subtype)
        VALUES (%s, %s, %s, %s, %s)
    """, (e.lemma.encode('utf8'), 'common noun', e.pos, e.semtype, e.subtype))
    print "Number of rows inserted: %d" % cursor.rowcount

## Populate translations table
def add_translations_db(e):

    cursor.execute ("""
        SELECT id FROM morph_word WHERE lemma=%s
    """, e.lemma.encode('utf8'))
    wordrow = cursor.fetchone ()
    if wordrow == None:
        return

    for t in e.translations:
        cursor.execute ("""
            SELECT id FROM morph_translationnob WHERE translation=%s
        """, t.encode('utf8'))
        translrow = cursor.fetchone ()
        if translrow == None:

            cursor.execute ("""
                INSERT INTO morph_translationnob (translation)
                VALUES (%s)
            """, (t.encode('utf8')))
            print "Number of rows inserted: %d" % cursor.rowcount

            cursor.execute ("""
                SELECT id FROM morph_translationnob WHERE translation=%s
            """, t.encode('utf8'))
            translrow = cursor.fetchone ()

        cursor.execute ("""
            SELECT word_id FROM morph_translationnob_word 
            WHERE word_id=%s AND translationnob_id=%s
        """, (wordrow[0], translrow[0]))
        row = cursor.fetchone ()
        if not row == None:
            continue

        cursor.execute ("""
            INSERT INTO morph_translationnob_word (word_id, translationnob_id)
            VALUES (%s, %s)
        """, (wordrow[0], translrow[0]))
        print "Number of rows inserted: %d" % cursor.rowcount



def add_forms_db(g):     
    
    cursor.execute ("""
        SELECT id FROM morph_word WHERE lemma=%s
    """, g.lemma.encode('utf8'))
    wordrow = cursor.fetchone ()
    if wordrow == None:
        return

    cursor.execute ("""
        SELECT id FROM morph_tag WHERE string=%s
    """, g.tags.encode('utf8'))
    tagrow = cursor.fetchone ()
    if tagrow == None:
        return

    # Check that the same word form is not added twice.
    cursor.execute ("""
        SELECT * FROM morph_form WHERE word_id=%s AND tag_id=%s AND fullform=%s
    """, (wordrow[0], tagrow[0], g.form.encode('utf8')))
    row = cursor.fetchone ()
    if not row == None:
        return

    cursor.execute ("""
        INSERT INTO morph_form (word_id, tag_id, fullform)
        VALUES (%s, %s, %s)
    """, (wordrow[0], tagrow[0], g.form.encode('utf8')))
    print "Number of rows inserted: %d" % cursor.rowcount


def read_generated():

    genfileObj = codecs.open(file, "r", "utf-8" )
    genObj=re.compile(r'^(?P<lemmaString>[\w]+)\+(?P<tagString>[\w\+]+)[\t\s]+(?P<formString>[\w]*)$', re.U)

    while True:
        line = genfileObj.readline()
        if not line: break
        if not line.strip(): continue
        matchObj=genObj.search(line) 
        if matchObj:
            g = Entry()
            g.lemma = matchObj.expand(r'\g<lemmaString>')
            print g.lemma.encode('utf-8')
            g.form = matchObj.expand(r'\g<formString>')
            if re.compile("\?").match(g.form.encode('utf-8')): continue
            print g.form.encode('utf-8')
            g.tags = matchObj.expand(r'\g<tagString>')
            print g.tags.encode('utf-8')

            if insert_to_db:
                add_forms_db(g)

    genfileObj.close()
    cursor.close ()
    if insert_to_db:
        conn.commit ()
    conn.close ()

def read_translations():
    semtype=""
    subtype=""

    fileObj = codecs.open(file, "r", "utf-8" )
    typeObj=re.compile(r'^#\s*(?P<typeString>[\w]*)\s*$', re.U)
    patternObj=re.compile(r'^(?P<fileName>[\w]+)[\t]+(?P<transString>[\w\, ]*)$', re.U)

    while True:
        line = fileObj.readline()
        if not line: break
        if not line.strip(): continue
        #print line
        matchObj=typeObj.search(line) 
        if matchObj:
            type = matchObj.expand(r'\g<typeString>')
            #print type.encode('utf-8')
            if type.isupper():
                semtype=type
            else:
                subtype=type
            continue;

        matchObj=patternObj.search(line) 
        if not matchObj: continue

        e = Entry()
        e.semtype = semtype
        e.subtype = subtype
        e.pos = pos

        e.lemma=matchObj.expand(r'\g<fileName>')

        translations = matchObj.expand(r'\g<transString>')
        e.translations = re.split(r'\, ', translations, re.U)
        for trans in e.translations:
           print trans.encode('utf8')

        print e.lemma.encode('utf8')

        # Insert into database.
        if insert_to_db:
            if words:
                add_word_db(e)
            if translations:
                add_translations_db(e)

    fileObj.close()
    cursor.close ()
    if insert_to_db:
        conn.commit ()
    conn.close ()


if forms:
    read_generated()
else:
    read_translations()

