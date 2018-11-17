from keras.preprocessing import image
from tqdm import tqdm
import numpy as np

import os
from os.path import join,exists


class ProcesamientoDatos:

    def preprocesar_detalle_lote(self, documento):
        """
        Preprocesa los datos de los sensores, las imágenes de las plantas y las imágenes multiespectrales del parámetro.
        Convierte las imágenes de las plantas y las imágenes multiespectrales en una lista de tensores 3d con shape
        (alto, ancho, 3), *************falta implementar el procesamiento a los datos de los sensores
        :param documento: Es un diccionario que contiene la informacion del archivo json de los datos de los sensores.
        :return: Una tupla de tres matrices dónde la primera matriz corresponde a los datos de los sensores procesados,
         el segundo las imágenes de las plantas procesadas, y el tercero las imágenes multiespectrales procesadas.
        """
        imgs_paths = []
        espectral_imgs_paths = []
        datos_sensores = {}
        for key in documento.keys():
            if key.startswith("plant"):  # Se revisan los paths de las imágenes que empiezan de esta forma
                imgs_paths.append(documento[key])
            elif key.startswith("re") or key.startswith("rgn"):
                espectral_imgs_paths.append(documento[key])
            elif not (key.startswith("_id") or key.startswith("timestamp") or key.startswith(
                    "owner_id") or key.startswith("farm_id") or key.startswith("lot_number")):
                datos_sensores[key] = documento[key]
        imgs_procesadas = None
        espectral_imgs_procesadas = None

        for img in imgs_paths:
            if img is None:
                imgs_paths.remove(img)
                continue
            if not exists(img): #Nos aseguramos que el archivo exista
                imgs_paths.remove(img)

        for img in espectral_imgs_paths:
            if img is None:
                imgs_paths.remove(img)
                continue
            if not exists(img):
                espectral_imgs_paths.remove(img)

        if imgs_paths:
            imgs_procesadas = self._procesar_imagenes(imgs_paths)
        if espectral_imgs_paths:
            espectral_imgs_procesadas = self._procesar_imagenes(espectral_imgs_paths, 4000, 3000)

        # Aquí se deberia agregar el codigo correspondiente para preprocesar los datos de los sensores

        return datos_sensores, imgs_procesadas, espectral_imgs_procesadas

    def _procesar_imagen(self, img_path, alto, ancho):
        """
        Este método permite procesar una imagen en el formato que requiere el modelo de machine learning.
        Es importante resaltar que este preprocesamiento no incluye procedimientos como la división de cada valor
        de cada pixel por 255.
        :param alto: El alto de la imagen objetivo
        :param ancho: El ancho de la imagen objetivo
        :param img_path: La direccion de la imagen
        :return: Un tensor 3d con shape (alto,ancho,3)
        """
        # loads RGB image as PIL.Image.Image type
        img = image.load_img(img_path, target_size=(alto, ancho))
        # convert PIL.Image.Image type to 3D tensor with shape (alto, ancho, 3)
        x = image.img_to_array(img)
        return np.expand_dims(x, axis=0)

    def _procesar_imagenes(self, img_paths, alto=224, ancho=224):
        """
         Este método permite procesar varias imagenes en el formato que requiere el modelo de machine learning
        :param alto: El alto de las imagenes objetivo
        :param ancho: El ancho de las imagenes objetivo
        :param img_paths: Una lista con las direcciones de las imagenes
        :return: Tensores apilados a nivel de filas. Ver np.vstack
        """
        list_of_tensors = [self._procesar_imagen(img_path, alto, ancho) for img_path in tqdm(img_paths)]
        return np.vstack(list_of_tensors)

    def _retornar_tupla_datos(self, dir_path):
        """
        Este método retorna los datos de entrenamiento o datos test preprocesados y con sus respectivos labels.
        Se vale de que hay 5 carpetas cada uno correspondiente al nombre de los 5 labels posibles(las posibles etapas
        del hongo de la roya) y cada foto la asocia con su correspondiente etapa
        :param dir_path: La direccion de la carpeta de los datos de entrenamiento o datos de test
        :return: Una dupla donde el primer elemento son todas las imágenes preprocesadas y el segundo todos los labels
        correspondientes.
        """
        path_imagenes = []
        labels = []
        for (path, ficheros, archivos) in os.walk(dir_path):
            for elemento in os.listdir(path):
                if join(path, elemento).lower().endswith(".jpeg") or join(path, elemento).endswith(".jpg"):
                    path_imagenes.append(join(path, elemento))
                    labels.append(int(path[-1]))
        x_set = self._procesar_imagenes(path_imagenes)
        labels = np.array(labels)
        return (x_set, labels)

    def _cargar_datos(self):
        """
        Este método se encarga de obtener una tupla con los datos de entrenamiento y de test ya preprocesados
        :return: Una tupla con los datos de entrenamiento y de test ya preprocesados
        """
        train = self._retornar_tupla_datos(join(os.path.dirname(os.path.abspath(__file__)), "datos_train"))
        test = self._retornar_tupla_datos(join(os.path.dirname(os.path.abspath(__file__)), "datos_test"))
        return (train, test)
