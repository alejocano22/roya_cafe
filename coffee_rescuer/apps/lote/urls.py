from django.urls import path,include
from apps.lote.views import vista_lote, historial_lote

app_name = 'lote'
urlpatterns = [
    path('<int:id_lote>/', vista_lote, name="vista_lote"),
    path('<int:id_lote>/historial_lote', historial_lote, name="historial_lote")
]
