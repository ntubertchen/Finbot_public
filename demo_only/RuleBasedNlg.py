from  exchange import exchange
from full_name2symbol import *

def RuleBasedNlg(action,slots):
    response = ''
    if action == 'exchange':
        if len(slots) == 2:
            rate = exchange(slots[0],slots[1])
            response = "The exchange rate from {0} to {1} is {2}".format( slots[0], slots[1], rate)
        else:
            response = "The exchange rate from {0} to {1} is {2}"
    elif action == 'get_exchange_rate':
        if len(slots)==3:
            currency = slots[0]
            ex_type = slots[1]
            direction = slots[2]
            rate = get_exchange_rate(slots[0],slots[1],slots[2])
            response = "The {1} exchange rate for {0} NTD {2} {3} is {4} in BANK OF TAIWAN".format(ex_type+'ing', direction, 'from' if ex_type == 'buy' else 'for', currency, rate)
        else:
            response = "The {1} exchange rate for {0} NTD {2} {3} is {4} in BANK OF TAIWAN"
    elif action == 'query':
        if len(slots) == 2:
            symbol = name2sym(slot[0])
            date = slot[1]
            data = query(symbol,date)
            item = ['openn', 'high', 'low', 'close', 'volume']
            response = "Share price on date {0}  ".format(date)
            for i in range(len(item)):
                response += "{0} : {1}     ".format(item[i],data[i])
        else:
            response = "Share price on date {0}  "
    return response 