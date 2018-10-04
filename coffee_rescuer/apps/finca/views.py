
from django.shortcuts import render,redirect

from apps.finca.models import Finca
from apps.lote.models import Lote
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required
#import os
# Create your views here.


@login_required
def mapa_view(request,id_finca):
	try:
		finca = Finca.objects.get(id = id_finca)
	except Exception:
		return redirect('index')	
	if request.user.id != finca.usuario.id:
		return redirect('index')	

	lotes = Lote.objects.filter(finca = id_finca)
	coordenadas = finca.obtener_coordenadas(str(id_finca))
	etapas = {}
	for lote in lotes:
		detalle_lote_actual = lote.obtener_detalle_lote_actual()
		if detalle_lote_actual:
			etapas[lote.id]= detalle_lote_actual.etapa_hongo
		else:
			etapas[lote.id]=lote.ultimo_estado_hongo
	promedio_estado_lotes = 0
	for etapa in etapas.values():		
		promedio_estado_lotes += etapa
	promedio_estado_lotes = int(promedio_estado_lotes / len(etapas))
	context = {"promedio_estado_lotes": promedio_estado_lotes,"finca": finca, "lotes":serializers.serialize('json',lotes,fields=["id","nombre"]), "etapas": json.dumps(etapas),"coordenadas":json.dumps(coordenadas)}
	return render(request,"finca/mapa.html",context)



