from django.shortcuts import render


def mostrar_index(request):
    """
    Este método permite mostrar el index de la aplicación web
    @param request: La petición al servidor
    """
    return render(request, 'informacion/index.html')

def mostrar_nosotros(request):
    """
    Este método permite mostrar el "sobre nosotros"  de la aplicación web
    @param request: La petición al servidor
    """
    return render(request, 'informacion/sobreNosotros.html')

def mostrar_galeria(request):
    """
    Este método permite mostrar la galería de la aplicación web
    @param request: La petición al servidor
    """
    return render(request, 'informacion/galeria.html')

def mostrar_contactanos(request):
    """
    Este método permite mostrar el "contactanos" de la aplicación web
    @param request: La petición al servidor
    """
    return render(request, 'informacion/contactanos.html')

