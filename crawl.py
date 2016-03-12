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
        friends_list = []
        for friend in tweepy.Cursor(api.friends).items():
            # Process a single status
            friends_list.append(friend._json)
    with open("my_friends.json", 'w') as fp:
        json.dump(friends_list,fp,indent = 4)
    return friends_list

def get_my_friends_ids(api):
    with open('my_friends_ids.json', 'w') as fp:
        for friend in tweepy.Cursor(api.friends_ids).items():
            # Process a single status
            json.dump(friend , fp, indent = 4)
            fp.write("\n")

def read_ids(file):
    with open(file, 'r') as fp:
        users = json.load(fp)
    for user in users:
        print user['id']

def my_friends_ids(file_read,file_write,api):
    with open(file_read, 'r') as fp:
        with open(file_write, 'a') as fp1:
            for id in fp:
                for page in tweepy.Cursor(api.user_timeline,user_id=id,
                                          count=200).pages(16):
                    for status in page:
                        json.dump(status._json, fp1 , indent = 4)

if __name__ == '__main__':
    #api = init_twitter("./keys.json")
    #get_my_tweets(api)
    #get_my_friends_ids(api)
    #friends_ids_list = my_friends_ids('my_friends_ids.json','friends_tweets.json',api)
    read_ids("my_friends.json")