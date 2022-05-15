import pymongo
import os
import tweepy

def get_tweets(user_name):
    ''' Collects tweets from user_name. Returnes a list of dictionaries.
    '''
    response = client.get_user(
    username=user_name,
    user_fields=['created_at', 'description', 'location',
                 'public_metrics', 'profile_image_url']
    )
    user = response.data
    cursor = tweepy.Paginator(
    method=client.get_users_tweets,
    id=user.id,
    exclude=['replies', 'retweets'],
    tweet_fields=['author_id', 'created_at', 'public_metrics']
    ).flatten(limit=3)
    tweets = [dict(tweet) for tweet in cursor]
    return tweets

# Create a connection to the MongoDB database server 
mongo_client = pymongo.MongoClient(host='mongodb', port=27017) 

# Create/use a database
db = mongo_client.twitter

# Define the collection
db.tweets.drop() #clean existing data
collection = db.tweets

BEARER_TOKEN = os.getenv('BEARER_TOKEN')

# Connect to tweepy
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True,
)

#Define user name
user_name = 'cnnbrk'  

# Get tweets and insert them in mongoDB collection db.tweets
tweets = get_tweets(user_name)
collection.insert_many(tweets)
