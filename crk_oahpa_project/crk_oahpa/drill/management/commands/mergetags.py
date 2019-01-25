from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')

from django.core.management.base import BaseCommand, CommandError

# from_yaml(cls, loader, node)

from optparse import make_option

import sys

Tag = oahpa_module.drill.models.Tag

def merge(queryset):
    main = queryset[0]
    tail = queryset[1:]
    related = main._meta.get_all_related_objects()
    valnames = dict()

    for r in related:
        valnames.setdefault(r.model, []).append(r.field.name)

    for model_object in tail:
        for model, field_names in valnames.iteritems():
            for field_name in field_names:
                model.objects.filter(**{field_name: model_object}).update(**{field_name: main})
        model_object.delete()

    print " %s is merged with other tags, now you can give it a canonical name." % main


# # #
#
#  Command class
#
# # #

def mergetags(tfilter=False):
	if tfilter:
		qset = Tag.objects.filter(string=tfilter)
	else:
		qset = Tag.objects.all()

	strings = qset.values_list('string', flat=True)
	strings = list(set(strings))

	print 'Merging:'
	for string in strings:
		tag = Tag.objects.filter(string=string)

		if tag.count() > 1:
			print 'Merging conflict in %s' % tag[0].string
			merge(tag)


class Command(BaseCommand):
	args = '--tagelement'
	help = """
	Strips tags of an element and then merges them all.
	"""
	def add_arguments(self, parser):
		parser.add_argument(
		'-t', '--tagelement',
        	dest='tagelement',
        	default=False,
        	help="Tag element to search for")

        	parser.add_argument(
            	'-d', '--dryrun',
            	dest='dryrun',
            	default=True,
            	help="List tags matching element instead of merging")


	def handle(self, *args, **options):
		import sys, os

		tag_element = options['tagelement']
		dry_run = options['dryrun']

		if tag_element:
			TVs = Tag.objects.filter(string__contains=tag_element)

			for TV in TVs:
				new_str = TV.string.replace(tag_element, '')
				filtered = Tag.objects.filter(string__contains=new_str)

				print 'Merging:'
				for t in filtered:
					print ' %s' % t.string

				filtered_up = filtered.update(string=new_str)
				merge(filtered)


			ts = Tag.objects.filter(string__contains='V+Inf')
			ts.update(string='V+Inf')
		else:
			mergetags()
