import random
import json
import itertools
#bleu 690295486889

class RNNNLG(object):
	"""lifelong loneliness generator"""
	def __init__(self):
		with open('nlg.json') as j:
			self.nl_dict = json.load(j)
		
	

	def generator(self,action,slot_value):
		key = action+'('+slot_value+')'
		#print 'action form State.py:', key
		if key in self.nl_dict:
			#print 'key exists, retriving'
			return self.nl_dict[key]
		else:
			#print 'unknown key, generating from template'
			if '=' in slot_value:
				slot = slot_value.split('=')[0]
				value = slot_value.split('=')[1]
				#print slot,value 
				nl = random.choice(RNNNLG.confirm_slot_nl[slot])
				nl = nl.replace('X',value)
				return nl

	confirm_slot_nl = {
					#exchange
					'country1': ['do you want to exchange from X ?','would you like to exchange from X ?'],
					'country2': ['do you want to exchange to X ?','would you like to exchange to X ?'],
					#'country1&country2': ['do you want to exchange from X to X ?'],
					#USDX
					'time_start': ['is the date from X ?','does the date start from X ?'],
					'time_end': ['is the date until X ?','does the date end in X ?'],
					#'time_start&time_end': ['do you want to see from X to X ?'],
					#query
                    'stock_name': ['do you want the stock named X ?','the name of the stock is X ?'],
					'date': ['is it on date X ?','is the date X ?'],
					#'stock_name&date': ['do you want to see X on X ?'],
					#get_exchange_rate
					'money_name': ['do you want to trade some X money ?','would you like to trade some X money ?'],
					'action': ['do you want to X ?', 'would you like to X ?'],
					'types': ['do you want to use X ?', 'would you like to use X ?'],
					#'money_name&action': ['do you want to X some X ?'],
					#'action&types': ['do you want to X with X ?'],
					#'money_name&types': ['do you mean X with X ?'],
	}
if __name__ == '__main__':
	test = RNNNLG()
	while(1):
		action = raw_input('action')
		slot = raw_input('slot')
		test.generator(action,slot)
	