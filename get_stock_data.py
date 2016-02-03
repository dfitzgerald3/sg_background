from bs4 import BeautifulSoup
import requests

def get_stock_data(ticker):
    
    ticker = str(ticker)
    
    url = 'http://finance.yahoo.com/q?s={}'.format(ticker.upper())
    
    r = requests.get(url)
    
    soup = BeautifulSoup(r.text)
    
    data = float(soup.find('span', attrs={'id':'yfs_l84_{}'.format(ticker.lower())}).text)
    
    return data