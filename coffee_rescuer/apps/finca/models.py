from django.db import models
from django.contrib.auth.models import User
from coffee_rescuer.settings import BASE_DIR
import os
import json
# Create your models here.

class Finca(models.Model):

	def __str__(self):
		return self.nombre if self.nombre else str(self.id)

	nombre = models.CharField(null=True,blank=True, max_length=50)
	usuario = models.ForeignKey(User, on_delete = models.CASCADE)
	archivo_coordenadas = models.FilePathField(path=os.path.join(BASE_DIR,'data'),match='coordenadas.json',recursive=True,allow_files=True,unique=True)
	
	def obtener_coordenadas(self,id_lote):
		archivo = open(self.archivo_coordenadas)
		contenido_archivo = archivo.read()
		datos_json = json.loads(contenido_archivo)
		return datos_json[id_lote]