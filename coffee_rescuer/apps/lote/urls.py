from django.urls import path,include
from apps.lote.views import vista_lote
app_name = 'lote'
urlpatterns = [
    path('<int:id_lote>/', vista_lote, name="vista_lote")
]
