from django.shortcuts import render


def mostrar_index(request):
    """
    Este método permite mostrar el index de la aplicación web
    @param request: La petición al servidor
    """
    return render(request, 'informacion/index.html')
