import numpy as np

np.random.seed(123)

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
from os import listdir, walk
from os.path import join
from modelo_de_clasificacion.preprocesamiento import datos_roya

import tensorflow as tf
from keras import backend as K
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def
import shutil
from coffee_rescuer.settings import BASE_DIR

class ModeloDiagnostico:
    def construir_modelo(self):
        model = Sequential()
        sess = tf.Session()
        K.set_session(sess)
        # K._LEARNING_PHASE = tf.constant(0)
        # K.set_learning_phase(0)

        datos = datos_roya()
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
        # print (Y_train[:10])

        X_train = X_train[0:2000]
        Y_train = Y_train[0:2000]

        X_test = X_test[0:2000]
        Y_test = Y_test[0:2000]
        # print(X_train.shape)
        # print (Y_train.shape)

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

        export_path = join(BASE_DIR,'modelo_de_clasificacion','folder_to_export')
        shutil.rmtree(export_path)
        builder = saved_model_builder.SavedModelBuilder(export_path)

        signature = predict_signature_def(inputs={'images': model.input},
                                          outputs={'scores': model.output})

        builder.add_meta_graph_and_variables(sess=sess,
                                             tags=[tag_constants.SERVING],
                                             signature_def_map={'predict': signature})
        builder.save()

        print("Modelo guardado correctamente")

    def __hacer_diagnostico(self, imgs_path):
        datos = datos_roya()
        path_imagenes = []
        for (path, ficheros, archivos) in walk(imgs_path):
            for elemento in listdir(path):
                if join(path, elemento).endswith(".png") or join(path, elemento).endswith(".jpg"):
                    path_imagenes.append(join(path, elemento))

        imagenes_procesadas = datos._procesar_imagenes(path_imagenes)

        export_dir = join(BASE_DIR, 'modelo_de_clasificacion', 'folder_to_export')
        with tf.Session() as sess:
            K.set_session(sess)
            meta_graph_def = tf.saved_model.loader.load(sess, [tag_constants.SERVING], export_dir)
            signature = meta_graph_def.signature_def
            x1_tensor_name = signature['predict'].inputs['images'].name
            y_tensor_name = signature['predict'].outputs["scores"].name
            x1 = sess.graph.get_tensor_by_name(x1_tensor_name)
            y = sess.graph.get_tensor_by_name(y_tensor_name)

            results = sess.run(y, feed_dict={x1: imagenes_procesadas})
            return np.argmax(results, axis=1)

    def obtener_promedio_diagnostico(self, imgs_path):
        y_pred = self.__hacer_diagnostico(imgs_path)
        promedio = 0
        for y in y_pred:
            promedio += y
        promedio /= len(y_pred)

        return int(round(promedio))


#modelo = ModeloDiagnostico()
#modelo.construir_modelo()
#promedio = modelo.obtener_promedio_diagnostico("datos_test")
#print(promedio)
