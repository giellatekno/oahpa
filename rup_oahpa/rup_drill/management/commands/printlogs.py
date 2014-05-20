from django.core.management.base import BaseCommand, CommandError

# from_yaml(cls, loader, node)

from optparse import make_option

import sys

from rup_drill.models import Log

def printLogs(queryset, csv=False, delimiter=False, attrs=False):
	""" Print filtered queryset.
	"""
	
	import csv as _csv
	_OUT = sys.stdout
	
	pkwargs = {'printattrs': attrs}
	
	# csv dialects
	if csv:
		class csv_out:
			delimiter = ','
			quotechar = '"'
			escapechar = '\\' 
			doublequote = True
			skipinitialspace = False
			lineterminator = '\n'
			quoting = _csv.QUOTE_ALL
		
		# This delimiter is only used for outputEntry method
		pkwargs['delimiter'] = '|'
	else:
		delimiter = pkwargs['delimiter'] = '|'

		class csv_out:
			escapechar = ''
			doublequote = False
			skipinitialspace = False
			lineterminator = '\n'
			quoting = _csv.QUOTE_NONE
		
		csv_out.delimiter = delimiter
	
	_fmt = lambda x: [a.encode('utf-8') for a in 
						x.outputEntry(**pkwargs).split(pkwargs['delimiter'])]

	printlines = (_fmt(item) for item in queryset)

	W = _csv.writer(_OUT, dialect=csv_out)

	# WriteCSV
	if csv:
		W.writerow(attrs)
	
	for r in printlines:
		W.writerow(r)
	
	return True


def filterLogs(filters=False):
	""" Filters logs, returns a queryset.
	"""
	if filters:
		return Log.objects.filter(**filters)
	else:
		return Log.objects.all()


##
 # 
 #  Command class
 #
 #
 
class Command(BaseCommand):
	args = ''
	help = '''
	Print log entries.
	Examples:

		./manage.py printlogs --game morfa_N --display-values "date,userinput"
		./manage.py printlogs --game 'contextual morfa'
	'''	
	
	GAMENAMES = list(set(Log.objects.all().values_list('game', flat=True)))
	GAMENAMES = ', '.join(GAMENAMES)
	_ATTRS = ['game',
			  'date',
			  'userinput',
			  'correct',
			  'iscorrect',
			  'example',
			  'feedback',
			  'comment']

	GAMEATTRS =  ', '.join(_ATTRS)

	option_list = BaseCommand.option_list + (
		make_option("-c", "--csv", dest="csv", default=False,
						  action='store_true',
						  help="CSV output."),

		make_option("-d", "--delimiter", dest="delimiter", default="|",
						  help="Specify a delimiter"),

		make_option("-x", "--display-values", dest="values", default=False,
			  help="Specify which values to display. Options: %s. Default: all." % GAMEATTRS),

		make_option("-g", "--game", dest="filter_game", default=False,
			  help="Display output only from a specific game. Options: %s." % GAMENAMES),
		
	)

	def handle(self, *args, **options):
		import sys, os

		delimiter = options['delimiter']
		values = options['values']
		filter_game = options['filter_game']
		csv = options['csv']

		# Prepare filters
		filters = {}
		if filter_game:
			filters['game'] = filter_game

		if all([filter_game,]) == False:
			filters = False
		
		# Prepare for display
		plogs = {}
		
		if csv:
			plogs['csv'] = True
			plogs['delimiter'] = False
			plogs['attrs'] = self._ATTRS
		else:
			plogs['csv'] = False
			plogs['delimiter'] = delimiter

		if values:
			displ_v = [a.strip() for a in values.split(',') if a.strip()]
			plogs['attrs'] = displ_v

		if filters:
			queryset = filterLogs(filters)
		else:
			queryset = filterLogs()
		
		plogs['queryset'] = queryset
		
		printLogs(**plogs)


