#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import mysqldb as connection
import datetime
import pandas as pd

def retrieve_sentiment(sym):
    sym = str(sym)
        
    c, conn = connection.connection()
        
    c.execute("SELECT * FROM sentiment WHERE symbol = %s", (sym,))
    
    data = c.fetchall()
    
    symbol = []
    sentiment = []
    time = []
    
    for i in data:
        symbol.append(i[0])
        sentiment.append(i[1])
#        time.append(datetime.datetime.fromtimestamp(int(i[2])).strftime('%Y-%m-%d %H:%M'))
        time.append(datetime.datetime.fromtimestamp(int(i[2])))
    
    df = pd.DataFrame(symbol)
    df['sentiment'] = sentiment
    df['time'] = time
    
    return df
    
    
    