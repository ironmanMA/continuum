__author__ = 'mohammad'

import tweepy
import simplejson as json

consumer_key = 'GvTphxFmPU8UdSsFtKGUvu0nM'
consumer_secret = 'f1K1pT6y7pIhI8P9s1qRJUQVklusRmnrSUBgRUhRlNoUGt4Pxk'
access_token = '2187696536-NzDYtaNKWICG4UBsRwvdlTq15ZtZ5f3hst8Vw1z'
access_token_secret = 'OfdqCKmvsYWlmEVnRTZNI9CeVLBNfKwQimTz8bfFh8mgU'

screen_name = 'boomerangcommer'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# count = 1
# for tweet in public_tweets:
#     print '[MY Tweet #',count ,'] ',tweet.text
#     count += 1

new_tweets = api.user_timeline(screen_name = screen_name,count=2)
count = 1
tweets = {}

for tweet in new_tweets:
    # print '[rBoom Tweet #',count ,'] ',tweet
    tweets['rBoom'+`count`] = tweet
    count += 1

print json.dumps({'tweets': tweets})
