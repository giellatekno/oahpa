# -*- encoding: utf-8 -*-

# NOTE: if copying this for a new language, remember to make sure that
# it's being imported in __init__.py

from morphology import generation_restriction

LEX_TO_FST = {
    'a': 'A',
    'adv': 'Adv',
    'n': 'N',
    'npl': 'N',
    'num': 'Num',
    'prop': 'Prop',
    'v': 'V',
}

@generation_restriction.tag_filter_for_iso('sma')
def lexicon_pos_to_fst_sma(form, tags, node=None):

    new_tags = []
    for t in tags:
        _t = []
        for p in t:
            _t.append(LEX_TO_FST.get(p, p))
        new_tags.append(_t)

    return form, new_tags, node


@generation_restriction.tag_filter_for_iso('sme')
def lexicon_pos_to_fst(form, tags, node=None):

    new_tags = []
    for t in tags:
        _t = []
        for p in t:
            _t.append(LEX_TO_FST.get(p, p))
        new_tags.append(_t)

    return form, new_tags, node

@generation_restriction.tag_filter_for_iso('sme')
def impersonal_verbs(form, tags, node=None):
    if len(node) > 0:
        context = node.xpath('.//l/@context')

        if ("upers" in context) or ("dat" in context):
            new_tags = [
                'V+Ind+Prs+Sg3'.split('+'),
                'V+Ind+Prt+Sg3'.split('+'),
                'V+Ind+Prs+ConNeg'.split('+'),
            ]

            return form, new_tags, node

    return form, tags, node

@generation_restriction.tag_filter_for_iso('sme')
def proper_nouns(form, tags, node):
    # TODO: this only works if we have pos="n" type="prop"
    if len(node) > 0:
        pos = node.xpath('.//l/@pos')
        _type = node.xpath('.//l/@type')
        if ("prop" in pos) or ("prop" in _type):
            tags = [
                'N+Prop+Sg+Gen'.split('+'),
                'N+Prop+Sg+Ill'.split('+'),
                'N+Prop+Sg+Loc'.split('+'),
            ]

    return form, tags, node

@generation_restriction.tag_filter_for_iso('sme')
def compound_numerals(form, tags, node):
    if len(node) > 0:
        if 'num' in node.xpath('.//l/@pos'):
            tags = [
                'Num+Sg+Gen'.split('+'),
                'Num+Sg+Ill'.split('+'),
                'Num+Sg+Loc'.split('+'),
            ]
    return form, tags, node


