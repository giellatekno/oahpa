# -*- encoding: utf-8 -*-

# NOTE: if copying this for a new language, remember to make sure that
# it's being imported in __init__.py

# * paradigm documentation here:
#   http://giellatekno.uit.no/doc/dicts/dictionarywork.html

from morphology import generation_overrides as rewrites

LEX_TO_FST = {
    'a': 'A',
    'adv': 'Adv',
    'n': 'N',
    'npl': 'N',
    'num': 'Num',
    'prop': 'Prop',
    'v': 'V',
}

@rewrites.pregenerated_form_selector('sme')
def pregenerate_sme(form, tags, node):
    _has_mini_paradigm = node.xpath('.//mini_paradigm[1]')

    _has_lemma_ref     = node.xpath('.//lemma_ref')
    if len(_has_lemma_ref) > 0:
        return form, [], node, []
    if len(_has_mini_paradigm) == 0:
        return form, tags, node
    else:
        mp = _has_mini_paradigm[0]

    def analysis_node(node):
        """ Node ->
            ("lemma", ["Pron", "Sg", "Tag"], ["wordform", "wordform"])
        """
        tag = node.xpath('.//@ms')
        if len(tag) > 0:
            tag = tag[0].split('_')
        else:
            tag = []

        wfs = node.xpath('.//wordform/text()')

        return (form, tag, wfs)

    analyses = map(analysis_node, mp.xpath('.//analysis'))

    return form, tags, node, analyses


@rewrites.tag_filter_for_iso('sme')
def lexicon_pos_to_fst(form, tags, node=None):

    new_tags = []
    for t in tags:
        _t = []
        for p in t:
            _t.append(LEX_TO_FST.get(p, p))
        new_tags.append(_t)

    return form, new_tags, node

@rewrites.tag_filter_for_iso('sme')
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

@rewrites.tag_filter_for_iso('sme')
def common_noun_pluralia_tanta(form, tags, node):
    """ Pluralia tanta common noun

    `ruossalassánit` with <l nr="Pl" /> requires only plural
    paradigm.
    """
    if len(node) > 0:
        nr = node.xpath('.//l/@nr')
        if ("pl" in nr) or ("Pl" in nr):
            tags = [
                'N+Pl+Nom'.split('+'),
                'N+Pl+Ill'.split('+'),
                'N+Pl+Loc'.split('+'),
            ]

    return form, tags, node

@rewrites.tag_filter_for_iso('sme')
def proper_noun_pluralia_tanta(form, tags, node):
    """ Pluralia tanta

    `Gállábártnit` with <l nr="Pl" /> requires only plural
    paradigm.

    Note, there is a singularia tanta, but this may require a separate
    rule, as it mostly concerns pronouns.
    """
    if len(node) > 0:
        _type = node.xpath('.//l/@type')
        nr = node.xpath('.//l/@nr')
        if (("pl" in nr) or ("Pl" in nr)) and ("Prop" in _type):
            tags = [
                'N+Prop+Pl+Gen'.split('+'),
                'N+Prop+Pl+Ill'.split('+'),
                'N+Prop+Pl+Loc'.split('+'),
            ]

    return form, tags, node

@rewrites.tag_filter_for_iso('sme')
def compound_numerals(form, tags, node):
    if len(node) > 0:
        if 'num' in node.xpath('.//l/@pos'):
            tags = [
                'Num+Sg+Gen'.split('+'),
                'Num+Sg+Ill'.split('+'),
                'Num+Sg+Loc'.split('+'),
            ]
    return form, tags, node

# @rewrites.postgeneration_filter_for_iso('sme')
# def verb_context(generated_result, *generation_input_args):
#     print "omg"
#     print generated_result
#     print generation_input_args
#     return generated_result
