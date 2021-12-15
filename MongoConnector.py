from pymongo import MongoClient

class MongoConnector:
    def __init__(self, user:str, password:str, db_name:str, collection_name:str, host:str, port:int):
        self.user = user
        self.password = password
        self.db_name = db_name
        self.collection_name = collection_name
        self.host = host
        self.port = port
        self.coll, self.db, self.conn = self.__connect(self.user, self.password, self.db_name, self.collection_name, self.host, self.port)
        
    def __connect(self, user:str, password:str, db_name:str, collection_name:str, host:str, port:int):
        conn = MongoClient(f'mongodb://{user}:{password}@{host}:{port}/')
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

