from RuleBasedNlg import RuleBasedNlg

class State(object):

    def __init__(self):
        self.previous_user_sentence = ""
        self.previous_system_response = ""
        self.current_user_sentence = ""
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

    def action_item_init(self):
        d = dict()
        exchange = ["country1","country2"]
        USDX = ["time_start", "time_end"]
        query = ["stock_name","date"]
        get_exchange_rate = ["money_name", "action", "types"]
        d["exchange"] = exchange
        d["USDX"] = USDX
        d["query"] = query
        d["get_exchange_rate"] = get_exchange_rate
        return d

    def update(self,slot,intent,user_in):
        #print("slot",slot)
        #print("intent",intent)
        #print("user in",user_in)
        if intent == 'closing':
            self.intent[0][0] = 'closing'
            return
        if intent == 'confirm_yes':
            for key in self.confirm:
                self.mapping[key] = [self.confirm[key]]
            self.confirm.clear()
        elif intent == 'confirm_no':
            self.confirm.clear()
        else: 
            self.slot = slot
            self.intent = intent
            self.current_user_sentence = user_in
            sentence = self.current_user_sentence.strip().split()

            #print(sentence)
            for i in range(len(sentence)):
                if self.slot[0][i] != 'O':
                    sentence[i] = sentence[i].strip(',')
                    sentence[i] = sentence[i].strip('.')
                    sentence[i] = sentence[i].strip('?')    
                    sentence[i] = sentence[i].replace('\'s', "")
                    self.slot[0][i]  = self.slot[0][i].strip('B-')
                    self.slot[0][i]  = self.slot[0][i].strip('I-')
                    #import pdb; pdb.set_trace()
                    #print ("self.slot",self.slot)
                    if self.slot[1][i] < self.threshold :
                        self.confirm[slot[0][i]] = [sentence[i]]
                    else :
                        if self.slot[0][i] in self.mapping:
                            self.mapping[self.slot[0][i]].append(sentence[i])
                        else:
                            self.mapping[self.slot[0][i]] = [sentence[i]]
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


    def reply(self):
        if self.user_state == 1:
            if self.intent[0][0] == 'closing':
                return {'system_action':['closing'],'action_item':['closing'],'slot':[]}, 'At your service'
            for requirement in self.action_item_require[self.intent[0][0]]:
                sentence = self.mapping[requirement][0]
                for i in range(len(self.mapping[requirement]) - 1):
                    sentence += ' ' + self.mapping[requirement][i + 1]
                self.mapping[requirement] = sentence
            temp = dict()
            for key in self.mapping:
                if key != "O":
                    temp[key] = self.mapping[key]
            response = dict()
            response['system_action'] = ['response']
            response['action_item'] = [self.intent[0][0]]
            response['slot'] = temp
            temp = []
            for i in range(len(self.action_item_require[self.intent[0][0]])):
                temp.append(self.mapping[self.action_item_require[self.intent[0][0]][i]])
            result = RuleBasedNlg(self.intent[0][0], temp)
            return response, result

        elif self.user_state == 2:
            if len(self.confirm) != 0:  
                self.previous_user_sentence = self.current_user_sentence
                sentence = 'Do you mean '
                for key in self.confirm:
                    sentence += self.confirm[key] + ', '
                self.previous_system_response = sentence
                return {'system_action':['confirm_answer'],'action_item': [self.intent[0][0]], 'slot': self.confirm}, self.previous_system_response
            elif self.intent[0][0] == 'exchange':
                if 'country1' in self.requirement :
                    if 'country2' in self.requirement :
                        self.previous_user_sentence = self.current_user_sentence
                        self.previous_system_response = "Which two countries is the exchange rate between?"
                        return {'system_action':['request'],'action_item': ['exchange'], 'slot': ['country1', 'country2']}, self.previous_system_response
                    else :
                        self.previous_user_sentence = self.current_user_sentence
                        self.previous_system_response = "Which currency is the exchange rate against"
                        return {'system_action':['request'],'action_item': ['exchange'], 'slot': ['country1']}, self.previous_system_response
                else :
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "Which currency is the exchange rate against"
                    return {'system_action':['request'],'action_item': ['exchange'], 'slot': ['country2']}, self.previous_system_response
            elif self.intent[0][0] == 'USDX':
                if 'time_start' in self.requirement :
                    if 'time_end' in self.requirement :
                        self.previous_user_sentence = self.current_user_sentence
                        self.previous_system_response = "What time period is the USDX during?"
                        return {'system_action':['request'],'action_item': ['USDX'], 'slot': ['time_start','time_end']}, self.previous_system_response
                    else :
                        self.previous_user_sentence = self.current_user_sentence
                        self.previous_system_response = "What date does the time period of USDX start in?"
                        return {'system_action':['request'],'action_item': ['USDX'], 'slot': ['time_start']}, self.previous_system_response
                else :
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "What date does the time period of USDX end in?"
                    return {'system_action':['request'],'action_item': ['USDX'], 'slot': ['time_end']}, self.previous_system_response
            elif self.intent[0][0] == 'get_exchange_rate':
                #print(self.requirement)
                if 'money_name' in self.requirement :
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "Which currency would you like to exchange?"
                    return {'system_action':['request'],'action_item': ['get_exchange_rate'], 'slot': ['money_name']}, self.previous_system_response
                elif 'action' in self.requirement :
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "What would you like to do to this currency?"
                    return {'system_action':['request'],'action_item': ['get_exchange_rate'], 'slot': ['action']}, self.previous_system_response
                else :
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "Would u like to exchange with your account or cash?"
                    return {'system_action':['request'],'action_item': ['get_exchange_rate'], 'slot': ['types']}, self.previous_system_response
            else :
                if 'stock_name' in self.requirement :
                    if 'date' in self.requirement :
                        self.previous_user_sentence = self.current_user_sentence
                        self.previous_system_response = "which stock do you like to see and what day is it?"
                        return {'system_action':['request'],'action_item': ['query'], 'slot': ['stock_name','date']}, self.previous_system_response
                    else :
                        self.previous_user_sentence = self.current_user_sentence
                        self.previous_system_response = "which stock do you want?"
                        return {'system_action':['request'],'action_item': ['query'], 'slot': ['stock_name']}, self.previous_system_response
                else :
                    self.previous_user_sentence = self.current_user_sentence
                    self.previous_system_response = "what date would you like to see?"
                    return {'system_action':['request'],'action_item': ['query'], 'slot': ['date']}, self.previous_system_response
