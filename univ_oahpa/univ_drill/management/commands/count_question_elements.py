from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

import sys

# # #
#
#  Command class
#
# # #


def count_activities():
    from univ_drill.models import Question
    from operator import mul

    def count_question_obj(question):
        counts = []
        elems = []
        for element in question.qelement_set.all():
            wqelems = element.wordqelement_set.all()
            c = wqelems.count()
            if c > 0:
                elems.append(element.wordqelement_set.all())
            counts.append(( element.syntax
                          , c
                          ))
        return counts, elems

    totals = []
    for question in Question.objects.filter(qatype='answer'):
        answer_counts, answer_elems = count_question_obj(question)
        question_counts, question_elems = count_question_obj(question.question)

        q_counts = [len(e) for e in question_elems]
        try:
            q_count = reduce(mul, q_counts)
        except TypeError:
            q_count = False

        if q_count:
            q_c_str = '*'.join([str(b) for b in q_counts])

            print question.question.qid
            print "  question:"
            for c in question_counts:
                print "    %s - %d possibilities" % c
            print "  total possible questions: %d " % q_count
            totals.append(q_count)
            print "    (%s)" % q_c_str
            print
        else:
            print question.question.qid
            print "  question has no elements"
            print

    print "Grand total: %d" % sum(totals)


class Command(BaseCommand):
    args = '--word'
    help = """
    Print all of the relations for a word by the word's lemma (-w)
    """
    option_list = BaseCommand.option_list + (
        # make_option("-w", "--word", dest="word_key", default=False,
        #                   help="Tag element to search for"),
    )

    def handle(self, *args, **options):
        import os

        count_activities()
