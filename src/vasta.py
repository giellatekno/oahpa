# -*- coding: utf-8 -*-
#
# Vasta command-line tool
#
# Add this line to your .profile (replace user with your username)
# export PYTHONPATH="/home/<user>/ped/:/home/<user>/ped/oahpa"
#


from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.template import Context, loader
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from random import randint
from django.utils.translation import ugettext as _
from oahpa.drill.game import *
from oahpa.drill.qagame import *
from optparse import OptionParser


parser = OptionParser()

parser.add_option("-p", "--pos", dest="pos",
                  help="part of speech")
parser.add_option("-g", "--grammar", dest="grammar",
                  help="Grammarfile")
parser.add_option("-q", "--qtype", dest="qtype",
                  help="question type")

(options, args) = parser.parse_args()

qasettings = {'pos' : 'N', 'qtype' : 'N-ILL', 'case' : ''}
if options.pos: qasettings['pos'] = options.pos
if options.qtype: qasettings['qtype'] = options.qtype


# Analyzer..
#fstdir="/Users/saara/gt/sme/bin"
#lookup = "/Users/saara/bin/lookup"
#lookup2cg = " | /Users/saara/gt/script/lookup2cg"
#vislcg3 = "/Users/saara/bin/vislcg3"
#preprocess = " | /Users/saara/gt/script/preprocess "
#dis = "/Users/saara/ped/sme/src/sme-ped.cg3"

fstdir="/opt/smi/sme/bin"
lo = "/opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/lookup"
lookup2cg = " | lookup2cg"
cg3 = "vislcg3"
preprocess = " | /usr/local/bin/preprocess "
if options.grammar:
    dis = options.grammar
else:
    dis = "/home/saara/ped/sme/src/sme-ped.cg3"

fst = fstdir + "/sme.fst"
lookup = " | " + lo + " -flags mbTT -utf8 -d " + fst        
vislcg3 = " | " + cg3 + " --grammar " + dis + " -C UTF-8"
disamb = lookup + lookup2cg + vislcg3

                
qasettings['gametype'] = "context"                
#qasettings['book'] = settings_form.books[settings_form.default_data['book']]

game = QAGame(qasettings)
game.init_tags()
new_db_info = {}
db_info = game.get_db_info(new_db_info, qasettings['qtype'])

question = Question.objects.get(Q(id=db_info['question_id']))
qtext = question.string

qstring =""
analysis = ""
qwords = db_info['qwords']
for w in qtext.split():
    cohort=""
    if qwords.has_key(w):
        qword = qwords[w]
        if qword.has_key('word'):
            if qword.has_key('fullform') and qword['fullform']:
                cohort = cohort + "\"<" + qword['fullform'][0].encode('utf-8') + ">\"\n"
                qstring = qstring + " " + qwords[w]['fullform'][0]

                lemma = Word.objects.filter(id=qword['word'])[0].lemma
                cohort = cohort + "\t\"" + lemma.encode('utf-8') + "\""
            if qword.has_key('tag') and qword['tag']:
                string = Tag.objects.filter(id=qword['tag'])[0].string
                tag = string.replace("+"," ")
                cohort = cohort + " " + tag.encode('utf+8') + "\n"
        else:
            word_lookup = "echo \"" + w.encode('utf-8') + "\"" + lookup + lookup2cg
            word = os.popen(word_lookup).readlines()
            for c in word:
                c.lstrip(" ")
                cohort = cohort + c
            qstring = qstring + " " + qwords[w]['fullform'][0]
    else:
        qstring = qstring + " " + w
        
    if not cohort:
        cohort = w + "\n"
        
    analysis = analysis + cohort

analysis = analysis + "\"<^qst>\"\n\t\"^qst\" QDL\n"

qstring = qstring.lstrip()
qstring = qstring[0].capitalize() + qstring[1:]

qstring = qstring + "?"
print qstring
data = sys.stdin.readlines()
data = ''.join(data)
data = data.rstrip()

ans_cohort=""
data_lookup = "echo \"" + data + "\"" + preprocess + lookup + lookup2cg
#print data_lookup
word = os.popen(data_lookup).readlines()
for c in word:
    c.lstrip(" ")
    ans_cohort = ans_cohort + c

analysis = analysis + ans_cohort
#print analysis
analysis = analysis.rstrip()
analysis = analysis.replace("\"","\\\"")

ped_cg3 = "echo \"" + analysis + "\"" + vislcg3
#print "***************"
#print ped_cg3
checked = os.popen(ped_cg3).readlines()

messageObj=re.compile(r'^.*(?P<msgString>&[\w-]*)\s*$', re.U)

print

msgstrings = []
for line in checked:
    line.strip()
    print line
    matchObj=messageObj.search(line)
    if matchObj:
        msgstring = matchObj.expand(r'\g<msgString>')
        msgstrings.append(msgstring)

for m in msgstrings:
    m = m.replace("&","")
    if Feedbackmsg.objects.filter(msgid=m).count() > 0:
        message = Feedbackmsg.objects.filter(msgid=m)[0].message
        print message
    else:
        print m


