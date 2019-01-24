from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')

from django.core.management.base import BaseCommand, CommandError
# -*- encoding: utf-8 -*-
# from_yaml(cls, loader, node)

from django.db.models import Q

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



Tagname = oahpa_module.drill.models.Tagname
Form = oahpa_module.drill.models.Form
Word = oahpa_module.drill.models.Word
Tagset = oahpa_module.drill.models.Tagset


def parse_tag(tag):
    """ Iterate through a tag string by chunks, and check for tag sets
    and tag names. Return the reassembled tag on success. """

    def fill_out(tags):
        from itertools import product

        def make_list(item):
            if type(item) == list:
                return item
            else:
                return [item]

        return list(product(*map(make_list, tags)))

    tag_string = []
    for item in tag.split('+'):
        if Tagname.objects.filter(tagname=item).count() > 0:
            tag_string.append(item)
        elif Tagset.objects.filter(tagset=item).count() > 0:
            tagnames = Tagname.objects.filter(tagset__tagset=item)
            tag_string.append([t.tagname for t in tagnames])
        else:
            tag_string.append(item)

    if len(tag_string) > 0:
        return ['+'.join(item) for item in fill_out(tag_string)]
    else:
        return False

_boolify = lambda v: True and v.lower() in ['yes', 'true', 'y'] or False

# TODO: for now i assume these don't change throughout the course of the
# operation, but they might.

# TODO: tags install-- need to cat all paradigms together

TAGS = Tagname.objects.all().values_list('tagname', flat=True)
TAGSETS = Tagset.objects.all().values_list('tagset', flat=True)

_T = dict([(t.tagset, t.tagname_set.all().values_list('tagname', flat=True))
            for t in Tagset.objects.all()])

# List of tags that agree in. Key-value pairs. Key in head, means agree
# tag must contain one of the items in the list.

# Languages with Subject agreement are easy, languages with object AGREEMENT
# or some other kind of agreement will need to have more key-value
# pairs. or perhaps a slightly different arrangement here...

AGREEMENT = {
    'Sg': ['Sg3'],
    'Du': ['Du3'],
    'Pl': ['Pl3'],

    'Sg1': ['PxSg1', 'Sg1'],
    'Sg2': ['PxSg2', 'Sg2'],
    'Sg3': ['PxSg3', 'Sg3'],

    'Du1': ['PxDu1', 'Du1'],
    'Du2': ['PxDu2', 'Du2'],
    'Du3': ['PxDu3', 'Du3'],

    'Pl1': ['PxPl1', 'Pl1'],
    'Pl2': ['PxPl2', 'Pl2'],
    'Pl3': ['PxPl3', 'Pl3'],

    '': '',
}

# TODO: Cleaning code thoughts
#        SUBJ = elements_d.get('SUBJ') or False
#        MAINV = elements_d.get('MAINV') or False

class FakeForm(object):
    pass


class GrammarDefaults(object):

    def expandTags(self, tags):

        all_tags = []

        for tag in tags:
            tag_items = parse_tag(tag)
            all_tags.append(tag_items)

        return all_tags

    def __init__(self, defaults_node):
        self.node = defaults_node
        definitions = _firstelement(self.node, 'definitions')

        tags = _firstelement(definitions, 'tags')
        partitions = _elements(self.node, 'partitions')
        tag_elements = _elements(tags, 'element')

        grammar_definitions = {}

        for element in tag_elements:
            elem_id = _attribute(element, 'id')
            grammar_definitions[elem_id] = {}

            grammars = _elements(element, 'grammar')

            word_id = _data(_firstelement(element, 'id'))

            tag_list = []

            for grammar in grammars:
                pos = _attribute(grammar, 'pos')
                tag = _attribute(grammar, 'tag')

                expanded = sum(self.expandTags([tag]), [])
                tag_list.extend(expanded)


            if len(tag_list) > 0:
                grammar_definitions[elem_id]['tags'] = tag_list

            if word_id:
                if word_id.strip():
                    grammar_definitions[elem_id]['lemmas'] = [word_id]

        self.grammar_definitions = grammar_definitions

