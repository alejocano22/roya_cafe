from django import forms
from django.forms.widgets import DateInput

class HistorialForm(forms.Form):
		start =  forms.DateField(widget=DateInput(attrs={'type': 'date'}),label="Fecha inicial")
		end =forms.DateField(widget=DateInput(attrs={'type': 'date'}), label="Fecha Final")
		
	