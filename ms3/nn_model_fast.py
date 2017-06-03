import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
from w2v_fast import DataPrepare
import argparse
import fileinput
import sys

class NN(object):
	"""docstring for NN"""
	def __init__(self,sess):
		self.sess = sess
		self.config = tf.ConfigProto()
		self.config.gpu_options.allow_growth = True

		self.path = ["../glove/glove.6B.200d.txt" , "../n_All/train/seq.in" , "../n_All/train/seq.out" , "../n_All/train/int", "../n_All/long.txt","../n_All/currency"]
		self.slotpath = '../n_All/slot_list'
		self.intentpath = '../n_All/intent_list'
		self.syspath = '../n_All/system_action_list'
		self.Data = DataPrepare(self.path,self.slotpath,self.intentpath,self.syspath)

		self.learning_rate = 0.0001
		self.epoc = 5
		self.batch_size = 1
		self.display_step = 30

		#network parameters
		self.sentence_length = self.Data.maxlength
		self.word_vector = 200 + self.Data.slot_dim + self.Data.int_dim

		self.summery_dim = 30
		self.n_hidden = 128
		self.n_words = self.Data.maxlength
		self.n_slot = self.Data.slot_dim
		self.n_intent = self.Data.int_dim

		self.x = tf.placeholder("float", [None, self.n_words, self.word_vector],name='x')
		self.y_slot = tf.placeholder("float", [None, self.n_words, self.n_slot],name='y_slot')
		self.y_intent = tf.placeholder("float", [None, 1 ,self.n_intent],name='y_intent')
		self.weights = {
			# Hidden layer weights => 2*n_hidden because of forward + backward cells
			'slot_out': tf.Variable(tf.random_normal([2* self.n_hidden, self.n_slot])),
			'intent_out': tf.Variable(tf.random_normal([2* self.n_hidden, self.n_intent]))
		}
		self.biases = {
			'slot_out': tf.Variable(tf.random_normal([self.n_slot])),
			'intent_out': tf.Variable(tf.random_normal([self.n_intent]))
		}

		with tf.variable_scope('slot_cell'):
			self.s_Lstmcell = {
				'fw_lstm' : rnn.BasicLSTMCell(self.n_hidden,forget_bias = 1.0),
				'bw_lstm' : rnn.BasicLSTMCell(self.n_hidden,forget_bias = 1.0)
		}
		with tf.variable_scope('intent_cell'):
			self.i_Lstmcell = {
				'fw_lstm' : rnn.BasicLSTMCell(self.n_hidden,forget_bias = 1.0),
				'bw_lstm' : rnn.BasicLSTMCell(self.n_hidden,forget_bias = 1.0)
		}
		

		self.slot_pred = self.slot_BiRNN(self.x, self.weights, self.biases,self.s_Lstmcell,self.n_words)
		self.s_pred = tf.nn.softmax(self.slot_pred,dim=-1)
		self._slot_loss = self.slot_loss(self.slot_pred,self.y_slot,self.Data)

		self.intent_pred = self.intent_BiRNN(self.x,self.weights,self.biases,self.i_Lstmcell,self.n_words)
		self.i_pred = tf.nn.softmax(self.intent_pred,dim=-1)
		self._intent_loss = self.intent_loss(self.intent_pred,self.y_intent)

		self._slot_optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self._slot_loss)
		self._intent_optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self._intent_loss)

		self.init = tf.global_variables_initializer()

		self.saver = tf.train.Saver()
		self.sess.run(self.init)

	def slot_BiRNN(self,x, weights, biases,Lstmcell,n_words):
		x = tf.unstack(x, self.n_words, 1)
		with tf.variable_scope('slot_rnn'):
			outputs, _, _ = rnn.static_bidirectional_rnn(Lstmcell['fw_lstm'], Lstmcell['bw_lstm'], x,dtype=tf.float32)
		pred = []
		for i in range(len(outputs)):
			pred.append(tf.matmul(outputs[i],weights['slot_out']) + biases['slot_out'])
		return pred

	def intent_BiRNN(self,x,weights,biases,Lstmcell,n_words):
		x = tf.unstack(x, self.n_words, 1)
		with tf.variable_scope('intent_rnn'):
			outputs, _, _ = rnn.static_bidirectional_rnn(Lstmcell['fw_lstm'] , Lstmcell['bw_lstm'] , x,dtype=tf.float32)
		pred = []
		for i in range(self.batch_size):
			pred.append(tf.matmul([outputs[-1][i]],weights['intent_out']) + biases['intent_out'])
		return pred

	def slot_loss(self,pred,y,Data):
		cost = []
		y = tf.transpose(y,perm=[1,0,2])
		for i in range(self.Data.maxlength):
			logit = tf.slice(pred,[i,0,0],[1,-1,-1])
			label = tf.slice(y,[i,0,0],[1,-1,-1])
			cost.append((tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logit[0],labels=label[0]))))
		loss = tf.reduce_sum(cost)
		return loss

	def intent_loss(self,pred,y):
		y = tf.transpose(y,perm=[1,0,2])
		pred = tf.transpose(pred,perm=[1,0,2])
		return tf.reduce_sum(tf.nn.softmax_cross_entropy_with_logits(logits=pred[0],labels=y[0]))

	def loadmodel(self):
		ckpt = tf.train.get_checkpoint_state("./model_fast")
		if ckpt and ckpt.model_checkpoint_path:
			self.saver.restore(self.sess,ckpt.model_checkpoint_path)

	def predict(self,sentence,state):
		batch = self.Data.sen2vec(sentence,state)
		intent,slot = self.sess.run([self.i_pred,self.s_pred],feed_dict={self.x:batch})
		intent_sum = np.argmax(intent[0],axis=1)
		slot = np.transpose(slot,(1,0,2))
		slot_sum = np.argmax(slot[0],axis=1)
		str_int = []
		str_slot = []
		for i in intent_sum:
			str_int.append(self.Data.rev_intdict[i])
		for i in slot_sum:
			str_slot.append(self.Data.rev_slotdict[i])
		prob_slot = []
		prob_intent = []
		for i in range(len(slot_sum)):
			prob_slot.append(slot[0][i][slot_sum[i]])
		for i in range(len(intent_sum)):
			prob_intent.append(intent[0][i][intent_sum[i]])
		all_slot = []
		all_int = []
		all_slot.append(str_slot)
		all_slot.append(prob_slot)
		all_int.append(str_int)
		all_int.append(prob_intent)
		return (all_slot,all_int)