class Agreement(object):

    @property
    def agreement(self):
        if self._agreement:
            return self._agreement

        # Any processing that needs to be done here?

        self._agreement = self.agreement_data['Agreements']
        return self._agreement

    @property
    def agreement_by_element_name_all(self):
        """ A dictionary of all agreement names by targeted elements
        """
        if self._agreement_by_element_name_all:
            return self._agreement_by_element_name_all

        elements_to_agreements_all = {}
        for agreement_pattern in self.agreement:
            elems = [e['element'] for e in agreement_pattern['elements']]
            for elem in elems:
                if elem in elements_to_agreements_all:
                    elements_to_agreements_all[elem].append(agreement_pattern['name'])
                else:
                    elements_to_agreements_all[elem] = [agreement_pattern['name']]

        self._agreement_by_element_name_all = elements_to_agreements_all
        return self._agreement_by_element_name_all


    @property
    def agreement_by_element_name_question(self):
        """ A dictionary of only agreement elements valid for the question.
        """
        if self._agreement_by_element_name_question:
            return self._agreement_by_element_name_question

        def question_only(item):
            if item.starts_with('Question/'):
                return item.replace('Question/', '')
            else:
                return None

        self._agreement_by_element_name_question = filter(question_only,
                    self.agreement_by_element_name_all)

        return self._agreement_by_element_name_question

    @property
    def agreement_by_element_name_answer(self):
        """ A dictionary of only agreement elements valid for the answer.
        """
        if self._agreement_by_element_name_answer:
            return self._agreement_by_element_name_answer

        def answer_only(item):
            if item.starts_with('Answer/'):
                return item.replace('Answer/', '')
            else:
                return None

        self._agreement_by_element_name_answer = filter(answer_only,
                    self.agreement_by_element_name_all)

        return self._agreement_by_element_name_answer

    @property
    def agreement_by_name(self):
        if self._agreement_by_name:
            return self._agreement_by_name

        by_name = {}
        for agr in self.agreement:
            by_name[agr['name']] = agr

        self._agreement_by_name = by_name
        return self.agreement_by_name

    def get_agreement(self, agreementname):
        agr_info = self.agreement_by_name.get(agreementname)

        if not agr_info:
            return False

        class Agr(object):

            def match_and_replace(agr_cls, head, targets):
                import re

                def pattern_match(x, y):
                    # TODO: Clean this up
                    # basically, can y match x with corresponding value replaced with AGR
                    x_head, x_agr, x_tail = x.partition('AGR')
                    agr_inner_re = re.escape(x).replace('AGR', '(?P<agr>\w+)')
                    agr_inner = re.match(agr_inner_re, y)
                    try:
                        agr_inner = agr_inner.group('agr')
                        z = y.replace(agr_inner, 'AGR')
                        if x == z:
                            return True
                    except:
                        return False

                    if y.startswith(x_head) and y.endswith(x_tail):
                        return True
                    else:
                        return False

                tag_patterns = agr_cls.head['tag']
                head_element = agr_cls.head['element']

                # TODO: when there are multiple targets
                targ_patterns = agr_cls.targets[0]['tag']
                targ_element = agr_cls.targets[0]['element']

                tag_pattern = False
                for tag_p in tag_patterns:
                    exps = parse_tag(tag_p)
                    for exp in exps:
                        if pattern_match(exp, head):
                            tag_pattern = exp
                            break

                try:
                    agr_inner_re = re.escape(tag_pattern).replace('AGR', '(?P<agr>\w+)')
                    agr_inner = re.match(agr_inner_re, head)
                    agr_inner = agr_inner.group('agr')
                except:
                    agr_inner = False

                # Take the chunk of the tag from the head tag pattern, and
                # insert the agreed version (from agreements) into the target
                # tag pattern then expand all the tags
                replacements = dict([(r[head_element], r[targ_element]) for r in agr_cls.replacements])
                agr_target = replacements.get(agr_inner)
                try:
                    target_tags_set = parse_tag(targ_patterns.replace('AGR', agr_target))
                except Exception, e:
                    print e
                    print " * Could not match agreement, is it defined in agreements.yaml?"
                    print 'name: ' + repr(agr_cls.name)
                    print 'tag_pattern: ' + repr(tag_pattern)
                    print 'targ_patterns: ' + repr(targ_patterns)
                    print 'head: ' + repr(head)
                    print 'targets: ' + repr(targets)
                    print 'replacements: ' + repr(replacements)
                    sys.exit()

                def target_match(t):
                    if t in target_tags_set:
                        return True
                    else:
                        return False
                    return True

                targets = filter(target_match, targets)

                return head, targets

            def agree_for(agr_cls, element_tags):

                # Get the head from the supplied tags
                head_element = element_tags.get(agr_cls.head_name, False)
                # TODO: no head found error

                # Get the possible target tags from the supplied tags
                target_elems = [(t.get('element'), element_tags.get(t.get('element')))
                                for t in agr_cls.targets]

                if len(agr_cls.targets) > 1:
                    print >> sys.stderr, "Multiple targets. TODO."
                    sys.exit()

                target_elems_name = target_elems[0][0]
                target_elems = target_elems[0][1]

                # filter out non-agreeing target tags
                head, agr_targets = agr_cls.match_and_replace(head_element, target_elems)

                agreement = {
                    agr_cls.head_name: head,
                    target_elems_name: agr_targets
                }

                return agreement

            def __init__(agr_cls):
                agr_cls.agr_info = agr_info
                agr_cls.name = agreementname

                is_head = lambda x: x and x.get('head', False) or False
                isnt_head = lambda x: not is_head(x)

                # TODO: need to make agr_info target elements available because
                # need tag for match and replace above, also potential that
                # there are mutliple targets, ugh, maybe should just ignore it
                # for now
                agr_cls.targets = filter(isnt_head, agr_info['elements'])

                # TODO: testing
                # print 'omg'
                # print agr_cls.targets
                agr_cls.head = filter(is_head, agr_info['elements'])

                if len(agr_cls.head) == 1:
                    agr_cls.head = agr_cls.head[0]
                    agr_cls.head_name = agr_cls.head['element']
                else:
                    # TODO: errors for multiple and no agr head specified
                    agr_cls.head = False
                    agr_cls.head_name = False

                agr_cls.replacements = agr_info['agreements']

        return Agr()



    def __init__(self, agreementfilename):
        import yaml

        self._agreement = False
        self._agreement_by_name = False
        self._agreement_by_element_name_all = False
        self._agreement_by_element_name_question = False
        self._agreement_by_element_name_answer = False


        with open(agreementfilename, 'r') as F:
            self.agreement_data = yaml.load(F)

    def agreement_requires_element(self, agreement_name, element_name):
        agreement_item = self.agreement_by_name.get(agreement_name, False)

        non_heads = [element_['element'] for element_ in agreement_item['elements']
                        if element_.get('head', False) != True]

        if len(non_heads) > 0:
            if element_name in non_heads:
                return True
            else:
                return False
        else:
            return False

    def find_possible_agreements(self, element_names, question_or_answer=False):
        """ Take a list of element names, and return possible agreement types.

            @param question_or_answer (False) - if set to question or answer,
            then only search for possible agreement items that have to do with
            that context.
        """

        # TODO: maybe need a list of partial agreement things if a head is
        # found but no tail is found, in the event that Question-Answer
        # agreement systems need to be handled
        agreements_matching_individual_elements = []
        element_names_agreements_and_tails_exist = []

        for element_name in element_names[:]:
            agreement_names = self.agreement_by_element_name_all.get(element_name, [])
            non_heads = [e for e in element_names[:] if e != element_name]

            for agr_name in agreement_names:
                for non_head in non_heads:
                    if self.agreement_requires_element(agr_name, non_head):
                        element_names_agreements_and_tails_exist.append((element_name, agr_name))

        return element_names_agreements_and_tails_exist





