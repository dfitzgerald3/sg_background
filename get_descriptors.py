# -*- coding: utf-8 -*-
"""
Created on Mon Jan 04 06:11:09 2016

@author: Dudz
"""

import pandas as pd
import wikipedia
import nltk
import pickle

f = 'C:\Users\Dudz\Documents\Personal\Project\Coding\NLP\Twitter_stocks\data\\tickers\s&p500_stocks.csv'

df = pd.read_csv(f)

descriptors ={}

for i in range(len(df)):
    try:
        summary = wikipedia.summary(df['Security'].iloc[i]).lower()
        tokens = nltk.word_tokenize(summary)
        pos = nltk.pos_tag(tokens)
            
        symbol = df['Ticker symbol'].iloc[i].lower()
        security = df['Security'].iloc[i].lower()
        sector = df['GICS\xa0Sector'].iloc[i].lower()
        sub_sector = df['GICS Sub Industry'].iloc[i].lower()
        
        security_info = [[symbol, security], [sector, sub_sector]]
        summary_desc = []
        
        for p in pos:
            if p[1] in ['NN', 'NNS', 'JJ']:
                summary_desc.append(p[0])
        
        security_info.append(set(summary_desc))
        
        d = {str(symbol): security_info}
        
        descriptors.update(d)  
        
        print i
    
    except Exception:
        continue
    
    
f = open('descriptors2.pickle', 'wb')
pickle.dump(descriptors, f)
f.close()    