from apps.lote import tasks
from datetime import datetime
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from coffee_rescuer.database_utilitys import Database
from apps.lote.models import Lote
from apps.finca.models import Finca
from coffee_rescuer.settings import BASE_DIR
import os
import json
from coffee_rescuer.celery import app


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    celular = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.usuario.username

#@app.task descomentar si se va a usar celery, tambien descomentar en usuario views
def actualizar_info_usuario(id_usuario):
    """
    Este método permite actualizar los datos que pertenecen a un usuario
    :param id_usuario: El id del usuario al que se le actualizaran los datos
    """
    db = Database()
    fincas = Finca.objects.filter(usuario=id_usuario)
    lotes_usuario = []
    for finca in fincas:
        lotes_finca_actual = Lote.objects.filter(finca=finca.id)
        for lote in lotes_finca_actual:
            detalle_lote_actual = lote.obtener_detalle_lote_actual()
            fecha_inicial = detalle_lote_actual.obtener_fecha_formato_python()
            new_lot_data = db.obtener_lot_data_usuario(id_usuario,fecha_inicial)
            for detalle_lote in new_lot_data:
                path_fotos = detalle_lote["plant_1"]
                path_fotos = os.path.dirname(path_fotos)
                path_sensores = os.path.join(path_fotos, os.path.basename(path_fotos) +".json")
                tasks.registrar_detalle_lote(lote.id,path_sensores git,path_fotos)
    db.cerrar_conexion()





