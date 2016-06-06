from django.core.management.base import BaseCommand, CommandError

# from_yaml(cls, loader, node)

from optparse import make_option

import sys

from crk_drill.models import Form, Word, Tag

def install_file(filename):
    from collections import defaultdict
    words_to_install = defaultdict(list)
    with open(filename, 'r') as F:
        for l in F.readlines():
            tag, _, form = l.strip().partition('\t')
            lemma, _, tag = tag.partition('+')
            if lemma in words_to_install:
                if tag in words_to_install[lemma]:
                    words_to_install[lemma][tag].append(form)
                else:
                    words_to_install[lemma] = {tag: [form]}
            else:
                words_to_install[lemma] = {tag: [form]}

    from itertools import izip_longest

    for lemma, forms in words_to_install.iteritems():
        print 'lemma: ', lemma
        ws = Word.objects.filter(lemma=lemma, pos='V')
        w = ws[0]
        for tag, wfs in forms.iteritems():
            fs = Form.objects.filter(word__lemma=lemma, tag__string=tag)
            print '  ', tag
            last_db = False
            t, _c = Tag.objects.get_or_create(string=tag)
            if _c:
                t.save()
            for new_form, db_form in izip_longest(wfs, fs, fillvalue=False):
                if db_form:
                    print '    ', "updating ", db_form, " with ", new_form
                    db_form.fullform = new_form
                    db_form.save()
                else:
                    print '    ', "creating new form for ", db_form, " with ", new_form
                    if last_db:
                        wo = last_db.word
                        ta = last_db.tag
                    else:
                        wo = w
                        ta = t
                    new = Form.objects.create(word=wo,
                                        tag=ta,
                                        fullform=new_form,)
                    if last_db:
                        for d in last_db.dialects.all():
                            new.dialects.add(d)
                        for fb in last_db.feedback.all():
                            new.feedback.add(fb)
                    new.save()

                last_db = db_form



# # # 
# 
#  Command class
#
# # #

def mergetags(tfilter=False):
    if tfilter:
        qset = Tag.objects.filter(string=tfilter)
    else:
        qset = Tag.objects.all()
    
    strings = qset.values_list('string', flat=True)
    strings = list(set(strings))

    print 'Merging:'
    for string in strings:
        tag = Tag.objects.filter(string=string)

        if tag.count() > 1:
            print 'Merging conflict in %s' % tag[0].string
            merge(tag)
    

class Command(BaseCommand):
    args = '--tagelement'
    help = """
    Strips tags of an element and then merges them all.
    """
    option_list = BaseCommand.option_list + (
        make_option("-f", "--filename", dest="filename", default=False,
                          help="Static file to read from"),
        # make_option("-d", "--dryrun", dest="dryrun", default="True",
        #                   help="List tags matching element instead of merging"),

        # TODO: question iterations count
    )

    def handle(self, *args, **options):
        import sys, os

        filename = options['filename']

        install_file(filename=filename)

