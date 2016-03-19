#! /usr/bin/python

from mysqldb import connection
import pandas as pd
import time
import datetime


###############################################################################
#                       Create Stock SENTIMENT
###############################################################################


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
c.close()

###############################################################################
#                       Create INDEX SENTIMETN
###############################################################################

#Specify files with Weighting Schemes
files = ['dia_weights.csv',
         'qqq_weights.csv',
         'spy_weights.csv']
         
#Establish Connection with DB
c, conn = connection()


#Read each file for each index, get the sentiment, weighting scheme, and volume
for f in files:
    path = '/braden/index_data/' + f
    
    df = pd.read_csv(path)    
    df = df.drop(df.index[0])
    
    index = f[:3]
    index_sent = 0
    index_volume = 0
    
    for i in range(len(df)):
        try:
        
            symbol = df.symbol.iloc[i]
            weight = df.weight.iloc[i]
            
            c.execute("SELECT sentiment, time, volume FROM hourly WHERE time = (SELECT MAX(time) FROM hourly) AND symbol = %s", 
                      (symbol, ))        
                      
            sent_data = c.fetchone()
            
            index_sent += sent_data[0] * weight            
            time = sent_data[1]
            index_volume += sent_data[2]
            
        except Exception:
            continue

    c.execute("INSERT INTO indexes (time, symbol, sentiment, volume) values (%s, %s, %s, %s)", 
              (time, index, index_sent, index_volume))
    
    conn.commit()