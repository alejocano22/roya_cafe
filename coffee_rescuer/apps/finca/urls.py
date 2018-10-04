from django.urls import path
from apps.finca.views import mapa_view

app_name = "finca"
urlpatterns = [
    path('<int:id_finca>/',mapa_view,name="mapa"), 
]