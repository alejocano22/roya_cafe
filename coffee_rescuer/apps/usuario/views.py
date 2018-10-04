from django.shortcuts import render,redirect
from apps.finca.models import Finca
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def fincas_listar(request):
	if request.user.is_staff:
		return redirect('admin:index')
	fincas = Finca.objects.filter(usuario= request.user.id)
	contexto = {"fincas":fincas}
	return render(request,"usuario/fincas.html",contexto)

