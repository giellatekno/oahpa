# TODO:  automatic optimize after syncdb

## from django.db.models.signals import post_syncdb
## import smadrill.models
## import sys
## 
## from smadrill.management.commands.optimize_tables import optimize_tables
## 
## post_syncdb.connect(optimize_tables, sender=smadrill.models)
