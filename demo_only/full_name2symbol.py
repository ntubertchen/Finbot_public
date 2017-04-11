import sqlite3

##given the full name return symbol
def name2sym(string):
    conn = sqlite3.connect('share_data.db3')
    cursor = conn.cursor()
    string = string + '%'
    cursor.execute('select * from symbols where full_name like ?', (string,))
    result = cursor.fetchall()[0][0]
    cursor.close()
    conn.close()
    return result

##use symbol above to get share information at a given date
## symbol, date are both string
def query(symbol, date):
    conn = sqlite3.connect('share_data.db3')
    cursor = conn.cursor()
    cursor.execute("select * from '%s' where symbol=?"%date, (symbol,))
    a = cursor.fetchall()
    cursor.close()
    conn.close()
    openn = a[0][2]
    high = a[0][3]
    low = a[0][4]
    close = a[0][5]
    volume = a[0][6]
    adj_close = a[0][7]
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
        elif types == 'spot':
            return result[0][4]
    elif buy == 'sell':
        if types == 'cash':
            return result[0][1]
        elif types == 'spot':
            return result[0][2]