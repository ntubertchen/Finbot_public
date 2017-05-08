from  exchange import exchange
from full_name2symbol import *
from USDX import USDX

def RuleBasedNlg(action,slots):
    response = ''
    data = None
    if action == 'exchange':
        data = exchange(slots[0],slots[1])
        response = "The exchange rate from {0} to {1} is {2}".format( slots[0], slots[1], data)

    elif action == 'get_exchange_rate':
        currency = slots[0]
        ex_type = slots[1]
        direction = slots[2]
        data = get_exchange_rate(slots[0],slots[1],slots[2])
        response = "The {1} exchange rate for {0} NTD {2} {3} is {4} in BANK OF TAIWAN".format(ex_type+'ing', direction, 'from' if ex_type == 'buy' else 'for', currency, data)

    elif action == 'query':
        symbol = name2sym(slots[0])
        date = slots[1]
        data = query(symbol,date)
        item = ['openn', 'high', 'low', 'close', 'volume']
        response = "Share price on date {0}  ".format(date)
        for i in range(len(item)):
            response += "{0} : {1}     ".format(item[i],data[i])
    elif action == 'USDX':
        data = USDX( slots[0], slots[1])
        for i in range(len(data)):
            response += 'Date: ' + data[i][0] + "     USDX: " + data[i][1] + '\n'
    if data == None:
        response = 'Cannot find the match information. Sincerely appologize.'

    return response 