from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PerfilUsuario(models.Model):
	usuario = models.OneToOneField(User,on_delete=models.CASCADE)
	telefono = models.PositiveIntegerField(null=True)
	celular = models.PositiveIntegerField()
	
	
	def __str__(self):
		return self.usuario.username