from TwitterHelper import *
from time import sleep
from tf_idf_extended import score_me
import re
 
 
since_id = None
ONE_HOUR = 60 * 60
tweet_ids = set()
 
 
def analyze(tweet):
    text = tweet['text']
    for pattern in twitter_namespace:
        text = re.sub(pattern, '', text)
 
    scores = score_me(doc=text, min_score=0.11, bigram=True, trigram=True, count=10)
    keywords = [item[0] for item in scores]
 
    for keyword in keywords:
        tweets = search_tweets(keyword)
        for tw in tweets:
            if tw['id'] not in tweet_ids and filtered_by_screen_name(tw['user']['screen_name']):
                favorites_create(tw)
                tweet_ids.add(tw['id'])
 
 
def filtered_by_screen_name(screen_name):
    blacklist = ['YOUR_SCREEN_NAME_AND_ALSO_UNWANTED_SCREEN_NAMES']
    return screen_name not in blacklist
 
 
while True:
    tweets = my_tweets(since_id=since_id)
    if tweets:
        since_id = tweets[0]['id']
        [analyze(tweet=tweet) for tweet in tweets if tweet is not None]
 
    sleep(ONE_HOUR)