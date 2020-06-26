import tweepy
import csv
#import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

from tweepy_auth import tweepy_auth

auth = tweepy_auth()
api = tweepy.API(auth,
    wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

df = pd.DataFrame(columns=['id', 'created_at', 'full_text', 'favorite_count',
        'retweet_count', 'hashtags'])

num_tweets = 0
max_id = 888888888888888888888
while True:
    #print(max_id)
    tweets = api.search(q=['#blacklivesmatter OR #blm'], 
        lang='en', 
        result_type='recent', 
        tweet_mode='extended', 
        count=100,
        max_id=max_id)

    if tweets:
        for tweet in tweets:
            hashtags = []
            for hashtag in tweet.entities['hashtags']:
                hashtags.append(hashtag['text'])

            #print(tweet.created_at)

            df = df.append({'id': tweet.id,
                    'created_at': tweet.created_at, 
                    'full_text': tweet.full_text.encode('utf-8','ignore'),
                    'favorite_count': tweet.favorite_count,
                    'retweet_count': tweet.retweet_count,
                    'hashtags': hashtags},
                    ignore_index=True)

            if tweet.id < max_id:
                max_id = tweet.id
            num_tweets += 1
    else:
        break
    print(num_tweets)
    print(tweet.created_at)

df['created_at'] = pd.to_datetime(df['created_at'])

print(df.head())
for name, group in df.groupby(pd.Grouper(key='created_at',freq='D')):
    parsed_name = str(name).split(' ')[0].replace('-', '_')
    print(parsed_name)
    group.to_csv('./data/blm_'+ parsed_name +'.csv', index=False)

