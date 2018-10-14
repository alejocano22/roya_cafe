from django.shortcuts import render, redirect

from apps.finca.models import Finca
from apps.lote.models import Lote
from apps.finca.models import obtener_coordenadas
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
def mapa_view(request, id_finca):
    """
    Este método permite mostrar la información de la página que contiene el mapa de la finca
    @param request: La petición al servidor
    @param id_finca:  El id de la finca de la que se mostrará el mapa
    """
    try:
        finca = Finca.objects.get(id=id_finca)
    except Exception:
        return redirect('index')
    if request.user.id != finca.usuario.id:
        return redirect('index')

    lotes = Lote.objects.filter(finca=id_finca)
    coordenadas = obtener_coordenadas(id_finca)
    etapas = {}
    for lote in lotes:
        detalle_lote_actual = lote.obtener_detalle_lote_actual()
        if detalle_lote_actual:
            etapas[lote.id] = detalle_lote_actual.etapa_hongo
        else:
            etapas[lote.id] = lote.ultimo_estado_hongo

    context = {"finca": finca,
               "lotes": serializers.serialize('json', lotes, fields=["id", "nombre"]),
               "etapas": json.dumps(etapas),
               "coordenadas": json.dumps(coordenadas)
               }
    return render(request, "finca/mapa.html", context)
