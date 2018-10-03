from django import forms
from django.forms.widgets import SelectDateWidget
import datetime
class HistorialForm(forms.Form):
		start =  forms.DateField(widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),),)
		end = forms.DateField(widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),),)
		
	