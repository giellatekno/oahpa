# -*- encoding: utf-8 -*-

# NOTE: if copying this for a new language, remember to make sure that
# it's being imported in __init__.py

from morphology import generation_restriction

@generation_restriction.tag_filter_for_iso('sme')
def impersonal_verbs(form, tags, node):
    if node is not None:
        context = node.xpath('.//l/@context')

        if ("upers" in context) or ("dat" in context):
            tags = [
                'V+Ind+Prs+Sg3'.split('+'),
                'V+Ind+Prt+Sg3'.split('+'),
                'V+Ind+Prs+ConNeg'.split('+'),
            ]

    return form, tags, node

@generation_restriction.tag_filter_for_iso('sme')
def proper_nouns(form, tags, node):
    # TODO: this only works if we have pos="n" type="prop"
    if node is not None:
        pos = node.xpath('.//l/@type')

        if ("prop" in pos):
            tags = [
                'N+Prop+Sg+Gen'.split('+'),
                'N+Prop+Sg+Ill'.split('+'),
                'N+Prop+Sg+Loc'.split('+'),
            ]

    return form, tags, node

@generation_restriction.tag_filter_for_iso('sme')
def compound_numerals(form, tags, node):
    if node is not None:
        if 'num' in node.xpath('.//l/@pos'):
            tags = [
                'Num+Sg+Gen'.split('+'),
                'Num+Sg+Ill'.split('+'),
                'Num+Sg+Loc'.split('+'),
            ]
    return form, tags, node




