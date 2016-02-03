# -*- coding: utf-8 -*-
"""
Created on Mon Jan 04 06:11:09 2016

@author: Dudz
"""

import pandas as pd
import urllib2
from bs4 import BeautifulSoup
import nltk
import pickle
from sklearn.feature_extraction import text

f = 'C:\\Users\\Dudz\\Documents\\Personal\\Project\\Coding\\NLP\\Twitter_stocks\\data\\tickers\\sp500_stocks.csv'

df = pd.read_csv(f)

descriptors ={}

stopwords = text.ENGLISH_STOP_WORDS

for i in range(len(df)):
    try:
        symbol = df['Ticker symbol'].iloc[i].lower()
        security = df['Security'].iloc[i].lower()
        sector = df['GICS\xa0Sector'].iloc[i].lower()
        sub_sector = df['GICS Sub Industry'].iloc[i].lower()
        
        security_info = [[symbol, security], [sector, sub_sector]]
        
        url = 'http://finance.yahoo.com/q/pr?s=' + str(symbol).upper() + '+Profile'
        page = urllib2.urlopen(url)
        
        soup = BeautifulSoup(page)
        summary = soup.find_all('p')[1].text.strip()
        
        tokens = nltk.word_tokenize(summary.lower())
        
        clean_tokens = []
        
        for t in tokens:
            if t not in stopwords:
                clean_tokens.append(t)
        
        pos = nltk.pos_tag(clean_tokens)
        
        summary_desc = []
        
        for p in pos:
            if p[1] in ['NN', 'NNS', 'NNP', 'NNPS']:
                summary_desc.append(p[0])
        
        security_info.append(set(summary_desc))
        
        d = {str(symbol): security_info}
        
        descriptors.update(d)  
        
        print security_info
    
    except Exception:
        continue
    
    
f = open('descriptors_yahoo.pickle', 'wb')
pickle.dump(descriptors, f)
f.close()    