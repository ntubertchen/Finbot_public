import sqlite3
import matplotlib.pyplot as plt
#import numpy as np


def date_convert(date):
    tmp = date.split('/')
    dash = '-'
    return dash.join(tmp)

##given the full name return symbol
def USDX(start, end):
    conn = sqlite3.connect('USDX.db3')
    cursor = conn.cursor()
    cursor.execute('select Date, Close Close from DXY where Date between \'' + start + '\' and \'' + end + '\'')
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()

    if len(result) == 0:
        return None

    return result