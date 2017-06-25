import random

USDX = ['B-time_start','B-time_end']
exchange = ['B-country','B-country']
get_exchange_rate = ['B-money_name','B-action','B-types']
query = ['B-stock_name','B-date']
USD = ['USDX']
closing = []
confirm_int = []
confirm_slot = []
intent = ["USDX","exchange","get_exchange_rate","query"]
system_action = ["request",'response',"closing","confirm_slot","confirm_int"]
slot = dict()
slot['USDX'] = USDX
slot['exchange'] = exchange
slot['get_exchange_rate'] = get_exchange_rate
slot['query'] = query
reply = dict()
slot_tag = dict()
reply['time_start'] = ['show me the USDX starts in 2017-01-01','I\'d like to know the USDX since 2017/01/01']
slot_tag['time_start'] = ['O O O O O B-time_start','O O O O O O O B-time_start']
reply['time_end'] = ['Give me the USDX until 2017/05/01.','I\'d like to know the USDX until 2017/01/01.']
slot_tag['time_end'] = ['O O O O O B-time_end','O O O O O O O B-time_end']
reply['USDX'] = ['Show me the USDX information.']
slot_tag['USDX'] = ['O O O O O']
reply['time_starttime_end'] = ['give me the USDX from 2017-01-02 to 2017-03-14']
slot_tag['time_starttime_end'] = ['O O O O O B-time_start O B-time_end']
reply['exchange'] = ['Give me the exchange rate.']
slot_tag['exchange'] = ['O O O O O']
reply['country'] = ['What is the exchange rate of USD?','How\'s the exchange rate of Japanese Yen?']
slot_tag['country'] = ['O O O O O O B-country','O O O O O B-country I-country']
reply['countrycountry'] = ['Give me the exchange rate between USD and NTD.']
slot_tag['countrycountry'] = ['O O O O O O B-country O B-country']
reply['get_exchange_rate'] = ['I want to exchange my currency']
slot_tag['get_exchange_rate'] = ['O O O O O O']
reply['money_name'] = ['I\'d like to sell some CNY.','I want to buy some USD.']
slot_tag['money_name'] = ['O O O B-action O B-money_name','O O O B-action O B-money_name']
reply['action'] = ['I want to buy some foreign currency']
slot_tag['action'] = ['O O O B-action O O O']
reply['type'] = ['I want to exchange my cash','I want to exchange the money in my account']
slot_tag['type'] = ['O O O O O B-types','O O O O O O O O B-types']
reply['money_nametype'] = ['I want to exchange my USD in cash']
slot_tag['money_nametype'] = ['O O O O O B-money_name O B-types']
reply['money_nameaction'] = ['i want to sell my USD','i want to buy some NTD']
slot_tag['money_nameaction'] = ['O O O B-action O B-money_name','O O O B-action O B-money_name']
reply['actiontype'] = ['i want to buy some foreign currency with my account']
slot_tag['actiontype'] = ['O O O B-action O O O O O B-types']
reply['money_nameactiontype'] = ['i want to buy USD with cash']
slot_tag['money_nameactiontype'] = ['O O O B-action B-money_name O B-types']
reply['query'] = ['show me the stock price']
slot_tag['query'] = ['O O O O O']
reply['stock_name'] = ['show me Comstock Mining stock price']
slot_tag['stock_name'] = ['O O B-stock_name I-stock_name O O']
reply['date'] = ['give me 2017-03-01','2017-03-01']
slot_tag['date'] = ['O O B-date','B-date']
reply['stock_namedate'] = ['show me Comstock Mining stock price on 2017-03-01']
slot_tag['stock_namedate'] = ['O O B-stock_name I-stock_name O O O B-date']
reply['closing'] = ['thanks']
reply['confirm_yes'] = ['yes']
slot_tag['confirm_yes'] = ['O']
reply['confirm_no'] = ['no']
slot_tag['confirm_no'] = ['O']
slot_tag['closing'] = ['O']
train_in = open('../n_All/train/seq.in','w')
out_train = open('../n_All/train/seq.out','w')
int_out = open('../n_All/train/int','w')
for i in range(2000):
	goal = random.choice(intent)
	s_tags = []
	req_tags = []
	if len(slot[goal]) == 2:
		s_tags.append(slot[goal][0])
		s_tags.append(slot[goal][1])
		s_tags.append(slot[goal][0] + " " +slot[goal][1])
		s_tags.append("")
		req_tags.append(slot[goal][1])
		req_tags.append(slot[goal][0])
		req_tags.append("")
		req_tags.append(slot[goal][0] + " " + slot[goal][1])
	elif len(slot[goal]) == 3:
		s_tags.append(slot[goal][0])
		s_tags.append(slot[goal][1])
		s_tags.append(slot[goal][2])
		s_tags.append(slot[goal][1] + " " +slot[goal][2])
		s_tags.append(slot[goal][0] + " " +slot[goal][2])
		s_tags.append(slot[goal][0] + " " +slot[goal][1])
		s_tags.append(slot[goal][0] + " " +slot[goal][2]+ " " +slot[goal][1])
		s_tags.append("")
		req_tags.append(slot[goal][1])
		req_tags.append(slot[goal][2])
		req_tags.append(slot[goal][0])
		req_tags.append(slot[goal][0])
		req_tags.append(slot[goal][1])
		req_tags.append(slot[goal][2])
		req_tags.append("")
		req_tags.append(slot[goal][0] + " " +slot[goal][2]+ " " +slot[goal][1])
	if random.random() < 0.85:
		index = random.randint(0,len(s_tags)-1)
		train_in.write(goal + " " + s_tags[index] + " SYSTEM_ACTION " + system_action[0] +" "+ req_tags[index] + " ***next*** ")
		int_out.write(goal+'\n')
		if goal == "USDX":
			if index == 0:
				intout = random.randint(0,len(reply['time_end'])-1)
				train_in.write(reply['time_end'][intout]+'\n')
				out_train.write(slot_tag['time_end'][intout]+'\n')
			elif index == 1:
				intout = random.randint(0,len(reply['time_start'])-1)
				train_in.write(reply['time_start'][intout]+'\n')
				out_train.write(slot_tag['time_start'][intout]+'\n')
			elif index == 2:
				intout = random.randint(0,len(reply['USDX'])-1)
				train_in.write(reply['USDX'][intout]+'\n')
				out_train.write(slot_tag['USDX'][intout]+'\n')
				#nothing
			elif index == 3:
				intout = random.randint(0,len(reply['time_starttime_end'])-1)
				train_in.write(reply['time_starttime_end'][intout]+'\n')
				out_train.write(slot_tag['time_starttime_end'][intout]+'\n')
		elif goal == "query":
			if index == 0:
				intout = random.randint(0,len(reply['date'])-1)
				train_in.write(reply['date'][intout]+'\n')
				out_train.write(slot_tag['date'][intout]+'\n')
			elif index == 1:
				intout = random.randint(0,len(reply['stock_name'])-1)
				train_in.write(reply['stock_name'][intout]+'\n')
				out_train.write(slot_tag['stock_name'][intout]+'\n')
			elif index == 2:
				intout = random.randint(0,len(reply['query'])-1)
				train_in.write(reply['query'][intout]+'\n')
				out_train.write(slot_tag['query'][intout]+'\n')
				#nothing
			elif index == 3:
				intout = random.randint(0,len(reply['stock_namedate'])-1)
				train_in.write(reply['stock_namedate'][intout]+'\n')
				out_train.write(slot_tag['stock_namedate'][intout]+'\n')
		elif goal == 'exchange':
			if index == 0:
				intout = random.randint(0,len(reply['country'])-1)
				train_in.write(reply['country'][intout]+'\n')
				out_train.write(slot_tag['country'][intout]+'\n')
			elif index == 1:
				intout = random.randint(0,len(reply['country'])-1)
				train_in.write(reply['country'][intout]+'\n')
				out_train.write(slot_tag['country'][intout]+'\n')
			elif index == 2:
				intout = random.randint(0,len(reply['exchange'])-1)
				train_in.write(reply['exchange'][intout]+'\n')
				out_train.write(slot_tag['exchange'][intout]+'\n')
				#nothing
			elif index == 3:
				intout = random.randint(0,len(reply['countrycountry'])-1)
				train_in.write(reply['countrycountry'][intout]+'\n')
				out_train.write(slot_tag['countrycountry'][intout]+'\n')
		elif goal == 'get_exchange_rate':
			if index == 0:
				intout = random.randint(0,len(reply['action'])-1)
				train_in.write(reply['action'][intout]+'\n')
				out_train.write(slot_tag['action'][intout]+'\n')
			elif index == 1:
				intout = random.randint(0,len(reply['type'])-1)
				train_in.write(reply['type'][intout]+'\n')
				out_train.write(slot_tag['type'][intout]+'\n')
			elif index == 2:
				intout = random.randint(0,len(reply['money_name'])-1)
				train_in.write(reply['money_name'][intout]+'\n')
				out_train.write(slot_tag['money_name'][intout]+'\n')
			elif index == 3:
				intout = random.randint(0,len(reply['money_name'])-1)
				train_in.write(reply['money_name'][intout]+'\n')
				out_train.write(slot_tag['money_name'][intout]+'\n')
			elif index == 4:
				intout = random.randint(0,len(reply['action'])-1)
				train_in.write(reply['action'][intout]+'\n')
				out_train.write(slot_tag['action'][intout]+'\n')
			elif index == 5:
				intout = random.randint(0,len(reply['type'])-1)
				train_in.write(reply['type'][intout]+'\n')
				out_train.write(slot_tag['type'][intout]+'\n')
			elif index == 6:
				intout = random.randint(0,len(reply['get_exchange_rate'])-1)
				train_in.write(reply['get_exchange_rate'][intout]+'\n')
				out_train.write(slot_tag['get_exchange_rate'][intout]+'\n')
			elif index == 7:
				intout = random.randint(0,len(reply['money_nameactiontype'])-1)
				train_in.write(reply['money_nameactiontype'][intout]+'\n')
				out_train.write(slot_tag['money_nameactiontype'][intout]+'\n')
	else:
		ran = random.random()
		if ran > 0.7:#response
			index = random.randint(0,len(s_tags)-1)
			train_in.write(goal + " " + s_tags[index] + " SYSTEM_ACTION response " + req_tags[-1] + " ***next*** ")
			train_in.write(reply['closing'][0]+'\n')
			out_train.write(slot_tag['closing'][0]+'\n')
			int_out.write('closing\n')
		elif ran >= 0.5:#confirm_slot
			index = random.randint(0,len(s_tags)-2)
			train_in.write(goal + " " + s_tags[index] + " SYSTEM_ACTION confirm_slot " + s_tags[index] + " ***next*** ")
			if random.random() > 0.5:
				train_in.write(reply['confirm_yes'][0]+'\n')
				out_train.write(slot_tag['confirm_yes'][0]+'\n')
				int_out.write('confirm_yes\n')
			else:
				train_in.write(reply['confirm_no'][0]+'\n')
				out_train.write(slot_tag['confirm_no'][0]+'\n')
				int_out.write('confirm_no\n')
		elif ran >= 0.3:#confirm_int
			train_in.write(goal + " SYSTEM_ACTION confirm_int " + goal + " ***next*** ")
			if random.random() > 0.5:
				train_in.write(reply['confirm_yes'][0]+'\n')
				out_train.write(slot_tag['confirm_yes'][0]+'\n')
				int_out.write('confirm_yes\n')
			else:
				train_in.write(reply['confirm_no'][0]+'\n')
				out_train.write(slot_tag['confirm_no'][0]+'\n')
				int_out.write('confirm_no\n')
		else:
			train_in.write(" SYSTEM_ACTION ***next*** hi\n")
			out_train.write("O\n")
			int_out.write('welcome\n')
