import tweepy
import csv
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

if not Path('blm.csv').is_file():
    with open('blm.csv', 'w') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(['id', 'created_at', 'full_text', 'favorite_count',
            'retweet_count', 'hashtags'])

csvFile = open('blm.csv', 'a', newline='')
csvWriter = csv.writer(csvFile, )

key_file = open('key.txt')

consumer_key = key_file.readline().rstrip('\n')
consumer_secret = key_file.readline().rstrip('\n')

today = datetime.today()
week_ago = today - timedelta(days=7)
week_ago_str = week_ago.strftime('%Y-%m-%d')

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, parser=tweepy.parsers.JSONParser())
tweets = tweepy.Cursor(api.search, 
    q=['#blacklivesmatter OR #blm'], 
    lang='en', 
    result_type='recent', 
    tweet_mode='extended', 
    count=100).items()

for tweet in tweets:
    print('\n############### New Tweet')
    print(tweet.id) # This is the tweet's id
    print(tweet.created_at) # when the tweet posted
    print(tweet.full_text) # content of the tweet
    print(tweet.favorite_count)
    print(tweet.retweet_count)

    hashtags = []
    for hashtag in tweet.entities['hashtags']:
        hashtags.append(hashtag['text'])
    print(hashtags)

    try:
        csvWriter.writerow(
            [tweet.id,
            tweet.created_at, 
            tweet.full_text.encode('utf-8','ignore'),
            tweet.favorite_count,
            tweet.retweet_count,
            hashtags])
    except:
        continue
        
csvFile.flush()
csvFile.close()
