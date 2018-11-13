from apps.finca.models import Finca
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.lote.tasks import enviar_mail
import json
import os
from coffee_rescuer.settings import BASE_DIR
from coffee_rescuer.celery import app
from datetime import datetime
import pytz
import tzlocal
from apps.lote.ETAPA_ROYA import ETAPA_ROYA
from apps.lote.formato_fecha import dar_formato_fecha
from django.db import models
from coffee_rescuer.views import predict_document



class Lote(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, null=True, blank=True)
    ultimo_estado_hongo = models.PositiveIntegerField(default=0,
                                                      choices=ETAPA_ROYA)  # El estado del último detalle_lote

    def obtener_detalle_desde(self, start):
        """
        Permite obtener todos los detalles de un lote desde una fecha especifica
        :param start: Fecha inicial del rango en datetime
        :return: Retorna una lista con diccionarios que contienen información de cada detalle de lote
        """
        detalle_lotes = DetalleLote.objects.filter(lote=self.id).order_by('id')
        registros = []
        for detalle_lote in detalle_lotes:
            fecha_actual = detalle_lote.obtener_fecha_formato_python()
            fecha_actual = fecha_actual.replace(tzinfo=None)
            if start <= fecha_actual:
                detalle_sensores = detalle_lote.obtener_info_sensores()
                registros.append(detalle_sensores)
        return registros

    def obtener_detalle_rango(self, start, end):
        """
        Permite obtener todos los detalles de un lote entre dos fechas especificas.
        Es importante entender que agrega a la informacion de cada detalle de lote dos fechas, el timestamp que es la
        fecha en UTC y en la fecha que se calcule del lugar donde accede el usuario. Además la fecha se formatea usando
        el siguiente formato: "dd 'de' MMMM 'de' yyyy 'a las' HH:mm:ss" usando los estándares de la libreria babel.
        También le agrega la etapa del hongo a cada una. Toda esta informacion se utiliza en la vista.
        @param start: Fecha inicial del rango en datetime
        @param end: Fecha final del rango en datetime
        @return: Retorna una lista con diccionarios que contienen información de cada detalle de lote
        """

        detalle_lotes = DetalleLote.objects.filter(lote=self.id).order_by('id')
        registros = []
        for detalle_lote in detalle_lotes:

            fecha_actual = detalle_lote.obtener_fecha_formato_python()
            if start <= fecha_actual <= end:
                detalle_sensores = detalle_lote.obtener_info_sensores()
                etapa = detalle_lote.etapa_hongo
                detalle_sensores['etapa'] = etapa

                detalle_sensores['timestamp'] = detalle_lote.obtener_fecha_formato_python()
                local_timezone = tzlocal.get_localzone()
                detalle_sensores['time'] = detalle_sensores['timestamp'].astimezone(local_timezone)
                detalle_sensores['time'] = detalle_sensores['time'].replace(tzinfo=None)

                registros.append(detalle_sensores)

        return registros

    def obtener_detalle_lote_actual(self):
        """
        Este método obtiene el detalle de un lote más actual que se encuentre en el sistema.
        @return: Un objeto tipo DetalleLote.
        """
        detalle_lotes = DetalleLote.objects.filter(lote=self.id).order_by('id')
        if len(detalle_lotes) == 0:
            return None
        detalle_lote_actual = detalle_lotes[0]
        fecha_mas_actual = detalle_lote_actual.obtener_fecha_formato_python()
        for detalle_lote in detalle_lotes:
            fecha = detalle_lote.obtener_fecha_formato_python()
            if fecha > fecha_mas_actual:
                detalle_lote_actual = detalle_lote
                fecha_mas_actual = fecha
        return detalle_lote_actual

    def __str__(self):
        return self.nombre if self.nombre else str(self.id)


class Coordenada(models.Model):
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()


class DetalleLote(models.Model):
    """
    Debido a que un mismo lote puede tener distintas fotos, informacion de sensores, y etapas del hongo en el tiempo
    el objetivo de esta clase es contener toda esta informacion de un mismo lote en cierta fecha definida en el
    timestamp de info_sensores
    """
    etapa_hongo = models.PositiveIntegerField(default=0, choices=ETAPA_ROYA)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    info_sensores = models.FilePathField(path=os.path.join(BASE_DIR, 'data'), match='.*.json$', recursive=True,
                                         allow_files=True, unique=True)  # poner data
    fotos = models.FilePathField(path=os.path.join(BASE_DIR, 'data'), match='lot_.*', recursive=True, allow_folders=True,
                                 allow_files=False, unique=True)

    def obtener_fecha_formato_python(self):
        """
        Este método obtiene la fecha del detalle de un lote que esta en utc y lo transforma a un objeto tipo datetime con tzinfo utc.
        @return: La fecha del detalle de un lote en un objeto datetime
        """
        fecha = self.obtener_fecha()
        day = int(fecha[0:2])
        month = int(fecha[2:4])
        year = int(fecha[4:8])
        hour = int(fecha[8:10])
        minute = int(fecha[10:12])
        second = int(fecha[12:14])
        fecha_formato_python = datetime(year, month, day, hour, minute, second, tzinfo=pytz.utc)
        return fecha_formato_python

    def obtener_fecha(self):
        """
        Obtiene la fecha del detalle de un lote en formato ddMMyyhhmmss.
        @return: La fecha del detalle de un lote en un string
        """
        archivo = open(self.info_sensores)
        contenido_archivo = archivo.read()
        archivo.close()
        datos_json = json.loads(contenido_archivo)
        return datos_json['timestamp']

    def obtener_info_sensores(self):
        """
        Obtiene un diccionario con la información de los sensores del detalle de lote
        :return: Un diccionario que se obtiene luego de parsear el archivo que contiene la información de los sensores
        """
        archivo = open(self.info_sensores)
        contenido_archivo = archivo.read()
        datos_json = json.loads(contenido_archivo)
        return datos_json

    def __str__(self):
        if self.lote.nombre:
            return self.lote.nombre + "-" + self.obtener_fecha()
        return str(self.lote.id) + "-" + self.obtener_fecha()


