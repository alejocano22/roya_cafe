from django import forms
from django.forms.widgets import HiddenInput


class EditorForm(forms.Form):
    jsonfield = forms.CharField(widget=HiddenInput(attrs={'id': 'infoNuevoMapa'}))


