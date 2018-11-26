#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# setup environment
from os import environ
import os, sys 
print " * Correcting paths" 
cur_path = os.getcwd()
parent_path = '/' + '/'.join([a for a in cur_path.split('/') if a][0:-1]) + '/' 
sys.path.insert(0, parent_path)
environ['DJANGO_SETTINGS_MODULE'] = 'smn_oahpa.settings'
import settings
settings.DEBUG = False


# Fun time

from smadrill.models import Word, Semtype
from django.db.models import Q, Count
from django.utils.encoding import force_unicode
import timeit


excl = 'exclude_smanob'  

# def main():
	# QUERY = Q(language='sma')
	# word_set = Word.objects.filter(wordtranslation__language='nob').annotate(num_xlations=Count('wordtranslation')).filter(num_xlations__gt=0).filter(QUERY).exclude(semtype__semtype=excl)
	# print word_set
	# return


# t = timeit.Timer("main()", 'gc.enable()')
# print t.timeit(number=10)
# main()

def main():
	stype = Word.objects.all()
	words = stype.filter(language='sma')
	excluded = words.exclude(semtype__semtype__in=excl)
	sources = excluded.filter(source__name__in=['dej']).order_by('?')[0:20]
	remove_none = [a for a in sources if a.wordtranslation_set.count() > 0]
	
	print remove_none
	return

t = timeit.Timer("main()", 'gc.enable()')
print t.timeit(number=10)
main()


