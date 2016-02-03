#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from os.path import join

from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.metrics import accuracy_score

import nltk
from nltk.stem import *

from statistics import mode


import pickle

stopwords = text.ENGLISH_STOP_WORDS
stemmer = LancasterStemmer()


tf_vect_f = open("/braden/pickled_algos/tfidf.pickle", "rb")
tf_vect = pickle.load(tf_vect_f)

#Import pickled classifiers and tokenizers
#clf_GaussianNB = pickle.load(open("pickled_algos/clf_GaussianNB.pickle", "rb")) 
clf_MultinomialNB = pickle.load(open("/braden/pickled_algos/clf_MultinomialNB.pickle", "rb")) 
#clf_BernoulliNB = pickle.load(open("pickled_algos/clf_BernoulliNB.pickle", "rb")) 
clf_LogisticRegression = pickle.load(open("/braden/pickled_algos/clf_LogisticRegression.pickle", "rb")) 
clf_SGDClassifier = pickle.load(open("/braden/pickled_algos/clf_SGDClassifier.pickle", "rb"))  
clf_LinearSVC = pickle.load(open("/braden/pickled_algos/clf_LinearSVC.pickle", "rb")) 
clf_NuSVC = pickle.load(open("/braden/pickled_algos/clf_NuSVC.pickle", "rb"))

def prepare_text(text):
    tweet_text = []
    try:
        tokens = nltk.word_tokenize(text.lower())
        clean_tokens = [word for word in tokens if word not in stopwords]
        stem_words = [stemmer.stem(token) for token in clean_tokens]
        tweet_text.append(" ".join(stem_words))
        X_test = tf_vect.transform(tweet_text)
                
        return X_test

    except Exception:
        pass
    
    

def predict_sentiment(tweet):
    vectors = prepare_text(tweet)
    
    predicted = []
    for i in [clf_SGDClassifier, clf_LogisticRegression, clf_NuSVC, clf_LinearSVC, clf_MultinomialNB]:
        y_pred = i.predict(vectors)
        predicted.append(y_pred)
        
    for x in range(len(predicted)):
        if predicted[x] == 'pos':
            predicted[x] = 1
        else:
            predicted[x] = -1
    
    sentiment = mode(predicted)
    sentiment_count = predicted.count(sentiment)
    confidence = (sentiment_count / len(predicted)) * 100
    
    return sentiment, confidence
    
    

