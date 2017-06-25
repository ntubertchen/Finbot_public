import numpy as np
import random

class DataPrepare(object):
  def __init__(self,path,slotpath,intentpath,systemactionpath):
    self.seed = 0
    self.maxlength = 40
    self.currencies = self.get_currencies(path[6])
    self.slotdict,self.rev_slotdict,self.slot_dim,self.intdict,self.rev_intdict,self.int_dim = self.get_slots(slotpath,intentpath,systemactionpath)
    self.worddict,self.dict_dim = self.get_glove(path[0])
    self.symbol2dict = self.sym2dict(path[4],path[5])

    self.encoded,self.reverse = self.set_word2vec(path[1])
    self.slotvalue = self.get_value(path[2],0)
    self.intentvalue = self.get_value(path[3],1)

  def get_currencies(self,path):
    batch = []
    with open(path,'r') as currency:
      for line in currency:
        line = line.strip().split('*')
        tmp = []
        for i in range(len(line)-1):
          tmp.append(line[i].lower())
        tmp.append(line[-1])
        batch.append(tmp)
    return batch

  def get_glove(self,GloVe):
    d = {}
    dict_dim = 0
    f = open(GloVe,'r')
    for l in f:
      tmp = l.strip().split()
      dict_dim = len(tmp)-1
      nptmp = np.zeros(dict_dim)
      for i in range(len(nptmp)):
        nptmp[i] = float(tmp[i+1])
      d[tmp[0]] = nptmp
    additional = ["usdx","_time","<unk>","_stock_name","_currency_symbol"]
    for i in range(len(additional)):
      tmp = np.zeros(dict_dim)
      tmp[i] = 200
      d[additional[i]] = tmp
    return d,dict_dim

  def get_slots(self,slotpath,intpath,systempath):
    d = {}
    rev_d = {}
    int_d = {}
    int_rev_d = {}
    count = 0
    num = 0
    with open(slotpath,'r') as f:
      for line in f:
       line = line.strip()
       d[line] = count
       rev_d[count] = line
       count += 1
    with open(intpath,'r') as f:
      for line in f:
        line = line.strip()
        int_d[line] = num
        int_rev_d[num] = line
        num += 1
    with open(systempath,'r') as f:
      for line in f:
        line = line.strip()
        d[line] = count
        rev_d[count] = line
        count += 1
    return d,rev_d,count,int_d,int_rev_d,num

  def set_word2vec(self,seq_in):
    """
     for ***next*** only
    """
    parser = [',','.','?']
    unkbook = open('nuk','w')
    training_set = []
    with open(seq_in,'r') as f:
      previous = []
      rev_set = []
      for line in f:
        line = line.strip().split('***next***')
        # prev next
        prev_vec = np.zeros(self.slot_dim + self.int_dim)
        prev_sen = line[0].strip().split('SYSTEM_ACTION')
        prev_userin = prev_sen[0]
        prev_sysout = prev_sen[1]
        if len(prev_userin) != 0:
          prev_userin = prev_userin.strip().split()
          for word in prev_userin:
            if word in self.slotdict:
              value = self.slotdict[word]
              prev_vec[value] += 1
            elif word in self.intdict:
              prev_vec[self.intdict[word] + self.slot_dim] += 1
            else:
              print ("error",word)
        if len(prev_sysout) != 0:
          prev_sysout = prev_sysout.strip().split()
          for word in prev_sysout:
            if word in self.slotdict:
              value = self.slotdict[word]
              prev_vec[value] += 50
            elif word in self.intdict:
              prev_vec[self.intdict[word] + self.slot_dim] += 50
            else:
              print ("error",word)
        original_sen = []
        line = line[1:]
        replacement = ['january','february','march','april','may','june','july','august','septpmber','october','november','december','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec','tomorrow','yesterday','next week','this weak','today']
        for i in range(len(line)):
          batch = []
          line[i] = self.word2sym(line[i])
          for j in range(len(parser)):
            line[i] = line[i].replace(parser[j],"")
          line[i] = self.word2sym(line[i])
          sen = line[i].strip().split()
          original_sen.append(line[i])
          for word in sen:
            word = word.lower()
            for k in range(len(self.currencies)):
              if word in self.currencies[k]:
                word = self.currencies[k][-1]
            if (word.count("/") == 2 and len(word) == 10) or (word.count('/') > 0) or (word in replacement):
              batch.append(np.concatenate([self.worddict['_time'],prev_vec],0))
            elif word in self.worddict:
              batch.append(np.concatenate([self.worddict[word],prev_vec],0))
            elif  word.count("-") == 2 and len(word) == 10:
              batch.append(np.concatenate([self.worddict['_time'],prev_vec],0))
            elif word.count("'s") == 1 or word.count("’s") == 1:
              word = word.replace("'s","")
              word = word.replace("’s","")
              if word in self.worddict:
                tmp = np.zeros(self.dict_dim)
                w1 = self.worddict[word]
                w2 = self.worddict["'s"]
                for j in range(len(tmp)):
                  tmp[j] = w1[j] + w2[j]
                batch.append(np.concatenate([tmp,prev_vec],0))
              else:
                batch.append(np.concatenate(self.worddict['<unk>'],np.zeros(self.slot_dim+self.int_dim),0))
                unkbook.write(word+'\n')
            elif word.count("'d") == 1 or word.count("’d") == 1:
              word = word.replace("'d","")
              word = word.replace("’d","")
              if word in self.worddict:
                tmp = np.zeros(self.dict_dim)
                w1 = self.worddict[word]
                w2 = self.worddict["'d"]
                for j in range(len(tmp)):
                  tmp[j] = w1[j] + w2[j]
                batch.append(np.concatenate([tmp,prev_vec],0))
              else:
                batch.append(np.concatenate(self.worddict['<unk>'],np.zeros(self.slot_dim+self.int_dim),0))
                unkbook.write(word+'\n')
            else:
              batch.append(np.concatenate(self.worddict['<unk>'],np.zeros(self.slot_dim+self.int_dim),0))
              unkbook.write(word+'\n')
          if len(batch) > self.maxlength:
            self.maxlength = len(batch)
          training_set.append([batch])
        rev_set.append(original_sen)
    return training_set,rev_set

  def get_value(self,label_p,num):
    training_set = []
    error = open('error','w')
    with open(label_p,'r') as f:
      for line in f:
        words = line.strip().split()
        tmp = []
        for word in words:
          if word in self.slotdict and num == 0:
            vec = np.zeros(self.slot_dim)
            vec[self.slotdict[word]] += 1
            tmp.append(vec)
          elif word in self.intdict and num == 1:
            vec = np.zeros(self.int_dim)
            vec[self.intdict[word]] += 1
            tmp.append(vec)
          else:
            print (word,"wtf")
            if num == 0:
              print (word,"GG")
        training_set.append(tmp)
    return training_set

  def get_batches(self):
    seq_in = []
    seq_out = []
    #5x30x200
    for sentence in self.encoded:#4sentence + guide
      for i in range(len(sentence)):#each sen
        for _ in range(self.maxlength - len(sentence[i])):
          sentence[i].append(np.zeros(200+self.slot_dim + self.int_dim))
      #print np.shape(sentence)
      seq_in.append(sentence)
    # #4x30x350
    for out in self.slotvalue:
      #senxlen
      l = self.maxlength - len(out)
      for _ in range(l):
        tmp = np.zeros(self.slot_dim)
        tmp[self.slotdict['O']] = 1
        out.append(tmp)
      seq_out.append(out)
    return seq_in,seq_out,self.intentvalue
    # intent = self.intentvalue
    # return seq_in,seq_out,intent

  def sym2dict(self,_stock_name,_currency_symbol):
    s = open(_stock_name,'r')
    c = open(_currency_symbol,'r')
    tmp1 = []
    tmp2 = []
    d = dict()
    for line in s:
      line = line.strip()
      tmp1.append(line)
    for line in c:
      line = line.strip()
      tmp2.append(line)
    d['stock_name'] = tmp1
    d['currency_symbol'] = tmp2
    return d

  def word2sym(self,sentence):
    s_l = self.symbol2dict['stock_name']
    c_l = self.symbol2dict['currency_symbol']
    # for stock_name in s_l:
    #   if sentence.count(stock_name) > 0:
    #     tmp = "_stock_name "
    #     for _ in range(len(stock_name.strip().split())-1):
    #       tmp += " _stock_name "
    #     sentence = sentence.replace(stock_name,tmp)
    for currency_symbol in c_l:
      if sentence.count(currency_symbol) > 0 and sentence.count("USDX") == 0:
        tmp = " _currency_symbol "
        for _ in range(len(currency_symbol.strip().split())-1):
          tmp += "_currency_symbol "
        sentence = sentence.replace(currency_symbol,tmp)
    return sentence

  def test_sen2vec(self,sentence):
    prev = np.zeros(self.int_dim+self.slot_dim)
    sentence = self.word2sym(sentence)
    batch = []
    parser = [',','.','?','\'s']
    sentence = sentence.strip().split()
    replacement = ['january','february','march','april','june','july','august','septpmber','october','november','december','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec','tomorrow','yesterday','today']
    for i in range(len(sentence)):
      for j in range(len(parser)): 
        sentence[i] = sentence[i].replace(parser[j],"")
      sentence[i] = self.word2sym(sentence[i])
    for word in sentence:
      word = word.lower()
      for k in range(len(self.currencies)):
        if word in self.currencies[k]:
          word = self.currencies[k][-1]
      print (word.count('/'))
      if word in replacement:
        batch.append(np.concatenate([self.worddict['_time'],prev],0))
      elif  (word.count("/") == 2 and len(word) == 10) or (word.count('/') > 0) or (word.isdigit()):
        batch.append(np.concatenate([self.worddict['_time'],prev],0))
      elif word in self.worddict:
        batch.append(np.concatenate([self.worddict[word],prev],0))
      elif  word.count("-") == 2 and len(word) == 10:
        batch.append(np.concatenate([self.worddict['_time'],prev],0))
      elif word.count("'s") == 1 or word.count("’s") == 1:
        word = word.replace("'s","")
        word = word.replace("’s","")
        if word in self.worddict:
          tmp = np.zeros(self.dict_dim)
          w1 = self.worddict[word]
          w2 = self.worddict["'s"]
          for j in range(len(tmp)):
            tmp[j] = w1[j] + w2[j]
          batch.append(np.concatenate([tmp,prev],0))
        else:
          batch.append(np.concatenate([self.worddict['<unk>'],np.zeros(self.slot_dim+self.int_dim)],0))
      elif word.count("'d") == 1 or word.count("’d") == 1:
        word = word.replace("'d","")
        word = word.replace("’d","")
        if word in self.worddict:
          tmp = np.zeros(self.dict_dim)
          w1 = self.worddict[word]
          w2 = self.worddict["'d"]
          for j in range(len(tmp)):
            tmp[j] = w1[j] + w2[j]
          batch.append(np.concatenate([tmp,prev],0))
        else:
          batch.append(np.concatenate([self.worddict['<unk>'],np.zeros(self.slot_dim+self.int_dim)],0))
      else:
        batch.append(np.concatenate([self.worddict['<unk>'],np.zeros(self.slot_dim+self.int_dim)],0))
    l = self.maxlength - len(batch)
    #print (self.maxlength,len(batch),l)
    for _ in range(l):
      batch.append(np.concatenate([np.zeros(200),np.zeros(self.slot_dim+self.int_dim)],0))
    return [batch]
    
  def sen2vec(self,sentence,state):
    print ('history',state.history)
    prev = np.zeros(self.int_dim+self.slot_dim)
    system = 0
    for key in state.history: ####
      if key == "request":
        system = 1
      if key in self.slotdict:
        if system == 1:
          prev[self.slotdict[key]] += 50
        else:
          prev[self.slotdict[key]] += 1
      elif key in self.intdict:
        if system == 1:
          prev[self.intdict[key]+ self.slot_dim] += 50
        else:
          prev[self.intdict[key]+ self.slot_dim] += 1
      elif key != "O":
        key = "B-" + key
        if key in self.slotdict:
          if system == 1:
            prev[self.slotdict[key]] += 50
          else:
            prev[self.slotdict[key]] += 1
        else:
          print ("key error",key)
      else:
        print (key,"error")
    # if state.history[-1][0] == 2:
    #   prev_int = state.history[-1][0][0]####
    #   if prev_int in self.intdict[prev_int]:
    #     prev[self.intdict[prev_int]]
    #   else:
    #     print("interror",prev_int)

    # sa = state.history[-1][-1]####
    # if sa in self.slotdict:
    #   prev[self.slotdict[sa]] += 1
    # else:
    #   print ("sa error",sa)
    sentence = self.word2sym(sentence)
    batch = []
    parser = [',','.','?','\'s']
    sentence = sentence.strip().split()
    replacement = ['january','february','march','april','may','june','july','august','septpmber','october','november','december','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec','tomorrow','yesterday','next week','this weak','today']
    for i in range(len(sentence)):
      for j in range(len(parser)): 
        sentence[i] = sentence[i].replace(parser[j],"")
      sentence[i] = self.word2sym(sentence[i])
    for word in sentence:
      word = word.lower()
      for k in range(len(self.currencies)):
        if word in self.currencies[k]:
          word = self.currencies[k][-1]
      if word in replacement:
        batch.append(np.concatenate([self.worddict['_time'],prev],0))
      elif  (word.count("/") == 2 and len(word) == 10) or (word.count('/') > 0) or (word.isdigit()):
        batch.append(np.concatenate([self.worddict['_time'],prev],0))
      elif word in self.worddict:
        batch.append(np.concatenate([self.worddict[word],prev],0))
      elif  word.count("-") == 2 and len(word) == 10:
        batch.append(np.concatenate([self.worddict['_time'],prev],0))
      elif word.count("'s") == 1 or word.count("’s") == 1:
        word = word.replace("'s","")
        word = word.replace("’s","")
        if word in self.worddict:
          tmp = np.zeros(self.dict_dim)
          w1 = self.worddict[word]
          w2 = self.worddict["'s"]
          for j in range(len(tmp)):
            tmp[j] = w1[j] + w2[j]
          batch.append(np.concatenate([tmp,prev],0))
        else:
          batch.append(np.concatenate([self.worddict['<unk>'],np.zeros(self.slot_dim+self.int_dim)],0))
      elif word.count("'d") == 1 or word.count("’d") == 1:
        word = word.replace("'d","")
        word = word.replace("’d","")
        if word in self.worddict:
          tmp = np.zeros(self.dict_dim)
          w1 = self.worddict[word]
          w2 = self.worddict["'d"]
          for j in range(len(tmp)):
            tmp[j] = w1[j] + w2[j]
          batch.append(np.concatenate([tmp,prev],0))
        else:
          batch.append(np.concatenate([self.worddict['<unk>'],np.zeros(self.slot_dim+self.int_dim)],0))
      else:
        batch.append(np.concatenate([self.worddict['<unk>'],np.zeros(self.slot_dim+self.int_dim)],0))
    l = self.maxlength - len(batch)
    #print (self.maxlength,len(batch),l)
    for _ in range(l):
      batch.append(np.concatenate([np.zeros(200),np.zeros(self.slot_dim+self.int_dim)],0))
    return [batch]