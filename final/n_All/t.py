stock = ['yahoo','nvidia','apple','tsmc','google','intel','htc','apple inc','Foxconn','facebook','acer','MTK','mediatek','asus']
first = ('query  SYSTEM_ACTION request B-stock_name B-date ***next***') 
second = ('query B-date SYSTEM_ACTION request B-stock_name ***next***')
s1 = ['O O','O O O B-date']
s2 = ['','']
i1 = ['what is','stock price on 2017-03-01']
i2 = ['','']
t1 = open('./test','w')
t2 = open('./test2','w')
t3 = open('./test3','w')
import random
for _ in range(2):
	for i in range(len(stock)):
		if random.random() > 2:
			t1.write(first + i1[0] + " "+stock[i]+" " + i1[1] + '\n')
			if len(stock[i].split()) > 1:
				t2.write(s1[0] + " B-stock_name I-stock_name " +s1[1] +'\n')
			else:
				t2.write(s1[0] + " B-stock_name "+ s1[1]+'\n')
			t3.write('query\n')
		else:
			t1.write(second + i2[0] + " "+stock[i]+" " + i2[1] + '\n')
			if len(stock[i].split()) > 1:
				t2.write(s2[0] + " B-stock_name I-stock_name " +s2[1] +'\n')
			else:
				t2.write(s2[0] + " B-stock_name "+ s2[1]+'\n')
			t3.write('query\n')