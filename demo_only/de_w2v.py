import numpy as np
import string
from nltk.tag import pos_tag
import tensorflow as tf
import random
 
 
class DataPrepare(object):
    """docstring for DataPrepare"""
    def __init__(self, path,slotlist,intentlist):
        #super(DataPrepare, self).__init__()
        self.seed = 0
        self.worddict,self.dict_dim = self.get_glove(path[0])
        self.slotdict,self.rev_slotdict = self.get_slots(slotlist)
        self.intentdict,self.rev_intentdict = self.get_intents(intentlist)
        self.path = path[1]
        self.maxlen = 23
   
    def get_glove(self,path):
        d = {}
        dict_dim = 0
        with open(path,'r') as f:
            for l in f:
                tmp = l.strip().split()
                dict_dim = len(tmp)-1
                d[tmp[0]] = np.asarray(tmp[1:])
        d['<unk>'] = np.zeros(dict_dim)
        return d,dict_dim
 
 
    def get_wordvec(self,sentence):
        encoded = list()
        reverse = []
        corp = []
        tmp = []
        _long = open('../Data/long.txt','r')
        for sen in _long:
            sen = sen.strip()
            corp.append(sen)
        name = ""
        reverse.append(sentence)
        for corp_name in corp:
            try:
                index = sentence.index(corp_name)
                name = corp_name
                sentence = sentence.replace(corp_name,"*****")
            except:
                whatever = 0
        sent = sentence.strip().split()
        sen_l = len(sent)
        for word in sent:
            word = word.strip()
            if word.lower() in self.worddict:
                tmp.append(self.worddict[word.lower()])
            elif(word== "*****"):
                name = name.strip().split()
                for i in range(len(name)):
                    fack_vec = np.zeros(self.dict_dim)
                    if i == 0:
                        fack_vec[0] = 100
                    else:
                        fack_vec[1] = 100
                    tmp.append(fack_vec)
                sen_l = sen_l + len(name) - 1
            else:
                tmp.append(self.worddict['<unk>'])
        for x in xrange(self.maxlen - sen_l):
            tmp.insert(0,np.zeros(self.dict_dim))
        assert len(tmp) == self.maxlen
        return tmp

    def get_slotvalue(self,path):
        slot = list()
        with open(path,'r') as f:
            for s in f:
                tmp = []
                s = s.strip().split()
                for token in s:
                    token = token.strip()
                    assert token in self.slotdict
                    arr = np.zeros(len(self.slotdict))
                    arr[self.slotdict[token]] = 1
                    tmp.append(arr)
                for x in xrange(self.maxlen - len(s)):
                    tmp.append(np.zeros(len(self.slotdict)))
                slot.append(tmp)
        print (len(slot))
        return slot
 
    def get_intentvalue(self,path):
        intent = list()
        with open(path,'r') as f:
            for i in f:
                tmp = np.zeros(len(self.intentdict))
                token = i.strip().split()
                for x in token:
                    assert x in self.intentdict
                tmp[[self.intentdict[x] for x in token]] += 1
                intent.append(tmp)
        print (len(intent))
        return intent

    def get_intents(self,intentlist):
        d = {}
        rev_d = {}
        for i in range(len(intentlist)):
            d[intentlist[i]] = i
            rev_d[i] = intentlist[i]
        return d,rev_d

    def get_slots(self,slotlist):
        d = {}
        rev_d = {}
        count = 0
        for s in slotlist:
            if s == 'O':
                d[s] = count
                rev_d[count] = s
                count+=1
            else:
                d[s] = count
                rev_d[count] = s
                count += 1
                # d['B-'+s] = count
                # count+=1
                # d['I-'+s] = count
                # count+=1
        return d,rev_d

    def demo_batch(self):
        f = open(self.path,'r')
        encoded = []
        original = []
        for line in f:
            original.append(line)
            encoded.append(self.get_wordvec(line))
        return encoded,original
 
if __name__ == '__main__':
    glove = 'glove.6B.200d.txt'
    utter = 'utter'
    slot = 'slot'
    intent = 'intent'
    path = [glove, utter, slot, intent]
    # slot = ["revenues","to","from","stock_number","time_range","currency","bank","risk","action"]
    # intent = ["get_interest_rate","get_exrate","get_best_exrate","get_stock_performance","get_stock_attr","get_stock_price","get_stock_EPS"]
    slot = ['O','country1','country2']
    intent = ['exchange']
    D = DataPrepare(path,slot,intent)
    import pdb;pdb.set_trace()