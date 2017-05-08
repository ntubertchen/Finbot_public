from state import State
from nn_model import NN
from rule_simulator import RuleSimulator, initializer
import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
from w2v import DataPrepare
import argparse
import fileinput
import pdb
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
	nl_input = initializer(user.goal)
	turn_by_turn(currturn,nl_input,'user')
	
	while (not over):
		#pdb.set_trace()
		#system side
		slot,intent = nlu.predict(nl_input,system)
		system.update(slot,intent,nl_input)
		frame_output,sys_nl = system.reply()
		#turn_by_turn(currturn+1,sys_nl,'system')
		#print(frame_output)
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

		a += ")\t"
		a += sys_nl
		turn_by_turn(currturn+1,a,'system')
		currturn += 2
		if currturn>= maxturn :
			print("[DM] maxturn reached")
			break
		reward -= 2
		#user side
		nl_input = user.next(frame_output)
		turn_by_turn(currturn,nl_input,'user')
		over = user.episode_over
		
	if user.success:
		print("Successful")
		reward += 2*maxturn
	else:
		print("Failing")
		reward -= maxturn

	return reward,user.success,currturn
def turn_by_turn(currturn,turn,who):
	print("[DM] turn{0} {1}:".format(currturn,who),turn)
if __name__ == '__main__':
	count = 1.
	succ = 0.
	turn = 0.
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	#config.gpu_options.per_process_gpu_memory_fraction = 0.2
	sess = tf.Session(config=config)
	nlu = NN(sess)
	nlu.loadmodel()
	for _ in range(30):
		r,s,c = run_an_episode(nlu)
		if s is True: succ+=1
		turn += c
		print ('reward:',r,';\trate:',succ/count,"avg_turn:",c/count)
		count+=1
