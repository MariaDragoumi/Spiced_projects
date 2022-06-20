## News Sentiment Analysis

Data pipeline implementation packaged in a container. News tweets are collected and stored in a NoSQL database and the sentiment polarity is analyzed. 
Finally, the text with the score are transferred through an ETL process to an SQL database and re-posted with a sentiment warning.  


Techstack: Docker, MongoDB, PostgreSQL, pymongo, regex, sqlalchemy, tweepy, vaderSentiment
