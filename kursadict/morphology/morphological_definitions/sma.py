# -*- encoding: utf-8 -*-

# NOTE: if copying this for a new language, remember to make sure that
# it's being imported in __init__.py

from morphology import generation_restriction

LEX_TO_FST = {
    'a': 'A',
    'adv': 'Adv',
    'n': 'N',
    'npl': 'N', # TODO: npl filter
    'num': 'Num',
    'prop': 'Prop',
    'v': 'V',
}

@generation_restriction.tag_filter_for_iso('sma')
def adj_pos_fix(form, tags, node=None):

    new_tags = []
    for t in tags:
        _t = []
        for p in t:
            _t.append(LEX_TO_FST.get(p, p))
        new_tags.append(_t)

    return form, new_tags, node


@generation_restriction.tag_filter_for_iso('sma')
def lexicon_pos_to_fst_sma(form, tags, node=None):

    new_tags = []
    for t in tags:
        _t = []
        for p in t:
            _t.append(LEX_TO_FST.get(p, p))
        new_tags.append(_t)

    return form, new_tags, node

@generation_restriction.tag_filter_for_iso('sma')
def include_hid_in_gen(form, tags, node):
    new_tags = tags[:]

    if len(node) > 0:
        hid = node.xpath('.//l/@hid')
        if hid:
            hid = hid[0]
            new_tags = []
            for tag in tags:
                ntag = [hid] + tag
                new_tags.append(ntag)

    return form, new_tags, node

@generation_restriction.tag_filter_for_iso('sma')
def proper_nouns(form, tags, node):
    if len(node) > 0:
        pos = node.xpath('.//l/@pos')
        _type = node.xpath('.//l/@type')

        if ("prop" in pos) or ("prop" in _type):
            tags = [
                'N+Prop+Sg+Gen'.split('+'),
                'N+Prop+Sg+Ill'.split('+'),
                'N+Prop+Sg+Ine'.split('+'),
            ]

    return form, tags, node


@generation_restriction.tag_filter_for_iso('sma')
def sma_common_noun_pluralia_tanta(form, tags, node):
    if len(node) > 0:
        num = node.xpath('.//l/@num')
        if ("pl" in num) or ("Pl" in num):
            tags = [
                '+'.join(tag).replace('Sg', 'Pl').split('+')
                for tag in tags
            ]

    return form, tags, node

