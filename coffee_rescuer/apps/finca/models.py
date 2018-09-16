from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Finca(models.Model):
	nombre = models.CharField(null=True,blank=True, max_length=50)
	usuario = models.ForeignKey(User, on_delete = models.CASCADE)

	def obtener_correo_usuario(self):
		return self.usuario.email

	def obtener_username(self):
		return self.usuario.username

	def __str__(self):
		return self.nombre if self.nombre else self.id

