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
    dates = ['20170102', '20170103','20170104','20170105','20170109','20170110','20170111','20170113','20170118','20170120','20170123','20170124','20170125','20170125','20170131','20170203','20170206','20170207','20170208','20170209','20170210','20170213','20170214','20170215','20170216','20170217','20170223','20170224','20170227','20170228','20170301','20170302','20170303','20170306','20170308','20170309','20170310','20170313','20170314','20170321','20170322','20170324','20170327','20170328','20170329','20170330','20170331',]
    if date not in dates:
        return None
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
        elif types == 'account':
            return result[0][4]
    elif buy == 'sell':
        if types == 'cash':
            return result[0][1]
        elif types == 'account':
            return result[0][2]