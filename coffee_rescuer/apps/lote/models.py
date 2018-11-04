from apps.finca.models import Finca
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.lote.tasks import enviar_mail
import json
import os
from coffee_rescuer.settings import BASE_DIR
from datetime import datetime
import pytz
import tzlocal
from apps.lote.ETAPA_ROYA import ETAPA_ROYA
from apps.lote.formato_fecha import dar_formato_fecha
from django.db import models
from modelo_de_clasificacion.modelo_keras import ModeloDiagnostico

class Lote(models.Model):
    finca = models.ForeignKey(Finca, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, null=True, blank=True)
    ultimo_estado_hongo = models.PositiveIntegerField(default=0, choices=ETAPA_ROYA) #El estado del último detalle_lote

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
    etapa_hongo = models.PositiveIntegerField(default=0, choices=ETAPA_ROYA)
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
    info_sensores = models.FilePathField(path=os.path.join(BASE_DIR, ''), match='.*.json$', recursive=True,
                                         allow_files=True, unique=True)  # poner data
    fotos = models.FilePathField(path=os.path.join(BASE_DIR, ''), match='lot.*', recursive=True, allow_folders=True,
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


# Esto es el método que se debe descomentar para cuando se tenga el modelo listo con ese método implementado.
@receiver(pre_save, sender=DetalleLote)
def pre_save_Lote(sender, instance, **kwargs):
    modelo = ModeloDiagnostico()
    try:
        instance.etapa_hongo = modelo.obtener_promedio_diagnostico(imgs_path=instance.fotos)
        print("holi")
    except Exception as e:
        print(e)

@receiver(post_save, sender=DetalleLote)
def post_save_detalle_lote(sender, instance, **kwargs):
    """
    Este método se encargará de enviar un correo al usuario y actualizar la última etapa del hongo en la info del lote.

    Este método se ejecuta cuando se agrega o hay un cambio de un detalle de un lote y su objetivo es enviar un correo
    al usuario cuando este detalle es el más actual de todos, su etapa es mayor o igual a dos, cuando la etapa del
    hongo ha cambiado respecto a la última registrada en el lote y, finalmente, sólo si el usuario tiene registrado
    un correo.
    También, si un detalle es el más actual de todos se modifica el ultimo_estado_hongo en la informacion del lote
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

    if es_detalle_actual and instance.lote.ultimo_estado_hongo != instance.etapa_hongo:

        instance.lote.ultimo_estado_hongo = instance.etapa_hongo  # Actualización último_estado_hongo del lote

        instance.lote.save()
        usuario = instance.lote.finca.usuario
        correo = usuario.email
        nombre_finca = instance.lote.finca.nombre
        if correo and instance.etapa_hongo >= ETAPA_ROYA[2][0]:  # Se debe enviar el correo solo en etapa 2 o mayor
            if not nombre_finca:
                nombre_finca = "con id: " + str(instance.lote.finca.id)
            asunto = 'Notificación automática de Coffee Rescuer'
            mensaje = '{}{}{}{}{}{}{}'.format(
                'Usuario ',
                usuario,
                '\nLe informamos que el estado de desarrollo del hongo de la roya en uno de sus lotes de la finca ',
                nombre_finca,
                ' ha cambiado. Le recomendamos revisar la plataforma\n',
                dar_formato_fecha(fecha),
                " formato UTC"
            )

            enviar_mail.delay(asunto, mensaje, correo)


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
        detalle_lote_actual = lote.obtener_detalle_lote_actual()
        if detalle_lote_actual:
            promedio_estado_lotes += detalle_lote_actual.etapa_hongo
        else:
            promedio_estado_lotes += lote.ultimo_estado_hongo

    promedio_estado_lotes = int(promedio_estado_lotes / len(lotes))
    instance.finca.promedio_estado_lotes = promedio_estado_lotes
    instance.finca.save()
