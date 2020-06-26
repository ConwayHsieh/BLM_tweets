import os
import csv
import json
import tweepy
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from tweepy_auth import tweepy_auth

'''
today = datetime.today()
week_ago = today - timedelta(days=7)
week_ago_str = week_ago.strftime('%Y-%m-%d')
'''
auth = tweepy_auth()

api = tweepy.API(auth,
    wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

tweets = tweepy.Cursor(api.search, 
    q=['#blacklivesmatter OR #blm'], 
    lang='en', 
    result_type='recent', 
    tweet_mode='extended', 
    count=100).items()

df = pd.DataFrame(columns=['id', 'created_at', 'full_text', 'favorite_count',
            'retweet_count', 'hashtags'])

for tweet in tweets:
    hashtags = []
    for hashtag in tweet.entities['hashtags']:
        hashtags.append(hashtag['text'])

    print(tweet.created_at)

    df = df.append({'id': tweet.id,
            'created_at': tweet.created_at, 
            'full_text': tweet.full_text.encode('utf-8','ignore'),
            'favorite_count': tweet.favorite_count,
            'retweet_count': tweet.retweet_count,
            'hashtags': hashtags},
            ignore_index=True)

df['created_at'] = pd.to_datetime(df['created_at'])

print(df.head())
for name, group in df.groupby(pd.Grouper(key='created_at',freq='D')):
    parsed_name = str(name).split(' ')[0].replace('-', '_')
    print(parsed_name)
    group.to_csv('./data/blm_'+ parsed_name +'.csv', index=False)
