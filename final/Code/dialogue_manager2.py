from state import State
from nn_model import NN
from rule_simulator2 import RuleSimulator, initializer2
import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
from w2v import DataPrepare
import argparse
import fileinput
w_in = open('../All/w_in','w')
w_s = open('../All/w_s','w')
w_i = open('../All/w_i','w')
w_sa = open('../All/w_sa','w')
w_r = open('../All/w_r','w')
def run_an_episode(nlu):
	
	reward = 0
	currturn = 0
	maxturn = 12
	system = State()

	#user
	user = RuleSimulator()
	print ("New episode, user goal:")
	user.goal.dump()
	print('_ _ _ _ _ _ _ _ _ _ _ _')
	over = user.episode_over
	#nl_input = initializer(user.goal)
	example_input = initializer2(user.goal)
	print("Here are the example input, TA can random choose one or type your own(do not just type the number of sentence):")
	i = 1
	for a in example_input:
		print(str(i)+". "+a)
		i += 1
	nl_input = input("TA types: ")
	turn_by_turn(currturn,nl_input,'user')
	import pdb;pdb.set_trace()
	
	while (not over):
		pdb.set_trace()
		#system side
		slot,intent = nlu.predict(nl_input,system)
		system.update(slot,intent,nl_input,w_in)
		
		frame_output, sys_nl = system.reply(w_s,w_i,w_sa)
		print("system: "+sys_nl)
		print(frame_output)
		a = str(frame_output['system_action'][0])
		a += "("
		if frame_output['system_action'][0] == "response" or frame_output['system_action'][0] == "confirm_answer":
			for i in frame_output['slot'].keys():
				a += str(i)
				a += ', '
		elif frame_output['system_action'][0] == 'request':
			for i in frame_output['slot']:
				a += str(i)
				a += ', '

		a += ")"

		turn_by_turn(currturn+1,a,'system')
		currturn += 2
		if currturn>= maxturn :
			print("[DM] maxturn reached")
			break
		reward -= 2
		#user side
		#nl_input = user.next(frame_output)
		example_next = user.next(frame_output)
		print("Here are some example response for User according to agent response, TA can type your own(if there's only Thanks, please type Thanks):")
		a = 1
		for i in example_next:
			print(str(a)+". "+i)
		nl_input = input("TA types: ")
		turn_by_turn(currturn,nl_input,'user')
		over = user.episode_over
		
	if user.success:
		print("Successful")
		reward += 2*maxturn
	else:
		print("Failing")
		reward -= maxturn

	return reward,user.success
def turn_by_turn(currturn,turn,who):
	print("[DM] turn{0} {1}:".format(currturn,who),turn)
if __name__ == '__main__':
	count = 1.
	succ = 0.
	config = tf.ConfigProto()
	#config.gpu_options.allow_growth = True
	config.gpu_options.per_process_gpu_memory_fraction = 0.2
	sess = tf.Session(config=config)
	nlu = NN(sess)
	nlu.loadmodel()
	for _ in range(30):
		r,s = run_an_episode(nlu)
		if s is True: succ+=1
		print ('reward:',r,';\trate:',succ/count)
		count+=1
