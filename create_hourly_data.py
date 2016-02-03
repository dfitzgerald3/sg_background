#! /usr/bin/python

from mysqldb import connection
import pandas as pd
import time
import datetime


#Query MySQL and find values within that last hour
time_greater_than = datetime.datetime.now() - datetime.timedelta(hours=1)
unix_time_greater_than = time.mktime(time_greater_than.timetuple())

c, conn = connection()
c.execute("SELECT * FROM sentiment WHERE time > %s", (unix_time_greater_than,))
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

transform = lambda x: x.hour
hour = df['date'].apply(transform)
df['hour'] = hour
df.columns = ['symbol', 'sentiment', 'date', 'hour']
stats = df.groupby('symbol')['sentiment'].agg(['mean', 'count'])


#Formate data and push to MySQL hourly table
now =  datetime.datetime.now()
now_hourly = datetime.datetime(now.year, now.month, now.day, now.hour)
unix_now = time.mktime(now_hourly.timetuple())


for i in range(len(stats)):
    c.execute("INSERT INTO hourly (time, symbol, sentiment, volume) values (%s, %s, %s, %s)", 
          (unix_now, stats.index[i], stats['mean'][i], stats['count'][i]))

conn.commit()