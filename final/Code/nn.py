import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
from w2v import DataPrepare
import argparse
import fileinput
import sys

config = tf.ConfigProto()
config.gpu_options.allow_growth = True

parser = argparse.ArgumentParser()
parser.add_argument('--glove', help='glove path')
parser.add_argument('--test',action='store_true',help='test or train')
args = parser.parse_args()

path = ["../glove/glove.6B.200d.txt" , "../All/Data/train/seq.in" , "../All/Data/train/seq.out" , "../All/Data/train/intent", "../All/long.txt","../All/currency"]
#t_path = ["../GloVe/glove.6B.200d.txt" , "../All/Data/test/seq.in" , "../All/Data/test/seq.out" , "../All/Data/test/intent"]
slotpath = '../All/Data/slot_list'
intentpath = '../All/Data/intent_list'
Data = DataPrepare(path,slotpath,intentpath)

learning_rate = 0.0001
epoc = 5
batch_size = 1
display_step = 30

#network parameters
sentence_length = Data.maxlength
word_vector = 200

summery_dim = 30
n_hidden = 128
n_words = Data.maxlength
n_slot = Data.slot_dim
n_intent = Data.intent_dim

s_x = tf.placeholder("float", [None, sentence_length, word_vector],name='s_x')
prev_sen_len = tf.placeholder("int32",[None],name='prev_sen_len')
sen_len = tf.placeholder("int32",[None],name='sen_len')
x = tf.placeholder("float", [None, n_words, word_vector],name='x')
y_slot = tf.placeholder("float", [None, n_words, n_slot],name='y_slot')
y_intent = tf.placeholder("float", [None, 1 ,n_intent],name='y_intent')


weights = {
    # Hidden layer weights => 2*n_hidden because of forward + backward cells
    'summery': tf.Variable(tf.random_normal([2*n_hidden,summery_dim])),
    'slot_out': tf.Variable(tf.random_normal([2*n_hidden, n_slot])),
    'intent_out': tf.Variable(tf.random_normal([2*n_hidden, n_intent]))
}
biases = {
    'summery': tf.Variable(tf.random_normal([summery_dim])),
    'slot_out': tf.Variable(tf.random_normal([n_slot])),
    'intent_out': tf.Variable(tf.random_normal([n_intent]))
}

with tf.variable_scope('summery_cell'):
    Lstmcell = {
        'fw_lstm' : rnn.BasicLSTMCell(n_hidden,forget_bias = 1.0),
        'bw_lstm' : rnn.BasicLSTMCell(n_hidden,forget_bias = 1.0)
}
with tf.variable_scope('slot_cell'):
    s_Lstmcell = {
        'fw_lstm' : rnn.BasicLSTMCell(n_hidden,forget_bias = 1.0),
        'bw_lstm' : rnn.BasicLSTMCell(n_hidden,forget_bias = 1.0)
}
with tf.variable_scope('intent_cell'):
    i_Lstmcell = {
        'fw_lstm' : rnn.BasicLSTMCell(n_hidden,forget_bias = 1.0),
        'bw_lstm' : rnn.BasicLSTMCell(n_hidden,forget_bias = 1.0)
}

def summery_BiRNN(x,weights,biases,Lstmcell,sen_len):
    x = tf.unstack(x,sentence_length,1)
    with tf.variable_scope('summery_nn'):
        outputs,_,_ = rnn.static_bidirectional_rnn(Lstmcell['fw_lstm'],Lstmcell['bw_lstm'],x,dtype=tf.float32)
    sum_len = tf.reduce_sum(sen_len,0)
    return tf.matmul(outputs[-1],weights['summery']) + biases['summery']


def slot_BiRNN(x, weights, biases,Lstmcell,n_words,sen_len):
    # Prepare data shape to match `bidirectional_rnn` function requirements
    # Current data input shape: (batch_size, n_sentences, vector_length)
    # Required shape: 'n_sentences' tensors list of shape (batch_size, vector_length)
    # Permuting batch_size and n_steps
    x = tf.unstack(x, n_words, 1)
    with tf.variable_scope('slot_rnn'):
        outputs, _, _ = rnn.static_bidirectional_rnn(Lstmcell['fw_lstm'], Lstmcell['bw_lstm'], x,dtype=tf.float32)
    # Linear activation, using rnn inner loop last output
    pred = []
    for i in range(len(outputs)):
        pred.append(tf.matmul(outputs[i],weights['slot_out']) + biases['slot_out'])
    return pred

