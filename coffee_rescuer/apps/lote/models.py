from django.db import models
from apps.finca.models import Finca
from  django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail


# Create your models here.

class Lote(models.Model):
	ETAPA_ROYA =  (
		(0,"Etapa 0"),
		(1,"Etapa 1"),
		(2,"Etapa 2"),
		(3,"Etapa 3")
		)
	finca = models.ForeignKey(Finca,on_delete=models.CASCADE)
	nombre = models.CharField(max_length=50,null=True,blank=True)
	etapa_hongo = models.PositiveIntegerField(default=0,choices=ETAPA_ROYA)

@receiver(post_save,sender=Lote)
def post_save_Lote(sender,instance,**kwargs):
	usuario = instance.finca.obtener_username()
	correo = instance.finca.obtener_correo_usuario()
	if instance.etapa_hongo >= 2 and correo:
		mensaje = '{}{}{}{}{}'.format(
		'Usuario ', 
		usuario,
		'\nLe informamos que el estado de desarrollo del hongo de la roya en uno de sus lotes de la finca ',
		instance.finca.nombre,
		' ha aumentado. Le recomendamos revisar la plataforma'
		)
		send_mail(
		'Notificación automática de CoffeeRescuer',
		mensaje,
		'coffeerescuer@gmail.com',
		[correo],
		fail_silently=False,
		)