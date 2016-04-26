# -*- coding: utf-8 -*-
import string
import json
import codecs
from crawl import load_json, extract_text, word_len_distr

def normalize_as_list(tweet):
    list = []
    exclude = set(string.punctuation)
    for special in exclude:
        tweet = [ch.replace(special, ' ') for ch in tweet]
    tweet = ''.join(ch for ch in tweet if ch not in exclude)
    for word in tweet.split():
        word = word.decode("utf-8")
        if len(word) <= 3:
            pass
        else:
            list.append(word)
    return list

def greek_stopwords(file):
    stopwords = []
    with codecs.open(file, 'r', encoding='utf-8')as fp:
        for word in fp:
            stopwords.append(word.strip())
    return stopwords

def normalize(tweet):
    list = []
    exclude = set(string.punctuation)
    for special in exclude:
        tweet = [ch.replace(special, ' ') for ch in tweet]

    tweet = ''.join(ch for ch in tweet if ch not in exclude)
    stopwords = greek_stopwords(
            'greek_stopwords.txt')
    tweet = ' '.join(word for word in tweet.split() if word.lower() not in
                     stopwords)
    return tweet


def json_rebuild(oldfile, newfile):
    """
    Give old and new filenames and replace ascii characters with normal
    unicodes ones in the new file
    :param oldfile:
    :param newfile:
    :return:
    """
    file = load_json(oldfile)
    for tweet in file:
        tweet['text'] = normalize(unicode(tweet['text']))
    with open(newfile, 'w') as fp:
        json.dump(file, fp, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    json_rebuild('friends_tweets.json', 'FINAL_TEST.json')
