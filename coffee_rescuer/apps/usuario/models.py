from apps.lote import tasks
from datetime import datetime
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from coffee_rescuer.database_utilitys import Database
from apps.lote import models as models_lote
from apps.finca import models as models_finca
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
    usuario = User.objects.get(id=id_usuario)
    fincas = models_finca.Finca.objects.filter(usuario=usuario)
    print("usuario ",usuario)
    print("fincas ", fincas)
    lotes_usuario = []
    for finca in fincas:
        lotes_finca_actual = models_lote.Lote.objects.filter(finca=finca.id)
        
        for lote in lotes_finca_actual:
            detalle_lote_actual = lote.obtener_detalle_lote_actual()
            
            if not detalle_lote_actual:
                fecha_inicial = datetime(2016,1,1)
            else:
                fecha_inicial = detalle_lote_actual.obtener_fecha_formato_python()
            print(fecha_inicial)
            new_lot_data = db.obtener_lot_data_usuario(int(usuario.username),fecha_inicial)
            for detalle_lote in new_lot_data:
                try:
                    path_fotos = detalle_lote["plant_1"]
                    path_fotos = os.path.dirname(path_fotos)
                    path_sensores = os.path.join(path_fotos, os.path.basename(path_fotos) +".json")
                    tasks.registrar_detalle_lote(lote.id,path_sensores,path_fotos)
                except:
                    pass
    db.cerrar_conexion()





