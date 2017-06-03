from episoda import *
import pdb
from pprint import pprint
class RLSimulator(object):
    """docstring for RuleSimulator"""
    def __init__(self):
        #super(RuleSimulator, self).__init__()
        self.initialize_episode()

    def initialize_episode(self):
        self.episode_over = False
        self.success = False
        self.goal = episode(object) #random generate a user goal
        assert (self.episode_over != 1),' but we just started'
        self.system_turns = 0.
        self.system_correct = 0.
        self.error = False
        self.syserr = False
        self.last_system_action = None
        self.reward = 0
        self.inform_slots = {}
        for i in self.goal.inform_slots:
            self.inform_slots[i] = 0
    def next(self, system_action):
        """ Generate next User Action based on last System Action """
        
        self.system_turns += 1
        
        ##get system action
        sys_act = system_action['system_action'][0]
        nl_response = None
        if sys_act == "closing":
            nl_response = ""
            sys = 0
            self.episode_over = True
            self.system_turns -= 1
            self.reward = 0
            if self.success == False:
                self.reward = -5             
        elif sys_act == "response":
            nl_response = self.response_response(system_action)
        elif sys_act == "confirm_intent":
            nl_response = self.response_confirm_intent(system_action)     
        elif system_action['action_item'][0] != self.goal.goal:
            self.reward = -5
            nl_response = self.action_item_error(system_action)
        elif sys_act == "inform":
            nl_response = self.response_inform(system_action)
        elif sys_act == "request":
            nl_response = self.response_request(system_action) 
        elif sys_act == "confirm_slot":
            nl_response = self.response_confirm_slot(system_action)
                         
        return nl_response
    def action_item_error(self,system_action):
        response = []
        print("[SIM]: wrong action_item")
        response.append(str("I don't understand what you are talking about."))
        response.append(str("What the fuck are you saying,")+str(initializer(self.goal)))
        return random.choice(response)
    def response_confirm_intent(self, system_action):
        response = None
        if system_action['action_item'][0] != self.goal.goal:
            self.reward = 2
            response = "No."
        else:
            self.reward = 0
            response = "Yes."
        return response
    def response_response(self, system_action):
        """emergency fix"""
        self.episode_over = True
        response = []
        error = 0
        if system_action['action_item'][0] != self.goal.goal:
            #response.append(str("Thanks"))
            print("[SIM]: wrong action_item")
            error = 1
            self.error = True
            self.syserr = True
            return initializer(self.goal)
        if len(system_action['slot']) != len(self.inform_slots):
            error = 1
            self.error = True
            self.syserr = True
            self.reward = -5
            return "this is not what I want, sorry."
        for i in system_action['slot']:
            if self.goal.inform_slots.get(i) == None:
                print("[SIM] unexisting slot{}".format(i))               
                error = 1
                self.error = True
                self.reward = -5
                return "this is not what I want, sorry."
            elif self.inform_slots[i] != 1:
                print("[SIM] unexisting slot{}".format(i))               
                error = 1
                self.error = True
                self.reward = -5
                return "this is not what I want, sorry."                
            #elif self.goal.inform_slots.get(i) != system_action['slot'][i]:
            #    print("[SIM] slot '{0}' error with (user: [{1}], system: [{2}])".format(i, self.goal.inform_slots.get(i), system_action['slot'][i]))
            #    error = 1
            #    self.error = True             
            #    return self.error_response(self.last_system_action)
        if error == 0:
            self.error = False
            self.system_correct += 1
            self.success = True
            self.episode_over = True
            response.append(str("Thanks"))
            print('[SIM]: correct response')
            self.reward = 5
            return random.choice(response)


    def response_request(self,system_action):
        response = []
        self.reward = 0
        if self.goal.goal == 'exchange':
            if system_action['action_item'][0] != 'exchange':
                print("[SIM]: wrong action_item")
                self.error = True
                self.syserr = True
                return initializer(self.goal)
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'country1':
                self.inform_slots['country1'] += 1
                if self.inform_slots['country1'] > 1:
                    self.reward = -2
                response.append(str(self.goal.inform_slots['country1']))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'country2':
                self.inform_slots['country2'] += 1
                if self.inform_slots['country2'] > 1:
                    self.reward = -2
                response.append(str(self.goal.inform_slots['country2']))
            elif len(system_action['slot']) == 2:
                response.append(str("The exchange rate between "+self.goal.inform_slots['country1']+" and "+self.goal.inform_slots['country2']))
                response.append(str(self.goal.inform_slots['country1']+" and "+self.goal.inform_slots['country2']))
                response.append(str("Between "+self.goal.inform_slots['country1']+" and "+self.goal.inform_slots['country2']))
            return random.choice(response)
        elif self.goal.goal == 'query':
            if system_action['action_item'][0] != 'query':
                print("[SIM]: wrong action_item")
                self.error = True
                self.syserr = True
                return initializer(self.goal)
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'stock_name':
                self.inform_slots['stock_name'] += 1
                if self.inform_slots['stock_name'] > 1:
                    self.reward = -2
                response.append(str(self.goal.inform_slots['stock_name']))
                response.append(str("the information of "+self.goal.inform_slots['stock_name']+", please"))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'date':
                self.inform_slots['date'] += 1
                if self.inform_slots['date'] > 1:
                    self.reward = -2
                response.append(str(str(self.goal.inform_slots['date'])+"'s")) 
            elif len(system_action['slot']) == 2:
                response.append(str("l'd like to see "+str(self.goal.inform_slots['date'])+"'s "+self.goal.inform_slots['stock_name']+" stock price"))
                response.append(str("Please show me "+str(self.goal.inform_slots['date'])+"'s "+self.goal.inform_slots['stock_name']+" stock price"))
            return random.choice(response)
        elif self.goal.goal == 'get_exchange_rate':
            if system_action['action_item'][0] != 'get_exchange_rate':
                print("[SIM]: wrong action_item")
                self.syserr = True
                self.error = True
                return initializer(self.goal)
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'money_name':
                self.inform_slots['money_name'] += 1
                if self.inform_slots['money_name'] > 1:
                    self.reward = -2
                response.append(str(self.goal.inform_slots['money_name']))
                response.append(str("To "+self.goal.inform_slots['money_name']))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'action':
                self.inform_slots['action'] += 1
                if self.inform_slots['action'] > 1:
                    self.reward = -2
                response.append(str("I want to "+self.goal.inform_slots['action']+" some"))
                response.append(str("To "+self.goal.inform_slots['action']+" it"))
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'types':
                self.inform_slots['types'] += 1
                if self.inform_slots['types'] > 1:
                    self.reward = -2
                if self.goal.inform_slots['types'] == 'spot':
                    response.append(str("My account"))
                else:
                    response.append(str(self.goal.inform_slots['types']+""))
                if self.goal.inform_slots['types'] == 'spot':
                    response.append(str("with my account"))
                else:
                    response.append(str("with "+self.goal.inform_slots['types']))
            return random.choice(response)
        elif self.goal.goal == 'USDX':
            if system_action['action_item'][0] != 'USDX':
                print("[SIM]: wrong action_item")
                self.syserr = True
                self.error = True 
                return initializer(self.goal)
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'time_start':
                self.inform_slots['time_start'] += 1
                if self.inform_slots['time_start'] > 1:
                    self.reward = -2
                response.append(str(str(self.goal.inform_slots['time_start'])))
                response.append(str("In "+str(self.goal.inform_slots['time_start'])+"."))
                response.append(str("The time period starts in "+str(self.goal.inform_slots['time_start'])+"."))
                response.append(str("Start in "+str(self.goal.inform_slots['time_start'])+"."))
                return random.choice(response)
            elif len(system_action['slot']) == 1 and system_action['slot'][0] == 'time_end':
                self.inform_slots['time_end'] += 1
                if self.inform_slots['time_end'] > 1:
                    self.reward = -2
                response.append(str("In "+str(self.goal.inform_slots['time_end'])+"."))
                response.append(str("The time period ends in "+str(self.goal.inform_slots['time_end'])+"."))
                response.append(str("Ends in " +str(self.goal.inform_slots['time_end'])+"."))
            elif len(system_action['slot']) == 2:
                response.append("From "+str(self.goal.inform_slots['time_start'])+" to "+str(self.goal.inform_slots['time_end'])+".")
                response.append("Between "+str(self.goal.inform_slots['time_start'])+" and "+str(self.goal.inform_slots['time_end'])+".")

            return random.choice(response)
    def response_inform(self,system_action):
        pass
    def response_confirm_slot(self,system_action):
        response = None
        wrong = False
        for i in system_action['slot']:
            if self.goal.inform_slots.get(i) != system_action['slot'][i]:
                response = "No."
                self.reward = 1
                wrong = True
            elif self.inform_slots[i] == 0:
                response = "You don't know what to confirm yet."
                self.reward = -3
                wrong = True
        if wrong is False:
            self.reward = -1
            response = "Yes."
        return response

if __name__ == '__main__':
    r = RLSimulator()
    r.goal.dump()
    tmp = {}
    tmp['system_action'] = ['response']
    tmp['action_item'] = [r.goal.goal]
    tmp['slot'] = r.goal.inform_slots
    pprint(tmp)
    print ("---------")
    #pdb.set_trace()
