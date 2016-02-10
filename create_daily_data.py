#! /usr/bin/python

from mysqldb import connection
import pandas as pd
import pandas.io.data as web
import time
import datetime


#Query MySQL and find values within that last day
time_after = datetime.datetime.now() - datetime.timedelta(days=1)
time_after = datetime.datetime(time_after.year, time_after.month, time_after.day)
unix_time_after = time.mktime(time_after.timetuple())

c, conn = connection()
c.execute("SELECT * FROM sentiment WHERE time > %s", (unix_time_after,))
data = c.fetchall()


#Push data to DataFrame to perform GroupBy operations
symbol = []
sentiment = []
date = []

for i in data:
    symbol.append(i[0])
    sentiment.append(i[1])
    date.append(datetime.datetime.fromtimestamp(int(i[2])))

df = pd.DataFrame(symbol)
df['sentiment'] = sentiment
df['date'] = date

transform = lambda x: x.day
day = df['date'].apply(transform)
df['day'] = day
df.columns = ['symbol', 'sentiment', 'date', 'day']
stats = df.groupby('symbol')['sentiment'].agg(['mean', 'count'])


#Format data and push to MySQL daily table
now =  datetime.datetime.now() - datetime.timedelta(days=1)
now_daily = datetime.datetime(now.year, now.month, now.day)
unix_now = time.mktime(now_daily.timetuple())

#Retrieve financial data for stocks
start = now_daily
end = now_daily
if start.weekday() < 5:
    for i in range(len(stats)):
        try:
            f = web.DataReader(stats.index[i], 'yahoo', start, end, retry_count=10, pause=0.5)    
            
            c.execute("INSERT INTO daily (date, symbol, open, close, high, low, sentiment, volume) values (%s, %s, %s, %s, %s, %s, %s, %s)", 
                  (unix_now, stats.index[i], f['Open'].values[0], f['Close'].values[0], f['High'].values[0], f['Low'].values[0], stats['mean'][i], stats['count'][i]))
        except Exception:
            continue
        
    conn.commit()
