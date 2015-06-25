from django.core.management.base import BaseCommand, CommandError
# -*- encoding: utf-8 -*-
# from_yaml(cls, loader, node)

from optparse import make_option
from django.utils.encoding import force_unicode

import sys

# # # 
# 
#  Questions stuff
#
# # #

from xml.dom import minidom as _dom
from optparse import OptionParser
# from django import db
import sys
import re
import string
import codecs
from itertools import product, combinations
from random import choice

# Some XML shortcuts
_elements = lambda e, x: e.getElementsByTagName(x)
_attribute = lambda e, x: e.getAttribute(x)
def _data(e):
    try: 
        return e.firstChild.data
    except AttributeError:
        return False

def _firstelement(e, x):
    e = _elements(e, x)
    try:
        return e[0]
    except IndexError:
        return None


from sms_drill.models import Tagname, Tagset, Form, Word

class Command(BaseCommand):
    args = ''
    help = """
    For testing the database for content. Pipe in new-line separated
    list of strings over stdin, and run them through the command.

    If you include a tag after the word (separated by a space), the form
    will be taken to be the lemma, and tested for generation with the tag.

    Ex.) echo "triâŋgg" | python manage.py check_forms

            (input)   (word)     (forms)                             (generated)
        -> triâŋgg    triâŋgg    triâŋgg, triâŋgg, triâŋgg, triâŋgg    --

    Ex.) echo "čieʹcc N+Pl+Nom" | python manage.py check_forms
            (input)           (word)    (forms)   (generated)
        -> čieʹcc+N+Pl+Nom    čieʹcc    čieʹcc    čieʹʒʒ

    The command may also be used interactively in the same way.

        python manage.py check_forms -i

    """
    option_list = BaseCommand.option_list + (
        make_option("-i", "--interactive", dest="interactive", default=False, action="store_true",
                          help="Take input interactively"),
    )

    def handle(self, *args, **options):
        import sys, os

        def word_match(s):
            ws = Word.objects.filter(lemma=s)
            if len(ws) > 0:
                return u', '.join(w.lemma for w in ws)
            else:
                return 'NO WORD'

        def form_match(s):
            ws = Form.objects.filter(fullform=s)
            if len(ws) > 0:
                return u', '.join(w.fullform for w in ws)
            else:
                return u'NO FORM'

        def form_tag_match(s, t):
            ws = Word.objects.filter(lemma=s, form__tag__string=t)
            if len(ws) > 0:
                fs = []
                for w in ws:
                    for f in w.form_set.filter(tag__string=t):
                        fs.append(f.fullform)
                return u', '.join(fs)
            else:
                return u'NO FORM'

        def semsets(s):
            ws = Word.objects.filter(lemma=s)
            fs = Word.objects.filter(form__fullform=s)
            if len(ws) > 0:
                sem = set()
                for w in ws:
                    for s in w.semtype.all():
                        sem.add(s.semtype)
                for f in fs:
                    for s in f.semtype.all():
                        sem.add(s.semtype)
                return u', '.join(sem)
            else:
                return 'NO SEMANTICS'

        def check_line(line):
            t = False
            ls = line.strip().decode('utf-8').split(' ')
            if len(ls) == 2:
                l, t = ls
            else:
                l = ls[0]
            if t:
                d = l + '+' + t
            else:
                d = l
            args = [
                d,
                word_match(l),
                form_match(l),
                semsets(l),
            ]
            if t:
                args.append(form_tag_match(l, t))
            else:
                args.append('--')
            print >> sys.stdout, '    '.join(args).encode('utf-8')

        interactive = options['interactive']

        if interactive:
            print "(input)   (word)     (forms)     (generated)    (semsets)"

            while True:
                line = raw_input(" > ")
                check_line(line)

            sys.exit()

        for line in sys.stdin:
            check_line(line)



# vim: set ts=4 sw=4 tw=0 syntax=python expandtab :


