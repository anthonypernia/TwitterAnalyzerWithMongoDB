
from TwitterExtractor import TwitterExtractor

if __name__ == "__main__":
    tw = TwitterExtractor("colombia " )
    tw.search_tweets(500)
    