from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')

odf = oahpa_module.drill.forms
from odf import *

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
        'common': {'boolean': True,
                   'value': 'on',
                   'name': 'Common places'},
        'rare': {'boolean': True,
                   'value': 'on',
                   'name': 'Rare places'},
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

        'num_bare': { 'options': dict(NUM_BARE_CHOICES),
                   'select': True,
                  'name': 'Case'},

        'num_level': { 'options': dict(NUM_LEVEL_CHOICES),
                   'select': True,
                  'name': 'Level'},

        'num_type': { 'options': dict(NUM_TYPE_CHOICES),
                   'select': True,
                  'name': 'Type'},

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
        'adjcase': {'options': dict(ADJCASE_CHOICES),
                 'select': True,
                 'name': 'Adjective case'},
        'grade': {'options': dict(GRADE_CHOICES),
                 'select': True,
                 'name': 'Grade'},

        'level': {'options': dict(VASTAS_LEVELS),
                  'select': True,
                  'name': 'Level'},

        'dialogue': {'options': dict(DIALOGUE_CHOICES),
                  'select': True,
                  'name': 'Dialogue'},


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
                    'params': ['geography', 'common', 'rare', 'transtype', 'source'],
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
                    'label': 'Date',
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
                    # 'conditional': [
                    #     { 'key': 'vtype',
                    #       'value': 'PRS',
                    #       'params': ['vtype_context'],
                    #     },
                    # ],
                },
                {
                    'params': ['pron_type', 'proncase',],
                    'label': 'Morfa-S Pronouns',
                    'value': 'morfa_s_pron',
                    'path': '/morfas/p/',
                },
                {
                    'params': ['num_bare', 'num_level', 'num_type'],
                    'label': 'Morfa-S Numerals',
                    'value': 'morfa_s_num',
                    'path': '/morfas/l/',
                },
                {
                    'params': ['grade', 'adjcase', 'book', 'stem_type'] + STEM_TYPE,
                    'label': 'Morfa-S Adjectives',
                    'value': 'morfa_s_adj',
                    'path': '/morfas/a/',
                },
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
        'vasta': {
            'subtypes': [
                {
                    'params': ['level'],
                    'label': 'Vasta-S',
                    'value': 'vasta_s',
                    'path': '/vastas/',
                },
                {
                    'params': ['level'],
                    'label': 'Vasta-F',
                    'value': 'vasta_f',
                    'path': '/vastaf/',
                },
            ],
            'label': 'Vasta',
            'value': 'vasta'
        },
        'sahka': {
            'subtypes': [
                {
                    'params': ['dialogue'],
                    'label': 'Sahka',
                    'value': 'sahka',
                    'path': '/sahka/',
                },
                {},
            ],
            'label': 'Sahka',
            'value': 'sahka'
        },

    }

    return GOAL_CHOICE_TREE, GOAL_PARAMETER_CHOICE_VALUES
