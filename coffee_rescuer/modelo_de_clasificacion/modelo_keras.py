import numpy as np

np.random.seed(123)
from coffee_rescuer.celery import app
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
from os import listdir, walk
from os.path import join, exists
from shutil import rmtree
import tensorflow as tf
from keras import backend as K
from modelo_de_clasificacion.preprocesamiento import ProcesamientoDatos
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def

RUTA_MODELO_GUARDADO = "modelo_de_clasificacion/modelo_en_h5/modelo_construido.h5"  # El nombre del archivo que contendrá el modelo guardado
RUTA_MODELO_GUARDADO_PB = 'modelo_de_clasificacion/modelo_en_pb'


def _construir_modelo():
    """
    Este método se encarga de construir el modelo de machine learning y guardarlo en formato.h5
    """
    sess = tf.Session()
    K.set_session(sess)
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

    model.save(RUTA_MODELO_GUARDADO)  # lo guarda en .h5
    print("Modelo guardado correctamente")
    sess.close()


def _convertir_modelo_pb():
    """
    Este método se encarga de convertir el modelo de machine learning de formato .h5 a formato.pb
    """
    model = load_model(RUTA_MODELO_GUARDADO)
    if exists(RUTA_MODELO_GUARDADO_PB):
        rmtree(RUTA_MODELO_GUARDADO_PB)
    with K.get_session() as sess:
        builder = saved_model_builder.SavedModelBuilder(RUTA_MODELO_GUARDADO_PB)

        signature = predict_signature_def(inputs={'images': model.input},
                                          outputs={'scores': model.output})

        builder.add_meta_graph_and_variables(sess=sess,
                                             tags=[tag_constants.SERVING],
                                             signature_def_map={'predict': signature})
        builder.save()
    print("Modelo convertido correctamente")


@app.task
def _hacer_diagnostico(imgs_path):
    """
    Este método se encarga de hacer el diagnostico del hongo de la roya de las fotos que estén en un path
    :param imgs_path: El path donde estan las fotos en formato jpg o png para hacerles el diagnostico
    :return: Una lista con los diagnosticos que se hicieron a imgs_path
    """
    procesador = ProcesamientoDatos()
    path_imagenes = []
    for (path, ficheros, archivos) in walk(imgs_path):
        for elemento in listdir(path):
            full_path = join(path, elemento)
            if full_path.endswith(".png") or full_path.endswith(".jpg"):
                path_imagenes.append(full_path)
    try:
        imagenes_procesadas = procesador._procesar_imagenes(path_imagenes)
        with tf.Session() as sess:
            K.set_session(sess)
            meta_graph_def = tf.saved_model.loader.load(sess, [tag_constants.SERVING], RUTA_MODELO_GUARDADO_PB)
            signature = meta_graph_def.signature_def
            x1_tensor_name = signature['predict'].inputs['images'].name
            y_tensor_name = signature['predict'].outputs["scores"].name
            x1 = sess.graph.get_tensor_by_name(x1_tensor_name)
            y = sess.graph.get_tensor_by_name(y_tensor_name)

            results = sess.run(y, feed_dict={x1: imagenes_procesadas})
            return np.argmax(results, axis=1)
    except Exception as e :
        raise Exception("Ha ocurrido un error, tal vez no esta el archivo.pb o es posible que no haya fotos en este "
                        "directorio: ", imgs_path)

@app.task
def obtener_promedio_diagnostico(imgs_path):
    """
    Este método se encarga de obtener el promedio del diagnostico del hongo de la roya de las fotos que estén en un path
    :param imgs_path: El path donde estan las fotos en formato jpg o png para hacerles el diagnostico
    :return: Un entero con el promedio del hongo de la roya en las fotos que están en imgs_path
    """
    try:
        y_pred = _hacer_diagnostico(imgs_path)
        promedio = 0
        for y in y_pred:
            promedio += y
        promedio /= len(y_pred)
        return int(round(promedio))
    except Exception as e :
        raise e

# promedio = modelo.obtener_promedio_diagnostico("datos_train")
# print(promedio)
