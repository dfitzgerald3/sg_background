#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle
import nltk
from nltk.stem import *
from sklearn.feature_extraction import text

import mysqldb as connection
import time

stopwords = text.ENGLISH_STOP_WORDS
stemmer = LancasterStemmer()

f = open('/braden/descriptors_mf_stop.pickle', 'rb')
desc = pickle.load(f)
f.close()

def assign_security(tweet, sentiment):
    tokens = nltk.word_tokenize(tweet)
    clean_tokens = [word for word in tokens if word not in stopwords]
    
    for i in desc:
        value = 0
        
        for d in range(len(desc[i])):
            for a in desc[i][d]:
                for t in clean_tokens:
                    if t == a:
                        if d == 0:
                            value = 1.0
                            break
                        elif d == 1 or d == 2:
                            value = 0.5
                            break
                        elif d == 3:
                            value += 0.1
                            continue
        
           
                
        if value >= 0.3:
            sent = value * sentiment
#            print(sent)
#            print(i)
            
            c, conn = connection.connection()
            
            
            c.execute("INSERT INTO sentiment (symbol, sentiment, time) VALUES (%s, %s, %s)",
                      (i, sent, time.time()))
                      
            
            conn.commit()
            
            
            
            
     
     