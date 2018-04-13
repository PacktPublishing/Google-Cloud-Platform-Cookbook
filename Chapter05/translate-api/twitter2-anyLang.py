# -*- coding: utf-8 -*-
"""
Extract data from Twitter and translate the tweets to a specific language

@author: Legorie
"""

import json
import argparse

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from google.cloud import translate

#Variables that contains the user credentials to access Twitter API
## Note: It is never a good idea to hardcode keys in the code.
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

def detect_translate(text, target_lang):
    
    translate_client = translate.Client()

    # Send the tweet text to the API and detects the language
    result = translate_client.detect_language(text)

    print(u'Tweet Text: {}'.format(text))
    print('Language: {}'.format(result['language']))

    # Checks if the detected language is in the target language
    # else the translation API is invoked to get the text translated
    if result['language'] != target_lang :
        translation = translate_client.translate(text,
            target_language=target_lang)
        print(u'Translation: {}'.format(translation['translatedText']))


class StdOutListener(StreamListener):

    def on_data(self, data):
        jdata = json.loads(data)
        #print(jdata['text'])
        detect_translate(jdata['text'], target_lang)
        print("------")
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('target_lang', help='Set your target language (use iso-639-1 codes) e.g: en, fr, ru, ja')

    args = parser.parse_args()
    target_lang = args.target_lang

    #A Tweepy streaming session is instantiated to receive the Twitter stream
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['news'])
