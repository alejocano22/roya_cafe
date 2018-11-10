from pymongo import MongoClient

class Database:

    def __init__(self):
        self.__client = MongoClient()
        self.__db = self.__client.coffee_leaf_rust_diagnosis



    def obtener_lot_data_usuario(self,id_usuario,fecha_inicial):
        lot_data = [data for data in self.__db.lot_data.find({"timestamp": {"$gt": fecha_inicial},"owner_id": id_usuario})]
        return  lot_data

    def cerrar_conexion(self):
        self.__client.close()