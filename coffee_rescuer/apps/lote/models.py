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

class Lote(models.Model):

	finca = models.ForeignKey(Finca,on_delete=models.CASCADE)
	nombre = models.CharField(max_length=50,null=True,blank=True)
	def obtener_nombre_finca(self):
		return self.finca.nombre
	def obtener_correo_usuario(self):
		return self.finca.obtener_correo_usuario()

	def obtener_username(self):
		return self.finca.obtener_username()

	def __str__(self):
		return self.nombre if self.nombre else self.id

class DetalleLote(models.Model):
	ETAPA_ROYA =  (
		(0,"Etapa 0"),
		(1,"Etapa 1"),
		(2,"Etapa 2"),
		(3,"Etapa 3"),
	)

	etapa_hongo = models.PositiveIntegerField(default=0,choices=ETAPA_ROYA)
	lote = models.ForeignKey(Lote,on_delete=models.CASCADE)
	info_sensores = models.FilePathField(path=os.path.join(BASE_DIR,'data'),match='.*.json$',recursive=True,allow_files=True,unique=True)
	fotos = models.FilePathField(path=os.path.join(BASE_DIR,'data'),match='lot.*',recursive=True,allow_folders=True,allow_files=False,unique=True)
	
	def obtener_fecha(self):
		archivo = open(self.info_sensores)
		contenido_archivo = archivo.read()
		datos_json = json.loads(contenido_archivo)
		return datos_json['timestamp']

	def __str__(self):
		if self.lote.nombre:
			return self.lote.nombre + "-"  + self.obtener_fecha()
		return self.lote.id + "-" + self.obtener_fecha()

@receiver(post_save,sender=DetalleLote)
def post_save_Lote(sender,instance,**kwargs):
	usuario = instance.lote.obtener_username()
	correo = instance.lote.obtener_correo_usuario()
	fecha = instance.obtener_fecha()
	day =  int(fecha[0:2])
	month = int(fecha[2:4])
	year = int(fecha[4:8])
	hour = int(fecha[8:10])
	minute = int(fecha[10:12])
	second = int(fecha[12:14])
	if instance.etapa_hongo >= 2 and correo and kwargs['created']:
		mensaje = '{}{}{}{}{}{}'.format(
		'Usuario ', 
		usuario,
		'\nLe informamos que el estado de desarrollo del hongo de la roya en uno de sus lotes de la finca ',
		instance.lote.obtener_nombre_finca(),
		' ha aumentado. Le recomendamos revisar la plataforma\n',
		datetime(year,month,day,hour,minute,second),
		)
		send_mail(
		'Notificación automática de CoffeeRescuer',
		mensaje,
		'coffeerescuer@gmail.com',
		[correo],
		fail_silently=False,
		)