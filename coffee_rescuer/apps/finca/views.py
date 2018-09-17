
from django.shortcuts import render
from apps.finca.models import Finca
from apps.lote.models import DetalleLote, Lote
import json
#import os
# Create your views here.



def mapa_view(request,id_finca):
	finca = Finca.objects.get(id = id_finca)
	lotes = Lote.objects.filter(finca = id_finca)
	lista = finca.obtener_coordenadas("2")
	detalle_lote = {}
	for x in lotes:
		lista_objetos = DetalleLote.objects.filter(lote = x.id)
		detalle_lote[x.id]=lista_objetos
	context = {"finca": finca, "lotes":lotes, "detalle_lote": detalle_lote,"coordenadas":json.dumps(lista)}
	return render(request,"finca/mapa.html",context)



