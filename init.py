
from TwitterExtractor import TwitterExtractor

if __name__ == "__main__":
    #Before to use, you need to in credentials.py: 
    # - Set the credentials of your Twitter account
    # - Set the credentials of your MongoDB
    # - Set query to search
    tw = TwitterExtractor()
    tw.search_tweets()
    