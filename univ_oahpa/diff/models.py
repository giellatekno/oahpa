from django.db import models
from univ_drill.models import Word

class WordDiff(models.Model):
	word = models.ForeignKey(Word, unique=True)
	checksum = models.TextField()

class ParadigmDiff(models.Model):
	key = models.CharField(max_length=50, unique=True)
	checksum = models.TextField()

# Create your models here.
