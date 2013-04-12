"""

A set of lexicon-related language specific rules, provided by
`lexicon.LexiconOverrides`. There is probably a better location
for this documentation, but for now ...

Example source formatting function:

    @lexicon_overrides.entry_source_formatter('sme')
    def format_source_sme(ui_lang, entry_node):
        # do some processing on the entry node ...
        if successful:
            return some_formatted_string
        return None

Example target string formatting function:

    @lexicon_overrides.entry_target_formatter('sme')
    def format_target_sme(ui_lang, entry_node, tg_node):
        # do some processing on the entry and tg node ...
        if successful:
            return some_formatted_string
        return None

"""

from lexicon import lexicon_overrides
from neahtta import tagfilter

@lexicon_overrides.entry_source_formatter('sma')
def format_source_sma(ui_lang, e):
    paren_args = []

    _str_norm = 'string(normalize-space(%s))'
    _lemma = e.xpath(_str_norm % 'lg/l/text()')
    _class = e.xpath(_str_norm % 'lg/l/@class')
    _pos = e.xpath(_str_norm % 'lg/l/@pos')

    if _pos:
        paren_args.append(tagfilter(_pos, 'sma', ui_lang))

    if _class:
        paren_args.append(_class.lower())

    if len(paren_args) > 0:
        return '%s (%s)' % (_lemma, ', '.join(paren_args))
    else:
        return _lemma

    return None

