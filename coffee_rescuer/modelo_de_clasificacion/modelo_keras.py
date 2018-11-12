import numpy as np

np.random.seed(123)
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
from os.path import join, exists
from shutil import rmtree
import tensorflow as tf
from keras import backend as K
from modelo_de_clasificacion.preprocesamiento import ProcesamientoDatos
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def


def _construir_modelo(RUTA_MODELO_GUARDADO="modelo_de_clasificacion/modelo_en_h5/modelo_construido.h5", ancho=640,
                      alto=480, batch_size=3):
    """
    Este método se encarga de construir el modelo de machine learning y guardarlo en formato.h5
    :param RUTA_MODELO_GUARDADO: Es el path completo del archivo que contendrá el modelo de machine learning y se creará
    en este método.
    :param ancho: El ancho de las imágenes que serán pasadas por este modelo.
    :param alto: El alto de la imágenes que serán pasadas por este modelo.
    :param batch_size: Controla el tamaño de cada grupo de datos que van a pasar a través de la red neuronal.
    """
    sess = tf.Session()
    K.set_session(sess)
    model = Sequential()
    datos = ProcesamientoDatos()
    (X_train, y_train), (X_test, y_test) = datos._cargar_datos()
    X_train = X_train.reshape(X_train.shape[0], ancho, alto, 3)
    X_test = X_test.reshape(X_test.shape[0], ancho, alto, 3)

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

    model.add(Conv2D(batch_size, (3, 3), activation='relu', input_shape=(ancho, alto, 3)))
    model.add(Conv2D(batch_size, (3, 3), activation='relu'))
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
              batch_size=batch_size, epochs=5, verbose=1)

    score = model.evaluate(X_test, Y_test, verbose=0)
    print(score)
    print("%s: %.2f%%" % (model.metrics_names[1], score[1] * 100))

    model.save(RUTA_MODELO_GUARDADO)  # lo guarda en .h5
    print("Modelo guardado correctamente")
    sess.close()


def _convertir_modelo_pb(RUTA_MODELO_GUARDADO="modelo_de_clasificacion/modelo_en_h5/modelo_construido.h5",
                         RUTA_MODELO_GUARDADO_PB='modelo_de_clasificacion/modelo_en_pb'):
    """
    Este método se encarga de convertir el modelo de machine learning de formato .h5 a formato.pb
    :param RUTA_MODELO_GUARDADO:Es el path completo del archivo que contiene el modelo de machine learning.
    :param RUTA_MODELO_GUARDADO_PB: Es la dirección de la carpeta dónde se guardará el modelo en .pb
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


def hacer_diagnostico(input, RUTA_MODELO_GUARDADO_PB="modelo_de_clasificacion/modelo_en_pb"):
    """
    Se encarga de hacer el diagnostico del hongo de la roya de las imágenes de plantas procesadas que estén en el input
    :param input: Es una tupla de tres matrices dónde la primera matriz corresponde a los datos de los sensores
    procesador, el segundo las imágenes de las plantas procesadas, y el tercero las imágenes multiespectrales procedas.
    :return: Una el promedio de los diagnósticos que se hicieron a las fotos procesadas que contenía el input
    """
    imagenes_procesadas = input[1]
    if imagenes_procesadas is None:
        return 0
    with tf.Session() as sess:
        K.set_session(sess)
        meta_graph_def = tf.saved_model.loader.load(sess, [tag_constants.SERVING], RUTA_MODELO_GUARDADO_PB)
        signature = meta_graph_def.signature_def
        x1_tensor_name = signature['predict'].inputs['images'].name
        y_tensor_name = signature['predict'].outputs["scores"].name
        x1 = sess.graph.get_tensor_by_name(x1_tensor_name)
        y = sess.graph.get_tensor_by_name(y_tensor_name)

        results = sess.run(y, feed_dict={x1: imagenes_procesadas})
        results = np.argmax(results, axis=1)
        return np.mean(results)
