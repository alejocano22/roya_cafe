from django.shortcuts import render,redirect
from apps.lote.models import Lote, DetalleLote
from apps.lote.form import HistorialForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
import tzlocal
import pytz
# Create your views here.
@login_required
def vista_lote(request,id_lote):
	try:
		lote = Lote.objects.get(id = id_lote)
	except Exception:
		return redirect('index')
	if request.user.id != lote.finca.usuario.id:
		return redirect('index')
	detalle_lote = lote.obtener_detalle_lote_actual()
	if detalle_lote:
		info_sensores = detalle_lote.obtener_info_sensores()
		context = {"info_sensores":info_sensores, "lote":lote, "etapa_hongo": detalle_lote.etapa_hongo}
	else:
		messages.info(request, "No hay información sobre este lote")
		context = {"lote":lote}
	return render(request,"lote/vistaLote.html",context)

@login_required
def historial_lote(request, id_lote):
	try:
		lote = Lote.objects.get(id = id_lote)
	except Exception:
		return redirect('index')
	if request.user.id != lote.finca.usuario.id:
		return redirect('index')

	historial = []
	if request.method == "POST":
		form = HistorialForm(request.POST)
		if form.is_valid():
			start_date = form.cleaned_data['start_date']
			start_time= form.cleaned_data['start_time']
			end_date = form.cleaned_data['end_date']
			end_time = form.cleaned_data['end_time']

			start_formato_python = datetime(
				start_date.year,
				start_date.month,
				start_date.day,
				int(start_time[0:2]),
				int(start_time[2:]),
				)

			end_formato_python = datetime(
				end_date.year,
				end_date.month,
				end_date.day,
				int(end_time[0:2]),
				int(end_time[2:]),
				)

			if start_formato_python > end_formato_python:
				messages.info(request, "La fecha inicial debe ser menor o igual a la fecha final")
			else:
				historial = lote.obtener_detalle_rango(start_formato_python.astimezone(pytz.utc), end_formato_python.astimezone(pytz.utc))
				context = {"lote":lote, "historial": historial,"form":form}
				return render(request, 'lote/historialDatos.html',context)

	else:
		form = HistorialForm()
	
	detalle_lotes = DetalleLote.objects.filter(lote=lote).order_by('id')
	for detalle in detalle_lotes:
		detalle_sensores = detalle.obtener_info_sensores()
		etapa = detalle.etapa_hongo

		detalle_sensores['timestamp'] = detalle.obtener_fecha_formato_python()
		local_timezone = tzlocal.get_localzone()

		detalle_sensores['time'] = detalle_sensores['timestamp'].replace(tzinfo=pytz.utc).astimezone(local_timezone)
		detalle_sensores['time'] = detalle_sensores['time'].replace(tzinfo = None)
		print("soy timestamp" , detalle_sensores['timestamp'])
		print("soy time" , detalle_sensores['time'])
		detalle_sensores['etapa'] = etapa
		historial.append(detalle_sensores)

	context = {"lote":lote, "historial": historial,"form":form}
	return render(request, 'lote/historialDatos.html',context)
