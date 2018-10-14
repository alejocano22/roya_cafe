from django.core import serializers
from django.db import models
from django.contrib.auth.models import User
from coffee_rescuer.settings import BASE_DIR
from django.apps import apps
import os


# Create your models here.
ETAPA_ROYA = (
    (0, "Etapa 0"),
    (1, "Etapa 1"),
    (2, "Etapa 2"),
    (3, "Etapa 3"),
    (4, "Etapa 4"),
)


class Finca(models.Model):

    def __str__(self):
        return self.nombre if self.nombre else str(self.id)

    nombre = models.CharField(null=True, blank=True, max_length=50)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    archivo_coordenadas = models.FilePathField(path=os.path.join(BASE_DIR, 'data'), match='coordenadas.json',
                                               recursive=True, allow_files=True, unique=True)
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

