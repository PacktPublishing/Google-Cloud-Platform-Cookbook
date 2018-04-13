# -*- coding: utf-8 -*-
"""
Extract data from Twitter and upload to BigQuery Table

@author: Legorie
"""

import json
import argparse

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from google.cloud import bigquery

#Variables that contains the user credentials to access Twitter API
## Note: It is never a good idea to hardcode keys in the code.
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

#Hardcoded values for BigQuery
bq_dataset_name = "TwitterData"
bq_table_name = "theTweets"
project_id = ""

def upload_bigQuery(name, text):
    bigquery_client = bigquery.Client(project=project_id)
    dataset_ref = bigquery_client.dataset(bq_dataset_name)
    table_ref = dataset_ref.table(bq_table_name)

    # Get the table from the API so that the schema is available.
    table = bigquery_client.get_table(table_ref)    

    rows_to_insert = [
     (name, text)
    ]    

    errors = bigquery_client.create_rows(table, rows_to_insert)  # API request

    if not errors:
        print('Loaded 1 row into table')
    else:
        print('Errors:')
        print(errors)

class StdOutListener(StreamListener):

    def on_data(self, data):
        jdata = json.loads(data)
        print(jdata['user']['screen_name'], jdata['text'])
        upload_bigQuery(jdata['user']['screen_name'], jdata['text'])
        print("---")
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('project_id', help='Your Cloud Platform project ID.')

    args = parser.parse_args()
    project_id = args.project_id

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['GCP','Google Cloud'])
