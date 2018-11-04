from keras.preprocessing import image
from tqdm import tqdm
import numpy as np

import os
from os.path import join


class ProcesamientoDatos:

    def _procesar_imagen(self, img_path):

        # loads RGB image as PIL.Image.Image type
        img = image.load_img(img_path, target_size=(224, 224))
        # convert PIL.Image.Image type to 3D tensor with shape (224, 224, 3)
        x = image.img_to_array(img)
        return np.expand_dims(x, axis=0)

    def _procesar_imagenes(self, img_paths):
        list_of_tensors = [self._procesar_imagen(img_path) for img_path in tqdm(img_paths)]
        return np.vstack(list_of_tensors)

    def _retornar_tupla_datos(self, dir_path):
        path_imagenes = []
        labels = []
        for (path, ficheros, archivos) in os.walk(dir_path):
            for elemento in os.listdir(path):
                if join(path, elemento).endswith(".png") or join(path, elemento).endswith(".jpg"):
                    path_imagenes.append(join(path, elemento))
                    labels.append(int(path[-1]))
        x_set = self._procesar_imagenes(path_imagenes)
        labels = np.array(labels)
        return (x_set, labels)

    def _cargar_datos(self):
        train = self._retornar_tupla_datos(join(os.path.dirname(os.path.abspath(__file__)), "datos_train"))
        test = self._retornar_tupla_datos(join(os.path.dirname(os.path.abspath(__file__)), "datos_test"))
        return (train, test)
