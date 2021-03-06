'''
A Bidirectional Recurrent Neural Network (LSTM) implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits (http://yann.lecun.com/exdb/mnist/)
Long Short Term Memory paper: http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf
Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function

import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
import test
from de_w2v import DataPrepare
import argparse
import RuleBasedNlg
'''
To classify images using a bidirectional recurrent neural network, we consider
every image row as a sequence of pixels. Because MNIST image shape is 28*28px,
we will then handle 28 sequences of 28 steps for every sample.
'''
# python s_v.py --glove "../glove/glove.6B.200d.txt" --train_p "../Data/" --slot_l "../Data/slot_l.txt" --intent_l "../Data/intent_l.txt"

parser = argparse.ArgumentParser()
parser.add_argument('--glove', help='glove path')
parser.add_argument('--train_p', help='training data path')
parser.add_argument('--test_p', help='testing data path')
parser.add_argument('--test',action='store_true',help='test or train')
parser.add_argument('--slot_l', help='slot tag list')
parser.add_argument('--intent_l', help='intent list')
parser.add_argument('--intent', action='store_false',help='intent training')
parser.add_argument('--slot', action='store_false',help='slot training')
args = parser.parse_args()

slot_l = []
intent_l = []
with open(args.slot_l,'r') as f:
    for x in f:
        slot_l.append(x.strip())
with open(args.intent_l,'r') as f:
    for x in f:
        intent_l.append(x.strip())
path = [args.glove,args.train_p+'.seq.in']

Data = DataPrepare(path,slot_l,intent_l)

# Parameters
learning_rate = 0.0001
training_iters = 10000
batch_size = 1
display_step = 50

# Network Parameters
#n_input = 28 # MNIST data input (img shape: 28*28)
#n_steps = 28 # timesteps
n_hidden = 128 # hidden layer num of features
#n_classes = 10 # MNIST total classes (0-9 digits)
Data.maxlen = 23
n_words = Data.maxlen
n_slot = len(slot_l)
n_intent = len(intent_l)
w2v_l = 200

# tf Graph input
x = tf.placeholder("float", [None, n_words, w2v_l])
#y_slot = tf.placeholder("float", [None, n_words, n_slot])
y_intent = tf.placeholder("float", [None, 1 ,n_intent])

# Define weights
weights = {
    # Hidden layer weights => 2*n_hidden because of forward + backward cells
    'slot_out': tf.Variable(tf.random_normal([2*n_hidden, n_slot])),
    'intent_out': tf.Variable(tf.random_normal([2*n_hidden, n_intent]))
}
biases = {
    'slot_out': tf.Variable(tf.random_normal([n_slot])),
    'intent_out': tf.Variable(tf.random_normal([n_intent]))
}



def intent_BiRNN(x,weights,biases):
    x = tf.unstack(x, n_words, 1)
    lstm_fw_cell = rnn.BasicLSTMCell(n_hidden, forget_bias=1.0)
    lstm_bw_cell = rnn.BasicLSTMCell(n_hidden, forget_bias=1.0)
    outputs, _, _ = rnn.static_bidirectional_rnn(lstm_fw_cell, lstm_bw_cell, x,dtype=tf.float32)
    return tf.matmul(outputs[-1],weights['intent_out']) + biases['intent_out']


def intent_loss(pred,y):
    return tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred,labels=y))

# pred = slot_BiRNN(x, weights, biases)
#pred_out = slot_out(Data,pred)
# loss = slot_loss(pred,y_slot)
pred = intent_BiRNN(x,weights,biases)
loss = intent_loss(pred,y_intent)
# else:
#     pred = intent_BiRNN(x,weights,biases)
#     pred_out = tf.argmax(pred,axis=1)
#     loss = intent_loss(pred,y_intent)
# Define loss and optimizer

optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)
# Evaluate model
#correct_pred = tf.equal(tf.argmax(pred,1), tf.argmax(y,1)) 
#accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

saver = tf.train.Saver()

# Initializing the variables
init = tf.global_variables_initializer()

with tf.Session() as sess:
    demo_out = open('tag.txt','r')
    demo_result = open('out.txt','w')
    d = []
    for _ in range(100):
        d.append(dict())
    counter = 0
    for line in demo_out:
        try:
            exist = line.index("*****")
            counter += 1
            continue
        except:
            line = line.strip()
            index = line[2:line.index(" ")]
            content = line[line.index(" ")+1:]
            d[counter][index] = content
    ckpt = tf.train.get_checkpoint_state("../intentmodel")
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess,ckpt.model_checkpoint_path)
    test_x,original = Data.demo_batch()
    counter = 0
    for demo in test_x:
        intent_out = sess.run(pred,feed_dict={x: [demo]})        
        intent_out = np.argmax(intent_out)
        slot = []
        if (Data.rev_intentdict[intent_out] == "exchange"):
            if "country1" in d[counter]:
                slot.append(d[counter]["country1"])
            if "country2" in d[counter]:
                slot.append(d[counter]["country2"])
            result = RuleBasedNlg.RuleBasedNlg('exchange',slot)
            demo_result.write(result+'\n')
            #call
        elif Data.rev_intentdict[intent_out] == "get_exchange_rate":
            if "money_name" in d[counter]:
                slot.append(d[counter]["money_name"])
            if "buy" in d[counter]:
                slot.append(d[counter]["buy"])
            if "type" in d[counter]:
                slot.append(d[counter]["type"])
            result = RuleBasedNlg.RuleBasedNlg('get_exchange_rate',slot)
            demo_result.write(result+'\n')
            #call
        elif Data.rev_intentdict[intent_out] == "query":
            if "symbol" in d[counter]:
                slot.append(d[counter]["symbol"])
            if "date" in d[counter]:
                slot.append(d[counter]["date"])
            result = RuleBasedNlg.RuleBasedNlg('query',slot)
            demo_result.write(result+'\n')
            #call
        counter+=1