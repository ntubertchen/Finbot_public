class Map(object):
	"""docstring for Map"""
	def __init__(self):
		self.slot,self.intent,self.map = self.mapping()

	def mapping(self):
		i_list = open('../All/Data/intent_list','r')
		s_list = open('../All/Data/slot_list','r')
		d = dict()
		i_l = []
		s_l = []
		i = 0
		for line in i_list:
			line = line.strip()
			d[line] = i
			i += 1
			i_l.append(line)
		for line in s_list:
			line = line.strip()
			d[line] = i 
			i += 1
			s_l.append(line)
		return s_l,i_l,d

