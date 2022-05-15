import pymongo
import time
import pandas as pd
time.sleep(5)
from sqlalchemy import create_engine
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

# Establish a connection to the MongoDB server
client = pymongo.MongoClient(host="mongodb", port=27017)

# Select the database to use withing the MongoDB server
db = client.twitter
docs = db.tweets.find()

pg = create_engine('postgresql://postgres:1234@postgresdb:5432/tweets', echo=True)
pg.execute('''
    DROP TABLE IF EXISTS tweets;
''')
pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(500),
    sentiment NUMERIC
);
''')
# Clean data
mentions_regex = '@[A-Za-z0-9]+'
url_regex ='https?:\/\/\S+' #this will not catch all possible URLs
hashtag_regex = '#'
rt_regex = 'RT\s'
new_line_regex = '\n'
analyzer = SentimentIntensityAnalyzer()

def clean_text(text):
    text = re.sub(mentions_regex, '', text)  #removes @mentions
    text = re.sub(hashtag_regex, '', text) #removes hashtag symbol
    text = re.sub(rt_regex, '', text) #removes RT to announce retweet
    text = re.sub(url_regex, '', text) #removes most URLs
    text = re.sub(new_line_regex, ' ', text) #removes most URLs
    return text

def get_score(text):
    score = analyzer.polarity_scores(text)
    return score['compound']

for doc in docs:
    text = doc['text']
    c_text = clean_text(doc['text'])
    if text:
        score = get_score(c_text)
        query = "INSERT INTO tweets VALUES (%s, %s);"
        pg.execute(query, (text, score))