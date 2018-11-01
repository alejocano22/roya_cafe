from apps.lote import tasks
from datetime import datetime
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
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
def actualizar_info_usuario(username):
    """
    Este método permite actualizar los datos que pertenecen a un usuario
    :param username: El username del usuario al que se le actualizaran los datos
    """
    for (path, ficheros, archivos) in os.walk(os.path.join(BASE_DIR, "data-example", username)):
        fecha_inicial_analisis = datetime.today() - timedelta(days=365)

        if os.path.basename(path).startswith("finca"):
            for fichero in ficheros:

                day = int(fichero[0:2])
                month = int(fichero[2:4])
                year = int(fichero[4:8])
                hour = int(fichero[8:10])
                minute = int(fichero[10:12])
                second = int(fichero[12:14])
                fecha_formato_python = datetime(year, month, day, hour, minute, second)

                if fecha_formato_python > fecha_inicial_analisis:
                    for elemento in os.listdir(os.path.join(path, fichero)):
                        path_archivo = os.path.join(path, fichero, elemento, elemento + ".json")
                        archivo = open(path_archivo)
                        contenido_archivo = archivo.read()
                        archivo.close()
                        datos_json = json.loads(contenido_archivo)
                        tasks.registrar_detalle_lote(fecha_inicial_busqueda=fecha_inicial_analisis,
                                                           datos_json=datos_json,
                                                           path_info_sensores=os.path.join(os.path.dirname(path_archivo),
                                                                        os.path.basename(path_archivo)),
                                                           path_fotos=os.path.join(os.path.dirname(path_archivo))
                                                           )
