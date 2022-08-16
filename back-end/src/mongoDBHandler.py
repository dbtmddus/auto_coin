from pymongo import MongoClient
from pymongo.cursor import CursorType
import configparser
from enum import Enum

db_name = 'auto_coin'
st1_collection = 'strategy1_soaring'
st2_collection = 'strategy2_volatility'

class MongoDBHandler:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        host = config['MONGODB']['host']
        port = config['MONGODB']['port']

        self._client = MongoClient(host, int(port))
        self._db = self._client[db_name]
        
    def insert_doc(self, data, collection_name):
        """
        if not isinstance(data, dict):
            raise Exception("data type should be dict")
        """
        print("insert collection ", collection_name, " data:", data)
        return self._db[collection_name].insert_one(data).inserted_id

    def recordOrder(self, name, res, price = None):
        #bid:매수 res :시장가매수는 매수총액:o, Volume:x, 거래시세:x
        #aks:매도 res :시장가매도는 매수총액:x, Volume:o, 거래시세:x
        print(name, " data : " , res.json())
        data = {}
        data['order'] = res.json()['side']
        data['market'] = res.json()['market']
        data['fee'] = res.json()['paid_fee']

        if (res.json()['side'] == 'bid'):
            data['amount'] = res.json()['price']
        elif (res.json()['side'] == 'ask'):
            data['amount'] = price * res.json()['volume']
        else:
            print("error, check 'side' info : ", res.json()['side'])
            return None            
        self.insert_doc(data, name)

    def displayCollection(self, collection_name):
        ret = self._db[collection_name].find()
        for document in ret:
          print(document)

    def displayCollectionList(self):
        print("db:", self._db)
        print("collections:", self._db.list_collection_names())

if __name__ == "__main__":
    db = MongoDBHandler()
    db.displayCollectionList()
    db.displayCollection(st1_collection)
    """
    data = {}
    data['order'] = "ysy"
    db.insert_doc(data, 'strategy1_soaring')
"""