@app.task
def actualizar_etapa_detalle_lote(id_detalle_lote):
    """
    Se encarga de usar el modelo de diagnostico para actualizar la etapa del hongo de la roya de un detalle_lote.
    Si el ultimo_estado_hongo de un lote es distinto a la etapa diagnosticada aqui se actualizará y
    tambien se enviará un correo si la etapa diagnosticada aqui es igual a 2 o mayor y el usuario tiene correo
    :param id_detalle_lote: detalle_lote a actualizar
    """
    try:
        detalle_lote = DetalleLote.objects.get(id=id_detalle_lote)
        archivo = open(detalle_lote.info_sensores)
        contenido_archivo = archivo.read()
        archivo.close()
        documento = json.loads(contenido_archivo)
        result_task = predict_document.delay(documento)
        etapa_hongo = int(result_task.get(disable_sync_subtasks=False))
        DetalleLote.objects.filter(id=id_detalle_lote).update(etapa_hongo=etapa_hongo)

        usuario = detalle_lote.lote.finca.usuario
        correo = usuario.email
        nombre_finca = detalle_lote.lote.finca.nombre
        nombre_lote  = detalle_lote.lote.nombre
        if detalle_lote.lote.ultimo_estado_hongo != etapa_hongo:
            detalle_lote.lote.ultimo_estado_hongo = etapa_hongo  # Actualización último_estado_hongo del lote
            detalle_lote.lote.save()
            if correo and etapa_hongo >= ETAPA_ROYA[2][0]:  # Se debe enviar el correo solo en etapa 2 o mayor
                if not nombre_finca:
                    nombre_finca = "con id: " + str(detalle_lote.lote.finca.id)
                if not nombre_lote:
                    nombre_lote = "con id: " + str(detalle_lote.lote.id)
                asunto = 'Notificación automática de Coffee Rescuer'
                fecha = detalle_lote.obtener_fecha_formato_python()
                mensaje = __construir_mensaje(nombre_finca, nombre_lote,usuario, fecha)
                enviar_mail.delay(asunto, mensaje, correo)
    except Exception as e:
        print("Ha ocurrido un error:", e)


def __construir_mensaje(finca, lote, usuario, fecha):
    """
    Se encarga de construir el mensaje de notificación para un usuario
    :param finca: La finca que requiere la atención del usuario
    :param lote: El lote que requiere la atención del usuario
    :param usuario: El username del usuario
    :param fecha: La fecha en la que se tomaron los datos
    :return: un string con el mensaje construido
    """
    mensaje = '{}{}{}{}{}{}{}{}{}'.format(
        'Usuario ',
        usuario,
        '\nLe informamos que el estado de desarrollo del hongo de la roya en el lote ',
        lote,
        ' de la finca ',
        finca,
        ' ha cambiado. Le recomendamos revisar la plataforma\n',
        dar_formato_fecha(fecha),
        " formato UTC"
    )
    return mensaje


@receiver(post_save, sender=DetalleLote)
def post_save_detalle_lote(sender, instance, **kwargs):
    """
    Se ejecuta cuando se agrega o hay un cambio de un detalle de un lote y su objetivo es actualizar su etapa del hongo
    Sólo actualiza la etapa del hongo si este detalle es el último de todos.
    @param sender: Este parámetro especifica cuál modelo es el responsable porque se ejecute este método, en este caso
    DetalleLote
    @param instance: El detalle de lote que se ha agregado o cambiado en la base de datos
    """

    fecha = instance.obtener_fecha_formato_python()
    detalle_lotes = DetalleLote.objects.filter(lote=instance.lote).order_by('id')
    es_detalle_actual = True
    for detalle_lote in detalle_lotes:
        fecha_aux = detalle_lote.obtener_fecha_formato_python()
        if fecha < fecha_aux:
            es_detalle_actual = False
            break

    if es_detalle_actual:
        actualizar_etapa_detalle_lote.delay(instance.id)


@receiver(post_save, sender=Lote)
def post_save_lote(sender, instance, **kwargs):
    """
    Este método se encargará de modificar el promedio del estado de los lotes de una finca.

    Este método se ejecuta cuando se agrega o hay un cambio de un lote y su objetivo es modificar el promedio del
    estado del hongo de la roya en los lotes de una finca.
    @param sender: Este parámetro especifica cuál modelo es el responsable porque se ejecute este método, en este caso
    Lote
    @param instance: El lote que se ha agregado o cambiado en la base de datos
    """
    lotes = Lote.objects.filter(finca=instance.finca)
    
    promedio_estado_lotes = 0
    for lote in lotes:
        promedio_estado_lotes += lote.ultimo_estado_hongo

    promedio_estado_lotes = int(round(promedio_estado_lotes / len(lotes)))
    instance.finca.promedio_estado_lotes = promedio_estado_lotes
    instance.finca.save()
