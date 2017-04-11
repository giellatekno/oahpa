from django import template
from django.utils.translation import ugettext_lazy as _


register = template.Library()

FILTER_EXCEPTIONS = dict([
	(u'Contextual Morfa', u'Morfa C'),
])

from mdf_drill.forms import ALL_CHOICES

key_to_string = {}

for s in ALL_CHOICES:
	for k, v in s:
		if k.lower() not in key_to_string:
			key_to_string[unicode(k.lower())] = v
		elif k.lower() in key_to_string:
			continue
			# print 'possible duplicate? ', k.lower(), ' ', v
			# key_to_string[unicode(k.lower())] = v

# TODO: Leksa - Place - maailma - tavalliset - harvat
#								  ^-----------------^

# TODO: Morfa - substantiivi - essiivi - 2syll/3syll
#										 ^---------^


@register.filter(name='filter_log')
def filter_log(value):
	""" Pass chunks of gamenames through all of the form choice elements to
	retrieve their gettext strings, if they exist, return an iterator.
	"""

	substituted = []

	items = [i for i in value.split(' - ') if i.strip()]
	# print items
	for item in items:
		subitems = item.split(', ')
		subitems = [a.split('/') for a in subitems]
		subitems = sum(subitems, [])

		sub_subs = []
		for subitem in subitems:
			if subitem not in FILTER_EXCEPTIONS:
				sub = key_to_string.get(subitem.lower(), subitem)
				if type(sub) not in [str, unicode]:
					sub_subs.append(sub)
				else:
					sub_subs.append(subitem)
			else:
				sub = FILTER_EXCEPTIONS[subitem]
				sub_subs.append(sub)


		substituted.extend(sub_subs)
	
	return substituted