class QObj(GrammarDefaults):
    """ Contains methods necessary for testing questions for Morfa-C.
        Eventually, this may be used to assemble Question objects and
        store them in the database, and then also used to create the
        questions in the actual game.

        If this is used to store database info, it seems like it Would
        almost be better to store tags and semantic types instead of creating
        a ton of WordQElements, because just as much sorting would need to be
        done to either read from WordQElements as it would be to sort through
        forms-- or at least this would be worth testing.


    """

    # Question-Answer agreement
    QAPN = {    'Sg':'Sg',            # Dïhte? Dïhte.
                'Pl':'Pl',            # Dah? Dah.

                'Sg1':'Sg2',        # Manne? Datne.
                'Sg2':'Sg1',        # Datne? Manne.
                'Sg3':'Sg3',        # Dïhte? Dïhte.

                'Du1':'Du2',        # Månnoeh? Dåtnoeh.
                'Du2':'Du1',        # Dåtnoeh? Månnoeh.
                'Du3':'Du3',        # Dah guaktah? Dah guaktah.

                'Pl1':'Pl2',        # Mijjieh? Dijjieh.
                'Pl2':'Pl1',        # Dijjieh? Mijjieh.
                'Pl3':'Pl3'}        # Dah? Dah.

    def handleMeta(self):
        """ assign qtypes and question IDs
        """

        self.qtype = ','.join([_data(q) for q in _elements(self.node, 'qtype')])
        self.qid = _attribute(self.node, 'id')

    def parseElements(self, elements):
        """
                <element id="SUBJ">
                    <sem class="PROFESSION"/>
                    <grammar pos="N"/>
                </element>
                <element id="MAINV">
                    <sem class="MOVEMENT_V"/>
                    <grammar tag="V+Ind+Tense+Person-Number"/>
                </element>
        """

        element_queries = []
        for element in elements:
            elem_q = {'query': {}}

            game, content, task, elem_id, sem, grammar, word_lemma, hid = [None]*8

            elem_id = _attribute(element, "id")
            task = _boolify(_attribute(element, "task"))
            game = _attribute(element, "game")
            content = _attribute(element, "content")

            elem_q['meta'] = {
                'id': elem_id,
                'task': task,
                'game': game,
            }

            if content:
                elem_q['meta']['content'] = content

            sem = _elements(element, 'sem')

            if sem:
                sem = [_attribute(s, 'class') for s in sem]
                if len(sem) > 0:
                    elem_q['query']['semtypes'] = sem

            grammar = _elements(element, 'grammar')
            default_lemma = False
            if elem_id in self.defaults:
                if self.defaults[elem_id].has_key('lemmas'):
                    default_lemma = self.defaults[elem_id]['lemmas']
                else:
                    default_lemma = False

                if self.defaults[elem_id].has_key('tags'):
                    default_tags = self.defaults[elem_id]['tags']
                else:
                    default_tags = False

            if grammar:
                g_pos = _attribute(grammar[0], 'pos')
                if g_pos:
                    elem_q['query']['pos'] = g_pos
                else:
                    g_pos = False

                tags = [_attribute(c, 'tag') for c in grammar]
                tags = [a for a in tags if a.strip()]

                if not tags:
                    if default_tags:
                        tags = default_tags

                expanded_tags = self.expandTags(tags)
                expanded_tags = sum(expanded_tags, [])
                # Need to insert grammar defaults here.
                # If grammar defaults for key exist, use this,
                # otherwise...
                if expanded_tags:
                    if g_pos:
                        t_match = g_pos + '+'
                        expanded_tags = [t for t in expanded_tags if t_match in t]
                    elem_q['query']['tags'] = expanded_tags

                # grammar tag specified, but grammar pos not.
                if tags and not g_pos:
                    g_pos = tags[0].partition('+')[0]
                    elem_q['query']['pos'] = g_pos
                    # errormsg = '*** Grammar tag specified, but Grammar PoS not specified'
                    # self.errors['self.parseElements'] = [errormsg]



            word_lemma = _firstelement(element, 'id')

            if default_lemma:
                elem_q['query']['lemma'] = default_lemma
            elif word_lemma:
                lemma, hid = _data(word_lemma), _attribute(word_lemma, 'hid')
                if lemma:
                    elem_q['query']['lemma'] = lemma
                if hid:
                    elem_q['query']['hid'] = int(hid)

            element_queries.append((elem_id, elem_q))

        return element_queries

    def elementizeText(self, text, elements):
        """
            >>> q = QObj()
            >>> text = "Mika SUBJ MAINV"
            >>> elements = [('SUBJ', {}), ('MAINV', {})]
            >>> q.elementizeText(text, elements)
            [('Mika', None), ('SUBJ', {}), ('MAINV', {})]

        """
        tokens = text.split(' ')
        new_elements = []
        elements_d = dict(elements)
        for token in tokens:
            if token in elements_d:
                new_elements.append((token, elements_d[token]))
            else:
                new_elements.append((token, None))

        return new_elements

    def filter_dialect(self, formqueryset):
        """ TODO: make this faster """
        return formqueryset
        if not self.dialect:
            return formqueryset

        withdialect = formqueryset.filter(dialects__dialect=self.dialect)

        if len(withdialect) == 0:
            withdialect = formqueryset

        exclude_ng = withdialect.exclude(dialects__dialect="NG")

        if len(exclude_ng) == 0:
            exclude_ng = withdialect

        return exclude_ng


    def queryElements(self, elements):
        element_to_query = {
            'tags': 'tag__string',
            'semtypes': 'word__semtype__semtype',
            'pos': 'word__pos',
            'lemma': 'word__lemma',
            'hid': 'word__hid',
        }
        for item, data in elements:
            qkwargs = {}
            if data:
                if data.has_key('query'):
                    qkwargs = {}
                    for k, v in data['query'].items():
                        if type(v) == list:
                            if len(v) > 0:
                                v = choice(v)
                            else:
                                v = False
                        elif type(v) == string:
                            if v.strip():
                                pass
                            else:
                                v = False

                        if v:
                            qkwargs[element_to_query[k]] = v

                    nocopy = False

                    if data.has_key('copy'):
                        if data['copy'] == True:
                            copies = dict(self.question_elements)[item]
                            data['wordforms'] = copies['wordforms']
                            if data.has_key('selected'):
                                data['selected'] = copies['selected']
                            else:
                                data['selected'] = item
                        else:
                            nocopy = True
                    else:
                        nocopy = True

                    if nocopy:
                        data['wordforms'] = wfs = self.filter_dialect(Form.objects.filter(**qkwargs))
                        wfs = wfs.order_by('?')
                        try:
                            data['selected'] = wfs[0]
                        except:
                            if not self.NO_ERRORS:
                                errormsg = 'Query failed\n'
                                errormsg += 'Question ID: %s\n' % self.qid
                                errormsg += 'Question element: %s\n' % repr(item)
                                errormsg += 'Query arguments: %s\n' % repr(qkwargs)
                                errormsg += 'Zero forms found.\n'
                                if len(qkwargs.keys()) > 0:
                                    qkw_tup = [(a, b) for a, b in qkwargs.items()]
                                    n_comb = range(1, len(qkw_tup)+1)
                                    query_product = []
                                    for c in n_comb:
                                        for a in combinations(qkw_tup, r=c):
                                            query_product.append(dict(a))

                                    for kp in query_product:
                                        count = Form.objects.filter(**kp).count()
                                        errormsg += '  Subquery: \n'
                                        for partk, partv in kp.items():
                                            errormsg += '    - %s: %s\n' % (partk, partv)
                                        errormsg += '    => Object count: %d\n' % count

                                self.errors['self.queryElements'] = errormsg.splitlines()


        return elements

    def elementsToSentence(self, elements, blanks=False):
        """    Expects list of tuples, element data with ['wordforms']

        """

        # TODO: should just append fullform to data, instead.
        # For testing now this is good.
        sentence = []
        for item, data in elements:
            if data:
                if data.has_key('wordforms'):
                    if data.has_key('selected'):
                        wf = data['selected']
                        if type(wf) == Form:
                            if data.has_key('meta'):
                                if data['meta'].has_key('task'):
                                    if data['meta']['task']:
                                        sentence.append('__')
                                    else:
                                        sentence.append(wf.fullform)
                                else:
                                    sentence.append(wf.fullform)
                        else:
                            sentence.append(item)
                    else:
                        sentence.append(item)
            else:
                sentence.append(item)

        return ' '.join([force_unicode(s) for s in sentence])

    def personQA(self, tag):
        QA_tags = []

        tag_elem = tag.split('+')
        new_elems = []
        for elem in tag_elem:
            if elem in self.QAPN.keys():
                elem = self.QAPN[elem]
            new_elems.append(elem)
        new_elems = '+'.join(new_elems)

        return new_elems

    def checkSyntax(self, elements):

        if elements:
            elements_d = dict(elements)
        else:
            return elements
        if self.agreement:
            agreement = self.agreement
        else:
            return elements

        keys = elements_d.keys()
        possible_agreements = agreement.find_possible_agreements(keys)

        # For each possible agreement, mark elem['meta']['agreement'] with the head
        for poss in possible_agreements:
            head, name = poss
            agree = agreement.get_agreement(name)
            targets = agree.targets
            head_elem = elements_d[head]

            try:                head_elem.pop('wordforms')
            except:             pass

            try:                head_elem.pop('copy')
            except:             pass

            try:                head_elem.pop('selected')
            except:             pass

            elements_d[head] = head_elem
            # assign head to each target
            for target in targets:
                e_d = elements_d.get(target['element'], False)
                if e_d:
                    e_d['meta']['agreement'] = head
                    elements_d[target['element']] = e_d


        elements_reorder = []
        for a, v in elements:
            elements_reorder.append((a, elements_d[a]))

        return elements_reorder


    def checkSyntaxOld(self, elements):
        elements_d = dict(elements)
        agr = False

        if elements_d.has_key('SUBJ') and elements_d.has_key('MAINV'):
            if elements_d['MAINV']['meta']:
                elements_d['MAINV']['meta']['agreement'] = 'SUBJ'

        if elements_d.has_key('MAINV') and elements_d.has_key('RPRON'):
            if elements_d['RPRON']['meta']:
                elements_d['RPRON']['meta']['agreement'] = 'MAINV'

        # Check for Question-Answer person agreement (see QAPN)
        if elements_d.has_key('SUBJ'):
            try:
                copy_key = elements_d['SUBJ'].has_key('copy')
            except AttributeError:
                print >> sys.stderr, '     *** Missing SUBJ element in question %s.' % self.qid
                copy_key = False
            if copy_key:
                if elements_d['SUBJ']['copy']:
                    SUBJ = elements_d.get('SUBJ')

                    if SUBJ['query']['pos'] == 'Pron':
                        # TODO: error handling - If this fails, there's something wrong with
                        # tags.txt or grammar_defaults, tags need to be
                        # corrected and reinstalled
                        subj_tags = SUBJ['query']['tags']
                        # Pop these items so that queryElements gets new forms.

                        try:                SUBJ.pop('wordforms')
                        except:                pass

                        try:                SUBJ.pop('copy')
                        except:                pass

                        try:                SUBJ.pop('selected')
                        except:                pass

                        SUBJ['query']['tags'] = [self.personQA(subj_tags)]


                    elements_d['SUBJ'] = SUBJ

        elements_reorder = []
        for a, v in elements:
            elements_reorder.append((a, elements_d[a]))

        return elements_reorder

    def selectItems(self, elements):

        def adjust_lookup_methods(D):
            """ Remove __in and select an item, used in filtering below
            """
            new_D = {}
            for k, v in D.iteritems():
                if type(v) == list:
                    new_v = choice(v)
                else:
                    new_v = v
                new_D[k] = new_v
            return new_D

        elements_d = dict(elements)
        agreement = self.agreement
        # TODO: testing
        # print '-=-=-=-'
        # print 'agreement: ' + repr(agreement)

        # Choose random tag
        # To include agreement, need to check if an element is the head And
        # then find target elements which should not just have a random choice
        # so much as a random choice from the set of filtered and agreed
        # elements

        # found_agreements = list()

        heads, agrees = False, False
        if agreement:
            possible_agreements = agreement.find_possible_agreements(elements_d.keys())
            if len(possible_agreements) > 0:
                heads = [pe[0] for pe in possible_agreements]
                agrees = [agreement.get_agreement(pe[1]) for pe in possible_agreements]
                # TODO: testing
                # print possible_agreements


        unchecked_elements = elements_d.copy()

        # Iterate through possible agreements, choose a random item for the
        # head, and then for each target choose the corresponding and agreeing
        # target.

        if heads and agrees:
            for head_elem, agree in zip(heads, agrees):
                head = elements_d.get(head_elem)
                # Choose a random head tag
                new_head = head.copy()
                if 'tags' in head['query']:
                    if type(head['query']['tags']) == list:
                        new_head['query']['tags'] = choice(head['query']['tags'])
                else:
                    print self.defaults
                    head['query']['tags'] = self.defaults
                    raw_input()

                # Agreement targets...
                targets_in_sentence = [t for t in agree.targets if t['element'] in elements_d.keys()]

                for targ in targets_in_sentence:
                    t = elements_d.get(targ['element'])
                    if not t:
                        msg = ("* Unable to build element <%s>, "
                                "not specified in questionfile or grammar" % targ['element'])
                        self.errors['self.selectItems'] = [msg]
                        continue
                    else:
                        targ_elem = elements_d[targ['element']]

                    # Filter agreement based on the head tag
                    agreed_t = agree.agree_for({
                        head_elem: new_head['query']['tags'],
                        targ['element']: t['query']['tags']
                    })
                    filtered_by_agreement = agreed_t[targ['element']]
                    # Replace tags with filtered tags
                    targ_elem['query']['tags'] = filtered_by_agreement
                    targ_elem['query'] = adjust_lookup_methods(targ_elem['query'])

                    elements_d[targ['element']] = targ_elem
                    unchecked_elements.pop(targ['element'])

                unchecked_elements.pop(head_elem)

        # If there are any elements left that haven't had a choice or filter made, do it.
        for elem_id, elem_data in unchecked_elements.items():
            if elem_data:
                e_data = elem_data.copy()

                if e_data.has_key('query'):
                    for k, v in e_data['query'].items():
                        if type(v) == list:
                            if len(v) > 0:
                                random_query = choice(v)
                                k_s = k.replace('__in', '')
                                e_data['query'][k_s] = random_query
                                if k_s != k:
                                    e_data['query'][k] = ''
                elements_d[elem_id] = e_data


        elements_reorder = []
        for a, v in elements:
            elements_reorder.append((a, elements_d[a]))

        # TODO: testing
        # print elements_reorder
        return elements_reorder

    def handleQuestions(self):
        question = _firstelement(self.node, 'question')

        text = _data(_firstelement(question, 'text'))
        elements = _elements(question, 'element')
        pelements = self.parseElements(elements)

        # TODO: Is this where we have to stop in order to use this class to
        # fill the database? Would need to create QElement and
        # WordQElements of all possible elements, so they can't be
        # trimmed or reduced to reflect element selections and agreement

        # Skip syntax and trimming steps, then query; which should
        # return all possible elements, then can begin creating Question
        # objects

        text_with_elements = self.elementizeText(text, pelements)

        # Check for agreement
        syntax_text = self.checkSyntax(text_with_elements)

        query_elements = self.selectItems(syntax_text)

        queried_elements = self.queryElements(query_elements)

        sentence_text = self.elementsToSentence(queried_elements)


        self.question_elements = queried_elements
        self.question_text = sentence_text + '?'


    def copyQuestion(self, aelements):
        aelements_d = dict(aelements)

        copy_elements = {}
        for k, v in aelements_d.items():
            if not v:
                copied = dict(self.question_elements).get(k)
                if copied:
                    copied['copy'] = True
            else:
                copied = v
                copied['copy'] = False
            copy_elements[k] = copied

        aelements_copied = []
        for a, v in aelements:
            aelements_copied.append((a, copy_elements[a]))
        return aelements_copied

    def selectTask(self, elements):
        """ Takes a list of elements, and returns selects the task.
            This should occur after the queries phase.
        """

        for element_id, element_data in elements:
            if element_data:
                if element_data.has_key('meta'):
                    if element_data['meta'].has_key('task'):
                        if element_data['meta']['task']:
                            return dict([(element_id, element_data)])
        return False

    def handleAnswers(self):
        answers = _elements(self.node, 'answer')
        # TODO: There is a forloop here, but this actually
        # only stores whatever question comes last in the loop.

        class Answer(object):
            pass

        self.answer_set = []

        for answer in answers:
            text = _data(_firstelement(answer, 'text'))
            elements = _elements(answer, 'element')
            pelements = self.parseElements(elements)
            text_with_elements = self.elementizeText(text, pelements)
            answer_elements = self.copyQuestion(text_with_elements)

            # Is this where we have to stop in order to use this class to
            # fill the database? Would need to create QElement and
            # WordQElements of all possible elements, so they can't be
            # trimmed or reduced to reflect element selections and agreement

            # Check for agreement, and also Q-A person changes
            syntax_text = self.checkSyntax(answer_elements)

            query_elements = self.selectItems(syntax_text)

            queried_elements = self.queryElements(query_elements)

            sentence_text = self.elementsToSentence(queried_elements)
            sentence_text_blank = self.elementsToSentence(queried_elements, blanks=True)

            answer = Answer()

            answer.task = self.selectTask(queried_elements)

            answer.answer_elements = queried_elements
            answer.answer_full_text = force_unicode(sentence_text + '.')
            answer.answer_text_blank = force_unicode(sentence_text_blank + '.')
            self.answer_set.append(answer)

    def reselect(self):
        """ Selects a new iteration of the same question.
        """
        # TODO: handleAnswers needs to set attributes for all steps,
        # uff.
        pass

    def requery(self):
        """ Reruns the queries, and selects a new iteration.
        """

        pass

    def __init__(self, q_node, grammar_defaults=False, agreements=None, dialect=False):
        self.agreement = agreements
        self.errors = {}
        self.NO_ERRORS = False
        self.dialect = dialect
        if grammar_defaults:
            self.defaults = grammar_defaults.grammar_definitions
        else:
            defaults_file = file('data_sma/meta/grammar_defaults.xml')
            defaults_tree = _dom.parse(defaults_file)

            self.defaults = GrammarDefaults(defaults_tree).grammar_definitions

        self.node = q_node
        self.handleMeta()
        self.handleQuestions()
        self.handleAnswers()




