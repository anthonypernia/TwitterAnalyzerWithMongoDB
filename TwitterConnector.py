import tweepy
from MongoConnector import MongoConnector
import json
import datetime

class TwitterConnector:
    
    def __init__(self, API_KEY:str, API_KEY_SECRET:str, ACCESS_TOKEN:str, ACCESS_TOKEN_SECRET:str):
        self.API_KEY = API_KEY
        self.API_KEY_SECRET = API_KEY_SECRET
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.ACCESS_TOKEN_SECRET = ACCESS_TOKEN_SECRET
        self.api = self.__connect(self.API_KEY, self.API_KEY_SECRET, self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        
    def __connect(self, API_KEY:str, API_KEY_SECRET:str, ACCESS_TOKEN:str, ACCESS_TOKEN_SECRET:str):
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=10, 
                                    retry_delay=5, retry_errors=5, timeout=60)
        api.verify_credentials()
        return api
    
    def get_api(self):
        return self.api
    
    def selecting_filter(self, filter_list:list) -> str:
        q = ''
        filters  = {
            "retweets" : "-filter:retweets ",
            "replies" : "-filter:replies ",
            "link" : "-filter:links ",
            "images" : "-filter:images ",
            "videos" : "-filter:videos ",
            "native_video" : "-filter:native_video ",
            "native_image" : "-filter:native_image ",
            "native_retweet" : "-filter:native_retweet'"
            }
        for i,f in enumerate(filter_list):
            if i == len(filter_list)-1:
              q += f'{filters[f]}'
            else:
              q += f'{filters[f]} AND '
        return q
    
    def get_tweets_and_save_mongoDB(self, mongo_connection:MongoConnector , query:str, count_limit:int, geo_loc_filter:str='', filters_by_default:list=['retweets', 'replies', 'link', 'images'] ) -> list:    
        count = 0
        id = None
        batch = 100
        filters_to_apply = self.selecting_filter(filters_by_default)
        complete_query = f'{query}  {filters_to_apply} {geo_loc_filter} '
        while count <= count_limit:
            try:
                tweets = self.api.search_tweets(q=f"{complete_query}", lang='es', tweet_mode='extended', max_id=id, count=batch)
                if tweets:
                    print(f'{len(tweets)} tweets found and last id is {id}')
                    
                    for tweet in tweets:
                        print(f'{tweet.full_text}')
                        json_tweet = json.dumps(tweet._json)
                        json_tweet = json.loads(json_tweet)
                        json_tweet['created_at_yyyymmdd'] = datetime.datetime.strptime(json_tweet['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
                        json_tweet['stored_at'] = datetime.datetime.now().strftime('%Y-%m-%d')
                        json_tweet['stored_at_full'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        mongo_connection.insert_one(json_tweet)
                        count += 1
                        id = tweet.id
                    if count>0:
                        print(f"{count} tweets inserted")
                else:
                    print('No tweets')
                    break
            except Exception as e:
                print(e)
                break