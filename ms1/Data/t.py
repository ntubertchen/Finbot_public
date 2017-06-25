t_in = open('train.seq.in','r')
l_in = []
for x in t_in:
	l_in.append(x)
t_label = open('train.label','r')
l_label = []
for x in t_label:
	l_label.append(x)
t_out = open('train.seq.out','r')
l_out = []
for x in t_out:
	l_out.append(x)
import random

a_in = open('ltrain.seq.in','w')
a_out = open('ltrain.seq.out','w')
a_label = open('ltrain.label','w')
for _ in range(len(l_in)/10):
	index = random.randint(0,len(l_in)-1)
	print (index,len(l_in),len(l_label))
	a_in.write(l_in[index])
	a_out.write(l_out[index])
	a_label.write(l_label[index])
