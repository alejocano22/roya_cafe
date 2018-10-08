
from django.urls import path
from apps.usuario.views import fincas_listar

app_name = "usuario"
urlpatterns = [
    path('',fincas_listar,name="fincas_listar"), 
    
]