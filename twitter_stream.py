#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import json

import sentiment as s

import assign_security as assign_security


import time


#consumer key, consumer secret, access token, access secret.
consumer_key ="hlmWGateQSHOryzEUgzvbHRGs"
consumer_secret ="crZ0bIwfjA9gh6lLqmwiXEZW9LS2JKz0Af64dKmiszEtXYxi7p"
access_token ="4548821234-jUACxmbBAIU8YIZifCmbzJtEbSSUxszuMI7PIPj"
access_token_secret ="TErfkU6X6obGuGnZBL8yAR1XvtxPKhcq4RijjtJjv5Fq0"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        try:
            tweet = all_data['text']
            sentiment, confidence = s.predict_sentiment(tweet)
                        
            
            if confidence > 70:
                assign_security.assign_security(tweet, sentiment)
                                
                
        except Exception:
            pass
        
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    
    while True:
        try:
            #This handles Twitter authetification and the connection to Twitter Streaming API
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, l, timeout=60)
        
            #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
            stream.filter(languages=['en'], track=['the', 'i', 'to', 'a', 'and', 'is', 'in', 'it', 'you', 'of', 'for'])
        
        except Exception as e:
            print("Error. Restarting Stream")
            time.sleep(5)
            