# # #
#
#  Command class
#
# # #

class FileLog(object):

    def __init__(self, fname):
        self.loglines = []

        if fname:
            self.fname = fname
            self.logfile = open(fname, 'w')
        else:
            self.fname = "stdout"
            self.logfile = False

    def log(self, string, pipe=False):

        import codecs
        import locale
        import sys
        sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
        sys.stderr = codecs.getwriter(locale.getpreferredencoding())(sys.stderr)

        if not string.endswith('\n'):
            string += '\n'

        string = force_unicode(string).encode('utf-8')

        if self.logfile:
            self.logfile.write(string)
        else:
            self.loglines.append(string)

        if not pipe:
            pipe = sys.stderr
        print >> pipe, string.rstrip('\n')


class Command(BaseCommand):
    args = '--grammarfile FILE --questionfile FILE'
    help = """
    """
    option_list = BaseCommand.option_list + (
        # make_option("-g", "--grammarfile", dest="grammarfile", default=False,
        #                   help="XML-file for grammar defaults for questions"),
        # make_option("-q", "--questionfile", dest="questionfile", default=False,
        #               help="XML-file that contains questions"),
        # make_option("--qid", dest="qid", default=False,
        #               help=("Specify a list of IDs to test with commas and no"
        #               "spaces, or specify a partial part of an id to filter"
        #               "questions by, e.g. ill1,ill2  OR  ill#; note the wildcard"
        #               "symbol.")),
        #
        # make_option("--iterations", dest="itercount", default=5,
        #                 help="The count of iterations for each question"),
        # make_option("--logfile", dest="logfile", default=False,
        #                 help="Store all output to a file in addition to stdout."),

        # make_option("--dialect", dest="dialect", default="GG",
        #               help=("Specify a dialect for presenting the generated output.")),

    )

    def print_strings(self, word, tag):
        NEGATIVE_VERB_PRES = oahpa_module.drill.forms.NEGATIVE_VERB_PRES
        TENSE_PRESENTATION = oahpa_module.drill.forms.TENSE_PRESENTATION
        PRONOUNS_LIST = oahpa_module.drill.forms.PRONOUNS_LIST

        form = FakeForm()
        form.pron = False

        if tag.pos == "V":
            # TODO: figure out word object here.
            if not form.pron:
                if tag.string.find("ConNeg") > -1:
                    # TODO: New choice for every refresh, fix!
                    pers = conneg_agr
                    pronoun = form.PronPNBase[pers]
                    neg_verb = NEGATIVE_VERB_PRES[pers]

                    form.pron = '%s %s' % (pronoun, neg_verb)
                elif tag.personnumber:
                    pronbase = PRONOUNS_LIST[tag.personnumber]
                    pronoun = pronbase
                    form.pron = pronoun

                    if form.pron and tag.mood == "Imprt":
                        form.pron_imp = "(" + form.pron + ")"
                        form.pron = ""
                    # TODO: conneg only in Prs

            # Odne 'today', ikte 'yesterday'
            if (tag.tense in ['Prs','Prt']) and (tag.mood == 'Ind'):
                time = TENSE_PRESENTATION.get(tag.tense, False)
                form.pron = '(%s) %s' % (pronoun, time) #' '.join([time, pronoun])

            if ("+Der/Pass" in tag.string) and ("+V" in tag.string):
                # Odne mun ___
                # Ikte mun ___
                # Ikte dat (okta) ___

                # Choose one if not set, if set then game is in progress, and
                # do not choose another
                pers = tag.personnumber
                if not pers:
                    pers = conneg_agr
                time = TENSE_PRESENTATION.get(tag.tense, False)
                pronoun = PASSIVE_PRONOUNS_LIST[pers]

                number = ''
                if pers in ['Sg3', 'Pl3']:
                    number = '(%s)' % DEMONSTRATIVE_PRESENTATION.get(tag.personnumber, False)

                form.pron = ' '.join([time, pronoun, number])

            # All pres?
            if tag.string.find("Der/AV") > -1:
                form.pron = TENSE_PRESENTATION.get(tag.tense, False) + " " + form.pron

            if word.object:
                form.object = word.object


        log_name = "morfa_%s" % tag.pos
        forms = Form.objects.filter(tag=tag, word__lemma=word.lemma)
        if len(forms) > 0:
            fullform = forms[0]
        else:
            fullform = '??'
            # TODO: when no form is generated, what?


        if '+3PlO' in tag.string:
            try:
                pl_object = Form.objects.filter(word__lemma=form.object, tag__string__in=['N+IN+Sg', 'N+AN+Sg'])
                pl_object_string = pl_object[0].fullform
            except Form.DoesNotExist:
                pl_object_string = form.object + '+Pl'
            except IndexError:
                pl_object_string = form.object + '+Pl'
            object = pl_object_string
        elif '+3SgO' in tag.string:
            object = form.object
        else:
            object = form.object


        q_word = word.lemma
        q_tag = tag.string
        q_string = "%(pron)s _________ %(obj)s" % {'pron': form.pron, 'obj': object, 'fullform': fullform}
        return (q_word, q_tag, q_string)

    def handle(self, *args, **options):
        # Morfa-S
        # Nouns:  type, book
        # Verbs: tense, tens_anim


        Form = oahpa_module.drill.models.Form
        Word = oahpa_module.drill.models.Word
        Tag = oahpa_module.drill.models.Tag

        import sys, os
        word_query = Q(pos='V') & Q(trans_anim__in=['TI', 'AI']) & Q(object__isnull=False)
        ws = Word.objects.filter(word_query)
        words_with_objects = []
        for w in ws:
            if w.object:
                words_with_objects.append(w)

        print >> sys.stderr, 'words with possible objects:  ' + str(len(words_with_objects))

        allowed_tags = Tag.objects.filter(
            Q(pos='V') & Q(tense__in=['Prs', 'Prt']) & Q(personnumber__in=['1Sg', '2Sg', '3Sg']) &\
                Q(mood='Ind')
        )

        frames = []
        for word in words_with_objects:
            for tag in allowed_tags:
                frames.append(self.print_strings(word, tag))

        print >> sys.stderr, len(frames)
        sorted_fs = list(set(frames))
        print >> sys.stderr, len(sorted_fs)

        for q_words, q_string, a in frames:
            print >> sys.stdout, q_words.encode('utf-8')
            print >> sys.stdout, a.encode('utf-8')
            print >> sys.stdout, '  '.encode('utf-8')
