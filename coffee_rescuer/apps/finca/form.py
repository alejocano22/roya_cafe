from django import forms
from django.forms.widgets import HiddenInput
from apps.finca.models import Finca

class EditorForm(forms.Form):
    jsonfield = forms.CharField(widget=HiddenInput(attrs={'id': 'infoNuevoMapa'}))


