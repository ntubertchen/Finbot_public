import numpy as np
import random

class DataPrepare(object):
  def __init__(self,path,slotpath,intentpath):
    self.seed = 0
    self.maxlength = 50
    self.slotdict,self.rev_slotdict,self.slot_dim = self.get_slots(slotpath)
    self.intentdict,self.rev_intentdict,self.intent_dim = self.get_slots(intentpath)
    self.worddict,self.dict_dim = self.get_glove(path[0])
    self.symbol2dict = self.sym2dict(path[4],path[5])

    self.encoded,self.previous,self.reverse,self.word_len = self.set_word2vec(path[1])
    self.slotvalue,self.slot_previous = self.get_value(path[2])
    self.intentvalue,self.intent_previous = self.get_value(path[3])
    

  def get_glove(self,GloVe):
    d = {}
    dict_dim = 0
    with open(GloVe,'r') as f:
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

  def get_slots(self,slotpath):
    d = {}
    rev_d = {}
    count = 0
    with open(slotpath,'r') as f:
      for line in f:
       line = line.strip()
       d[line] = count
       rev_d[count] = line
       count += 1
    return d,rev_d,count

  def set_word2vec(self,seq_in):
    """
     for ***next*** only
    """
    parser = [',','.','?']
    unkbook = open('nuk','w')
    with open(seq_in,'r') as f:
      training_set = []
      previous = []
      rev_set = []
      word_len = []
      for line in f:
        line = line.strip().split('***')
        original_sen = []
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
            if word in self.worddict:
              batch.append(self.worddict[word])
            elif  word.count("/") == 2 and len(word) == 10:
              batch.append(self.worddict['_time'])
            elif  word.count("-") == 2 and len(word) == 10:
              batch.append(self.worddict['_time'])
            elif word.count("'s") == 1 or word.count("’s") == 1:
              word = word.replace("'s","")
              word = word.replace("’s","")
              if word in self.worddict:
                tmp = np.zeros(self.dict_dim)
                w1 = self.worddict[word]
                w2 = self.worddict["'s"]
                for j in range(len(tmp)):
                  tmp[j] = w1[j] + w2[j]
                batch.append(tmp)
              else:
                batch.append(self.worddict['<unk>'])
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
                batch.append(tmp)
              else:
                batch.append(self.worddict['<unk>'])
                unkbook.write(word+'\n')
            else:
              batch.append(self.worddict['<unk>'])
              unkbook.write(word+'\n')
          if len(batch) > self.maxlength:
            self.maxlength = len(batch)
          if i == 0:
            previous.append([batch])
            word_len.append(len(batch))
          else:
            training_set.append([batch])
        rev_set.append(original_sen)
    return training_set,previous,rev_set,word_len

  def get_value(self,label_p):
    training_set = []
    previous = []
    error = open('error','w')
    with open(label_p,'r') as f:
      for line in f:
        line = line.split('***')
        for i in range(len(line)):
          if i == 0:
            previous.append(self.get_labelvalue(line[i]))
          else:
            training_set.append(self.get_labelvalue(line[i]))
    return training_set,previous

  def get_labelvalue(self,out_sentence):
    batch = []
    l = out_sentence.strip().split()
    error = open('error','w')
    for word in l:
      word = word.strip()
      if word in self.slotdict:
        vec = np.zeros(self.slot_dim)
        vec[self.slotdict[word]] = 1
        batch.append(vec)
      elif word in self.intentdict:
        vec = np.zeros(self.intent_dim)
        vec[self.intentdict[word]] = 1
        batch.append(vec)
      else:
        batch.append(self.worddict['<unk>'])
        error.write(word+'\n')
        print ("error",word)
    return batch

  def get_batches(self):
    seq_in = []
    seq_out = []
    prev_in = []
    prev_out = []
    #5x30x200
    for sentence in self.encoded:#4sentence + guide
      for i in range(len(sentence)):#each sen
        for _ in range(self.maxlength - len(sentence[i])):
          sentence[i].append(np.zeros(200))
      #print np.shape(sentence)
      seq_in.append(sentence)
    for sentence in self.previous:#4sentence + guide
      for i in range(len(sentence)):#each se
        for _ in range(self.maxlength - len(sentence[i])):
          sentence[i].append(np.zeros(200))

      prev_in.append(sentence)
    # #4x30x350
    for out in self.slotvalue:
      for i in range(len(out)):
        #print (np.shape(out),self.maxlength - len(out[i]))
        for _ in range(self.maxlength - len(out)):
          tmp = np.zeros(self.slot_dim)
          tmp[self.slotdict['O']] = 1
          out.append(tmp)
      seq_out.append(out)
    for out in self.slot_previous:
      for i in range(len(out)):
        for _ in range(self.maxlength - len(out[i])):
          out.append(np.zeros(self.slot_dim))
      prev_out.append(out)
    return prev_in,prev_out,self.intent_previous,seq_in,seq_out,self.intentvalue,self.word_len
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
    for stock_name in s_l:
      if sentence.count(stock_name) > 0:
        tmp = "_stock_name "
        for _ in range(len(stock_name.strip().split())-1):
          tmp += " _stock_name "
        sentence = sentence.replace(stock_name,tmp)
    for currency_symbol in c_l:
      if sentence.count(currency_symbol) > 0 and sentence.count("USDX") == 0:
        tmp = " _currency_symbol "
        for _ in range(len(currency_symbol.strip().split())-1):
          tmp += "_currency_symbol "
        sentence = sentence.replace(currency_symbol,tmp)
    return sentence

  def sen2vec(self,sentence):
    sentence = self.word2sym(sentence)
    batch = []
    parser = [',','.','?','\'s']
    sentence = sentence.strip().split()
    for i in range(len(sentence)):
      for j in range(len(parser)):
        sentence[i] = sentence[i].replace(parser[j],"")
      sentence[i] = self.word2sym(sentence[i])
    for word in sentence:
      word = word.lower()
      if word in self.worddict:
        batch.append(self.worddict[word])
      elif  word.count("/") == 2 and len(word) == 10:
        batch.append(self.worddict['_time'])
      elif  word.count("-") == 2 and len(word) == 10:
        batch.append(self.worddict['_time'])
      elif word.count("'s") == 1 or word.count("’s") == 1:
        word = word.replace("'s","")
        word = word.replace("’s","")
        if word in self.worddict:
          tmp = np.zeros(self.dict_dim)
          w1 = self.worddict[word]
          w2 = self.worddict["'s"]
          for j in range(len(tmp)):
            tmp[j] = w1[j] + w2[j]
          batch.append(tmp)
        else:
          batch.append(self.worddict['<unk>'])
      elif word.count("'d") == 1 or word.count("’d") == 1:
        word = word.replace("'d","")
        word = word.replace("’d","")
        if word in self.worddict:
          tmp = np.zeros(self.dict_dim)
          w1 = self.worddict[word]
          w2 = self.worddict["'d"]
          for j in range(len(tmp)):
            tmp[j] = w1[j] + w2[j]
          batch.append(tmp)
        else:
          batch.append(self.worddict['<unk>'])
      else:
        batch.append(self.worddict['<unk>'])
    l = self.maxlength - len(batch)
    #print (self.maxlength,len(batch),l)
    for _ in range(l):
      batch.append(np.zeros(200))
    return [batch]
