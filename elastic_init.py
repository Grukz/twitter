import json
import requests
from elasticsearch import Elasticsearch

def create_json_with_index():
    with open('./friends_tweets.json', 'r') as file:
        tweets = json.load(file)
        counter = 1
        with open('./testing_elastic.json','w')as file2:
            for tweet in tweets:
                file2.write('{"index":{"_index":"tweets","_type":"tweet",'
                            '"_id":"'+str(counter)+'"}}')
                counter += 1
                file2.write("\n")
                json.dump(tweet , file2)
                file2.write("\n")


def upload_doc(es, _id, doc_data={}):
    """
    get a single document as a python dictionary and create a document in
    elasticsearch
    :param es: elasticsearch engine
    :param _id: id of document
    :param doc_data: the dictionary containing the document
    :return:
    """
    es.create(index="tweets", doc_type="tweet", body=doc_data, id = _id)



if __name__ == '__main__':
    es = Elasticsearch(hosts='http://okeanos.gr:9200/')
    uri_search = 'http://okeanos.gr:9200/tweets/tweet/_search'
    uri_create = 'http://okeanos.gr:9200/tweets/tweet/'
    id = 0
    with open('testing_mongo.json', 'r') as fp:
        for line in fp:
            upload_doc(es, id, line)
            id += 1