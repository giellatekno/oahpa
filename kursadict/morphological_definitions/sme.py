# -*- encoding: utf-8 -*-

# NOTE: if copying this for a new language, remember to make sure that
# it's being imported in __init__.py

from morphology import generation_restriction

@generation_restriction.tag_filter_for_iso('sme')
def impersonal_verbs(form, tags, node):
    context = node.xpath('.//l/@context')

    if ("upers" in context) or ("dat" in context):
        tags = [
            'V+Ind+Prs+Sg3'.split('+'),
            'V+Ind+Prt+Sg3'.split('+'),
            'V+Ind+Prs+ConNeg'.split('+'),
        ]

    return form, tags, node


