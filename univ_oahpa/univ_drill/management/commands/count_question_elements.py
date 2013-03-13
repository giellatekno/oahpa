from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

import sys

# # #
#
#  Command class
#
# # #


# TODO: Person-Number in tag? *9

def count_activities():
    from univ_drill.models import Question, Word
    from operator import mul

    # TODO tags: 
    def count_question_obj(question):

        criteria = []

        counts = []
        elems = []
        _semtypes = []

        _question_has_pn = False

        for element in question.qelement_set.all():
            if element.syntax in [syntax for syntax, _ in counts]:
                continue

            if element.semtype and element.semtype.semtype not in criteria:
                ws = Word.objects.filter(semtype=element.semtype)
                c = ws.count()
                _semtypes.append(element.semtype)
                if c > 0:
                    elems.append(element.wordqelement_set.all())
                criteria.append(element.semtype.semtype)
                counts.append(( element.semtype.semtype
                              , c
                              ))
            if not _question_has_pn:
                if element.tags:
                    has_pn = [ a.personnumber
                               for a in element.tags.all()
                               if a.personnumber.strip() ]
                    if len(has_pn) > 0:
                        _question_has_pn = True

        if _question_has_pn:
            counts.append(( "PERSON-NUMBER"
                          , 9
                          ))
        return counts, elems

    totals = []
    for question in Question.objects.filter(qatype='answer'):
        answer_counts, answer_elems = count_question_obj(question)
        question_counts, question_elems = count_question_obj(question.question)


        question_answer_counts = list(set(answer_counts + question_counts))

        q_counts = [n for t, n in question_answer_counts]
        try:
            q_count = reduce(mul, q_counts)
        except TypeError:
            q_count = False

        if q_count:
            q_c_str = '*'.join([str(b) for b in q_counts])

            print question.question.qid
            print "  question:"
            for c in question_answer_counts:
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