def intent_BiRNN(x,weights,biases,Lstmcell,n_words,sen_len):
    x = tf.unstack(x, n_words, 1)
    with tf.variable_scope('intent_rnn'):
        outputs, _, _ = rnn.static_bidirectional_rnn(Lstmcell['fw_lstm'] , Lstmcell['bw_lstm'] , x,dtype=tf.float32)
    pred = []
    for i in range(batch_size):
        pred.append(tf.matmul([outputs[-1][i]],weights['intent_out']) + biases['intent_out'])
    return pred

def slot_loss(pred,y,Data):
    cost = []
    y = tf.transpose(y,perm=[1,0,2])
    for i in range(Data.maxlength):
        logit = tf.slice(pred,[i,0,0],[1,-1,-1])
        label = tf.slice(y,[i,0,0],[1,-1,-1])
        cost.append((tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logit[0],labels=label[0]))))
    loss = tf.reduce_sum(cost)
    return loss

def intent_loss(pred,y):
    y = tf.transpose(y,perm=[1,0,2])
    pred = tf.transpose(pred,perm=[1,0,2])
    return tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(logits=pred[0],labels=y[0]))

summery_out = summery_BiRNN(s_x,weights,biases,Lstmcell,prev_sen_len)
summery_l = []
for _ in range(n_words):
    summery_l.append(summery_out[0])
input_x = []
for i in range(batch_size):
    input_x.append(tf.concat([x[i],summery_l],1))


slot_pred = slot_BiRNN(input_x, weights, biases,s_Lstmcell,n_words,sen_len)
s_pred = tf.nn.softmax(slot_pred,dim=-1)
SAP_slot = tf.reduce_sum(slot_pred,0)
_slot_loss = slot_loss(slot_pred,y_slot,Data)


intent_pred = intent_BiRNN(input_x,weights,biases,i_Lstmcell,n_words,sen_len)
i_pred = tf.nn.softmax(intent_pred,dim=-1)
_intent_loss = intent_loss(intent_pred,y_intent)

_slot_optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(_slot_loss)
_intent_optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(_intent_loss)

init = tf.global_variables_initializer()

saver = tf.train.Saver()

if args.test == False:
    # Launch the graph
    with tf.Session(config=config) as sess:
        sess.run(init)
        # Keep training until reach max iterations
        prev_sen , prev_slot , prev_intent , seq_in , seq_slot  , seq_int , word_length = Data.get_batches()
        batch_seq = []
        for i in range(len(seq_in)):
            batch_seq.append(i)
        np.random.shuffle(batch_seq)
        for _ in range(3):
            for i in range(len(seq_in)):
                batch_x,batch_slot,batch_intent,prev_batch,word_len = seq_in[batch_seq[i]],seq_slot[batch_seq[i]],seq_int[batch_seq[i]],prev_sen[batch_seq[i]],word_length[batch_seq[i]]
                word_len = [10]
                #print ("aaa",np.shape(batch_x),np.shape(prev_batch),np.shape(batch_slot))
                _,_ = sess.run([_slot_optimizer,_intent_optimizer],feed_dict={s_x:prev_batch,x:batch_x,y_slot:[batch_slot],y_intent:[batch_intent],prev_sen_len:word_len,sen_len:word_len})
                s_l,i_l,_pred = sess.run([_slot_loss,_intent_loss,s_pred],feed_dict={s_x:prev_batch,x:batch_x,y_slot:[batch_slot],y_intent:[batch_intent],prev_sen_len:word_len,sen_len:word_len})
                _pred = np.transpose(_pred,(1,0,2))
                _pred = np.argmax(_pred[0],axis=1)
                print (Data.reverse[batch_seq[i]])
                for i in range(len(_pred)):
                    sys.stdout.write(Data.rev_slotdict[_pred[i]]+" ")
                print()
        save_path = saver.save(sess,"../model/model.ckpt")
else:
    print ("testing")
    with tf.Session(config=config) as sess:
        ckpt = tf.train.get_checkpoint_state("../model")
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess,ckpt.model_checkpoint_path)