import random

class RNNNLG(object):
	"""lifelong lonliness generator"""
	def __init__(self, arg):
		pass
	
	def nlg(self,action,slots):
		psuedo_slot = random.choice(RNNNLG.nlg_action[action].keys())
		action_nl = random.choice(RNNNLG.nlg_action[action][psuedo_slot])
		return action_nl

	inform_no_match_nl = {'inform_no_match': ["Sorry, I cannot find matching results .","Sorry, I can't find .",'no find .','not found .']}

	hello_nl = {'hello':['Hello, welcome to Finbot. I can: 1. excahnge between two currencies 2. query US stock prices 3. get exchange rate between Taiwan and foreign money 4. check the USDX index How may I help you?']}

	request_nl = {
					'country1': ['against which currency ?','against what money ?','which currency is it against ?'],
					#'country1&country2': ['between which two country -s ?'],
					'time_start': ['what date does the time period start in ?', 'what is the starting date ?','starting from ?'],
					'time_end': ['what date does the time period end in ?','what is the ending date ?','ending in ?'],
					#'time_start&time_end': ['what time period ?','during what period ?','when from and when to ?'],
					'money_name': ['which currency ?','what kind of money ?','what type of currency ?'],
					'action': ['what to do to this currency ?', 'would you like to sell or buy ?', 'to sell or to buy ?'],
					'types': ['with your account or cash ?','by cash or your account ?'],
					'stock_name': ['which stock ?','can you yell me the stock name ?','stock name ?'],
					'date': ['what date would you like to see ?','on which day ?','what date are you interested in ?']
	}

	confirm_intent_nl = {
						'exchange': ['you want to know the exchange rate ?','you want the exchange rate .'],
						'USDX': ['you want to know the USDX ?','you want to know the USDX .'],
						'query': ['you want to know the stock price ?','you want to know the stock price .'],
						'get_exchange_rate':['you want to trade foreign money ?','you want to trade foreign money .']
	}

	confirm_slot_nl = {
						#exchange
						'country1': ['do you want to exchange from X ?','from X ?','ok, exchange from X .'],
						'country2': ['do you want to exchange to X ?','to X ?','ok, exchange to X .'],
						#'country1&country2': ['do you want to exchange from X to X ?'],
						#USDX
						'time_start': ['do you want to see from X ?','from X ?'],
						'time_end': ['do you want to see until X ?','until X ?'],
						#'time_start&time_end': ['do you want to see from X to X ?'],
						#query
						'stock_name': ['do you want to see X ?', 'did you say X ?','you said X .'],
						'date': ['do you want to see on X ?','on X ?'],
						#'stock_name&date': ['do you want to see X on X ?'],
						#get_exchange_rate
						'money_name': ['do you want to trade some X ?','did you say X ?','you said X .'],
						'action': ['do you want to X ?', 'to X ?','you want to X .'],
						'types': ['do you want to use X ?', 'use X ?'],
						#'money_name&action': ['do you want to X some X ?'],
						#'action&types': ['do you want to X with X ?'],
						#'money_name&types': ['do you mean X with X ?'
					}
	nlg_action = {'request':request_nl, 'confirm_slot':confirm_slot_nl, 'confirm_intent':confirm_intent_nl, 'hello':hello_nl, 'inform_no_match':inform_no_match_nl}

if __name__ == '__main__':
	test = RNNNLG(object)
	action = ['hello', 'confirm_intent','confirm_slot','request','inform_no_match']

	print (test.nlg(random.choice(action),'types'))