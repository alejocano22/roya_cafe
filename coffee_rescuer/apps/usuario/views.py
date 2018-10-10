from django.shortcuts import render, redirect
from apps.finca.models import Finca
from django.contrib.auth.decorators import login_required
from django.core import serializers

# Create your views here.
@login_required
def fincas_listar(request):
    """
    Este método permite mostrar la información de la página que contiene las fincas de un usuario.
    @param request: La petición al servidor
    """
    if request.user.is_staff:
        return redirect('admin:index')
    fincas = Finca.objects.filter(usuario=request.user.id)
    contexto = {"fincas": fincas}
    return render(request, "usuario/fincas.html", contexto)
