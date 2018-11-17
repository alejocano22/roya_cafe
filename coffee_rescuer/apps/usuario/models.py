from apps.lote import tasks
from datetime import datetime
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from coffee_rescuer.database_utilitys import Database
from apps.lote import models as models_lote
from apps.finca import models as models_finca
import os
from coffee_rescuer.celery import app
import pytz

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    celular = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.usuario.username


@app.task
def actualizar_info_usuario(username):
    """
    Este método permite actualizar los datos que pertenecen a un usuario
    :param username: El username del usuario al que se le actualizaran los datos
    """
    db = Database()
    usuario = User.objects.get(username=username)
    fincas = models_finca.Finca.objects.filter(usuario=usuario)
    for finca in fincas:
        lotes_finca_actual = models_lote.Lote.objects.filter(finca=finca.id)

        for lote in lotes_finca_actual:
            detalle_lote_actual = lote.obtener_detalle_lote_actual()

            if not detalle_lote_actual:
                fecha_inicial = datetime(2016, 1, 1)
            else:
                fecha_inicial = detalle_lote_actual.obtener_fecha_formato_python()
                fecha_inicial = fecha_inicial.replace(tzinfo=pytz.utc)
            new_lot_data = db.obtener_lot_data_usuario(username,lote.id, fecha_inicial)
            for detalle_lote in new_lot_data:
                usuario = str(detalle_lote["owner_id"])
                finca = str(detalle_lote["farm_id"])
                fecha  = detalle_lote["timestamp"].replace(tzinfo=pytz.utc)
                fecha = fecha.astimezone(pytz.timezone("America/Bogota"))
                day   = str(fecha.day)
                day   = darle_formato_str(day)
                month = str(fecha.month)
                month   = darle_formato_str(month)
                year  = str(fecha.year)
                year = darle_formato_str(year)
                hour  = str(fecha.hour)
                hour = darle_formato_str(hour)
                minute = str(fecha.minute)
                minute = darle_formato_str(minute)
                second = str(fecha.second)
                second = darle_formato_str(second)
                timestamp = day + month + year + hour + minute + second 
                lot_number = str(detalle_lote["lot_number"])
                path_sensores = os.path.join("data",usuario,finca,
                                              timestamp,"lot_" + lot_number,"lot_" + lot_number + ".json")
                
                if os.path.exists(path_sensores):
                    tasks.registrar_detalle_lote(lote.id, path_sensores)

    db.cerrar_conexion()

def darle_formato_str(string_fecha):
    if len(string_fecha) < 2:
        string_fecha  = "0" + string_fecha
    return string_fecha
