from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

import sys

# # #
#
#  Command class
#
# # #

from univ_drill.models import Question, Word

def count_activities(gametype='morfa'):
    from operator import mul

    def count_question_obj(question):

        criteria = []

        counts = []
        _semtypes = []

        _question_has_pn = False
        _question_has_tense = False

        _question_has_subj = False
        _subj_is_pron = False
        _subj_is_noun = False

        for element in question.qelement_set.all():
            if element.syntax == 'SUBJ':
                _question_has_subj = True
                poses = element.tags.values_list('pos', flat=True).distinct()
                if 'Pron' in poses and 'N' in poses:
                    _subj_is_pron = True
                elif 'Pron' in poses:
                    _subj_is_pron = True
                elif 'N' in poses:
                    _subj_is_noun = True

            if element.syntax in [syntax for syntax, _ in counts]:
                continue

            if element.semtype and element.semtype.semtype not in criteria:
                ws = element.wordqelement_set.filter(word__semtype=element.semtype)\
                                 .exclude(word__language__in=['fin', 'nob', 'sma', 'swe'])\
                                 .values_list('word__lemma', flat=True)\
                                 .distinct()
                c = ws.count()

                _semtypes.append(element.semtype)
                criteria.append(element.semtype.semtype)
                counts.append(( element.semtype.semtype
                              , c
                              ))
            if not _question_has_tense:
                if element.tags:
                    has_tense = [ a.tense
                                for a in element.tags.all()
                               if a.tense.strip() ]

                    if 'Prs' in has_tense and 'Prt' in has_tense:
                        _question_has_tense = True

            if not _question_has_pn:
                if element.tags:
                    has_pn = set([ a.personnumber
                               for a in element.tags.all()
                               if a.personnumber.strip() ])

                    if 'Sg1' in has_pn and 'Du1' in has_pn:
                        _question_has_pn = True

        if len(_semtypes) == 0:
            counts.append(( "SEMTYPE"
                          , 1
                          ))

        if _question_has_pn and _question_has_subj:
            if _subj_is_pron:
                counts.append(( "PERSON-NUMBER"
                              , 9
                              ))
            elif _subj_is_noun:
                counts.append(( "PERSON-NUMBER"
                              , 2
                              ))

        if _question_has_tense:
            counts.append(( "TENSE"
                          , 2
                          ))
        return counts

    totals = []

    inc = {
        'question__gametype': gametype,
        'qatype': 'answer'
    }
    exc = {
        'question__qid__startswith': 'px'
    }
    for question in Question.objects.filter(**inc).exclude(**exc):
        question_answer = question
        question = question.question
        answer_counts = count_question_obj(question_answer)
        question_counts = count_question_obj(question)

        question_answer_counts = list(set(answer_counts + question_counts))

        q_counts = [n for t, n in question_answer_counts]
        try:
            q_count = reduce(mul, q_counts)
        except TypeError:
            q_count = False

        if q_count:
            q_c_str = '*'.join([str(b) for b in q_counts])

            print question.qid
            print "  question:"
            for c in question_answer_counts:
                print "    %s - %d possibilities" % c
            print "  total possible questions: %d " % q_count
            totals.append(q_count)
            print "    (%s)" % q_c_str
            print
        else:
            print question.qid
            print "  question has no elements"
            print

    print "Grand total: %d" % sum(totals)


class Command(BaseCommand):
    args = '--word'
    help = """
    """
    option_list = BaseCommand.option_list + (
        make_option("-t", "--type", dest="gametype", default=False,
                          help="Gametype"),
    )

    def handle(self, *args, **options):
        if not options.get('gametype'):
            print "Please specify a gametype with --type"
            print "--type=cealkka, --type=morfa"
        else:
            if options.get('gametype') not in ['cealkka', 'morfa']:
                print "Please specify a gametype with --type"
                print "--type=cealkka, --type=morfa"
            count_activities(options.get('gametype'))
