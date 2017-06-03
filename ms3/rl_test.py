from state import State
from nn_model_fast import NN
from rl_simulator import RLSimulator, initializer
import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
from w2v_fast import DataPrepare
import argparse
import fileinput
import pdb
dialog = []
def run_an_episode(nlu):
    
    reward = 0
    currturn = 0
    maxturn = 12
    system = State()

    #user
    user = RLSimulator()
    print ("New episode, user goal:")
    user.goal.dump()
    print('_ _ _ _ _ _ _ _ _ _ _ _')
    over = user.episode_over
    nl_input = initializer(user.goal)
    turn_by_turn(currturn,nl_input,'user')
    
    while (not over):
        #system side
        slot,intent = nlu.predict(nl_input,system)
        system.update(slot,intent,nl_input,reward)
        frame_output,sys_nl = system.reply()
        #turn_by_turn(currturn+1,sys_nl,'system')
        #print(frame_output)
        a = str(frame_output['action_item'][0])
        a += "\t"
        a += str(frame_output['system_action'][0])
        a += "("
        # if frame_output['system_action'][0] == "response" or frame_output['system_action'][0] == "confirm_answer":
        #   for i in frame_output['slot'].keys():
        #       a += str(i)
        #       a += ', '
        # elif frame_output['system_action'][0] == 'request':
        #   for i in frame_output['slot']:
        #       a += str(i)
        #       a += ', '
        if frame_output.get('slot') != None:
            a += str(frame_output['slot'])
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
        if user.syserr == True:
            print ("GG")
            system = State()
            user.syserr = False
        turn_by_turn(currturn,nl_input,'user')
        over = user.episode_over
        reward += user.reward
    if user.success:
        print("Successful")
        reward += 2*maxturn
    else:
        print("Failing")
        reward -= maxturn

    return reward,user.success,currturn
def turn_by_turn(currturn,turn,who):
    global dialog
    x = ("[DM] turn{0} {1}:".format(currturn,who),turn)
    dialog.append(x)
    print("[DM] turn{0} {1}:".format(currturn,who),turn)
if __name__ == '__main__':
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    #config.gpu_options.per_process_gpu_memory_fraction = 0.2
    sess = tf.Session(config=config)
    nlu = NN(sess)
    nlu.loadmodel()
    count = 1.
    succ = 0.
    turn = 0.
    reward = 0.
    accu_acc = 0.
    for _ in range(10000):
        global dialog
        dialog = []
        r,s,c = run_an_episode(nlu)
        if s is True:
            with open('./dialog2.txt', 'w') as f:
                for i in dialog:
                    f.write(str(i)+str("\n"))
                f.write("reward: {0}".format(r))
            succ+=1
        turn += c
        reward += r
        turn_acc = 100. if s is True else ((turn/2)-1)/(turn/2)
        accu_acc += turn_acc
        print(str("number : ")+str(_))
        print("--- end of episode ---")
        print('reward: {0} ,it was a {1} dialogue. frame_accuray:{2}'.format(r,'successful' if s is True else 'failing',turn_acc))
        print('avg_reward: {0}\nsucc_rate: {1}\navg_turns: {2}\navg_turnacc:{3}\n\n========================='.format(reward/count, succ/count, turn/count, accu_acc/count))
        print(str("success number : ")+str(succ))
        count+=1
