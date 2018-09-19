from django.shortcuts import render
from apps.lote.models import Lote
from django.core import serializers
import json
#import os
# Create your views here.



def vista_lote(request,id_lote):
	lote = Lote.objects.get(id = id_lote)
	detalle_lote = lote.obtener_detalle_lote_actual()

	info_sensores = detalle_lote.obtener_infosensores()

	context = {"info_sensores":info_sensores, "lote":lote, "etapa_hongo": detalle_lote.etapa_hongo}
	return render(request,"lote/vistaLote.html",context)
