with open('train.seq.out','r') as f:
	d = dict()
	for s in f:
		s = s.strip().split()
		for x in s:
			if x not in d:
				d[x] = 1
	slot_l = open('slot_l.txt','w')
	for key,value in d.iteritems():
		slot_l.write(key+'\n')
with open('train.label','r') as f:
	d = dict()
	for s in f:
		if s not in d:
			d[s] = 1
			print (s)
	print ("a")
	intent_l = open('intent_l.txt','w')
	for key,value in d.iteritems():
		print (key)
		intent_l.write(key)
