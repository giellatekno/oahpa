# -*- coding: utf-8 -*-

from settings import *
from drill.models import *
from xml.dom import minidom as _dom
from optparse import OptionParser
from django.db.models import Q
import sys
import re
import string
import codecs


class Entry:
    pass


class Paradigm:

    def __init__(self):
        self.tagset = {}
        self.paradigms = {}

    def handle_tags(self, tagfile, add_db):
        tags =[]
        fileObj = codecs.open(tagfile, "r", "utf-8" )
        tags = fileObj.readlines()
        fileObj.close()
        
        classObj=re.compile(r'^#\s*(?P<typeString>[\w\-]*)\s*$', re.U)
        stringObj=re.compile(r'^(?P<tagString>[\w]*)\s*$', re.U)

        tagclass=""
        for line in tags:
            line.strip()
            matchObj=classObj.search(line) 
            if matchObj:
                tagclass = matchObj.expand(r'\g<typeString>')
            else:
                matchObj=stringObj.search(line)
                if matchObj:
                    string = matchObj.expand(r'\g<tagString>')
                    self.tagset[string]=tagclass
                    if add_db and tagclass and string:
                        #print "adding " + tagclass + " " + string
                        tagset, created = Tagset.objects.get_or_create(tagset=tagclass)
                        pos, created = Tagname.objects.get_or_create(tagname=string,tagset=tagset)


    def read_paradigms(self,paradigmfile,tagfile, add_database):
        if not self.tagset:
            self.handle_tags(tagfile)

        fileObj = codecs.open(paradigmfile, "r", "utf-8" )
        posObj=re.compile(r'^(?P<posString>[\w]+)\+.*$', re.U)

        while True:
            line = fileObj.readline()
            if not line: break
            if not line.strip(): continue
            matchObj=posObj.search(line)
            if matchObj:
                pos=matchObj.expand(r'\g<posString>')
            if not self.paradigms.has_key(pos):
                self.paradigms[pos]=[]
            self.paradigms[pos].append(line)


    def create_paradigm(self, lemma, pos):

        if not self.tagset:
            self.handle_tags()

        self.paradigm = []
							  
        genObj=re.compile(r'^(?P<lemmaString>[\wáŋčžšđŧ]+)\+(?P<tagString>[\w\+]+)[\t\s]+(?P<formString>[\wáŋčžšđŧ]*)$', re.U)
        all=""

        if self.paradigms.has_key(pos):
            for a in self.paradigms[pos]:
                all = all + lemma + "+" + a

        # generator call
        fstdir="/opt/smi/sme/bin"
        lookup = "/usr/local/bin/lookup"

        #fstdir="/Users/saara/gt/sme/bin"
        #lookup = "/Users/saara/bin/lookup"

        gen_norm_fst = fstdir + "/isme-norm.fst"
        gen_gg_restr_fst = fstdir + "/isme-KJ.restr.fst"            
        gen_kj_restr_fst = fstdir + "/isme-GG.restr.fst"            

        gen_norm_lookup = "echo \"" + all.encode('utf-8') + "\" | " + lookup + " -flags mbTT -utf8 -d " + gen_norm_fst
        gen_gg_restr_lookup = "echo \"" + all.encode('utf-8') + "\" | " + lookup + " -flags mbTT -utf8 -d " + gen_gg_restr_fst
        gen_kj_restr_lookup = "echo \"" + all.encode('utf-8') + "\" | " + lookup + " -flags mbTT -utf8 -d " + gen_kj_restr_fst
        lines_tmp = os.popen(gen_norm_lookup).readlines()
        lines_gg_restr_tmp = os.popen(gen_gg_restr_lookup).readlines()
        lines_kj_restr_tmp = os.popen(gen_kj_restr_lookup).readlines()

        for line in lines_tmp:

            if not line.strip(): continue
            matchObj=genObj.search(line)
            if matchObj:
                g = Entry()
                g.dialects=[]
                g.classes={}
                lemma = matchObj.expand(r'\g<lemmaString>')
                g.form = matchObj.expand(r'\g<formString>')
                if re.compile("\?").match(g.form): continue
                # If line is included in either dialect
                if line in set(lines_gg_restr_tmp): 
                    g.dialects.append("GG")
                if line in set(lines_kj_restr_tmp): 
                    g.dialects.append("KJ")
                g.tags = matchObj.expand(r'\g<tagString>')
                for t in g.tags.split('+'):
                    if self.tagset.has_key(t):
                        tagclass=self.tagset[t]
                        g.classes[tagclass]=t
                self.paradigm.append(g)


    def generate_numerals(self):
        """
        Generate all the cardinal numbers
        Create paradigms and store to db
        """

        language = "sme"
        #fstdir="/opt/smi/" + language + "/bin"
        #lookup = /usr/local/bin/lookup
        
        fstdir="/Users/saara/gt/" + language + "/bin"        
        lookup = "/Users/saara/bin/lookup"

        numfst = fstdir + "/" + language + "-num.fst"

        for num in range(1,20):

            num_lookup = "echo \"" + str(num) + "\" | " + lookup + " -flags mbTT -utf8 -d " + numfst
            numerals = os.popen(num_lookup).readlines()

            # Take only first one.
            # Change this if needed!
            num_list=[]
            for num in numerals:
                line = num.strip()
                if line:
                    nums = line.split('\t')
                    num_list.append(nums[1].decode('utf-8'))
            numstring = num_list[0]

            w, created = Word.objects.get_or_create(wordid=num, lemma=numstring, pos="Num")
            w.save()

            self.create_paradigm(numstring, "Num")
            for form in self.paradigm:
                form.form = form.form.replace("#","")
                g=form.classes
                t,created=Tag.objects.get_or_create(string=form.tags,pos=g.get('Wordclass', ""),\
                                                    number=g.get('Number',""),case=g.get('Case',""),\
                                                    possessive=g.get('Possessive',""),grade=g.get('Grade',""),\
                                                    infinite=g.get('Infinite',""), \
                                                    personnumber=g.get('Person-Number',""),\
                                                    polarity=g.get('Polarity',""),\
                                                    tense=g.get('Tense',""),mood=g.get('Mood',""), \
                                                    subclass=g.get('Subclass',""), \
                                                    attributive=g.get('Attributive',""))
                
                t.save()
                form, created = Form.objects.get_or_create(fullform=form.form,tag=t,word=w)
                form.save()


