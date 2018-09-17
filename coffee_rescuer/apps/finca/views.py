
from django.shortcuts import render
from apps.finca.models import Finca
from apps.lote.models import Lote
import json
#import os
# Create your views here.



def mapa_view(request,id_finca):
	finca = Finca.objects.get(id = id_finca)
	lotes = Lote.objects.filter(finca = id_finca)
	coordenadas = finca.obtener_coordenadas(str(id_finca))
	detalles_lote = {}
	for lote in lotes:
		detalle_lote_actual = lote.obtener_detalle_lote_actual()
		if detalle_lote_actual:
			detalles_lote[lote.id]= detalle_lote_actual
		else:
			detalles_lote[lote.id]=lote.ultimo_estado_hongo
			
	context = {"finca": finca, "lotes":lotes, "detalles_lote": detalles_lote,"coordenadas":json.dumps(coordenadas)}
	return render(request,"finca/mapa.html",context)



