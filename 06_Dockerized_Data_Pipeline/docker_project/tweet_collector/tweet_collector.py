#import imp
import time
from datetime import datetime, timedelta
import logging
import random
import pymongo
#from faker import Faker
import os
import tweepy

# Create a connection to the MongoDB database server
mongo_client = pymongo.MongoClient(host='mongodb', port=27017) # hostname = servicename for docker-compose pipeline
#client = pymongo.MongoClient(host='localhost') 
# Create/use a database
db = mongo_client.twitter
# equivalent of CREATE DATABASE twitter;

# Define the collection
db.tweets.drop()
collection = db.tweets

BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# CREATE TABLE tweets;
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True,
)

search_query = "elon musk -is:retweet -is:reply -is:quote lang:de -has:links"
response = client.get_user(
    username='elonmusk',
    user_fields=['created_at', 'description', 'location',
                 'public_metrics', 'profile_image_url']
)

user = response.data
def get_tweets(user,search_query):
    cursor = tweepy.Paginator(
    method=client.get_users_tweets,
    id=user.id,
    exclude=['replies', 'retweets'],
    tweet_fields=['author_id', 'created_at', 'public_metrics']
    ).flatten(limit=20)
    tweets = [dict(tweet) for tweet in cursor]
    return tweets
tweets = get_tweets(user,search_query)
collection.insert_many(tweets)
# old_tweets = ''

# while True:  ####Do with streamlistener class see: https://docs.tweepy.org/en/v3.5.0/streaming_how_to.html
#     tweets = get_tweets(search_query) 
    
#     # Insert the tweet into the collection
#     logging.warning('Cheking for tweets')
    
#     if len(tweets) != len(old_tweets):
#         logging.warning('-----Tweet being written into MongoDB-----')
#         #logging.warning(tweets)
#         collection.insert_many(tweets) #equivalent of INSERT INTO tweet_data VALUES (....);
#         logging.warning(str(datetime.now()))
#         logging.warning('----------\n')
#     old_tweets = tweets
#     time.sleep(50)