d = dict()
country = [['new taiwan dollars','new taiwan dollar', 'taiwan','ntd'],['us dollars', 'us dollar', 'usa','us','united states',"u.s.a",'u.s.','u.s','american dollars', 'american dollar',"america"],
['japanese','japan','yen'],['rmb', 'china'],['eu'],['france']]
currency = ['TWD', 'USD', 'JPY', 'CNY', 'EUR', 'FRF']
#for i in range (len(country)):
#	d[country[i]] = currency[i]
l = "usd"
print(len(country))
l = l.lower()
for i in range(len(country)):
	for j in range(len(country[i])):
		if i == 1:
			if country[i][j] == 'us':
				if l.find('usd') != -1:
					continue
		print(country[i][j])
		print(l.find(country[i][j]))
		if l.find(country[i][j]) != -1:
			l = l.replace(country[i][j],currency[i])
			break
#for c in country:
#	print(c)
#	print(l.find(c))
#	if l.find(c) != -1:
#		l = l.replace(c,d[c])
print(l)