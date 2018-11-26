from django.core.management.base import BaseCommand, CommandError

# from_yaml(cls, loader, node)

from optparse import make_option

import sys

from courses.models import Activity

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
    
    print " %s is merged with other activities, now you can give it a canonical name." % main


# # # 
# 
#  Command class
#
# # #

def mergeactivities(tfilter=False):
	qset = Activity.objects.all()
	
	strings = qset.values_list('name', flat=True)
	strings = list(set(strings))

	print 'Merging:'
	for string in strings:
		tag = Activity.objects.filter(name=string)

		if tag.count() > 1:
			print 'Merging conflict in %s' % tag[0].name
			merge(tag)

class Command(BaseCommand):
	args = '--tagelement'
	help = """
	Strips tags of an element and then merges them all.
	"""
	option_list = BaseCommand.option_list + (
		make_option("-d", "--dryrun", dest="dryrun", default="True",
						  help="List tags matching element instead of merging"),
		
		# TODO: question iterations count
	)

	def handle(self, *args, **options):
		import sys, os

		dry_run = options['dryrun']
		
		mergeactivities()



