from django import forms
from django.forms.widgets import DateInput
from datetime import date
class HistorialForm(forms.Form):
		fecha_hoy = date.today()
		start =  forms.DateField(widget=DateInput(attrs={'class':'form-control','type': 'date','max':str(fecha_hoy),'min':'2017-01-01'}),label="Fecha Inicial")
		end =forms.DateField(widget=DateInput(attrs={'class':'form-control','type': 'date','max':str(fecha_hoy),'min':'2017-01-01'}), label="Fecha Final")
		
	