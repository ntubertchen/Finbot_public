f1 = open('seq.out','r')
f2 = open('intent','r')
outf1 = open('slot_list','w')
outf2 = open('intent_list','w')
slot = dict()
intent = dict()
for line in f1:
	line = line.replace('***','')
	line = line.split()
	for word in line:
		if word not in slot:
			outf1.write(word+'\n')
			slot[word] = 1
for line in f2:
	line = line.replace('***','')
	line = line.split()
	for word in line:
		if word not in intent:
			outf2.write(word+'\n')
			intent[word] = 1