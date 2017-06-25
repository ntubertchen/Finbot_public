import json
from pprint import pprint

a = open('./all.json')
data = json.load(a)
d = {}
for country in data:
	l = country['currencies']
	# N
	for n in l:
		if n['name'] not in d and n['name'] != None and n['code'] != None:
			d[n['name']] = country['name'] + ' * ' + n['code']
o = open('./out','w')
for key in d:
	o.write(key.encode('utf-8')+' * '+ d[key].encode('utf-8')+'\n')
	#print (key,d[key])