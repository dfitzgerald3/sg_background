# -*- coding: utf-8 -*-
"""
Created on Fri Jan 01 17:28:40 2016

@author: Dudz
"""

import os
from os.path import join

from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn import metrics

import nltk
from nltk.stem import *

from statistics import mode
import numpy as np

import pickle



#Import files with sentiment data
pos_path = 'C:\\Users\\Dudz\\Documents\\Personal\\Project\\Coding\\NLP\\Twitter_stocks\\data\\aclImdb\\train\\pos'
pos_path_test = 'C:\\Users\\Dudz\\Documents\\Personal\\Project\\Coding\\NLP\\Twitter_stocks\\data\\aclImdb\\test\\pos'
neg_path = 'C:\\Users\\Dudz\\Documents\\Personal\\Project\\Coding\\NLP\\Twitter_stocks\\data\\aclImdb\\train\\neg'
neg_path_test = 'C:\\Users\\Dudz\\Documents\\Personal\\Project\\Coding\\NLP\\Twitter_stocks\\data\\aclImdb\\test\\neg'


#Function to process data
def data_prep(f, sentiment):
    array = []
    for file in os.listdir(f):
        try:
            file = join(f, file)
            array.append([open(file, "r").read(), sentiment])
        except Exception:
            continue
    
    return array

pos_files = data_prep(pos_path, 'pos')
neg_files = data_prep(neg_path, 'neg')


#Tokenize, clean, and stem data in preperation for training
stopwords = text.ENGLISH_STOP_WORDS

stemmer = LancasterStemmer()


X = []
y = []

for i in pos_files:
    try:
        tokens = nltk.word_tokenize(i[0].lower())
        clean_tokens = [word for word in tokens if word not in stopwords]
        stem_words = [stemmer.stem(token) for token in clean_tokens]
        X.append(" ".join(stem_words))
        y.append(i[1])
    except Exception:
        continue
    
for i in neg_files:
    try:
        tokens = nltk.word_tokenize(i[0].lower())
        clean_tokens = [word for word in tokens if word not in stopwords]
        stem_words = [stemmer.stem(token) for token in clean_tokens]
        X.append(" ".join(stem_words))
        y.append(i[1])
    except Exception:
        continue
    


#Create a training and test dataset from cleaned data   
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


#Use the TfidfVectorizer
tf_vect = TfidfVectorizer()
X_train = tf_vect.fit_transform(X_train)
X_test = tf_vect.transform(X_test)

tfidf_f = open("pickled_algos/tfidf.pickle", "wb")
pickle.dump(tf_vect, tfidf_f)
tfidf_f.close()



#SGDClassifier Classifier
clf_SGDClassifier = SGDClassifier(n_jobs=-1).fit(X_train, y_train)
predicted_SGDClassifier = clf_SGDClassifier.predict(X_test)
accuracy_SGDClassifier = np.mean(predicted_SGDClassifier == y_test)

clf_SGDClassifier_f = open("pickled_algos/clf_SGDClassifier.pickle", "wb")
pickle.dump(clf_SGDClassifier, clf_SGDClassifier_f)
clf_SGDClassifier_f.close()

print('SGDClassifier accuracy: %s' %accuracy_SGDClassifier)
print(metrics.classification_report(predicted_SGDClassifier, y_test))



#LogisticRegression Classifier
clf_LogisticRegression = LogisticRegression(n_jobs=-1).fit(X_train, y_train)
predicted_LogisticRegression = clf_LogisticRegression.predict(X_test)
accuracy_LogisticRegression = np.mean(predicted_LogisticRegression == y_test)

clf_LogisticRegression_f = open("pickled_algos/clf_LogisticRegression.pickle", "wb")
pickle.dump(clf_LogisticRegression, clf_LogisticRegression_f)
clf_LogisticRegression_f.close()

print('LogisticRegression accuracy: %s' %accuracy_LogisticRegression)
print(metrics.classification_report(predicted_LogisticRegression, y_test))



#NuSVC Classifier
clf_NuSVC = NuSVC().fit(X_train, y_train)
predicted_NuSVC = clf_NuSVC.predict(X_test)
accuracy_NuSVC = np.mean(predicted_NuSVC == y_test)

clf_NuSVC_f = open("pickled_algos/clf_NuSVC.pickle", "wb")
pickle.dump(clf_NuSVC, clf_NuSVC_f)
clf_NuSVC_f.close()

print('NuSVC accuracy: %s' %accuracy_NuSVC)
print(metrics.classification_report(predicted_NuSVC, y_test))



#LinearSVC Classifier
clf_LinearSVC = LinearSVC().fit(X_train, y_train)
predicted_LinearSVC = clf_LinearSVC.predict(X_test)
accuracy_LinearSVC = np.mean(predicted_LinearSVC == y_test)

clf_LinearSVC_f = open("pickled_algos/clf_LinearSVC.pickle", "wb")
pickle.dump(clf_LinearSVC, clf_LinearSVC_f)
clf_LinearSVC_f.close()

print('LinearSVC accuracy: %s' %accuracy_LinearSVC)
print(metrics.classification_report(predicted_LinearSVC, y_test))



#BernoulliNB Classifier
clf_BernoulliNB = BernoulliNB().fit(X_train, y_train)
predicted_BernoulliNB = clf_BernoulliNB.predict(X_test)
accuracy_BernoulliNB = np.mean(predicted_BernoulliNB == y_test)

clf_BernoulliNB_f = open("pickled_algos/clf_BernoulliNB.pickle", "wb")
pickle.dump(clf_BernoulliNB, clf_BernoulliNB_f)
clf_BernoulliNB_f.close()

print('BernoulliNB accuracy: %s' %accuracy_BernoulliNB)
print(metrics.classification_report(predicted_BernoulliNB, y_test))



#MultinomialNB Classifier
clf_MultinomialNB = MultinomialNB().fit(X_train, y_train)
predicted_MultinomialNB = clf_MultinomialNB.predict(X_test)
accuracy_MultinomialNB = np.mean(predicted_MultinomialNB == y_test)

clf_MultinomialNB_f = open("pickled_algos/clf_MultinomialNB.pickle", "wb")
pickle.dump(clf_MultinomialNB, clf_MultinomialNB_f)
clf_MultinomialNB_f.close()

print('MultinomialNB accuracy: %s' %accuracy_MultinomialNB)
print(metrics.classification_report(predicted_MultinomialNB, y_test))





def prepare_text(text):
    tweet_text = []
    try:
        tokens = nltk.word_tokenize(text.lower())
        clean_tokens = [word for word in tokens if word not in stopwords]
        stem_words = [stemmer.stem(token) for token in clean_tokens]
        tweet_text.append(" ".join(stem_words))
        X_test = tf_vect.transform(tweet_text)
        
    except Exception:
        pass
    
    return X_test
    
def predict_sentiment(tweet):
    predicted = []
    for i in [clf_SGDClassifier, clf_LogisticRegression, clf_NuSVC, clf_LinearSVC, clf_MultinomialNB]:
        y_pred = i.predict(tweet)
        predicted.append(y_pred)
        
    for x in range(len(predicted)):
        if predicted[x] == 'pos':
            predicted[x] = 1
        else:
            predicted[x] = 0
    
    sentiment = mode(predicted)
    sentiment_count = predicted.count(sentiment)
    confidence = (sentiment_count / len(predicted)) * 100
    
    return sentiment, confidence

        
