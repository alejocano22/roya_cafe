from django.shortcuts import render, redirect

from apps.finca.models import Finca
from apps.lote.models import Lote
from apps.finca.models import obtener_coordenadas
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required
from apps.finca.form import EditorForm
from apps.lote.models import Coordenada
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


def editor_view(request,id_finca):

    if request.method == "POST":
        form = EditorForm(request.POST)
        form.is_valid()
        jdata = form.cleaned_data['jsonfield']
        json_data = str(jdata )
        json_data = json.loads(json_data)
        for coordenada in json_data["datos"]:
            id_lote = int(coordenada["id"])
            lote = Lote.objects.get(id=id_lote)
            Coordenada.objects.create(lote=lote, x=coordenada["x"], y=coordenada["y"], width=coordenada["w"],height=coordenada["h"])

    form = EditorForm()
    context = {"finca": id_finca,"form":form}
    return render(request, "finca/editorMapa.html", context)
