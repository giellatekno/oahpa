# -*- coding: utf-8 -*-
from django.forms import ModelForm, Form
from django.utils.translation import ugettext as _
from models import Feedback

GAME_CHOICES = (
	('morfa', 'Morfa'),
	('vasta', 'Vasta'),
	('numra', 'Numra'),
	('sahka', 'Sahka'),
	('leksa', 'Leksa'),
	('all', 'All'),
)


# class FeedbackForm(forms.Form):
# 	message = forms.CharField(widget=forms.Textarea(attrs={'rows':'15', 'cols': '50'}))
# 	name = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
# 	email = forms.EmailField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
# 	place = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
# 	confirmation = forms.BooleanField(required=False,initial=True)
# 	#game = forms.ChoiceField(initial='Morfa', choices=GAME_CHOICES, widget=forms.MultiValueField)
# 	#language = forms.ChoiceField(initial='Morfa', choices=LANG_CHOICES, widget=forms.RadioSelect)
# 	# default_data = {'language' : 'sme', 'game' : 'all'}
#
# #	def __init__(self, *args, **kwargs):
# #		self.set_settings
# #		super(NumForm, self).__init__(*args, **kwargs)


class FeedbackForm(forms.ModelForm):
	"""
		ModelForm version of the above form.
	"""
	message = forms.CharField(widget=forms.Textarea(attrs={'rows':'15', 'cols': '50'}))
	name = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
	email = forms.EmailField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
	place = forms.CharField(widget=forms.TextInput(attrs={'size':'40'}), required=False)
	confirmation = forms.BooleanField(required=False,initial=True)

	class Meta:
		model = Article
		fields = ('message', 'name', 'email', 'place', 'confirmation')
