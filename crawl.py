import json
import tweepy
from tweepy import OAuthHandler
import requests
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
from requests.packages.urllib3.exceptions import SNIMissingWarning

requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)

def init_twitter(filename):
    with open(filename, 'r') as data_file:
        keys = json.load(data_file)
    consumer_key = keys.get(u'consumer_key')
    consumer_secret = keys.get(u'consumer_secret')
    access_token = keys.get(u'access_token')
    access_secret = keys.get(u'access_secret')
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)
    return api

def get_my_tweets(api):
    with open('my_tweets.json', 'a') as fp:
        for status in tweepy.Cursor(api.home_timeline).items(10):
            # Process a single status
            json.dump(status._json, fp, indent = 4)

def get_my_friends(api):
    with open('my_friends.json', 'a') as fp:
        for friend in tweepy.Cursor(api.friends).items():
            # Process a single status
            json.dump(friend._json, fp, indent = 4)

if __name__ == '__main__':
    api = init_twitter("./keys.json")
    get_my_tweets(api)
    get_my_friends(api)