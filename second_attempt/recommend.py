from __future__ import division

try:
	import cPickle as pickle
except:
	import pickle 
import tools
import similar
import os

class recommend:
	def __init__(self,outputfile,similaritymeasure,pathstr,train,test):
		self.outputfile = os.getcwd() + '//results' + outputfile
		self.similaritymeasure = similaritymeasure
		self.pathstr = pathstr
		self.train = train
		self.test = test
		self.prefs = {}
		self.predictprefs = []
		self.movietag = {}
	def loadtrainset(self):
		prefs={}
		try:
			with open(self.pathstr + self.train) as train:
				for line in train:
					(userid,movieid,rating,time) = line.split('\t')
					prefs.setdefault(userid,{})
					prefs[userid][movieid] = float(rating)
		except IOError as err:
			print 'File error' + str(err)
		self.prefs = prefs
	def loadtestset(self):
		prefs = []
		try:
			with open(self.pathstr + self.test) as test:
				for line in test:
					(userid,movieid,rating,time) = line.split('\t')
					movieid = movieid.replace('\r\r\n','')
					prefs.append((userid,movieid))
		except IOError as err:
			print 'File error: ' + str(err)
		self.predictprefs = prefs
	def transformprefs(self,prefs):
		result = {}
		for person in prefs:
			for item in prefs[person]:
				result.setdefault(item,{})
				result[item][person] = prefs[person][item]
		return result 
	def topmatches(self,prefs,item,similaritymeasure,n=100):
		if similaritymeasure == similar.sim_cosine_improved_tag:
			scores = [(similaritymeasure(prefs,item,other,self.movietag),other) for other in prefs if other != item]
		else:
			scores = [(similaritymeasure(prefs,item,other),other) for other in prefs if other!= item]
		scores.sort()
		scores.reverse()
		return scores[0:n]
	def getrecommendeditems(self,user):
		return None
	def predictrating(self,user,movie):
		return None

class itembasedrecommender(recommend):
	def __init__(self,outputfile,similaritymeasure):
		recommend.__init__(self,outputfile,similaritymeasure = similar.sim_cosine_improved,pathstr = os.getcwd() + '//ml-100k/',train = 'u1.base', test = 'u1.test')
		self.itemmatch =None
	
	def calculatesimilaritems(self,n,resultfile):
		result = {}
		c = 0
		prefsonitem = self.transformprefs(self.prefs)
		for i in prefsonitem.keys():
			result.setdefault(i,[])
		for item in prefsonitem:
			c = c + 1
			if c%5==0:
				print "%d / %d" % (c,len(prefsonitem))
			scores = self.topmatches(prefsonitem,item, similaritymeasure = self.similaritymeasure,n=n)
			result[item] = scores
		tools.dumppickle(result,resultfile)
	def loaditemmatch(self,itemfile):
		self.itemmatch = tools.loadpickle(itemfile)
	def predictrating(self,user,movie):
		totals = 0.0
		simsums = 0.0
		sim = 0.0
		predict = 0
		itemlist = self.itemmatch[movie]
		for other in itemlist:
			if other[1] == movie:
				continue
			sim = other[0]
			if sim<=0:
				continue
			if movie not in self.prefs[user] or self.prefs[user][movie] == 0:
				if other[1] in self.prefs[user]:
					totals = totals + self.prefs[user][other[1]] * sim
					simSums =  simSums + sim
		if simSums == 0:
			predict = 4.0
		else:
			predict = totals / simSums
		return predict
	def getrecommendeditems(self,user):
		prefsonuser = self.loadbasefileonuser()
		userratings = prefsonuser[user]
		scores = {}
		totalsim = {}
		for (item,rating) in userratings.items():
			
			for (similarity,item2) in self.itemmatch[item]:
				if similarity<=0:
					continue
				if item2 in userratings:
					continue
				scores.setdefault(item2,0)
				scores[item2] = scores[item2] + (similarity * rating)
				
				totalsim.setdefault(item2,0)
				totalsim[item2] = totalsim[item2] + similarity
		rankings = [(round(score / totalsim[item],7),item) for item,score in scores.items()]
		rankings.sort()
		rankings.reverse()
		return rankings

class userbasedrecommender(recommend):
	def __init__(self,outputfile,similaritymeasure):
		recommend.__init__(self,outputfile,similaritymeasure = similar.sim_cosine_improved,pathstr = os.getcwd() + '//data-v',train = 'training_set.txt',test = 'predict.txt')
		self.usermatch = None
	def calculatesimilarusers(self,n,resultfile):
		result = {}
		c = 0
		for i in self.prefs.keys():
			result.setdefault(i,[])
		for user in self.prefs:
			c = c+1
			if c%5==0:
				print "%d / %d" % (c,len(self.prefs))
			scores = self.topMatches(self.prefs, user, similarityMeasure=self.similarityMeasure, n=n)
			result[user] = scores
		tools.dumppickle(result,resultfile)
	def loadusermatch(self,userfile):
		self.usermatch = tools.loadpickle(userfile)
	def predictrating(self,user,movie):
		totals = 0.0
		simSums = 0.0
		sim = 0.0
		predict = 0
		userList = self.userMatch[user]
		for other in userList:
			if other[1] == user:
				continue
			sim = other[0]
			if sim <= 0:
				continue
			if movie not in self.prefs[user] or self.prefs[user][movie] == 0:
				if movie in self.prefs[other[1]]:
					totals += self.prefs[other[1]][movie] * sim
					simSums += sim
		if simSums == 0:
			predict = 4.0
		else:
			predict = totals / simSums
		return predict
	def getrecommendeditems(self,user):
		prefs = self.loadtrainset()
		totals = {}
		simsums = {}
		sim = 0.0
		for other in self.topmatches(prefs, user, similaritymeasure = similar.sim_cosine, n=99):
			if other[1] == user:
				continue
			sim = other[0]
			if sim<=0:
				continue
			for item in prefs[other[1]]:
				if item not in prefs[user] or prefs[user][item]==0:
					totals.setdefault(item,0)
					totals[item] = totals[item] + (prefs[other[1]][item] * sim)
					simsums.setdefault(item,0)
					simsums[item] = simsums[item] + sim
		rankings = [(total/simsums[item],item) for item,total in totals.items()]
		rankings.sort()
		rankings.reverse()
		return rankings
	
		
		
			
		
		
			
	
	
	
		
					
