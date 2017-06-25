from full_name2symbol import *
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
from state import State
import dateparser
from USDX import *

# date = dateparser.parse('')
# date = str(date)
# date = date[0:10]
# print(date)

# symbol = name2sym('Alphabet')
# print(symbol)
# print(query('GOOG', '2017-01-05'))

# date = 'today'
# tickers = [symbol]
# data_source = 'google'
# start_date = date
# end_date = date
# print(data.DataReader(tickers, data_source, start_date, end_date))



a = State()
#slot,intent,user_in

slot = [['O'],[0.7]]
intent = [['welcome'], [0.6]]
user_in = 'Greetings'
a.update(slot, intent, user_in, 2)
print(a.reply(1, 2, 3))
print('\n')

# slot = [['O', 'O', 'B-country', 'O', 'B-country'],[0.7, 0.2, 0.6, 0.1, 0.7]]
# intent = [['exchange'], [0.6]]
# user_in = 'Start in USD to CNY'
# a.update(slot, intent, user_in, 2)
# print(a.reply(1, 2, 3))
# print(a.history)
# print('\n')

slot = [['O', 'O', 'O'],[0.7, 0.2, 0.6]]
intent = [['exchange'], [0.6]]
user_in = 'Start in CNY'
a.update(slot, intent, user_in, 2)
print(a.reply(1, 2, 3))
print(a.history)	
print('\n')

# slot = [['O', 'O', 'B-country'],[0.7, 0.2, 0.6]]
# intent = [['exchange'], [0.6]]
# user_in = 'Start in CNY'
# a.update(slot, intent, user_in, 2)
# print(a.reply(1, 2, 3))
# print(a.history)	
# print('\n')

# slot = [['O', 'O', 'B-date'],[0.7, 0.2, 0.6,]]
# intent = [['query'], [0.6]]
# user_in = 'Start in 2017-01-01'
# a.update(slot, intent, user_in, 2)
# print(a.reply(1, 2, 3))
# print(a.history)
# print('\n')

# slot = [['O', 'O', 'time_start'],[0.7, 0.2, 0.6]]
# intent = [['USDX'], [0.6]]
# user_in = 'Start in 2017-04-01'
# a.update(slot, intent, user_in, 2)
# print(a.reply(1, 2, 3))
# #print(a.history)
# print('\n')

# slot = [['O', 'O', 'B-time_end', 'I-time_end', 'I-time_end'],[0.7, 0.2, 0.6, 0.6, 0.6]]
# intent = [['USDX'], [0.6]]
# user_in = '	Start in June 25 2017'
# a.update(slot, intent, user_in, 2)
# print(a.reply(1, 2, 3)[1])
# #print(a.history)
# print('\n')

# slot = [['stock_name'],[0.7]]
# intent = [['query'], [0.6]]
# user_in = 'Apple'
# a.update(slot, intent, user_in, 2)
# print(a.reply(1, 2, 3))
# print('\n')


# slot = [['O', 'O', 'B-date', 'I-date', 'I-date'],[0.7, 0.2, 0.5, 0.8, 0.9]]
# intent = [['query'], [0.6]]
# user_in = 'End in June 15 2015'
# a.update(slot, intent, user_in, 2)
# print(a.reply(1, 2, 3))
# print('\n')

# print(USDX('2017-05-01', '2017-05-25'))