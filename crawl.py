import json
import ijson
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
    """
    connects to twitter and dumps all MY to tweets to a json file
    """
    with open('my_tweets.json', 'a') as fp:
        for status in tweepy.Cursor(api.home_timeline).items(10):
            # Process a single status
            json.dump(status._json, fp, indent = 4)

def get_my_friends(api):
    """
    connects to twitter and dumps all the people I follow to a json file
    """
    with open('my_friends.json', 'a') as fp:
        friends_list = []
        for friend in tweepy.Cursor(api.friends).items():
            # Process a single status
            friends_list.append(friend._json)
    with open("my_friends.json", 'w') as fp:
        json.dump(friends_list,fp,indent = 4)
    return friends_list

def get_my_friends_ids(api):
    """
    connects to twitter and dumps my friends' ids in a json file
    """
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

def get_my_friends_tweets(file_read,file_write,api):
    """
    opens file_read from which it reads the ids of my friends(in
    this
    file we have just the ids) and then fetches all their tweets in the
    file_write
    """
    with open(file_read, 'r') as fp:
        with open(file_write, 'a') as fp1:
            for id in fp:
                for page in tweepy.Cursor(api.user_timeline,user_id=id,
                                          count=200).pages(16):
                    for status in page:
                        json.dump(status._json, fp1 , indent = 4)


def get_tweets_from_friends(file_read,file_write,api):
    """
    opens file_read from which it reads the ids of my friends(in
    this
    file we have just the ids) and then fetches all their tweets in the
    file_write
    here we try to fetch all the tweets first and then write them to the file
    """
    with open(file_read, 'r') as fp:
        for id in fp:
            for page in tweepy.Cursor(api.user_timeline,user_id=id,
                                          count=200).pages(16):
                for status in page:
                    json.dump(status._json, open(file_write, 'a'), indent = 4)
                    with open(file_write, 'a') as fp1:
                        fp1.write(",\n")



    #del tweets[:]

def get_tweets_from_friends_new(file_read,file_write,api):
    """
    opens file_read from which it reads the ids of my friends(in
    this
    file we have just the ids) and then fetches all their tweets in the
    file_write
    here we try to fetch all the tweets first and then write them to the file
    """
    with open(file_read, 'r') as fp:
        for id in fp:
            for statuses in tweepy.Cursor(api.user_timeline,
                                          user_id=id).items():
                json.dump(statuses._json, open(file_write, 'a'), indent = 4)
                with open(file_write, 'a') as fp:
                    fp.write(",\n")


if __name__ == '__main__':
    #api = init_twitter("./keys.json")
    #get_my_tweets(api)
    #get_my_friends_ids(api)
    #friends_ids_list = get_my_friends_tweets('my_friends_ids.json','friends_tweets.json',api)
    #get_my_friends_ids(api)
    #read_ids("my_friends.json")
    #get_tweets_from_friends('my_friends_ids.json','friends_tweets.json',api)
    counter=0
    with open('friends_tweets.json', 'r') as fp:
        for line in fp:
            if line.__contains__('"id":'):
                counter+=1
    print counter