from django.core import serializers
from django.db import models
from django.contrib.auth.models import User
from coffee_rescuer.settings import BASE_DIR
from django.apps import apps
import os
from apps.lote.ETAPA_ROYA import ETAPA_ROYA

# Create your models here.

class Finca(models.Model):

    def __str__(self):
        return self.nombre if self.nombre else str(self.id)

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(null=True, blank=True, max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    promedio_estado_lotes = models.PositiveIntegerField(default=0, choices=ETAPA_ROYA)


def obtener_coordenadas(id_finca):
    Lote = apps.get_model('lote', 'Lote')
    Coordenada = apps.get_model('lote', 'Coordenada')
    """
    Este método permite obtener las coordenadas de los lotes de una finca para pintarlos en el mapa.
    @param id_finca: El numero de identificación de la finca
    @return: Un diccionario con las coordenadas (x,y) de los lotes y su tamano, width y height (w,h)
    """
    lotes = Lote.objects.filter(finca=id_finca)
    coordenadas = {}
    for lote in lotes:
        try:
            coordenada = Coordenada.objects.get(lote=lote)
            coordenada = {"x": coordenada.x,"y": coordenada.y, "w": coordenada.width, "h": coordenada.height}
            coordenadas[lote.id] = coordenada
        except Exception as e:
            print(e,"nalga")

    return coordenadas

