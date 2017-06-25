import sqlite3
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import requests

##given the full name return symbol
def name2sym(string):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(string)
    result = requests.get(url).json()
    for x in result['ResultSet']['Result']:
        return x['symbol']

##use symbol above to get share information at a given date
## symbol, date are both string
def query(symbol, date):
    tickers = [symbol]
    data_source = 'google'
    start_date = date
    end_date = date
    try:
        panel_data = data.DataReader(tickers, data_source, start_date, end_date)
    except Exception as e:
        print("1")
        return None
    if len(panel_data.major_axis) == 0:
        print('2')
        return None


    for i in range(len(panel_data.major_axis)):
        openn = panel_data['Open'][symbol][panel_data.major_axis[i]]
        high = panel_data['High'][symbol][panel_data.major_axis[i]]
        low = panel_data['Low'][symbol][panel_data.major_axis[i]]
        close = panel_data['Close'][symbol][panel_data.major_axis[i]]
        volume = panel_data['Volume'][symbol][panel_data.major_axis[i]]
        adj_close = panel_data['Close'][symbol][panel_data.major_axis[i]]
    return openn, high, low, close, volume, adj_close

# buy = 'buy' or 'sell'
# type = 'cash' or 'spot'
def get_exchange_rate(money_name, buy, types):
    conn = sqlite3.connect('share_data.db3')
    cursor = conn.cursor()
    cursor.execute('select * from exchange_rate where money_name=?', (money_name,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if buy == 'buy':
        if types == 'cash':
            return result[0][3]
        elif types == 'account':
            return result[0][4]
    elif buy == 'sell':
        if types == 'cash':
            return result[0][1]
        elif types == 'account':
            return result[0][2]
