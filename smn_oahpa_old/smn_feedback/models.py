from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Feedback(models.Model):
	name = models.CharField(max_length=100,blank=True)
	place = models.CharField(max_length=100,blank=True)
	game = models.CharField(max_length=10,blank=True)
	language = models.CharField(max_length=10,blank=True)
	email = models.CharField(max_length=50,blank=True)
	message = models.CharField(max_length=500,blank=True)
	confirmation = models.BooleanField()
	confirmed_by = models.CharField(max_length=20,blank=True)
	comments = models.CharField(max_length=100,blank=True)
	date = models.DateField(blank=True, null=True)
	confirmation_date = models.DateField(blank=True, null=True)
