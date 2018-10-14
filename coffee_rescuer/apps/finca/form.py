from django import forms
from django.forms.widgets import TextInput
import json

class EditorForm(forms.Form):
    jsonfield = forms.CharField(widget=TextInput(attrs={'id': 'infoNuevoMapa'}))
