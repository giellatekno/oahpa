from univ_drill.forms import *

__all__ = [
    'prepare_goal_params',
]

def prepare_goal_params(rq=None):

    # Here's a definition of all the choice possibilities that will be
    # available to users below.

    # TODO: add the rest of the form choices.

    # TODO: bisyllabic, trisyllabic, contracted choices as checkboxes
    GOAL_PARAMETER_CHOICE_VALUES = {
        'source': {'options': dict(BOOK_CHOICES),
                   'select': True,
                   'name': 'Book'},
        'geography': {'options': dict(GEOGRAPHY_CHOICES),
                   'select': True,
                      'name': 'Geography'},
        'common': {'options': dict(FREQUENCY_CHOICES),
                   'select': True,
                   'name': 'Word frequency'},
        'semtype': {'options': dict(SEMTYPE_CHOICES),
                   'select': True,
                    'name': 'Semantic set'},
        'transtype': {'options': dict(TRANS_CHOICES),
                   'select': True,
                      'name': 'Translation'},

        'numgame': {'options': dict(NUMGAME_CHOICES),
                   'select': True,
                    'name': 'Game type'},
        'maxnum':  {'options': dict(NUM_CHOICES),
                   'select': True,
                    'name': 'Max number'},

        'gametype':  {'options': dict(KLOKKA_CHOICES),
                   'select': True,
                    'name': 'Difficulty'},

        'case':  {'options': dict(CASE_CHOICES),
                   'select': True,
                  'name': 'Case'},
        'vtype': {'options': dict(VTYPE_CHOICES),
                   'select': True,
                  'name': 'Verb type'},

        'contracted': {
            'boolean': True,
            'value': 'on',
            'name': 'contracted',
        },

        'bisyllabic': {
            'boolean': True,
            'value': 'on',
            'name': 'bisyllabic',
        },

        'trisyllabic': {
            'boolean': True,
            'value': 'on',
            'name': 'trisyllabic',
        },

        'pron_type': {'options': dict(PRONOUN_SUBCLASSES),
                   'select': True,
                  'name': 'Pronoun type'},
        'proncase': {'options': dict(CASE_CHOICES),
                   'select': True,
                  'name': 'Pronoun case'},

        'case_context':  {'options': dict(CASE_CONTEXT_CHOICES),
                   'select': True,
                  'name': 'Case'},
        'vtype_context': {'options': dict(VTYPE_CONTEXT_CHOICES),
                   'select': True,
                  'name': 'Verb type'},
        # TODO: test adj
        'adj_context': {'options': dict(ADJ_CONTEXT_CHOICES),
                   'select': True,
                  'name': 'Adjective type'},
        'pron_context': {'options': dict(PRON_CONTEXT_CHOICES),
                   'select': True,
                  'name': 'Pronoun type'},
        'num_context': {'options': dict(NUM_CONTEXT_CHOICES),
                   'select': True,
                  'name': 'Numeral case'},
        'derivation_type_context': {'options': dict(DERIVATION_CHOICES),
                   'select': True,
                  'name': 'Derivation type'},

        # TODO: adj grade choices in context?
    }

    # This is a definition of the form tree that wil be presented.  Each
    # key represents a main type, and this is a list of subtypes.  Each
    # subtype contains `params`, which are HTTP parameters that will be
    # set on the URL. If any need to be hidden and only displayed in
    # certain cases, these will be defined in 'conditional', which is a
    # list of objects, where the key is the parameter that the condition
    # relates to, and a value is defined with a list of parameters that
    # will be displayed if this condition is true.

    # Eventually this might be able to be automatically constructed from
    # something.

    STEM_TYPE = ['bisyllabic', 'trisyllabic', 'contracted']

    GOAL_CHOICE_TREE = {
        'leksa': {
            'subtypes': [
                {
                    'path': '/leksa/',
                    'label': 'Words',
                    'value': 'leksa',
                    'params': ['source', 'semtype', 'transtype'],
                },
                {
                    'path': '/leksa/sted/',
                    'label': 'Placenames',
                    'value': 'leksa_place',
                    'params': ['geography', 'common', 'transtype'],
                }
            ],
            'label': 'Leksa',
            'value': 'leksa',
        },
        'numra': {
            'subtypes': [
                {
                    'path': '/numra/',
                    'label': 'Cardinal numbers',
                    'value': 'numra_number',
                    'params': ['numgame', 'maxnum'],
                },
                {
                    'path': '/numra/ord/',
                    'label': 'Ordinal numbers',
                    'value': 'numra_ordinal',
                    'params': ['numgame', 'maxnum'],
                },
                {
                    'path': '/numra/klokka/',
                    'label': 'Time',
                    'value': 'numra_klokka',
                    'params': ['gametype', 'numgame', 'maxnum'],
                },
                {
                    'path': '/numra/dato/',
                    'label': 'Time',
                    'value': 'numra_dato',
                    'params': ['numgame'],
                },
            ],
            'label': 'Numra',
            'value': 'numra',
        },
        'morfas': {
            'subtypes': [
                {
                    'params': ['case', 'book', 'stem_type'] + STEM_TYPE,
                    'label': 'Morfa-S Nouns',
                    'value': 'morfa_s_noun',
                    'path': '/morfas/s/',
                },
                {
                    'params': ['vtype', 'book', 'stem_type'],
                    'label': 'Morfa-S Verb',
                    'value': 'morfa_s_verb',
                    'path': '/morfas/v/',
                    'conditional': [
                        { 'key': 'vtype',
                          'value': 'PRS',
                          'params': ['something'],
                        },
                        { 'key': 'vtype',
                          'value': 'PRT',
                          'params': ['something_else'],
                        },
                    ],
                },
                {
                    'params': ['pron_type', 'proncase',],
                    'label': 'Morfa-S Pronouns',
                    'value': 'morfa_s_pron',
                    'path': '/morfas/p/',
                },
                # TODO: Morfa-S Adj
                # TODO: Morfa-S Pronouns
                # TODO: Morfa-S Numerals
                # TODO: Morfa-S Derivations
            ],
            'label': 'Morfa-S',
            'value': 'morfa_s'
        },
        'morfac': {
            'subtypes': [
                {
                    'params': ['case_context',],
                    'label': 'Morfa-C Nouns',
                    'value': 'morfa_c_noun',
                    'path': '/morfac/s/',
                },
                {
                    'params': ['vtype_context',],
                    'label': 'Morfa-C Verb',
                    'value': 'morfa_c_verb',
                    'path': '/morfac/v/',
                },
                {
                    'params': ['adj_context',],
                    'label': 'Morfa-C Adjectives',
                    'value': 'morfa_c_adj',
                    'path': '/morfac/a/',
                },
                {
                    'params': ['pron_context',],
                    'label': 'Morfa-C Pronouns',
                    'value': 'morfa_c_pron',
                    'path': '/morfac/p/',
                },
                {
                    'params': ['num_context',],
                    'label': 'Morfa-C Numerals',
                    'value': 'morfa_c_num',
                    'path': '/morfac/l/',
                },
                {
                    'params': ['derivation_type_context'],
                    'label': 'Morfa-C Derivations',
                    'value': 'morfa_c_der',
                    'path': '/morfac/der/',
                },
            ],
            'label': 'Morfa-C',
            'value': 'morfa_c'
        },
    }

    return GOAL_CHOICE_TREE, GOAL_PARAMETER_CHOICE_VALUES
