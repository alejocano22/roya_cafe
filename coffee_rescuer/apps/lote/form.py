from django import forms
from django.forms.widgets import DateInput
import tzlocal
import datetime
import pytz

HORAS_TOMA_DATOS = (
    ("0000", "00:00"),
    ("0300", "3:00"),
    ("0630", "6:30"),
    ("0900", "9:00"),
    ("1200", "12:00"),
    ("1500", "15:00"),
    ("1700", "17:00"),
    ("1900", "19:00"),
)


class HistorialForm(forms.Form):
    fecha_hoy = datetime.datetime.utcnow()
    local_timezone = tzlocal.get_localzone()
    fecha_hoy = fecha_hoy.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    fecha_hoy = fecha_hoy.date()

    start_date = forms.DateField(
        widget=DateInput(attrs={'class': 'form-control', 'type': 'date', 'max': str(fecha_hoy), 'min': '2017-01-01'}),
        label="Fecha Inicial")
    start_time = forms.ChoiceField(choices=HORAS_TOMA_DATOS, label='Hora Inicial')

    end_date = forms.DateField(
        widget=DateInput(attrs={'class': 'form-control', 'type': 'date', 'max': str(fecha_hoy), 'min': '2017-01-01'}),
        label="Fecha Final")
    end_time = forms.ChoiceField(choices=HORAS_TOMA_DATOS, label='Hora Final')
