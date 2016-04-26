# -*- coding: greek -*-
import json, re, math
import ijson
import tweepy
from tweepy import OAuthHandler
from collections import Counter
import requests
import matplotlib.pyplot as plt
import numpy as np
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
    api = tweepy.API(auth,wait_on_rate_limit = True,
                     wait_on_rate_limit_notify = True)
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


def get_tweets_from_friends(file_read, file_write , api, from_id, to_id):
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
                                      since_id= from_id, max_id
            = to_id,
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

def extract_text(file):
    with open(file, 'r') as fp:
        tweets = json.load(fp)
    all_tweets={}
    id={}
    text={}
    for tweet in tweets:
        all_tweets[tweet['id']]= tweet['text']
    output= json.dumps(all_tweets, sort_keys=True,indent=4, separators=(',',
                                                                       ': '))
    return all_tweets

def load_json(file):
    """
    just load the json file
    :param file:
    :return:
    """
    with open(file, 'r') as fp:
        tweets = json.load(fp)
    return tweets


def get_words(tweet):
    splitter=re.compile('\\W*')
    # Split the words by non-alpha characters
    words=[s.lower( ) for s in splitter.split(tweet)
    if len(s)>2 and len(s)<20]
    # Return the unique set of words only
    return dict([(w,1) for w in words])

def count_words(tweet):
    """
    :param tweet: the text from 1 tweet
    :return: the length of the tweet in words
    """
    words=[]
    for w in tweet.split():
        words.append(w)
    return len(words)


def word_len_distr(tweets_dict):
    """
    Takes as input a dictionary of the form {id:text} and returns the
    distribution of the count of words
    :param tweets_dict: dictionary of the form {id:text}
    :return: the sorted distribution of word count
    """
    counts = []
    for id in tweets_dict:
        counts.append(count_words(tweets_dict[id]))
    return sorted(Counter(counts).iteritems(),key= lambda x: x[0],reverse=True)


def hashtags_freq(json):
    hashtags=[]
    for tweet in json:
        list = tweet["entities"]["hashtags"]
        if list:
            for item in list:
                hashtags.append(item[u'text'])
    return sorted(Counter(hashtags).iteritems(),key= lambda x: x[1],
                  reverse=True)

def mentions_freq(json):
    mentions=[]
    for tweet in json:
        user_list = tweet["entities"]["user_mentions"]
        if user_list:
            for user in user_list:
                mentions.append(user['name'])
    return sorted(Counter(mentions).iteritems(),key= lambda x: x[1],
                  reverse=True)

def urls_freq(json):
    urls=[]
    for tweet in json:
        url_list = tweet["entities"]["urls"]
        if url_list:
            for url in url_list:
                urls.append(url["display_url"])
    return sorted(Counter(urls).iteritems(),key= lambda x: x[1],
                  reverse=True)

def words_freq(json):
    words=[]
    for tweet in json:
        unicode = tweet['text'].decode('utf-8')
        for w in unicode.split():
            words.append(w)
    return sorted(Counter(words).iteritems(),key= lambda x: x[1],
                  reverse=True)


def plot_figure(label, filename, list_of_tuples):
     # save the word(names) and their respective frequencies separately
    xaxis = zip(*repr(list_of_tuples).decode("unicode-escape"))[0]
    yaxis = zip(*list_of_tuples)[1]
    x_pos = np.arange(len(list_of_tuples))

    # calculate slope and intercept for the linear trend line
    slope, intercept = np.polyfit(x_pos, yaxis, 1)
    trendline = intercept + (slope * x_pos)

    plt.plot(x_pos, trendline, color='red', linestyle='--')
    plt.bar(x_pos, yaxis,align='center')
    from matplotlib import rc
    import matplotlib as mpl
    mpl.rcParams['font.family'] = 'Arial'
    plt.xticks(x_pos,  xaxis)
    plt.ylabel(label)
    plt.savefig(filename)


if __name__ == '__main__':
    #api = init_twitter("./keys.json")
    #get_my_friends_ids(api)
    """year_ids = [12688864940, 22407857857101824, 166595393906413569,
                288970763451645952, 428511662610468864, 552963257116655617, 714176974076248064]
    old_id = year_ids[0]
    #for id in year_ids:
        get_tweets_from_friends('my_friends_ids.json',
                                'friends_tweets_06042016.json',
                                api, old_id, id )
        old_id = id"""
    #get_tweets_from_friends('my_friends_ids.json','friends_tweets.json',api)
    """counter=0
    with open('friends_tweets.json', 'r') as fp:
        for line in fp:
            if line.__contains__('"id":'):
                counter+=1
    print counter"""
    #tweets = extract_text('friends_tweets.json')
    #counts = word_len_distr(tweets)
    #for key, value in counts:
    #   print 'number of tweets with ', key, 'words: ', value
    #json_file = load_json('tweets[test].json')
    json_file = load_json('friends_tweets.json')
    #hashtags = hashtags_freq(json_file)
    #mentions = mentions_freq(json_file)
    #urls =  urls_freq(json_file)
    words =  words_freq(json_file)
    #print repr(words).decode("unicode-escape")
    #all_tweets = load_json('friends_tweets.json')
    #plot_figure('Word Frequencies','test-figure.png',words)
    #plot_figure('Hashtag Frequencies','hashtags.png',mentions)
    for key, value in words[:50]:
       print key
    print "here we change"
    for key, value in words[:50]:
       print value