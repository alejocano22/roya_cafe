from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
	usuario = models.OneToOneField(User,on_delete=models.CASCADE)
	telefono = models.PositiveIntegerField(null=True)
	celular = models.PositiveIntegerField()
	
	