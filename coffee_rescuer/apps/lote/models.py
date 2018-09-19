from django.db import models
from apps.finca.models import Finca
from  django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import json
import os
from coffee_rescuer.settings import BASE_DIR
from datetime import datetime
# Create your models here.
ETAPA_ROYA =  (
		(0,"Etapa 0"),
		(1,"Etapa 1"),
		(2,"Etapa 2"),
		(3,"Etapa 3"),
		(4,"Etapa 4"),
	)

class Lote(models.Model):

	finca = models.ForeignKey(Finca,on_delete=models.CASCADE)
	nombre = models.CharField(max_length=50,null=True,blank=True)
	ultimo_estado_hongo = models.PositiveIntegerField(default=0,choices=ETAPA_ROYA)

	def obtener_detalle_lote_actual(self):
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

class DetalleLote(models.Model):

	etapa_hongo = models.PositiveIntegerField(default=0,choices=ETAPA_ROYA)
	lote = models.ForeignKey(Lote,on_delete=models.CASCADE)
	info_sensores = models.FilePathField(path=os.path.join(BASE_DIR,'data'),match='.*.json$',recursive=True,allow_files=True,unique=True)
	fotos = models.FilePathField(path=os.path.join(BASE_DIR,'data'),match='lot.*',recursive=True,allow_folders=True,allow_files=False,unique=True)
	
	def obtener_fecha_formato_python(self):
		fecha = self.obtener_fecha()
		day =  int(fecha[0:2])
		month = int(fecha[2:4])
		year = int(fecha[4:8])
		hour = int(fecha[8:10])
		minute = int(fecha[10:12])
		second = int(fecha[12:14])
		fecha_formato_python = datetime(year,month,day,hour,minute,second)
		return fecha_formato_python
	#Formato ddMMyyhhmmss
	def obtener_fecha(self):
		archivo = open(self.info_sensores)
		contenido_archivo = archivo.read()
		datos_json = json.loads(contenido_archivo)
		return datos_json['timestamp']

	def obtener_infosensores(self):
		archivo = open(self.info_sensores)
		contenido_archivo = archivo.read()
		datos_json = json.loads(contenido_archivo)
		return datos_json	

	def __str__(self):
		if self.lote.nombre:
			return self.lote.nombre + "-"  + self.obtener_fecha()
		return self.lote.id + "-" + self.obtener_fecha()

@receiver(post_save,sender=DetalleLote)
def post_save_Lote(sender,instance,**kwargs):
	
	fecha = instance.obtener_fecha_formato_python()
	detalle_lotes = DetalleLote.objects.filter(lote=instance.lote).order_by('id')
	es_detalle_actual = True
	for detalle_lote in detalle_lotes:
		fecha_aux = detalle_lote.obtener_fecha_formato_python()
		if fecha < fecha_aux:
			es_detalle_actual = False
			break

	if es_detalle_actual and instance.lote.ultimo_estado_hongo != instance.etapa_hongo:
		usuario = instance.lote.finca.usuario
		correo = usuario.email	
		nombre_finca  = instance.lote.finca.nombre
		
		if correo:
			mensaje = '{}{}{}{}{}{}'.format(
			'Usuario ', 
			usuario,
			'\nLe informamos que el estado de desarrollo del hongo de la roya en uno de sus lotes de la finca ',
			nombre_finca,
			' ha cambiado. Le recomendamos revisar la plataforma\n',
			fecha,
			)
			send_mail(
			'Notificación automática de CoffeeRescuer',
			mensaje,
			'coffeerescuer@gmail.com',
			[correo],
			fail_silently=False,
			)
		instance.lote.ultimo_estado_hongo = instance.etapa_hongo
		instance.lote.save()