from rli import Map
import numpy as np
import tensorflow as tf

class rl_model(object):
	"""docstring for rl_model"""
	def __init__(self,sess):
		self.sess = sess
		self.map = Map()
		self.train_win,self.train_slot,self.train_intent,self.train_reward,self.train_systemaction = self.get_all_batches()
		self.w_in = tf.placeholder("float", [len(self.map.slot) + len(self.map.intent)],name='w_in')
		self.w_s = tf.placeholder("float",[len(self.map.slot),1],name='w_s')
		self.w_i = tf.placeholder("float",[len(self.map.intent),1],name='w_i')
		self.w_sa = tf.placeholder("float",[4,1],name='w_sa')
		self.n_hidden = 128
		self.weights = {
			'w_s': tf.Variable(tf.random_normal([ self.n_hidden,len(self.map.slot)])),
			'w_i': tf.Variable(tf.random_normal([ self.n_hidden, len(self.map.intent)])),
			'w_sa': tf.Variable(tf.random_normal([ self.n_hidden, 4]))
		}
		self.biases = {
			'w_s': tf.Variable(tf.random_normal([len(self.map.slot)])),
			'w_i': tf.Variable(tf.random_normal([len(self.map.intent)])),
			'w_sa': tf.Variable(tf.random_normal([4]))
		}
		self.layer = {
			'l1': tf.Variable(tf.random_normal([len(self.map.slot) + len(self.map.intent),self.n_hidden])),
			'l2': tf.Variable(tf.random_normal([len(self.map.slot) + len(self.map.intent),self.n_hidden])),
			'l3': tf.Variable(tf.random_normal([len(self.map.slot) + len(self.map.intent),self.n_hidden]))
		}
		self.layer_biases = {
			'b1': tf.Variable(tf.random_normal([self.n_hidden])),
			'b2': tf.Variable(tf.random_normal([self.n_hidden])),
			'b3': tf.Variable(tf.random_normal([self.n_hidden]))
		}
		self.w1 = tf.nn.relu(tf.matmul(self.w_in,self.layer['l1']) + self.layer_biases['b1'])
		self.w2 = tf.nn.relu(tf.matmul(self.w_in,self.layer['l2']) + self.layer_biases['b2'])
		self.w3 = tf.nn.relu(tf.matmul(self.w_in,self.layer['l3']) + self.layer_biases['b3'])

		self.o1 = tf.negative(tf.log(tf.sigmoid(tf.matmul(self.w1,self.weights['w_s']) + self.biases['w_s'])))
		self.o2 = tf.negative(tf.log(tf.sigmoid(tf.matmul(self.w2,self.weights['w_i']) + self.biases['w_i'])))
		self.o3 = tf.negative(tf.log(tf.sigmoid(tf.matmul(self.w3,self.weights['w_sa']) + self.biases['w_sa'])))

		self.c1 = tf.reduce_sum(tf.matmul([self.o1],self.w_s))
		self.c2 = tf.reduce_sum(tf.matmul([self.o2],self.w_i))
		self.c3 = tf.reduce_sum(tf.matmul([self.o3],self.w_sa))

		self.t1 = tf.train.RMSPropOptimizer(0.0025,0.99,0.0,1e-6).minimize(self.c1)
		self.t2 = tf.train.RMSPropOptimizer(0.0025,0.99,0.0,1e-6).minimize(self.c2)
		self.t3 = tf.train.RMSPropOptimizer(0.0025,0.99,0.0,1e-6).minimize(self.c3)

		self.save_path = ""
		self.init = tf.global_variables_initializer()

		self.saver = tf.train.Saver()
		self.sess.run(self.init)


	def train(self):
		for i in range(len(self.train_win)):
			_,_,_ = self.sess.run([self.t1,self.t2,self.t3],feed_dict={'w_in':self.train_win[i],'w_s':self.train_slot[i],'w_i':self.train_intent[i],'w_sa':self.train_systemaction[i]})
		self.save_path = self.saver.save(sess,"../model/model.ckpt")

	def predict(self):
		ckpt = tf.train.get_checkpoint_state("../model")
		if ckpt and ckpt.model_checkpoint_path:
			self.saver.restore(self.sess,ckpt.model_checkpoint_path)
		
	def get_all_batches(self):
		w_in = open('../All/w_in','r')
		maxlen = len(self.map.slot) + len(self.map.intent)
		train_win = []
		for line in w_in:
			line = line.strip().split()
			tmp = np.zeros(maxlen)
			for word in line:
				if word in self.map:
					tmp[self.map[word]] = 1
				else:
					print ('error rl batches' + word)
			train_win.append(tmp)
		w_r = open('../All/w_r','r')
		train_reward = []
		for line in w_r:
			line = line.strip()
			train_reward.append(int(line))

		w_s = open('../All/w_s','r')
		train_slot = []
		i = 0
		for line in w_s:
			line = line.strip().split()
			tmp = np.zeros(len(self.map.slot))
			for word in line:
				if word in self.map:
					tmp[self.map[word]] = train_reward[i]
				else:
					print ('error rl batches' + word)
			i += 1
			train_slot.append(tmp)
		w_i = open('../All/w_i','r')
		train_intent = []
		i = 0
		for line in w_i:
			line = line.strip().split()
			tmp = np.zeros(len(self.map.slot))
			for word in line:
				if word in self.map:
					tmp[self.map[word]] = train_reward[i]
				else:
					print ('error rl batches' + word)
			i += 1
			train_intent.append(tmp)
		w_sa = open('../All/w_sa','r')
		d = {'closing':0,'response':1,'confirm_answer':2,'request':3}
		train_systemaction = []
		i = 0
		for line in w_sa:
			line = line.strip()
			tmp = np.zeros(len(d))
			if line in d:
				tmp[d[line]] = train_reward[i]
				train_systemaction.append(tmp)
			else
				print ('error rl batches' + line)
			i += 1

		return train_win,train_slot,train_intent,train_reward,train_systemaction
