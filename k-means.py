from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics
import logging
from optparse import OptionParser
import sys
from time import time
import matplotlib.pyplot as plt
import pylab as pl

import numpy as np
import crawl

def greek_stopwords(file):
    stopwords = []
    with open(file, 'r')as fp:
        for word in fp:
            stopwords.append(unicode(word, 'utf-8'))
    return stopwords

def ClusterIndicesNumpy(clustNum, labels_array): #numpy
    return np.where(labels_array == clustNum)[0]

def ClusterIndicesComp(clustNum, labels_array): #list comprehension
    return np.array([i for i, x in enumerate(labels_array) if x == clustNum])

if __name__ == '__main__':
    new_file = crawl.load_json('FINAL_TEST.json')
    stopwords = greek_stopwords(
            'greek_stopwords.txt')
    vectorizer = TfidfVectorizer(analyzer='word', max_df=0.5,
                                 use_idf=True, stop_words=stopwords)
    X = vectorizer.fit_transform(tweet["text"] for tweet in new_file)
    km = KMeans(n_clusters=7, init='k-means++', max_iter=100, n_init=3,
                verbose='verbose')
    print("Clustering sparse data with %s" % km)
    t0 = time()
    km.fit(X)
    print("done in %0.3fs" % (time() - t0))
    print()
    print("Clusters :")
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    labels = km.labels_
    terms = vectorizer.get_feature_names()
    for i in range(7):
        ds = X[np.where(labels==i)]
        print "Cluster %d:" % i
        print "       size of cluster : ",\
            len(ClusterIndicesNumpy(i, km.labels_))
        print "       top terms : ",
        for ind in order_centroids[i, :10]:
            print ' %s' % terms[ind],
        print

