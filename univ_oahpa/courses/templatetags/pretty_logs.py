from django import template
from django.utils.translation import ugettext_lazy as _


register = template.Library()

FILTER_WORDS = [
	'Contextual',
	'ordinal',
	'cardinal',
	'clock',
	'dato',
	'Place',
]

from univ_drill.forms import ADJCASE_CHOICES, ADJEX_CHOICES, ADJ_CONTEXT_CHOICES, BOOK_CHOICES, CASE_CHOICES, CASE_CHOICES_PRONOUN, CASE_CONTEXT_CHOICES, DIALOGUE_CHOICES, FREQUENCY_CHOICES, GEOGRAPHY_CHOICES, GRADE_CHOICES, KLOKKA_CHOICES, LEVEL_CHOICES, NUMGAME_CHOICES, NUMGAME_CHOICES_PL, NUMLANGUAGE_CHOICES, NUM_BARE_CHOICES, NUM_CHOICES, NUM_CONTEXT_CHOICES, NUM_LEVEL_CHOICES, POS_CHOICES, PRONOUN_SUBCLASSES, PRON_CONTEXT_CHOICES, RECIP_REFL_CHOICES, SEMTYPE_CHOICES, TRANS_CHOICES, VASTA_LEVELS, VERB_CLASSES, VTYPE_CHOICES, VTYPE_CONTEXT_CHOICES

tuple_sets = [
ADJCASE_CHOICES, ADJEX_CHOICES, ADJ_CONTEXT_CHOICES, BOOK_CHOICES,
CASE_CHOICES, CASE_CHOICES_PRONOUN, CASE_CONTEXT_CHOICES, DIALOGUE_CHOICES,
FREQUENCY_CHOICES, GEOGRAPHY_CHOICES, GRADE_CHOICES, KLOKKA_CHOICES,
LEVEL_CHOICES, NUMGAME_CHOICES, NUMGAME_CHOICES_PL, NUMLANGUAGE_CHOICES,
NUM_BARE_CHOICES, NUM_CHOICES, NUM_CONTEXT_CHOICES, NUM_LEVEL_CHOICES,
POS_CHOICES, PRONOUN_SUBCLASSES, PRON_CONTEXT_CHOICES, RECIP_REFL_CHOICES,
SEMTYPE_CHOICES, TRANS_CHOICES, VASTA_LEVELS, VERB_CLASSES, VTYPE_CHOICES,
VTYPE_CONTEXT_CHOICES, 

				# CASE_CHOICES, 
				# CASE_CHOICES_PRONOUN, 
				# CASE_CONTEXT_CHOICES,
				# PRONOUN_SUBCLASSES,
				# PRON_CONTEXT_CHOICES,
				# ADJCASE_CHOICES,
				# ADJEX_CHOICES,
				# VTYPE_CHOICES,
				# VTYPE_CONTEXT_CHOICES,
]

key_to_string = {}

for s in tuple_sets:
	for k, v in s:
		key_to_string[k] = v


@register.filter(name='filter_log')
def filter_log(value):
	""" Pass chunks of gamenames through all of the form choice elements to
	retrieve their gettext strings, if they exist, return an iterator.
	"""

	substituted = []

	items = value.split(' - ')
	for item in items:
		subitems = item.split(', ')

		sub_subs = []
		for subitem in subitems:
			sub = key_to_string.get(subitem, subitem)
			sub_subs.append(sub)

		substituted.extend(sub_subs)
	
	return substituted

