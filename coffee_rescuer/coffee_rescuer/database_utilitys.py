from pymongo import MongoClient


class Database:

    def __init__(self):
        self.__client = MongoClient()
        self.__db = self.__client.coffee_leaf_rust_diagnosis

    def obtener_lot_data_usuario(self, owner_id,lote_id, fecha_inicial):
        """
        Permite obtener los datos de un lote de un usuario de la bd coffee_leaf_rust_diagnosis desde cierta fecha.
        :param owner_id: La identificación del usuario en la base de datos coffee_leaf_rust_diagnosis.
        Es importante resaltar, que esta identificación en coffee_rescuer_db es el campo
        username y se trata como un string.
        :param lote_id: El id del lote del que se obtendrán datos
        :param fecha_inicial: Fecha inicial en datetime para la obtención de datos.
        :return: una lista con los datos de los lotes de un usuario.
        """
        if owner_id.isnumeric():
            owner_id = int(owner_id)
        lot_data = [data for data in
                    self.__db.lot_data.find({"timestamp": {"$gt": fecha_inicial}, "owner_id": owner_id,"lot_number":lote_id})]
        return lot_data

    def cerrar_conexion(self):
        self.__client.close()
