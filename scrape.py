# -*- coding: utf-8 -*-
"""Twitter trends collection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aOYrz3Uf-FJ1nA_5tIaZiT-Ie5Dp8_Jg

# Steps:

    1. Get trending topics using trends_avalible() method from tweepy.
    2. save those trending topics to json and after that create a list of trneding topics names
    3. Now use query method to get those topics tweets and save them in CSV with there query.

# Collecting trending topics

**reference** : https://medium.com/analytics-vidhya/how-to-get-trending-tweets-in-any-country-with-python-and-tweepy-af2bfe760251

## 1. Libray importing
"""


import tweepy
import os
import json
import sys
import datetime
import pandas as pd

"""## 2. Api keys and tokens"""

api_key = 'bfGWM7G7WylwHnayWAsv1mmHS'
api_secret = 'jELrN8U7agcSlDw0k4nWilRiO2etj0DGSEwkWlTGI4wWqCBlVZ'

access_token = '1170647549520121856-hdfu8cmphlXjl5acd21i7rUCf36HCS'
access_token_secret = 'Llpcdz1vkxhbpbzhAYmZILuG5MlgtxGl9la0J4mKUSNTy'

"""## 3. Authorization and Authentication"""

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

"""## 4. Collecting trending topics"""

if __name__ == "__main__":
    #Avalible locations
    loc = api.trends_available()
    # writing a JSON file that has the available trends around the world
    with open("avalible_locs.json", "w") as wp:
        wp.write(json.dumps(loc, indent=1))

"""# Saving trending topics

## 1. Loding json data
"""

file = open('avalible_locs.json')
json_data = json.load(file)

json_data[:20]

"""## 2. saving trending topics"""

treding_topics= []
for i in range(len(json_data)):
    if json_data[i]['name']:
        treding_topics.append(json_data[i]['name'])

treding_topics[:20]

"""# Collecting trending tweets"""

def trending_tweets(api, topics):
    tweets = api.search(q=topics, language='en')
    return tweets

trending_tweets(api, "Worldwide")

def process_raw_tweet(tweet):
    processed_tweet = {}
    processed_tweet['id'] = tweet.id
    processed_tweet['username'] = tweet.user.screen_name
    processed_tweet['tweet_text'] = tweet.text
    processed_tweet['retweets'] = tweet.retweet_count
    processed_tweet['location'] = tweet.user.location
    processed_tweet['created_at'] = tweet.created_at
    return processed_tweet

def upload_tweets(tweets):
    today_date = datetime.date.today()
    file_path = "data/{}/data.csv".format(today_date)
    df = pd.DataFrame.from_dict(tweets, orient='index')
    if not os.path.isfile(file_path):
        file = open(file_path, "w+", encoding='utf-8')
        return df.to_csv(file)
    else: 
        return df.to_csv(file_path, mode='a', header=False)

def main(treding_topics):
    treding_topics = ['Worldwide','Winnipeg','Ottawa','Quebec','Montreal']
    today_date = datetime.date.today()
    processed_tweets = []
    
    for topic in treding_topics:
        file_path = "data/{}/{}/data.csv".format(today_date, topic)
        tweets = trending_tweets(api, topic)
        
        if tweets:
            for tweet in tweets:
                processed_tweets = process_raw_tweet(tweet)
            df = pd.DataFrame.from_dict(processed_tweets, orient='index')
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            else:
                return df.to_csv(file_path, mode='a', header=False)

if __name__ == "__main__":
    main(treding_topics)
