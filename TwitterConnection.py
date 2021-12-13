import tweepy
from MongoConnection import MongoConnection
import json
import datetime

class TwitterConnection:
    
    def __init__(self, API_KEY:str, API_KEY_SECRET:str, ACCESS_TOKEN:str, ACCESS_TOKEN_SECRET:str):
        self.API_KEY = API_KEY
        self.API_KEY_SECRET = API_KEY_SECRET
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.ACCESS_TOKEN_SECRET = ACCESS_TOKEN_SECRET
        self.api = self.__connect(self.API_KEY, self.API_KEY_SECRET, self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
        
    def __connect(self, API_KEY:str, API_KEY_SECRET:str, ACCESS_TOKEN:str, ACCESS_TOKEN_SECRET:str):
        auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        api.verify_credentials()
        return api
    
    def get_api(self):
        return self.api
    
    def selecting_filter(self, filter_list:list) -> str:
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
        return ''.join([filters[i] for i in filter_list])
    
    def get_tweets_and_save_mongoDB(self, mongo_connection:MongoConnection , query:str, count_limit:int, lat:int=None, km:int=None, lon:int=None, filters_by_default:list=['retweets', 'replies'] ) -> list:    
        count = 0
        id = None
        filters_to_apply = self.selecting_filter(filters_by_default)
        geo_loc = f"geocode:{lat},{lon},{km}km" if lat and lon and km else ""
        complete_query = f'{query}  {filters_to_apply} {geo_loc} '
        while count <= count_limit:
            try:
                tweets = self.api.search_tweets(q=f"{complete_query}", lang='es', tweet_mode='extended',max_id=id)
                if tweets:
                    for tweet in tweets:
                        json_tweet = json.dumps(tweet._json)
                        
                        json_tweet = json.loads(json_tweet)
                        json_tweet['created_at_yyyymmdd'] = datetime.datetime.strptime(json_tweet['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
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