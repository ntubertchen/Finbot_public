from RuleBasedNlg import RuleBasedNlg
from full_name2symbol import *
import dateparser
import random
from RNNNLG import RNNNLG

class State(object):

    def __init__(self):
        self.previous_user_sentence = ""
        self.previous_system_response = ""
        self.current_user_sentence = ""
        self.history = []
        self.slot = ''
        self.intent = []
        self.mapping = dict()
        self.action_item_require = self.action_item_init()
        self.user_state = 0
        self.requirement = []
        self.threshold = 0.3
        self.confirm = dict()
#        dialog = {'exchange':['Which currency is the exchange rate against?', 'Which two countries is the exchange rate between?'], 
#        'USDX':['What date does the time period of USDX start in?', 'What date does the time period of USDX end in?', 'What time period is the USDX during?'],
#        'get_exchange_rate':['Which currency would you like to exchange?', 'What would you like to do to this currency?', 'Would u like to exchange with your account or cash?'],
#        'query':['which stock do you want?', 'What date would you like to see?', 'Which stock do you like to see and what day is it?']}

    def refresh(self):
        self.previous_user_sentence = ""
        self.previous_system_response = ""
        self.current_user_sentence = ""
        self.history = []
        self.slot = ''
        self.intent = []
        self.mapping = dict()
        self.action_item_require = self.action_item_init()
        self.user_state = 0
        self.requirement = []
        self.threshold = 0
        self.confirm = dict()

    def action_item_init(self):
        d = dict()
        exchange = ["country1","country2"]
        USDX = ["time_start", "time_end"]
        query = ["stock_name","date"]
        get_exchange_rate = ["money_name", "action", "types"]
        confirm_yes = []
        confirm_no = []
        welcome = []
        d["exchange"] = exchange
        d["USDX"] = USDX
        d["query"] = query
        d["get_exchange_rate"] = get_exchange_rate
        d['confirm_yes'] = confirm_yes
        d['confirm_no'] = confirm_no
        d['welcome'] = welcome
        return d

    def update(self,slot,intent,user_in,w_in):
        self.history = []
        print("slot",slot)
        print("intent",intent)
        print("user in",user_in)
        if intent[0][0] == 'closing':
            self.intent[0][0] = 'closing'
            self.user_state = 0
            return
        elif intent[0][0] == 'welcome':
            self.intent = intent
            self.user_state = 2
            return
        if intent[0][0] == 'confirm_yes':
            for key in self.confirm:
                self.mapping[key] = [self.confirm[key][0]]
                #print(key, self.mapping[key])
            self.confirm.clear()
        elif intent[0][0] == 'confirm_no':
            self.confirm.clear()
            #print(self.intent)
        else: 
            self.slot = slot
            self.intent = intent
            self.current_user_sentence = user_in
            sentence = self.current_user_sentence.strip().split()
            self.history.append(self.intent[0][0])

            #print(sentence)
            for i in range(len(sentence)):
                seq = 0
                if self.slot[0][i] != 'O':
                    sentence[i] = sentence[i].strip(',')
                    sentence[i] = sentence[i].strip('.')
                    sentence[i] = sentence[i].strip('?')
                    sentence[i] = sentence[i].replace('\'s', "")
                    self.slot[0][i]  = self.slot[0][i].strip('B-')
                    self.slot[0][i]  = self.slot[0][i].strip('I-')
                    if self.slot[0][i] == 'date' or self.slot[0][i] == 'time_start' or self.slot[0][i] == 'time_end':
                        date_string = sentence[i]
                        j = i
                        while True:
                            if slot[0][j - 1] == 'date' or self.slot[0][j - 1] == 'time_start' or self.slot[0][j - 1] == 'time_end':
                                #print(sentence[j - 1] + '-----' + date_string)
                                date_string = sentence[j - 1] + ' ' + date_string
                                j = j - 1
                            else:
                                break
                        if i == len(sentence) - 1 or sentence[i + 1] == 'O':
                            date = dateparser.parse(date_string)
                            date = str(date)
                            date = date[0:10]
                            sentence[i] = date
                        print(sentence[i])
                    if self.slot[1][i] < self.threshold :
                        self.confirm[slot[0][i]] = [sentence[i]]
                    else :
                        if self.intent[0][0] == 'exchange':
                            if 'country1' in self.mapping:
                                if seq == 1:
                                    self.mapping['country1'].append(sentence[i])
                                else :
                                    if 'country2' in self.mapping:
                                        self.mapping['country2'].append(sentence[i])
                                    else:
                                        #print('2')
                                        self.mapping['country2'] = [sentence[i]]
                            else: 
                                self.mapping['country1'] = [sentence[i]]
                                #print('1')
                                seq = 1

                        else:
                            if self.slot[0][i] == 'date' or self.slot[0][i] == 'time_start' or self.slot[0][i] == 'time_end':
                                self.mapping[self.slot[0][i]] = [sentence[i]]
                            elif self.slot[0][i] in self.mapping:
                                print(self.mapping[self.slot[0][i]])
                                self.mapping[self.slot[0][i]].append(sentence[i])
                            else:
                                self.mapping[self.slot[0][i]] = [sentence[i]]
                    if self.slot[0][i] in self.history:
                        pass
                    else:
                        if self.slot[0][i] == 'country1' or self.slot[0][i] == 'country2':
                            self.history.append('country')
                        else:
                            self.history.append(self.slot[0][i])
                else: 
                    seq = 0
        if self.user_state == 0 or self.user_state == 2:
            #print(self.current_user_sentence)
            for i in range(len(self.action_item_require[self.intent[0][0]])):
                if self.action_item_require[self.intent[0][0]][i] in self.mapping:
                    if self.action_item_require[self.intent[0][0]][i] in self.requirement:
                        self.requirement.remove(self.action_item_require[self.intent[0][0]][i])
                else :
                    if not self.action_item_require[self.intent[0][0]][i] in self.requirement:
                        self.requirement.append(self.action_item_require[self.intent[0][0]][i])
            #print(len(self.requirement), len(self.confirm))
            if len(self.requirement) == 0 and len(self.confirm) == 0:
                self.user_state = 1
            else :
                self.user_state = 2


    def reply(self,w_s,w_i,w_sa):
        if self.user_state == 1:
            if self.intent[0][0] == 'closing':
                self.refresh()
                self.history.append('closing')
                return {'system_action':['closing'],'action_item':['closing'],'slot':[]}, 'At your service', 0
            for requirement in self.action_item_require[self.intent[0][0]]:
                sentence = self.mapping[requirement][0]
                print(len(self.mapping[requirement]))
                #print(sentence)
                for i in range(len(self.mapping[requirement]) - 1):
                    sentence += ' ' + self.mapping[requirement][i + 1]
                self.mapping[requirement] = sentence
                #print(sentence)
            temp = dict()
            for key in self.action_item_require[self.intent[0][0]]:
                temp[key] = self.mapping[key]
            response = dict()
            response['system_action'] = ['response']
            response['action_item'] = [self.intent[0][0]]
            response['slot'] = temp
            temp = []
            for i in range(len(self.action_item_require[self.intent[0][0]])):
                temp.append(self.mapping[self.action_item_require[self.intent[0][0]][i]])
            print(temp)
            result = RuleBasedNlg(self.intent[0][0], temp)
            self.refresh()
            self.history.append('response')
            return response, result, 0

        elif self.user_state == 2:
            if self.intent[0][0] == 'welcome':
                self.history.append('welcome')
                return {'system_action':['welcome'],'action_item': [self.intent[0][0]], 'slot': self.confirm}, "Hello, welcome to Finbot. I can:\n1. exchange between two currencies\n2. query US stock prices \n3. get exchange rate between Taiwan and foreign money \n4. check the USDX index\nHow may I help you?'", 0

            if self.intent[0][0] == 'query':
                if 'stock_name' in self.mapping:
                    sentence = self.mapping['stock_name'][0]
                    for i in range(len(self.mapping['stock_name']) - 1):
                        sentence += ' ' + self.mapping['stock_name'][i + 1]
                    result = query(name2sym(sentence), '2017-01-05')
                    if result == None:
                        print("None")
                        self.refresh()
                        return {'system_action':['stock_name_not_found']}, 'The name of stock is not found in database, sorry', 0
                if 'date' in self.mapping:
                    result = query('GOOG', self.mapping['date'][0])
                    if result == None:
                        print("None")
                        self.refresh()
                        return {'system_action':['date_not_found']}, 'The stock market is closed at this day, sorry', 0


            ran = (random.choice(self.requirement))
            a = RNNNLG()
            if len(self.confirm) != 0:  
                self.previous_user_sentence = self.current_user_sentence
                sentence = 'Do you mean '
                for key in self.confirm:
                    sentence += self.confirm[key][0] + ', '
                self.previous_system_response = sentence
                self.history.append('confirm_answer')
                return {'system_action':['confirm_answer'],'action_item': [self.intent[0][0]], 'slot': self.confirm}, self.previous_system_response, 0
            elif self.intent[0][0] == 'exchange':
                self.history.append('request')
                if 'country1' in  self.requirement:
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "Which currency is the exchange rate against"
                    self.history.append('country')
                    print('require country1')
                    return {'system_action':['request'],'action_item': ['exchange'], 'slot': ['country1']}, random.choice(a.generator('?request', 'country1')), 0
                elif 'country2' in  self.requirement:
                    #print(self.mapping['country1'])
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "Which currency is the exchange rate against"
                    self.history.append('country')
                    print('require country2')
                    return {'system_action':['request'],'action_item': ['exchange'], 'slot': ['country2']}, random.choice(a.generator('?request', 'country2')), 0
            elif self.intent[0][0] == 'USDX':
                self.history.append('request')
                if 'time_start' == ran :
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "What date does the time period of USDX start in?"
                    self.history.append('time_start')
                    return {'system_action':['request'],'action_item': ['USDX'], 'slot': ['time_start']}, random.choice(a.generator('?request', 'time_start')), 0
                elif 'time_end' == ran :
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "What date does the time period of USDX end in?"
                    self.history.append('time_end')
                    return {'system_action':['request'],'action_item': ['USDX'], 'slot': ['time_end']}, random.choice(a.generator('?request', 'time_end')), 0
            elif self.intent[0][0] == 'get_exchange_rate':
                self.history.append('request')
                #print(self.requirement)
                if 'money_name' == ran :
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "Which currency would you like to exchange?"
                    self.history.append('money_name')
                    return {'system_action':['request'],'action_item': ['get_exchange_rate'], 'slot': ['money_name']}, random.choice(a.generator('?request', 'money_name')), 0
                elif 'action' == ran :
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "What would you like to do to this currency?"
                    self.history.append('action')
                    return {'system_action':['request'],'action_item': ['get_exchange_rate'], 'slot': ['action']}, random.choice(a.generator('?request', 'action')), "quick_action"
                else :
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "Would u like to exchange with your account or cash?"
                    self.history.append('types')
                    return {'system_action':['request'],'action_item': ['get_exchange_rate'], 'slot': ['types']}, random.choice(a.generator('?request', 'types')), "quick_types"
            else :
                self.history.append('request')
                if 'stock_name' == ran :
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "which stock do you want?"
                    self.history.append('stock_name')
                    return {'system_action':['request'],'action_item': ['query'], 'slot': ['stock_name']}, random.choice(a.generator('?request', 'stock_name')), 0
                elif 'date' == ran:
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "what date would you like to see?"
                    self.history.append('date')
                    return {'system_action':['request'],'action_item': ['query'], 'slot': ['date']}, random.choice(a.generator('?request', 'date')), 0
