from pymongo import MongoClient

class Database:

    def __init__(self):
        client = MongoClient()
        self.db = client.coffee_leaf_rust_diagnosis


    def obtener_lot_data(self,fecha_inicial,fecha_final):
        lot_data = [data for data in self.db.lot_data.find({"timestamp": {"$gte": fecha_inicial, "$lt": fecha_final}})]
        return  lot_data