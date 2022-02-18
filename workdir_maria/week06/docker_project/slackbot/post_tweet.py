import requests
from sqlalchemy import create_engine
import pandas as pd
import os
import time
time.sleep(10)
webhook_url = os.getenv('WEBHOOK_URL') 

pg = create_engine('postgresql://postgres:1234@postgresdb:5432/tweets', echo=True)

query = '''
    SELECT * FROM tweets;
'''
tweetsdf = pd.read_sql_query(query, pg)

news = 'CNN latest news: \n'
for index, row in tweetsdf.iterrows():
    text = row['text']
    sentiment = row['sentiment']
    news += f'--> {text} \nSentiment: {sentiment} \n\n'

data = {"text": news}
requests.post(url=webhook_url, json=data)

