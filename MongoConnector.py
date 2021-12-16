from pymongo import MongoClient

class MongoConnector:
    def __init__(self, db_uri:str , db_name:str, collection_name:str):
        self.db_name = db_name
        self.db_uri = db_uri
        self.collection_name = collection_name
        self.coll, self.db, self.conn = self.__connect(self.db_uri ,self.db_name, self.collection_name)
        
    def __connect(self, db_uri:str,  db_name:str, collection_name:str):
        conn = MongoClient(f'{db_uri}')
        db = conn[db_name]
        coll = db[collection_name] 
        return coll, db , conn
    
    def get_collection(self):
        return self.coll
    
    def get_db(self):
        return self.db
    
    def get_connection(self):
        return self.conn
    
    def close_connection(self):
        self.conn.close()
        
    def insert_one(self, data):
        self.coll.insert_one(data)
    
    def insert_many(self, data):
        self.coll.insert_many(data)
    
    def get_all(self):
        return self.coll.find()
    
    def get_by_id(self, id):
        return self.coll.find_one({'_id':id})
    
    def get_by_query(self, query):
        return self.coll.find(query)

