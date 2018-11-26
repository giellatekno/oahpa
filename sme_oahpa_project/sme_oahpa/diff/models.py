from django.db import models

from local_conf import LLL1
import importlib
oahpa_module = importlib.import_module(LLL1+'_oahpa')

Word = oahpa_module.drill.models.Word

class WordDiff(models.Model):
	word = models.ForeignKey(Word, unique=True)
	checksum = models.TextField()

class ParadigmDiff(models.Model):
	key = models.CharField(max_length=50, unique=True)
	checksum = models.TextField()

# Create your models here.
