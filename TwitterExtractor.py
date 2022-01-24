

import tweepy
import json
import credentials
from MongoConnector import MongoConnector
from TwitterConnector import TwitterConnector


class TwitterExtractor:
    
    def __init__(self, query:str = 'anthonyperniah', count_twees:int=300, date_since:str = None, date_until:str=None, lat:str = None, lon:str=None, km:str=None) -> None:
        self.filter_date = f'since:{date_since} until:{date_until}' if date_since and date_until else ''
        self.query = credentials.QUERY if len(credentials.QUERY) > 1 else query
        self.lat = lat
        self.lon = lon
        self.km= km
        self.count_twees = int(credentials.COUNT_TWEETS) if int(credentials.COUNT_TWEETS) > 1 else count_twees
        self.geo_loc_filter = f"geocode:{self.lat},{self.lon},{self.km}km" if self.lat and self.lon and self.km else ""
        self.prefix_collection = credentials.PREFIX_COLLECTION
        self.API_KEY = credentials.API_KEY
        self.API_KEY_SECRET = credentials.API_KEY_SECRET
        self.ACCESS_TOKEN = credentials.ACCESS_TOKEN 
        self.ACCESS_TOKEN_SECRET = credentials.ACCESS_TOKEN_SECRET
        self.db_name = credentials.DB_NAME
        self.db_collection_name = f'{self.prefix_collection.strip()}{self.query.strip()}'.replace(' ', '_').lower()
        self.db_uri = credentials.DB_URI
        self.twitter_connection, self.twitter_connector = self.set_data_twitter(self.API_KEY, self.API_KEY_SECRET, self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        self.mongo_connection , self.mongo_connector = self.set_data_mongo(self.db_uri, self.db_name, self.db_collection_name)
    
    def set_data_twitter(self, API_KEY:str, API_KEY_SECRET:str, ACCESS_TOKEN:str, ACCESS_TOKEN_SECRET:str):
        twitter_connector = TwitterConnector(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return twitter_connector.get_api(), twitter_connector
        
    def set_data_mongo(self, db_uri:str, db_name:str, db_collection_name:str):
        mongo_connector = MongoConnector(db_uri, db_name, db_collection_name)
        return mongo_connector.get_connection(), mongo_connector


    def search_tweets(self):
        if self.mongo_connection:
            print('Mongo Connected')
            if self.twitter_connection:
                print('Twitter Connected')
                print(f'Searching tweets about {self.query}')
                self.twitter_connector.get_tweets_and_save_mongoDB(self.mongo_connector, query = self.query, count_limit= self.count_twees)
            else:
                print('Twitter Connection Error')
        else:
            print('Mongo connection error')
