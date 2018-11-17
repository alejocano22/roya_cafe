import json
from django.shortcuts import render
from coffee_rescuer.settings import BASE_DIR
from modelo_de_clasificacion.preprocesamiento import ProcesamientoDatos
from modelo_de_clasificacion import modelo_keras
from coffee_rescuer.celery import app
from os import walk
from os.path import join,basename,exists
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
def predict(request):
    """
    Permite utilizar un endpoint /predict para que se consuma un servicio de prediccion utilizando el modelo de keras.
    Funciona como un servicio, permite que a través de una petición post y enviando la dirección de una
    carpeta (por ejemplo coffee_leaf_rust_diagnosis/data/1152448911/1/11112018112233/) por medio del body, se haga
    una evaluación del modelo de machine learning y se retorne la evaluación en un documento json
    :param request: La petición al servidor
    :return: Un objeto de HttpResponse con un json que contiene la información de cada lote con su respectiva etapa del
    hongo
    """
    result_json = {}
    if request.method == 'POST':
         info_request = json.loads(request.body)
         path_timestamp_folder = info_request["data"]
         #Ignoramos coffee_leaf_rust_diagnosis porque lo que tenemos es un acceso directo a data
         path_timestamp_folder = path_timestamp_folder[len("coffee_leaf_rust_diagnosis//")-1:]
         path_timestamp_folder = join(BASE_DIR, path_timestamp_folder)
         for (path, ficheros, archivos) in walk(path_timestamp_folder):
            for archivo in archivos:
                if archivo.startswith("lot_") and archivo.endswith(".json"):
                    full_path = join(path, archivo)
                    archivo = open(full_path)
                    contenido_archivo = archivo.read()
                    archivo.close()
                    documento =  json.loads(contenido_archivo)
                    result_task = predict_document.delay(documento=documento)
                    etapa_hongo = int(result_task.get(disable_sync_subtasks=False))
                    documento["development_stage"] = etapa_hongo
                    result_json[basename(path)] = documento
    return HttpResponse(json.dumps(result_json), content_type='application/json')


@app.task
def predict_document(documento):
    """
    Retorna el promedio de la clasificación del hongo roya a partir del análisis de imágenes de las plantas de un lote.
    Se encarga de usar la información en el documento json, para llamar a los métodos que realizan el procesamiento de
    la imágenes y la evaluación de las mismas en el modelo de machine learning.
    :param documento: Es un diccionario que contiene la informacion del archivo json de los datos de los sensores.
    :return: Un entero que es el promedio del estado del hongo de la roya en ese lote.
    """
    procesador = ProcesamientoDatos()
    input = procesador.preprocesar_detalle_lote(documento)
    promedio_prediccion_imagenes = modelo_keras.hacer_diagnostico(input)
    return int(round(promedio_prediccion_imagenes))

