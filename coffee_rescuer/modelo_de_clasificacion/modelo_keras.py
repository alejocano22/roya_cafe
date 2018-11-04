import numpy as np

np.random.seed(123)
from coffee_rescuer.celery import app
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
from os import listdir, walk
from os.path import join
from modelo_de_clasificacion.preprocesamiento import ProcesamientoDatos

RUTA_MODELO_GUARDADO = "modelo_de_clasificacion/modelo_construido.h5"  # El nombre del archivo que contendrá el modelo guardado


class ModeloDiagnostico:
    
    def _construir_modelo(self):
        model = Sequential()
        datos = ProcesamientoDatos()
        (X_train, y_train), (X_test, y_test) = datos._cargar_datos()
        X_train = X_train.reshape(X_train.shape[0], 224, 224, 3)
        X_test = X_test.reshape(X_test.shape[0], 224, 224, 3)

        X_train = X_train.astype('float32')
        X_test = X_test.astype('float32')
        X_train /= 255
        X_test /= 255

        # print(y_train[:10])
        Y_train = np_utils.to_categorical(y_train, 5)
        Y_test = np_utils.to_categorical(y_test, 5)
        # print(Y_train[:10])

        X_train = X_train[0:2000]
        Y_train = Y_train[0:2000]

        X_test = X_test[0:2000]
        Y_test = Y_test[0:2000]
        # print(X_train.shape)
        # print(Y_train.shape)

        model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
        model.add(Conv2D(32, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(5, activation='softmax'))

        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])

        model.fit(X_train, Y_train,
                  batch_size=32, epochs=5, verbose=1)

        score = model.evaluate(X_test, Y_test, verbose=0)
        print(score)
        print("%s: %.2f%%" % (model.metrics_names[1], score[1] * 100))

        model.save(RUTA_MODELO_GUARDADO)
        print("Modelo guardado correctamente")

    def _hacer_diagnostico(self, imgs_path):
        procesador = ProcesamientoDatos()
        path_imagenes = []
        for (path, ficheros, archivos) in walk(imgs_path):
            for elemento in listdir(path):
                full_path = join(path, elemento)
                if full_path.endswith(".png") or full_path.endswith(".jpg"):
                    path_imagenes.append(full_path)

        imagenes_procesadas = procesador._procesar_imagenes(path_imagenes)
        nuevo_modelo = self._cargar_modelo()

        predicciones = nuevo_modelo.predict(x=imagenes_procesadas)
        predicciones = np.argmax(predicciones, axis=1)
        return predicciones

    def _cargar_modelo(self):
        model = load_model(RUTA_MODELO_GUARDADO)
        
        
    def obtener_promedio_diagnostico(self, imgs_path):
        modelo = ModeloDiagnostico()
        y_pred = modelo._hacer_diagnostico(imgs_path)
        promedio = 0
        for y in y_pred:
            promedio += y
        promedio /= len(y_pred)
        return int(round(promedio))


# promedio = modelo.obtener_promedio_diagnostico("datos_train")
# print(promedio)
