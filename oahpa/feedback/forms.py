# -*- coding: utf-8 -*-
import string
import sys
from django import newforms as forms
from django.http import Http404
from django.db.models import Q
from django.utils.translation import ugettext as _
from random import randint
from models import *


GAME_CHOICES = (
    ('morfa', 'Morfa'),
    ('vasta', 'Vasta'),
    ('numra', 'Numra'),
    ('sahka', 'Sahka'),
    ('leksa', 'Leksa'),
    ('all', 'All'),
)


class FeedbackForm(forms.Form):

    message = forms.CharField(widget=forms.Textarea(attrs={'rows':'15', 'cols': '50'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
    place = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
    confirmation = forms.BooleanField(required=False,initial=True)
    #game = forms.ChoiceField(initial='Morfa', choices=GAME_CHOICES, widget=forms.MultiValueField)
    #language = forms.ChoiceField(initial='Morfa', choices=LANG_CHOICES, widget=forms.RadioSelect)
    default_data = {'language' : 'sme', 'game' : 'all'}
                    
#    def __init__(self, *args, **kwargs):
#        self.set_settings
#        super(NumForm, self).__init__(*args, **kwargs)
