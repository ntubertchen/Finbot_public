import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
from w2v import DataPrepare
import argparse
import fileinput
import sys

class NN(object):
	"""docstring for NN"""
	def __init__(self,sess):
		self.sess = sess
		self.config = tf.ConfigProto()
		self.config.gpu_options.allow_growth = True

		self.path = ["../glove/glove.6B.200d.txt" , "../All/Data/train/seq.in" , "../All/Data/train/seq.out" , "../All/Data/train/intent", "../All/long.txt","../All/currency"]
		self.slotpath = '../All/Data/slot_list'
		self.intentpath = '../All/Data/intent_list'
		self.Data = DataPrepare(self.path,self.slotpath,self.intentpath)

		self.learning_rate = 0.0001
		self.epoc = 5
		self.batch_size = 1
		self.display_step = 30

		#network parameters
		self.sentence_length = self.Data.maxlength
		self.word_vector = 200

		self.summery_dim = 30
		self.n_hidden = 128
		self.n_words = self.Data.maxlength
		self.n_slot = self.Data.slot_dim
		self.n_intent = self.Data.intent_dim

		self.s_x = tf.placeholder("float", [None, self.sentence_length, self.word_vector],name='s_x')
		self.prev_sen_len = tf.placeholder("int32",[None],name='prev_sen_len')
		self.sen_len = tf.placeholder("int32",[None],name='sen_len')
		self.x = tf.placeholder("float", [None, self.n_words, self.word_vector],name='x')
		self.y_slot = tf.placeholder("float", [None, self.n_words, self.n_slot],name='y_slot')
		self.y_intent = tf.placeholder("float", [None, 1 ,self.n_intent],name='y_intent')
		self.weights = {
			# Hidden layer weights => 2*n_hidden because of forward + backward cells
			'summery': tf.Variable(tf.random_normal([2* self.n_hidden,self.summery_dim])),
			'slot_out': tf.Variable(tf.random_normal([2* self.n_hidden, self.n_slot])),
			'intent_out': tf.Variable(tf.random_normal([2* self.n_hidden, self.n_intent]))
		}
		self.biases = {
			'summery': tf.Variable(tf.random_normal([self.summery_dim])),
			'slot_out': tf.Variable(tf.random_normal([self.n_slot])),
			'intent_out': tf.Variable(tf.random_normal([self.n_intent]))
		}

		with tf.variable_scope('summery_cell'):
			self.Lstmcell = {
				'fw_lstm' : rnn.BasicLSTMCell(self.n_hidden,forget_bias = 1.0),
				'bw_lstm' : rnn.BasicLSTMCell(self.n_hidden,forget_bias = 1.0)
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
		self.summery_out = self.summery_BiRNN(self.s_x , self.weights , self.biases , self.Lstmcell , self.prev_sen_len)
		self.summery_l = []
		for _ in range(self.n_words):
			self.summery_l.append(self.summery_out[0])
		self.input_x = []
		for i in range(self.batch_size):
			self.input_x.append(tf.concat([self.x[i],self.summery_l],1))

		self.slot_pred = self.slot_BiRNN(self.input_x, self.weights, self.biases,self.s_Lstmcell,self.n_words,self.sen_len)
		self.s_pred = tf.nn.softmax(self.slot_pred,dim=-1)
		self.SAP_slot = tf.reduce_sum(self.slot_pred,0)
		self._slot_loss = self.slot_loss(self.slot_pred,self.y_slot,self.Data)

		self.intent_pred = self.intent_BiRNN(self.input_x,self.weights,self.biases,self.i_Lstmcell,self.n_words,self.sen_len)
		self.i_pred = tf.nn.softmax(self.intent_pred,dim=-1)
		self._intent_loss = self.intent_loss(self.intent_pred,self.y_intent)

		self._slot_optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self._slot_loss)
		self._intent_optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self._intent_loss)

		self.init = tf.global_variables_initializer()

		self.saver = tf.train.Saver()
		self.sess.run(self.init)
	def summery_BiRNN(self,x,weights,biases,Lstmcell,sen_len):
		x = tf.unstack(x,self.sentence_length,1)
		with tf.variable_scope('summery_nn'):
			outputs,_,_ = rnn.static_bidirectional_rnn(Lstmcell['fw_lstm'],Lstmcell['bw_lstm'],x,dtype=tf.float32)
		sum_len = tf.reduce_sum(sen_len,0)
		return tf.matmul(outputs[-1],weights['summery']) + biases['summery']


	def slot_BiRNN(self,x, weights, biases,Lstmcell,n_words,sen_len):
			# Prepare data shape to match `bidirectional_rnn` function requirements
		# Current data input shape: (batch_size, n_sentences, vector_length)
		# Required shape: 'n_sentences' tensors list of shape (batch_size, vector_length)
		# Permuting batch_size and n_steps
		x = tf.unstack(x, self.n_words, 1)
		with tf.variable_scope('slot_rnn'):
			outputs, _, _ = rnn.static_bidirectional_rnn(Lstmcell['fw_lstm'], Lstmcell['bw_lstm'], x,dtype=tf.float32)
		# Linear activation, using rnn inner loop last output
		pred = []
		for i in range(len(outputs)):
			pred.append(tf.matmul(outputs[i],weights['slot_out']) + biases['slot_out'])
		return pred

	def intent_BiRNN(self,x,weights,biases,Lstmcell,n_words,sen_len):
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
		ckpt = tf.train.get_checkpoint_state("./model")
		if ckpt and ckpt.model_checkpoint_path:
			self.saver.restore(self.sess,ckpt.model_checkpoint_path)
	def predict(self,sentence,prev):
		#prev = state.previous_user_sentence +" "+ state.previous_system_response
		prev = self.Data.sen2vec(prev)
		batch = self.Data.sen2vec(sentence)
		intent,slot = self.sess.run([self.i_pred,self.s_pred],feed_dict={self.s_x:prev,self.x:batch})
		intent_sum = np.argmax(intent[0],axis=1)
		slot = np.transpose(slot,(1,0,2))
		slot_sum = np.argmax(slot[0],axis=1)
		str_int = []
		str_slot = []
		for i in intent_sum:
			str_int.append(self.Data.rev_intentdict[i])
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
	def valid(self):
		prev_sen , prev_slot , prev_intent , seq_in , seq_slot  , seq_int , word_length = self.Data.get_batches()
		for i in range(len(seq_in)):
			batch_x,batch_slot,batch_intent,prev_batch,word_len = seq_in[i],seq_slot[i],seq_int[i],prev_sen[i],word_length[i]
			word_len = [10]
			s_l,i_l,_pred = self.sess.run([self._slot_loss,self._intent_loss,self.s_pred],feed_dict={self.s_x:prev_batch,self.x:batch_x,self.y_slot:[batch_slot],self.y_intent:[batch_intent],self.prev_sen_len:word_len,self.sen_len:word_len})
			_pred = np.transpose(_pred,(1,0,2))
			_pred = np.argmax(_pred[0],axis=1)
			print (self.Data.reverse[i])
			for i in range(len(_pred)):
				sys.stdout.write(self.Data.rev_slotdict[_pred[i]]+" ")
			print()
