from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, null=True,blank=True)
    celular = models.CharField(max_length=20, null=True,blank=True)

    def __str__(self):
        return self.usuario.username
